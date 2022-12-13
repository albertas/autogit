from logging import getLogger
from typing import Union

import httpx
from git.cmd import Git

from gitmultirepoupdater.data_types import RepoState
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor

logger = getLogger()


def get_http_request_params_for_pull_request_creation(repo: RepoState) -> dict[str, Union[str, dict]]:
    # Gitlab create MR docs: https://docs.gitlab.com/ee/api/merge_requests.html#create-mr
    # Github create MR docs: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#create-a-pull-request
    repo.target_branch = get_target_branch(repo)

    domain = f"https://api.github.com/repos/{repo.owner}/{repo.name}/pulls"
    headers = {
      "Accept": "application/vnd.github+json",
      "Authorization": f"Bearer {GITHUB_OAUTH_TOKEN}",
      "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {
        "title": repo.args.commit_message,
        "body": repo.args.commit_message,
        "head": repo.branch,
        "base": repo.target_branch,  # this parameter should be optional
    }

    return {
        "domain": domain,
        "headers": headers,
        "data": data,
    }



async def create_pull_request(repo: RepoState):
    # https://stackoverflow.com/questions/56027634/creating-a-pull-request-using-the-api-of-github
    url, headers, data = get_http_request_params_for_pull_request_creation(repo)

    client = httpx.Client()
    client.post()

    # curl \
    #   -X POST \
    #   -H "Accept: application/vnd.github+json" \
    #   -H "Authorization: Bearer <YOUR-TOKEN>"\
    #   -H "X-GitHub-Api-Version: 2022-11-28" \
    #   https://api.github.com/repos/OWNER/REPO/pulls \
    #   -d '{"title":"Amazing new feature","body":"Please pull these awesome changes in!","head":"octocat:new-feature","base":"master"}'

    pass


def create_pull_request_for_each_repo(repos: dict[str, RepoState], executor: ThrottledTasksExecutor) -> None:
    for repo in repos.values():
        executor.run(create_pull_request(repo))
    executor.wait_for_tasks_to_finish()
