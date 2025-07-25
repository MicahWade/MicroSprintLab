import json
import random
from timedInput import Tinput

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

Now it’s time to start coding! You have 1 hour to implement your ida.

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


def main():
    print(welcomeMessage)
    input()
    idea = getRandomIdea()
    print(ideaMessage % (idea["title"], idea["description"]))
    print(idea["title"])
    print(idea["description"])
    Tinput(300, outOfTimeMessage)


if __name__ == "__main__":
    main()
