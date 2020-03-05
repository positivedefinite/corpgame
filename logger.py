import logging, sys

class Logger(logging.Logger):
    def __init__(self, name):
        super().__init__(name, level=logging.DEBUG)
        self.handler = logging.StreamHandler(sys.stdout)
        self.handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        self.handler.setFormatter(formatter)
        self.addHandler(self.handler)

    def setLevel(self, level):
        level = level.lower()
        if level == "debug":
            super(Logger, self).setLevel(logging.DEBUG)
        elif level == "error":
            super(Logger, self).setLevel(logging.ERROR)
        elif level == "info":
            super(Logger, self).setLevel(logging.INFO)
        elif level == "warning":
            super(Logger, self).setLevel(logging.WARNING)

    def setFile(self, file='logs.txt'):
        self.handlers = []
        fh = logging.FileHandler(file)
        fh.setLevel(logging.DEBUG)
        self.addHandler(self.handler)
        self.addHandler(fh)


log = Logger("cbcm-game")
