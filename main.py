import json
import random
from timedInput import Tinput
import os
import newTerminal
import timer
import gitManager

projectPath = os.path.expanduser("~/Documents/MicroSprintLab/Projects")
if not os.path.exists(projectPath):
    os.makedirs(projectPath)

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
    with open("settings.json", "r") as file:
        data = json.load(file)
        editor = data["editor"]
        language = data["language"]
        remote = data["remote"]
    global currentProjectPath
    if currentProjectPath is oneHourPath:
        currentProjectPath = os.path.join(
            currentProjectPath, projectTitle.replace(" ", "")
        )
    if not os.path.exists(currentProjectPath):
        os.makedirs(currentProjectPath)
    makeFile(currentProjectPath, f"main{language}")
    newTerminal.openOtherTerminal(f"{editor} {currentProjectPath}/main{language}")
    timeSpent = int(3600 - timer.timer(3600))
    gitManager.finishProject(
        projectTitle,
        projectDescription,
        currentProjectPath,
        projectPath,
        timeSpent,
        remote,
    )


def main():
    print(welcomeMessage)
    input()
    idea = getRandomIdea()
    createOneHourProjectPath()
    print(ideaMessage % (idea["title"], idea["description"]))
    Tinput(300, outOfTimeMessage)
    setupProject(idea["title"], idea["description"])


if __name__ == "__main__":
    main()
