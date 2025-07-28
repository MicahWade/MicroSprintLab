import json

with open("settings.json", "r") as file:
    data = json.load(file)
    nvim = data["nvim"]

if nvim:
    import nvimManager
else:
    from timedInput import Tinput


def DisplayText(text: str):
    global nvimManager
    if nvim and nvimManager:
        nvimManager.DisplayTextWait(text)
    else:
        print(text)
        input()


def TimedDisplayText(text: str, time: int):
    global nvimManager
    global Tinput
    if nvim and nvimManager:
        nvimManager.FullscreenCountdownWithText(text, time)
    else:
        print(text)
        Tinput(time)
