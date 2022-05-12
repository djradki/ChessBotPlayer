from pynput.mouse import Button, Controller


class Mouse():
    def __init__(self):
        print("STATIC CLASS")
        pass

    
    @staticmethod
    def click(horizontalPixel: int, verticalPixel: int) -> None:
        mouse = Controller()
        mouse.position = (horizontalPixel, verticalPixel)
        mouse.press(Button.left)
        mouse.release(Button.left)
        mouse.position = (0,0)


    @staticmethod
    def dragAndDrop(firstScreenCoordinates: tuple, secondScreenCoordinates: tuple) -> None:
        mouse = Controller()

        mouse.position = (int(firstScreenCoordinates[0]), int(firstScreenCoordinates[1]))
        mouse.press(Button.left)

        mouse.position = (int(secondScreenCoordinates[0]), int(secondScreenCoordinates[1]))
        mouse.release(Button.left)

        Mouse.resetPositionToZero()
        
        #print("Dragged from {0}x{1} to {2}x{3}".format(firstScreenCoordinates[0], firstScreenCoordinates[1], secondScreenCoordinates[0], secondScreenCoordinates[1]))


    @staticmethod
    def moveToCoordinates(firstScreenCoordinates: tuple) -> None:
        mouse = Controller()
        mouse.position = (int(firstScreenCoordinates[0]), int(firstScreenCoordinates[1]))


    @staticmethod
    def resetPositionToZero() -> None:
        mouse = Controller()
        mouse.position = (0,0)
