from mss import mss
import numpy as np
from enum import Enum
from boardDetector import BoardDetector
import logging


#dontTouch!!
class Side(Enum):
    WHITE = 1
    BLACK = -1


#dontTouch!!
class Piece(Enum):
    pass


#dontTouch!!
class WhitePiece(Piece):
    #EMPTY = ' '
    KING = 'K'
    QUEEN = 'Q'
    BISHOP = 'B'
    KNIGHT = 'N'
    ROOK = 'R'
    PAWN = 'P'


#dontTouch!!
class BlackPiece(Piece):
    #EMPTY = ' '
    KING = 'k'
    QUEEN = 'q'
    BISHOP = 'b'
    KNIGHT = 'n'
    ROOK = 'r'
    PAWN = 'p'


class Board():
    # board dimensions
    __firstCorner = None
    __secondCorner = None
    __width = None
    __height = None
    __sct = None
    __monitor = None

    # config
    labelNumber = ["1", "2", "3", "4", "5", "6", "7", "8"]
    labelLetter = ["a", "b", "c", "d", "e", "f", "g", "h"]

    # data
    side: Side = None
    #castlingBlack = False
    #castlingWhite = False
    #__enemyCastling = False
    oldBoard = None
    curBoard = None
    positionsFlags = None


    #DONE
    def __init__(self) -> None:
        logging.info("Initializing Board...");
        self.__resetBoard()
        self.__detectBoard()
        #self.__chooseSide()
        #self.__initPositionsFlags()
        self.__initBoardDetector()
    

    #DONE
    def __detectBoard(self) -> None:
        logging.debug("Detecting top-left corner of the board")
        print("Click on top-left corner of the board")
        self.__firstCorner = BoardDetector.detectBoard()

        logging.debug("Detecting bottom-right corner of the board")
        print("Click on bottom-right corner of the board")
        self.__secondCorner = BoardDetector.detectBoard()

        self.__width = abs(self.__secondCorner[0] - self.__firstCorner[0])
        self.__height = abs(self.__secondCorner[1] - self.__firstCorner[1])
        self.__tileWidth = self.__width / len(self.labelLetter)
        self.__tileHeight = self.__height / len(self.labelNumber)

        logging.debug("\twidth: {} height: {}".format(str(self.__width), str(self.__height)))
        logging.debug("\ttileWidth: {} tileHeight: {}".format(str(self.__tileWidth), str(self.__tileHeight)))


    #DONE
    def __resetBoard(self) -> None:
        logging.debug("Resetting board")
        self.__firstCorner = None
        self.__secondCorner = None
        self.__width = None
        self.__height = None
        self.__tileWidth = None
        self.__tileHeight = None

        self.side = None
        #self.castlingBlack = False
        #self.castlingWhite = False
        self.__enemyCastling = False
        self.positionsFlags = []


    #DONE
    def clearBoardImageCache(self) -> None:
        logging.debug("Clearing board image cache")
        self.oldBoard = None
        self.curBoard = None
        self.curBoard = np.array( self.__sct.grab(self.__monitor) )
        self.oldBoard = self.curBoard


    #DONE
    def setSide(self, side: Side) -> None:
        logging.info("Set Side: " + str(side))
        self.side = side
        self.__initPositionsFlags()


    #DONE
    def translateMoveToPixels(self, move: str) -> tuple:
        logging.debug("TranslateMoveToPixels...")
        coordinates, isPromotion = self.getCoordinatesFromMove(move)
        firstCoordinate = coordinates[0]
        secondCoordinate = coordinates[1]
        
        firstCoordinate[0] += 1
        firstCoordinate[1] += 1

        secondCoordinate[0] += 1
        secondCoordinate[1] += 1

        tmpPixel1 = int( self.__firstCorner[0] + ( firstCoordinate[1]*self.__tileWidth - self.__tileWidth/2) )
        tmpPixel2 = int( self.__firstCorner[1] + ( firstCoordinate[0]*self.__tileHeight - self.__tileHeight/2) )

        tmpPixel3 = int( self.__firstCorner[0] + ( secondCoordinate[1]*self.__tileWidth - self.__tileWidth/2) )
        tmpPixel4 = int( self.__firstCorner[1] + ( secondCoordinate[0]*self.__tileHeight - self.__tileHeight/2) )

        firstScreenCoordinates = (tmpPixel1, tmpPixel2)
        secondScreenCoordinates = (tmpPixel3, tmpPixel4)

        data = (firstScreenCoordinates, secondScreenCoordinates)

        logging.debug("TranslateMoveToPixels move: " + str(move) + " pixels: " + str(data) + " promotion: " + str(isPromotion))
        
        return data, isPromotion


    #DONE
    def __initPositionsFlags(self) -> None:
        logging.debug("Initializing Positions Flags")
        if self.side == Side.WHITE:
            self.positionsFlags = [
                [BlackPiece.ROOK, BlackPiece.KNIGHT, BlackPiece.BISHOP, BlackPiece.QUEEN, BlackPiece.KING, BlackPiece.BISHOP, BlackPiece.KNIGHT, BlackPiece.ROOK],
                [BlackPiece.PAWN]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [WhitePiece.PAWN]*8,
                [WhitePiece.ROOK, WhitePiece.KNIGHT, WhitePiece.BISHOP, WhitePiece.QUEEN, WhitePiece.KING, WhitePiece.BISHOP, WhitePiece.KNIGHT, WhitePiece.ROOK]
            ]

        else:
            self.positionsFlags = [
                [WhitePiece.ROOK, WhitePiece.KNIGHT, WhitePiece.BISHOP, WhitePiece.KING, WhitePiece.QUEEN, WhitePiece.BISHOP, WhitePiece.KNIGHT, WhitePiece.ROOK],
                [WhitePiece.PAWN]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [BlackPiece.PAWN]*8,
                [BlackPiece.ROOK, BlackPiece.KNIGHT, BlackPiece.BISHOP, BlackPiece.KING, BlackPiece.QUEEN, BlackPiece.BISHOP, BlackPiece.KNIGHT, BlackPiece.ROOK]
            ]


    #DONE
    def __initBoardDetector(self) -> None:
        logging.info("Initializing Board Detector")
        self.__sct = mss()
        self.__monitor = {"top": self.__firstCorner[1], "left": self.__firstCorner[0], "width": self.__width, "height": self.__height}
        self.curBoard = np.array( self.__sct.grab(self.__monitor) )
        self.oldBoard = self.curBoard


    #DONE
    #BGRA - Blue Green Red Alpha
    #img[rows, cells(columns), color(BGRA)]                 chessboard: [ranks, files, squares]
    def detectBoardChange(self) -> None:
        logging.info("Detecting board change")
        img = np.array( self.__sct.grab(self.__monitor) )

        moves = self.getChangedCoordinates()

        # while (img == self.curBoard).all():
        #     self.curBoard = img
        #     img = np.array( self.__sct.grab(self.__monitor) )

        while moves == None:
            self.curBoard = img
            img = np.array( self.__sct.grab(self.__monitor) )
            moves = self.getChangedCoordinates()
        
        self.oldBoard = self.curBoard
        self.curBoard = img
        
        return moves

    
    #ToRemove
    def handleBoardChange(self) -> None:
        logging.warn("handleBoardChange")
        changedCoordinates = self.getChangedCoordinates()

        if changedCoordinates is not None:
            pass


    #DONE
    def printBoard(self) -> None:
        #a = self.positionsFlags
        print(" +---+---+---+---+---+---+---+---+ ")
        logging.debug(" +---+---+---+---+---+---+---+---+ ")
        for item in self.positionsFlags:
            #item = self.positionsFlags[i]
            a = list(map(lambda x: ' ' if x is None else x.value, item))
            print(" | {} | ".format(" | ".join(a)))
            print(" +---+---+---+---+---+---+---+---+ ")
            logging.debug(" | {} | ".format(" | ".join(a)))
            logging.debug(" +---+---+---+---+---+---+---+---+ ")


    #TODO check (Get Enemy move)
    def getChangedMove(self, changedCoordinates, isBot = False) -> str:
        #self.handleBoardChange()
        #changedCoordinates = self.getChangedCoordinates()
        changedMove = None
        firstCoordinates = None
        secondCoordinates = None
        startPiece = None
        endPiece = None

        print("--------------------")
        print("-" + str(changedCoordinates) + "-")
        print("--------------------")

        if changedCoordinates is not None and changedCoordinates != []:
            #Normal move
            if len(changedCoordinates) == 2:
                #print("Normal Move")
                firstPiece = self.getPieceOnCoordinates(changedCoordinates[0])
                secondPiece = self.getPieceOnCoordinates(changedCoordinates[1])

                print(firstPiece)
                print(secondPiece)

                #If bot is White then we are checking which piece is black (startpos)
                if self.side == Side.WHITE:
                    if firstPiece is not None and firstPiece.value in set(item.value for item in BlackPiece):
                        firstCoordinates = changedCoordinates[0]
                        secondCoordinates = changedCoordinates[1]
                        startPiece = firstPiece
                    elif secondPiece is not None and secondPiece.value in set(item.value for item in BlackPiece):
                        firstCoordinates = changedCoordinates[1]
                        secondCoordinates = changedCoordinates[0]
                        endPiece = secondPiece
                
                #If bot is Black then we are checking which piece is white (startPos)
                elif self.side == Side.BLACK:
                    if firstPiece is not None and firstPiece.value in set(item.value for item in WhitePiece):
                        firstCoordinates = changedCoordinates[0]
                        secondCoordinates = changedCoordinates[1]
                        startPiece = firstPiece
                    elif secondPiece is not None and secondPiece.value in set(item.value for item in WhitePiece):
                        firstCoordinates = changedCoordinates[1]
                        secondCoordinates = changedCoordinates[0]
                        endPiece = secondPiece

            #castling
            elif len(changedCoordinates) == 4:
                #if self.side == Side.WHITE:
                #top-right
                print("CASTLING left : right")
                print(self.getPieceOnCoordinates(changedCoordinates[0]))
                print(self.getPieceOnCoordinates(changedCoordinates[3]))
                if self.getPieceOnCoordinates(changedCoordinates[0]) == BlackPiece.KING or self.getPieceOnCoordinates(changedCoordinates[0]) == WhitePiece.KING:
                    print("King on left")
                    firstCoordinates = changedCoordinates[0]    #from
                    secondCoordinates = changedCoordinates[2]   #to
                    #self.positionsFlags[changedCoordinates[1][0]][changedCoordinates[1][1]] = self.positionsFlags[changedCoordinates[3][0]][changedCoordinates[3][1]]   #
                    #self.positionsFlags[changedCoordinates[3][0]][changedCoordinates[3][1]] = None
                #top-left
                elif self.getPieceOnCoordinates(changedCoordinates[3]) == BlackPiece.KING or self.getPieceOnCoordinates(changedCoordinates[3]) == WhitePiece.KING:
                    print("King on right")
                    firstCoordinates = changedCoordinates[3]    #from
                    secondCoordinates = changedCoordinates[1]   #to
                    #self.positionsFlags[changedCoordinates[2][0]][changedCoordinates[2][1]] = self.positionsFlags[changedCoordinates[0][0]][changedCoordinates[0][1]]   #
                    #self.positionsFlags[changedCoordinates[0][0]][changedCoordinates[0][1]] = None
                # elif self.side == Side.BLACK:
                #     if self.getPieceOnCoordinates(changedCoordinates[0]) == BlackPiece.QUEEN:
                #         pass
                #     elif self.getPieceOnCoordinates(changedCoordinates[3]) == BlackPiece.QUEEN:
                #         pass


            #TODO en passant
            elif len(changedCoordinates) == 3:
                pass


            if firstCoordinates is not None and secondCoordinates is not None:
                changedMove = self.getMoveFromCoordinates(firstCoordinates, secondCoordinates)
            else:
                return

            #self.__executeMoveAsCoordinates()
            self.executeMove(changedMove)
        
        logging.info("GetChangeMove move: " + str(changedMove))

        return changedMove


    def executeMove(self, move: str) -> None:
        logging.debug("ExecuteMove move: " + str(move))
        coordinates, promotion = self.getCoordinatesFromMove(move)
        firstCoordinates = coordinates[0]
        secondCoordinates = coordinates[1]

        #checking if king moved 2 squares - castling
        pieceOnFirstCoordinate = self.getPieceOnCoordinates(firstCoordinates)
        if pieceOnFirstCoordinate == WhitePiece.KING or pieceOnFirstCoordinate == BlackPiece.KING:
            distance = ((float(firstCoordinates[0]) - float(secondCoordinates[0]))**2.0 + (float(firstCoordinates[1]) - float(secondCoordinates[1]))**2.0)**0.5
            #print("DISTANCE: " + str(distance))

            if distance == 2.0 and firstCoordinates[0] == secondCoordinates[0]:
                logging.debug("Detected castling: " + move)
                #king goes right
                if secondCoordinates[1] > firstCoordinates[1]:
                    self.positionsFlags[firstCoordinates[0]][firstCoordinates[1]+1] = self.positionsFlags[firstCoordinates[0]][7]
                    self.positionsFlags[firstCoordinates[0]][7] = None
                #king goes left
                elif secondCoordinates[1] < firstCoordinates[1]:
                    self.positionsFlags[firstCoordinates[0]][firstCoordinates[1]-1] = self.positionsFlags[firstCoordinates[0]][0]
                    self.positionsFlags[firstCoordinates[0]][0] = None
                    pass

            elif distance == 2.0:
                msg = "Distance 2.0 in king move but not on same row?"
                logging.critical(msg)
                print(msg)
                
        self.positionsFlags[secondCoordinates[0]][secondCoordinates[1]] = self.positionsFlags[firstCoordinates[0]][firstCoordinates[1]]
        self.positionsFlags[firstCoordinates[0]][firstCoordinates[1]] = None


    #DONE
    def getChangedCoordinates(self) -> list:
        changedCoordinates = None

        if self.oldBoard is not None:
            changedCoordinates = list()

            for i in range(len(self.labelNumber)):
                heightLeftOffset = int((i)*self.__tileHeight)+10
                heightRightOffset = int((i+1)*self.__tileHeight)-10
                

                for j in range(len(self.labelLetter)):
                    widthLeftOffset = int((j)*self.__tileWidth)+10
                    widthRightOffset = int((j+1)*self.__tileWidth)-10
                    #print(self.positionsFlags[i][j])

                    if (self.oldBoard[heightLeftOffset:heightRightOffset, widthLeftOffset:widthRightOffset] != self.curBoard[heightLeftOffset:heightRightOffset, widthLeftOffset:widthRightOffset]).any():
                        changedCoordinates.append((i,j))

        if changedCoordinates == []:
            changedCoordinates = None

        if changedCoordinates is not None:
            logging.debug("GetChangedCoordinates coordinates: " + str(changedCoordinates))

        return changedCoordinates


    #TODO check
    def getMoveFromCoordinates(self, firstData: tuple, secondData: tuple) -> str:
        move = ''
        
        firstCoordinate = [None, None]
        secondCoordinate = [None, None]
        firstCoordinate[0], firstCoordinate[1] = firstData[0], firstData[1]
        secondCoordinate[0], secondCoordinate[1] = secondData[0], secondData[1]

        if self.side == Side.WHITE:
            firstCoordinate[0] = 7 - firstCoordinate[0]
            #firstCoordinate[1] = 7 - firstCoordinate[1]     #TODO make sure it's not necessary
            secondCoordinate[0] = 7 - secondCoordinate[0]
            #secondCoordinate[1] = 7 - secondCoordinate[1]   #TODO make sure it's not necessary
            pass
        else:
            firstCoordinate[1] = 7 - firstCoordinate[1]
            secondCoordinate[1] = 7 - secondCoordinate[1]

        move += self.labelLetter[firstCoordinate[1]] + self.labelNumber[firstCoordinate[0]]
        move += self.labelLetter[secondCoordinate[1]] + self.labelNumber[secondCoordinate[0]]

        #Pawns cannot go backwards
        if self.getPieceOnCoordinates(secondCoordinate) == WhitePiece.PAWN:
            if secondCoordinate[0] == 0 or secondCoordinate[0] == 8:
                newPiece = input("Enter promoted piece: ")
                move += newPiece
            # if self.side == Side.WHITE and secondCoordinate[0] == 8:
            #     pass
            # elif self.side == Side.BLACK and secondCoordinate[0] == 8:
            #     pass

        logging.debug("GetMoveFromCoordinates coordinates: " + str(firstData) + " -> " + str(secondData) + " move: " + str(move))

        return move


    #DONE
    #list coordinates
    def getCoordinatesFromMove(self, move: str, isBot = False) -> tuple:
        logging.debug("GetCoordinatesFromMove...")
        
        data = tuple()
        promotion = None
        # print(move)
        # print("----------")
        moveLength = 0 if move is None else len(move)
        # print(moveLength)
        #print(move)
        #print(moveLength)
        if moveLength == 4 or moveLength == 5:
            firstCoordinate = [self.labelNumber.index(move[1:2]), self.labelLetter.index(move[0:1])]
            secondCoordinate = [self.labelNumber.index(move[3:4]), self.labelLetter.index(move[2:3])]
            #print(firstCoordinate)
            #print(secondCoordinate)
            if self.side == Side.WHITE:
                firstCoordinate[0] = 7 - firstCoordinate[0]
                #firstCoordinate[1] = 7 - firstCoordinate[1]     #TODO make sure it's not necessary
                secondCoordinate[0] = 7 - secondCoordinate[0]
                #secondCoordinate[1] = 7 - secondCoordinate[1]   #TODO make sure it's not necessary
            else:
                firstCoordinate[1] = 7 - firstCoordinate[1]
                secondCoordinate[1] = 7 - secondCoordinate[1]

            data = firstCoordinate, secondCoordinate

            if moveLength == 5:
                promotion = move[4]
        
        logging.debug("GetCoordinatesFromMove move: " + str(move) + " coordinates: " + str(data) + " promotion: " + (promotion if promotion is not None else ''))

        return data, promotion


    #DONE
    def getPieceOnCoordinates(self, coordinates: tuple) -> Piece:
        piece = self.positionsFlags[coordinates[0]][coordinates[1]]
        logging.debug("PieceOnCoordinates coordinates: " + str(coordinates) + " piece: " + 'None' if piece is None else piece.value)
        return piece
