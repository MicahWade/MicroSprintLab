import json

from gitdb.db.pack import glob

with open("settings.json", "r") as file:
    data = json.load(file)
    nvim = data["nvim"]

if nvim:
    import nvimManager
else:
    from timedInput import Tinput


def displayText(text: str):
    global nvimManager
    if nvim and nvimManager:
        nvimManager.displayTextWait(text)
    else:
        print(text)
        input()


def timedDisplayText(text: str, time: int):
    global nvimManager
    global Tinput
    if nvim and nvimManager:
        nvimManager.fullscreenCountdownWithText(text, time)
    else:
        print(text)
        Tinput(time)
