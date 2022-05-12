from datetime import datetime
from engine import Engine
from board import Board
from chessPlayer import ChessPlayer

import logging


if __name__ == "__main__":
    logging.basicConfig(filename="logger.log", encoding="utf-8", format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG)
    logging.log(logging.CRITICAL, "---------------------------------------------------------------------------------------")
    logging.log(logging.CRITICAL, "-----------------------------------NEW LOG---------------------------------------------")
    logging.log(logging.CRITICAL, "---------------------------------------------------------------------------------------")
    logging.info("Starting program...")

    clockTime = int(input("Time on Clock [_min]: ")) * 60 #seconds
    startTime = datetime.now()

    engine = Engine()
    engine.newGame()

    board = Board()

    timeDiff = (clockTime - (datetime.now() - startTime).seconds) * 1000

    player = ChessPlayer(engine, board)
    player.play(timeDiff)

    logging.info("End of log")
