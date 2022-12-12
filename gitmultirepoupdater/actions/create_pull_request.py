from logging import getLogger
from typing import Optional, Tuple

import httpx

from gitmultirepoupdater.data_types import RepoState
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor

logger = getLogger()


def get_pull_request_http_request_data(repo_url: str, from_branch: str, to_branch: Optional[str]) -> Tuple[str, str, str]:
    owner, name = get_repo_owner_and_name(repo_url)

    domain = "https://api.github.com/repos/OWNER/REPO/pulls"
    headers = {
      "Accept": "application/vnd.github+json",
      "Authorization": f"Bearer {GITHUB_OAUTH_TOKEN}",
      "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {
        "title": repo_state.commit_message,
        "body": repo_state.body,
        "head": repo_state.head,
        "base": repo_state.base,  # this parameter should be optional
    }

    return

# Gitlab create MR docs: https://docs.gitlab.com/ee/api/merge_requests.html#create-mr
# Github create MR docs: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#create-a-pull-request

async def create_pull_request(repo_state: RepoState):
    # https://stackoverflow.com/questions/56027634/creating-a-pull-request-using-the-api-of-github
    url, headers, data = get_pr_request_data()

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


def create_pull_request_for_each_repo(repo_states: list[RepoState], executor: ThrottledTasksExecutor) -> None:
    for repo_state in repo_states:
        executor.run(create_pull_request(repo_state))
    executor.wait_for_tasks_to_finish()
