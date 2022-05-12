from pynput.mouse import Listener as listen


class BoardDetector():
    @staticmethod
    def onClick(x, y, button, pressed):
        global myX
        global myY
        if pressed:
            myX = x
            myY = y
            print("Detected:\tx:{0} y:{1}".format(x,y))
            return False


    @staticmethod
    def detectBoard() -> tuple:
        global myX
        global myY
        myX = 1
        myY = 1
        with listen(on_click=BoardDetector.onClick) as listener:
            listener.join()
            return (myX, myY)
    

    @staticmethod
    def waitForClick() -> None:
        with listen(on_click=BoardDetector.onClick) as listener:
            listener.join()
            return None
