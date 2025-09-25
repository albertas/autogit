import json
from logging import getLogger

import httpx

from autogit.constants import PullRequestStates
from autogit.data_types import HttpRequestParams, RepoState
from autogit.utils.helpers import get_access_token
from autogit.utils.throttled_tasks_executor import ThrottledTasksExecutor

logger = getLogger()


def get_http_request_params_for_pull_request_creation(
    repo: RepoState,
) -> HttpRequestParams:
    """Gitlab create MR docs: https://docs.gitlab.com/ee/api/merge_requests.html#create-mr
    Github create MR docs: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#create-a-pull-request.
    """
    if repo.domain == 'github.com':
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
        url = f'https://{repo.domain}/api/v4/projects/{repo.owner}%2F{repo.name}/merge_requests'
        headers = {'PRIVATE-TOKEN': get_access_token(repo.url)}
        data = {
            'source_branch': repo.branch,
            'target_branch': repo.target_branch,
            'title': repo.args.commit_message,
        }
    return HttpRequestParams(
        url=url,
        headers=headers,
        data=data,
    )


def print_pull_requests(repos):
    print('\n\033[1;34m|' + 'Created Pull Requests'.center(77, '-') + '|\033[0m')
    show_not_created_pull_requests = False
    for repo in repos.values():
        if repo.pull_request_state == PullRequestStates.CREATED.value:
            print(
                f'\033[1;34m|\033[0m {repo.pull_request_url.ljust(75, " ")} \033[1;34m|\033[0m'
            )
        else:
            show_not_created_pull_requests = True
    if show_not_created_pull_requests:
        print('\033[1;34m|' + 'Not created Pull Requests'.center(77, '-') + '|\033[0m')
        for repo in repos.values():
            if repo.pull_request_state == PullRequestStates.GOT_BAD_RESPONSE.value:
                print(
                    f'\033[1;34m|\033[0m {repo.url.ljust(75, " ")} \033[1;34m|\033[0m'
                )
                print(
                    f'\033[1;34m|\033[0m   status_code={repo.pull_request_status_code} reason={repo.pull_request_reason} \033[1;34m|\033[0m'
                )
    print('\033[1;34m|' + ''.center(77, '-') + '|\033[0m')


async def create_pull_request(repo: RepoState) -> None:
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
            repo.pull_request_url = response.json().get(
                'web_url', response.json().get('url')
            )
        else:
            repo.pull_request_state = PullRequestStates.GOT_BAD_RESPONSE.value
            repo.pull_request_status_code = response.status_code
            repo.pull_request_reason = json.dumps(response.json())


def create_pull_request_for_each_repo(
    repos: dict[str, RepoState], executor: ThrottledTasksExecutor
) -> None:
    for repo in repos.values():
        executor.run(create_pull_request(repo))
    executor.wait_for_tasks_to_finish()
    print_pull_requests(repos)
