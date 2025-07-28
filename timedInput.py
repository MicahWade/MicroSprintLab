import threading


def Tinput(time: int):
    def GetInput():
        answer = str(input())

    inputThread = threading.Thread(target=GetInput)
    inputThread.daemon = True
    inputThread.start()
    inputThread.join(time)
    if inputThread.is_alive():
        return 0
