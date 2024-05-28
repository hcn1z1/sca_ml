import typing
from PyQt5.QtCore import QObject, QThread, pyqtSignal

class Thread(QThread):
    finished = pyqtSignal(object)
    def __init__(self, function, *args, parent=None):
        super().__init__(parent)
        self.function = function
        self.args = args

    def run(self):
        result = self.function()
        self.finished.emit(self.args)
        print("YES WE FINISHED and OMITTED")