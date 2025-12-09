from PyQt5.QtCore import QThread

class ThreadWorker(QThread):
    def __init__(self, function):
        super().__init__()
        self.function = function

    def run(self):
        self.function()
