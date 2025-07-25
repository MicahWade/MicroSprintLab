import json
import random

welcomeMessage = """
Welcome to MicroSprintLab!

When you press ENTER, you will have:

  - 5 minutes to think and research the idea.
  - 1 hour to code it.

Get ready to innovate fast!

supportingess ENTER to start...
"""


def getRandomIdea():
    with open("ideas.json", "r") as file:
        data = json.load(file)["projects"]
    return random.choice(data)


def main():
    print(welcomeMessage)
    input()
    print(getRandomIdea())


if __name__ == "__main__":
    main()
