import typing
from PySide6.QtCore import QObject, QTimer,QThread

class Timer(QThread):
    def __init__(self, function, *args, parent=None):
        super().__init__(parent)
        self.args = args
        self.function = function
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(500)

    def run(self):
        self.function(*self.args)
