import git
import os

readme = """
#%s

this was codded in %ss
"""


def finishProject(title: str, path, projectPath, time: int):
    mainRepo = firstSetup(projectPath)
    with open(os.path.join(path, "readme.md"), "w") as file:
        file.write(readme % (title, time))


def firstSetup(projectPath):
    try:
        repo = git.Repo(projectPath)
    except (git.InvalidGitRepositoryError, git.NoSuchPathError):
        repo = git.Repo.init(projectPath)
    repo.git.add(all=True)
    return repo
