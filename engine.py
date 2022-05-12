import subprocess
import logging
from config import Config

class Engine():
    # data
    moves = []


    def __init__(self, memoryMB=Config.hashMemory, thr=Config.threads):
        logging.info("Starting Engine...");
        self.__engine = subprocess.Popen(Config.path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.write("uci")
        self.write("setoption name Threads value "+str(thr))
        self.write("setoption name Hash value "+str(memoryMB))
        self.write("isready")

        tmp = self.read()
        while tmp != "readyok":
            tmp = self.read()
        print("Engine ready")
            

    def __encodeMessageToPIPE(self, msg: str) -> bytes:
        return "{}\n".format(msg).encode()


    def __decodeMessageFromPIPE(self, msg: bytes) -> str:
        return msg.decode("utf-8")


    def write(self, msg: str) -> None:
        logging.debug("Sending message to engine: " + msg)
        self.__engine.stdin.write(self.__encodeMessageToPIPE(msg))
        self.__engine.stdin.flush()


    def read(self) -> str:
        msg = self.__decodeMessageFromPIPE(self.__engine.stdout.readline()).strip()
        logging.debug("Received message from engine: " + msg)
        return msg


    def newGame(self) -> None:
        logging.info("Starting new game")
        self.moves.clear()
        self.write("ucinewgame")
        print("New game")


    def setStartPos(self) -> None:
        data = " ".join(self.moves)
        # print("position startpos moves "+data)
        self.write("position startpos moves " + data)


    def findDepthMove(self, depth=Config.depth) -> str:
        self.write("go depth " + str(depth))
        return self.readBestMoveResponse()


    def findTimeMove(self, time=Config.moveTime) -> str:
        self.write("go movetime " + str(time))
        return self.readBestMoveResponse()


    def findClockWhiteMove(self, clockTime: int) -> str:
        self.write("go wtime " + str(clockTime))
        return self.readBestMoveResponse()


    def findClockBlackMove(self, clockTime: int) -> str:
        self.write("go btime " + str(clockTime))
        return self.readBestMoveResponse()


    def readBestMoveResponse(self) -> str:
        tmp = self.read()
        while tmp.split()[0] != "bestmove":
            tmp = self.read()

        logging.debug("bestmove: " + tmp.split()[1])
        return tmp.split()[1]


    def move(self, move: str) -> None:
        logging.info("Engine move: " + move)
        self.moves.append(move)
