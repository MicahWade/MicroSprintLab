import time
import threading


def timer(second: int) -> int:
    remainingTime = second
    reminders = [second // 2, second // 3, second // 4, second // 5, 300, 180, 120, 60]

    def reminder(reminderNumber): ...

    thread = threading.Thread()

    def timerinput():
        test = input()

    thread = threading.Thread(target=timerinput)
    thread.daemon = True
    thread.start()

    def checkForInput(thread):
        if thread.is_alive():
            return 1
        else:
            return 0

    lastTime = time.time()
    print(remainingTime)
    while remainingTime > 0:
        if checkForInput(thread) == 0:
            return int(remainingTime)
        if reminders[0] > remainingTime:
            reminder(reminders[0])
        print("Remaining time: {:.1f}s".format(remainingTime), end="\r", flush=True)
        if remainingTime > 500:
            time.sleep(0.5)
        else:
            time.sleep(0.05)
        if lastTime is not None:
            remainingTime -= time.time() - lastTime
            lastTime = time.time()
        else:
            lastTime = time.time()
    return 1
