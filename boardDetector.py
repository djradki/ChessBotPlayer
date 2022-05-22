import logging
from pynput.mouse import Listener as listen
from pynput.mouse import Controller


class BoardDetector():
    @staticmethod
    def onClick(x, y, button, pressed):
        global myX
        global myY
        mouse = Controller()

        if pressed:
            myX = mouse.position[0]
            myY = mouse.position[1]
            logging.info("Detected:\tx:{0} y:{1}".format(x,y))
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
