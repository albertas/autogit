"""Action:
- Parse domain names from provided list of repositories.
- Detect known Access Tokens from environment variables.
- Detect for each domain if it is Github or Gitlab and API version.
- Detect which Access Token works with which domain.


Returns:
 domains = {
   "<domain_name>": {
        "token": "<token>",
        "api_version": "<version>",
        "type": "Gitlab|Github",
    }
 }

"""

from autogit.data_types import RepoState


def get_tokens_and_api_versions(repos: dict[str, RepoState]) -> None:
    """:return: domains = {
      "<domain_name>": {
        "token": "<token>",
        "api_version": "<version>",
        "type": "Gitlab|Github",
      }
    }
    """
    # TODO: implement this part.

    ## TODO: add support for such API keys in environment:
    # 'GITLAB_ACCESS_TOKEN': '<GITLAB_ACCESS_TOKEN>',
    # 'GITLAB_OAUTH_TOKEN': '<GITLAB_ACCESS_TOKEN>',
    # 'GITLAB_TOKEN': '<GITLAB_ACCESS_TOKEN>',
    #
    # 'GITHUB_OAUTH_TOKEN': '<GITHUB_OAUTH_TOKEN>',
    # 'GITHUB_TOKEN': '<GITHUB_OAUTH_TOKEN>',
    # 'GITHUB_ACCESS_TOKEN': '<GITHUB_OAUTH_TOKEN>',
    #
    # 'GIT_TOKEN': '<GIT_TOKEN>',
    # 'GIT_ACCESS_TOKEN': '<GIT_TOKEN>',
    # 'GIT_OAUTH_TOKEN': '<GIT_TOKEN>',


# curl --header "PRIVATE-TOKEN: personal-access-token" your-gitlab-url/api/v4/version
