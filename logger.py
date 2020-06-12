import logging, sys

class Logger(logging.Logger):
    def __init__(self, name):
        super().__init__(name, level=logging.DEBUG)
        self.handler = logging.StreamHandler(sys.stdout)
        self.handler.setLevel(logging.WARNING)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.handler.setFormatter(formatter)
        self.addHandler(self.handler)
        #File output
        fh = logging.FileHandler(f"./data/{name}.log")
        fh.setLevel(logging.WARNING) #change for file logging level change
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.addHandler(fh)

    def setLevel(self, level):
        level = level.lower()
        if level == "debug":
            self.handlers[0].setLevel(logging.DEBUG)
        elif level == "error":
            self.handlers[0].setLevel(logging.ERROR)
        elif level == "info":
            self.handlers[0].setLevel(logging.INFO)
        elif level == "warning":
            self.handlers[0].setLevel(logging.WARNING)

log = Logger('Corpgame')