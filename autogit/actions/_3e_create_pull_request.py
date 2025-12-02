import json
import asyncio
from logging import getLogger

import httpx

from autogit.constants import PullRequestStates
from autogit.data_types import HttpRequestParams, RepoState
from autogit.utils.helpers import get_access_token

logger = getLogger()


def get_http_request_params_for_pull_request_creation(
    repo: RepoState,
) -> HttpRequestParams:
    """Gitlab create MR docs: https://docs.gitlab.com/ee/api/merge_requests.html#create-mr
    Github create MR docs: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#create-a-pull-request.
    """
    if repo.domain == 'github.com':
        # TODO: add group support
        url = f'https://api.github.com/repos/{repo.owner}/{repo.name}/pulls'
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {get_access_token(repo.url)}',
            'X-GitHub-Api-Version': '2022-11-28',
        }
        data = {
            'title': repo.args.commit_message,
            'body': repo.args.commit_message,
            'head': repo.branch,
            'base': repo.target_branch,
        }

    else:  # Use gitlab.com API by default
        project_id = repo.path.replace('/', '%2F')
        url = f'https://{repo.domain}/api/v4/projects/{project_id}/merge_requests'
        headers = {'PRIVATE-TOKEN': get_access_token(repo.url)}
        data = {
            'source_branch': repo.branch,
            'title': repo.args.commit_message,
        }
        if repo.target_branch:
            data['target_branch'] = repo.target_branch
    return HttpRequestParams(
        url=url,
        headers=headers,
        data=data,
    )


async def create_pull_request(repo: RepoState) -> bool:
    """Create pull request.

    :return: bool - was pull request created successfully.
    """
    # TODO: split this method into seperate ones for Gitlab and Github
    repo.pull_request_state = PullRequestStates.CREATING.value

    # https://stackoverflow.com/questions/56027634/creating-a-pull-request-using-the-api-of-github
    request_params = get_http_request_params_for_pull_request_creation(repo)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=request_params.url,
            headers=request_params.headers,
            data=request_params.data,
        )
        if response.status_code < 400:
            repo.pull_request_state = PullRequestStates.CREATED.value
            repo.pull_request_url = response.json().get('web_url', response.json().get('url'))
        else:
            repo.pull_request_state = PullRequestStates.GOT_BAD_RESPONSE.value
            repo.pull_request_status_code = response.status_code
            repo.pull_request_reason = json.dumps(response.json())

        if repo.args.merge or repo.args.merge_on_success:

            project_id = repo.path.replace('/', '%2F')
            pull_request_id = response.json().get('iid')
            url = f'https://{repo.domain}/api/v4/projects/{project_id}/merge_requests/{pull_request_id}/merge'

            if repo.args.verbose:
                print(f"Merginge PR url: {url}")

            data = {}
            if repo.args.merge_on_success:
                data['auto_merge'] = True

            await asyncio.sleep(2)  # Wait for Gitlab to process created PR
            response = await client.put(
                url=url,
                headers=request_params.headers,
                json=data,
            )
            if repo.args.verbose:
                print(f"Merge: {response}")

            if response.status_code < 400:
                if repo.args.merge_on_success:
                    repo.pull_request_state = PullRequestStates.SET_TO_AUTO_MERGE.value
                else:
                    repo.pull_request_state = PullRequestStates.MERGED.value
            else:
                if repo.args.merge_on_success:
                    repo.pull_request_state = PullRequestStates.FAILED_TO_AUTO_MERGE.value
                else:
                    repo.pull_request_state = PullRequestStates.FAILED_TO_MERGE.value

    return repo.pull_request_state in [
        PullRequestStates.CREATED.value,
        PullRequestStates.MERGED.value,
        PullRequestStates.SET_TO_AUTO_MERGE.value,
    ]
