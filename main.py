import json
import random
import os
import newTerminal
import timer
import gitManager
from displayText import displayText, timedDisplayText

projectPath = os.path.expanduser("~/Documents/MicroSprintLab/Projects")
if not os.path.exists(projectPath):
    os.makedirs(projectPath)

with open("settings.json", "r") as file:
    data = json.load(file)
    editor = data["editor"]
    language = data["language"]
    remote = data["remote"]
    nvim = data["nvim"]
oneHourPath = os.path.join(projectPath, "OneHour")

currentProjectPath = oneHourPath
welcomeMessage = """
Welcome to MicroSprintLab!

When you press ENTER, you will have:

  - 5 minutes to think and research the idea.
  - 1 hour to code it.

Get ready to innovate fast!

ENTER to start...
"""

outOfTimeMessage = """
Thinking & Research Time Is Over

Your 5-minute period for thinking and research has ended.

Now it’s time to start coding! You have 1 hour to implement the idea.

Good luck—let’s see what you can create!
"""

ideaMessage = """
%s

%s
You have 5 minutes to Think and Research if you are done early Press ENTER"""


def getRandomIdea():
    with open("ideas.json", "r") as file:
        data = json.load(file)["projects"]
    return random.choice(data)


def createOneHourProjectPath():
    if not os.path.exists(oneHourPath):
        os.makedirs(oneHourPath)


def makeFile(directory, name, startingInfo=None):
    with open(os.path.join(directory, name), "w") as fp:
        if startingInfo is None:
            pass
        else:
            fp.write(startingInfo)


def setupProject(projectTitle: str, projectDescription: str):
    global currentProjectPath
    if currentProjectPath is oneHourPath:
        currentProjectPath = os.path.join(
            currentProjectPath, projectTitle.replace(" ", "")
        )
    if not os.path.exists(currentProjectPath):
        os.makedirs(currentProjectPath)

    makeFile(currentProjectPath, f"main{language}")
    if not nvim:
        newTerminal.openOtherTerminal(f"{editor} {currentProjectPath}/main{language}")
        timeSpent = int(3600 - timer.timer(3600))
    else:
        import nvimManager

        nvimManager.openFileInSingleTab(f"{currentProjectPath}/main{language}")
    gitManager.finishProject(
        projectTitle,
        projectDescription,
        currentProjectPath,
        projectPath,
        timeSpent,
        remote,
    )


def main():
    displayText(welcomeMessage)
    idea = getRandomIdea()
    createOneHourProjectPath()
    timedDisplayText(ideaMessage % (idea["title"], idea["description"]), 300)
    setupProject(idea["title"], idea["description"])


if __name__ == "__main__":
    main()
