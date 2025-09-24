`autogit` is a command line tool for updating multiple GitLab or GitHub repositories with a single command.

## Usage
Generate an access token at [GitLab](https://gitlab.com/-/profile/personal_access_tokens)
or [GitHub](https://github.com/settings/tokens)
and set it as environment variable:

```bash
export GITLAB_ACCESS_TOKEN=<token>
export GITHUB_OAUTH_TOKEN=<token>
export GIT_TOKEN=<token>  # This one is used if previous ones are not found
```

Provide a list of repositories and a script or a command to run inside each of them:

```bash
autogit --repos repos.txt update_repo.py
```

Where `repos.txt` could be:
```
https://gitlab.com/<handle>/<repo-title>
https://gitlab.com/<handle>/<repo-title2>
https://github.com/<handle>/<repo-title>
```

Try it yourself:

```bash
autogit \
  --repo https://github.com/<handle>/<repo-title> \
  --branch=add-hello-world-file \
  --clone-to=tmp \
  --commit-message="Add hello-world.txt file" \
  touch hello-world.txt
```

These steps will be executed for each specified repository:
1. The repository will be cloned into `/tmp/` directory.
2. A new branch will be created or fetched if it already exists.
3. The command or a script will be executed inside the repository.
4. A commit containing all the changes will be created.
5. Newly created commit will be pushed to remote repository.
6. A pull request will be created.
7. [optional] A comment will be left next to the PR.
8. [optional] The pull request will be merged.


These options could be used to specify more details:

| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Option&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description | Type | Required |
| ---------------- | ----------- | ---- | -------- |
| `--branch`       | A name of a branch which will be created or used to add a commit and to create pull request from. | String | Yes |
| `--commit-message` | A commit message which will be used for all of the changes made.  | String | No |
| `--clone-to`           | Path to temporal directory which will be used to clone repositories to | String | No |
| `--repo`           | Link to repository | String | No |
| `--repos`          | Filename which contains a list of repository links | String | No |

More examples:

```bash
autogit --repos repos.txt ./examples/update_mypy_version.py
```

## Efficiency
`autogit` is implemented in Python and uses coroutines to make multiple parallel API calls. Delays are being made after each API call in order not to get throttled.

## Roadmap
- [ ] Add unit tests for all the paths (mock gitpython, httpx requests)
    - [ ] Implement state change dependencies on the tests.
    - [ ] Implement RecorderMock for packages.

- [ ] Package and release to PyPi
- [ ] Run command as command line tool
    - [ ] Stand-alone executable file download in Github releases.
- [ ] Make API calls to GitLab
- [ ] Support different API calls
- [ ] Advanced features:
    - [ ] Merge PRs which have all requirements like approvals met.

## Development
`make venv` - will create virtual env with dev dependencies.
`make check` - will run Flake8, MyPy and PyTest checks.

## Related projects
This tool was inspired by:
- https://github.com/earwig/git-repo-updater
- https://github.com/gruntwork-io/git-xargs
