from board import Board, Side
from chessPlayer import ChessPlayer
from mouse import Mouse


class Test():
    def __init__(self, side: Side) -> None:
        print(side)
        self.board = Board()
        self.board.setSide(side)


    def testing1Arg(self, func, inputData, expectedResult):
        value = func(inputData)
        result = value == expectedResult

        print(result)
        if result == False:
            print(inputData, end='\t->\t')
            print(value, end='\tshould:\t')
            print(expectedResult)


    def testing2Arg(self, func, inputData, inputData2, expectedResult):
        value = func(inputData, inputData2)
        result = value == expectedResult

        print(result)
        if result == False:
            print(inputData, end='\t')
            print(inputData2, end='\t->\t')
            print(value, end='\tshould:\t')
            print(expectedResult)


    def CoordinatesFromMove(self) -> None:
        testData = []
        if self.board.side == Side.BLACK:
            testData.append(["e2e4", (([1,3], [3,3]), None)])
            testData.append(["f7f6", (([6,2], [5,2]), None)])
            testData.append(["g8f6", (([7,1], [5,2]), None)])

        else:
            testData.append(["e2e4", (([6,4], [4,4]), None)])
            testData.append(["f7f6", (([1,5], [2,5]), None)])
            testData.append(["g8f6", (([0,6], [2,5]), None)])
    
        for item in testData:
            self.testing1Arg(self.board.getCoordinatesFromMove, item[0], item[1])


    def MoveFromCoordinates(self) -> None:
        testData = []
        if self.board.side == Side.BLACK:
            testData.append([(1,3), (3,3), "e2e4"])
            testData.append([(6,2), (5,2), "f7f6"])
            testData.append([(7,1), (5,2), "g8f6"])
        
        else:
            testData.append([(6,4), (4,4), "e2e4"])
            testData.append([(6,2), (5,2), "c2c3"])
            testData.append([(7,1), (5,2), "b1c3"])
        
        for item in testData:
            self.testing2Arg(self.board.getMoveFromCoordinates, item[0], item[1], item[2])

    
    def testMouseMove(self, move: str) -> None:
        coordinates, isPromotion = self.board.translateMoveToPixels(move)
        Mouse.moveToCoordinates(coordinates[1])
        

if __name__ == "__main__":
    testBlack = Test(Side.BLACK)
    testBlack.CoordinatesFromMove()
    testBlack.MoveFromCoordinates()

    testWhite = Test(Side.WHITE)
    testWhite.CoordinatesFromMove()
    testWhite.MoveFromCoordinates()


    testBlack.testMouseMove("e2e4")
    
