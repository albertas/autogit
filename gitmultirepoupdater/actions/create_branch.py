import git

from gitmultirepoupdater.utils.helpers import to_kebab_case
from gitmultirepoupdater.data_types import RepoState
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor

async def create_branch(repo_state: RepoState):
    new_branch_name = to_kebab_case(repo_state.args.commit_message)
    repo_state.branch_name = new_branch_name
    repo = git.Repo(repo_state.repo_path) 

    new_branch = repo.create_head(new_branch_name)
    new_branch.checkout()

    # main = self.repo.heads.main
    # repo.git.pull('origin', main)

    #creating file
    # dtime = strftime('%d-%m-%Y %H:%M:%S', localtime())

    # with open(self.local_repo_path + path.sep + 'lastCommit' + '.txt', 'w') as f:
    #     f.write(str(dtime))

    # if not path.exists(self.local_repo_path):
    #     os.makedirs(self.local_repo_path)

    # print('file created---------------------')

    # if repo.index.diff(None) or repo.untracked_files:

    #     repo.git.add(A=True)
    #     repo.git.commit(m='msg')
    #     repo.git.push('--set-upstream', 'origin', current)
    #     print('git push')
    # else:
    #     print('no changes')


def create_branch_for_each_repo(repo_states: dict[str, RepoState], executor: ThrottledTasksExecutor) -> None:
    for repo_state in repo_states.values():
        executor.run_not_throttled(create_branch(repo_state))
    executor.wait_for_tasks_to_finish()
