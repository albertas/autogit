from logging import getLogger
from typing import TypedDict, Union

import httpx
from git.cmd import Git
from gitmultirepoupdater.constants import PullRequestStates

from gitmultirepoupdater.data_types import RepoState, HttpRequestParams
from gitmultirepoupdater.utils.helpers import get_access_token
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor

logger = getLogger()


def get_http_request_params_for_pull_request_creation(repo: RepoState) -> HttpRequestParams:
    """
    Gitlab create MR docs: https://docs.gitlab.com/ee/api/merge_requests.html#create-mr
    Github create MR docs: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#create-a-pull-request
    """
    if repo.domain == "github.com":
        url = f"https://api.github.com/repos/{repo.owner}/{repo.name}/pulls"
        headers = {
          "Accept": "application/vnd.github+json",
          "Authorization": f"Bearer {get_access_token(repo.url)}",
          "X-GitHub-Api-Version": "2022-11-28"
        }
        data = {
            "title": repo.args.commit_message,
            "body": repo.args.commit_message,
            "head": repo.branch,
            "base": repo.target_branch,
        }

    else:  # Use gitlab.com API by default
        url = f"https://{repo.domain}/api/v4/projects/{repo.owner}%2F{repo.name}/merge_requests"
        headers = {
            "PRIVATE-TOKEN": get_access_token(repo.url)
        }
        data = {
            "source_branch": repo.branch,
           "target_branch": repo.target_branch,
            "title": repo.args.commit_message,
        }
    return HttpRequestParams(
        url=url,
        headers=headers,
        data=data,
    )


async def create_pull_request(repo: RepoState):
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


def create_pull_request_for_each_repo(repos: dict[str, RepoState], executor: ThrottledTasksExecutor) -> None:
    for repo in repos.values():
        executor.run(create_pull_request(repo))
    executor.wait_for_tasks_to_finish()
