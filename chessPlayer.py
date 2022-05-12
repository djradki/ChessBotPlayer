import logging
from boardDetector import BoardDetector
from engine import Engine
from board import Board, Side
from mouse import Mouse
from datetime import datetime
from enum import Enum
from config import Config

#TODO
#   En passant                (board)


class ChessPlayer():
    def __init__(self, engine: Engine, board: Board):
        logging.info("Initializing ChessPlayer...")
        self.engine = engine
        self.board = board
        self.clockTime = 0
        self.side = None
        self.__chooseSide()
        print("init Chess Player")


    #DONE
    def __chooseSide(self):
        logging.info("Player choosing side...")

        side = None

        while side != "w" and side != "b":
            side = input("Your side [w|b]: ")
            
        if side == "w":
            self.side = Side.WHITE
        elif side == "b":
            self.side = Side.BLACK

        self.board.setSide(self.side)


    def play(self, clockTime: int): #left clockTime in ms
        logging.info("Playing...")
        self.clockTime = clockTime
        
        self.board.printBoard()

        if self.side == Side.WHITE:
            move = "e2e4"
            coordinates, _ = self.board.translateMoveToPixels(move)
            Mouse.dragAndDrop(coordinates[0], coordinates[1])
            self.makeMove(move)

        else:
            move = input("Write enemy's first move: ")
            coordinates, _ = self.board.translateMoveToPixels(move)
            Mouse.dragAndDrop(coordinates[0], coordinates[1])
            self.makeMove(move)

            #Find best move
            self.engine.setStartPos()
            bestMove = self.findBestMove()
            # oldTime = datetime.now()
            # bestMove = self.engine.findTimeMove(5000)
            # newTime = datetime.now()

            # if (newTime - oldTime).seconds < 1:
            #     time.sleep(2)

            coordinates, isPromotion = self.board.translateMoveToPixels(bestMove)
            Mouse.dragAndDrop(coordinates[0], coordinates[1])

            if isPromotion is not None:
                print("Choose: {0}".format(isPromotion))
                BoardDetector.waitForClick()
                Mouse.resetPositionToZero()

            self.makeMove(bestMove)
            self.board.clearBoardImageCache()

        while True:
            self.board.printBoard()
            self.board.clearBoardImageCache()
            boardCoordinates = self.board.detectBoardChange()
            startTime = datetime.now()


            # changedCoordinates = self.board.getChangedCoordinates()
            changedMove = self.board.getChangedMove(boardCoordinates)
            print("-----")
            print("-" + str(changedMove) + "-")
            print("-----")
            if changedMove == None or changedMove == '':
                continue
            #self.board.executeMove(changedMove)    #(board should automaticly execute enemy move)
            self.engine.move(changedMove)
            print("Enemy move: " + changedMove)

            #Find best move
            self.engine.setStartPos()
            bestMove = self.findBestMove()
            
            # if Config.playerType == Config.PlayerType.TIME:
            #     bestMove = self.engine.findTimeMove()
            # else:
            #     bestMove = self.engine.findDepthMove()
            # newTime = datetime.now()

            # if (newTime - oldTime).seconds < 2:
            #     time.sleep(2)

            print("bestmove: " + bestMove)

            #Get pixels coordinates and move piece
            coordinates, isPromotion = self.board.translateMoveToPixels(bestMove)
            Mouse.dragAndDrop(coordinates[0], coordinates[1])
            
            #If promotion then wait for click
            if isPromotion is not None:
                print("Choose: {0}".format(isPromotion))
                #self.board.positionsFlags
                BoardDetector.waitForClick()
                Mouse.resetPositionToZero()
            
            self.clockTime -= (datetime.now() - startTime).seconds * 1000

            #Update program's data
            # self.engine.move(bestMove)
            # self.board.executeMove(bestMove)
            self.makeMove(bestMove)

            #Clear 'old' image board cache
            self.board.clearBoardImageCache()
            #self.board.detectBoardChange()
    
    
    def makeMove(self, move: str) -> None:
        self.engine.move(move)
        self.board.executeMove(move)


    def findBestMove(self) -> str:
        bestMove = ''

        if Config.playerType == Config.PlayerType.TIME:
            bestMove = self.engine.findTimeMove()
        elif Config.playerType == Config.PlayerType.DEPTH:
            bestMove = self.engine.findDepthMove()
        elif Config.playerType == Config.PlayerType.CLOCK_TIME:
            if self.board.side == Side.WHITE:
                bestMove = self.engine.findClockWhiteMove(self.clockTime)
            elif self.board.side == Side.BLACK:
                bestMove = self.engine.findClockBlackMove(self.clockTime)
            else:
                logging.critical("Wrong side during finding bestMove")
                exit()

        return bestMove
