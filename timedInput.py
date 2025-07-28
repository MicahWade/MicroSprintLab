import threading


def Tinput(time: int):
    def getInput():
        answer = str(input())

    thread = threading.Thread(target=getInput)
    thread.daemon = True
    thread.start()
    thread.join(time)
    if thread.is_alive():
        return 0
