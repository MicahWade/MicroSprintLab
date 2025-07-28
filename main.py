import json
import random
import os
import newTerminal
import timer
import gitManager
from displayText import DisplayText, TimedDisplayText

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


def GetRandomIdea():
    with open("ideas.json", "r") as file:
        data = json.load(file)["projects"]
    return random.choice(data)


def CreateOneHourProjectPath():
    if not os.path.exists(oneHourPath):
        os.makedirs(oneHourPath)


def MakeFile(directory, name, startingInfo=None):
    with open(os.path.join(directory, name), "w") as fp:
        if startingInfo is not None:
            fp.write(startingInfo)


def SetupProject(projectTitle: str, projectDescription: str):
    global currentProjectPath
    if currentProjectPath is oneHourPath:
        currentProjectPath = os.path.join(
            currentProjectPath, projectTitle.replace(" ", "")
        )
    if not os.path.exists(currentProjectPath):
        os.makedirs(currentProjectPath)

    MakeFile(currentProjectPath, f"main{language}")
    if not nvim:
        newTerminal.OpenOtherTerminal(f"{editor} {currentProjectPath}/main{language}")
        timeSpent = int(3600 - timer.Timer(3600))
    else:
        import nvimManager

        nvimManager.SetupIdeaCommand(projectTitle, projectDescription)
        nvimManager.OpenFileInSingleTab(f"{currentProjectPath}/main{language}")
        timeSpent = int(3600 - nvimManager.TimerWithRemindersAndPopup(3600))
        nvimManager.CloseNvim()

    gitManager.FinishProject(
        projectTitle,
        projectDescription,
        currentProjectPath,
        projectPath,
        timeSpent,
        remote,
    )


def Main():
    DisplayText(welcomeMessage)
    idea = GetRandomIdea()
    CreateOneHourProjectPath()
    TimedDisplayText(ideaMessage % (idea["title"], idea["description"]), 300)
    SetupProject(idea["title"], idea["description"])


if __name__ == "__main__":
    Main()
