import time

from PySide6.QtWidgets import  QWidget
from PySide6.QtUiTools import loadUiType
from core.timer import Timer
from core.thread import Thread
from core.customizedtest import Evolution
from .model import ModelLayout
from .dataset import DatasetLayout

Testing_UI,_ = loadUiType("uis/loading_screen.ui")

class TestLayout(QWidget,Testing_UI):
    def __init__(self,parent=None):
        super(TestLayout,self).__init__(parent)
        self.setupUi(self)
        self.model = ModelLayout
        self.dataset = DatasetLayout 
        self.setted = False
        self.controller = False
        self.second_controller = False
        self.X = []
        self.Y = []
    
    def threads_controler(self):
        if self.controller == False and type(self.test.prediction) != type(None):
            self.prediction_complited()
            self.controller = True
            self.textEdit.setText("")
            self.textEdit.insertHtml('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: "\\2610"; }\nli.checked::marker { content: "\\2612"; }\n</style></head><body style=" font-family:"Source Code Pro"; font-size:15pt; font-weight:400; font-style:normal;">\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt;">Computing Target Byte (Third)</span></p></body></html>')
        elif self.controller and self.test.x != [] and self.second_controller == False:
            self.computing_complited()
            self.textEdit.setText("")
            self.textEdit.insertHtml('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: "\\2610"; }\nli.checked::marker { content: "\\2612"; }\n</style></head><body style=" font-family:"Source Code Pro"; font-size:15pt; font-weight:400; font-style:normal;">\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt;">Calculating and exporting all expected keys</span></p></body></html>')
            self.second_controller = True
            
        elif self.controller and self.second_controller and self.test.expected_keys != []:
            self.calculate_expected_keys_complited()
            self.timer.timer.stop()

    def start_thread(self):
        self.test = Evolution(self.model.path,self.dataset.path,self.dataset.start_index_,self.dataset.amount_)
        self.timer = Timer(TestLayout.threads_controler,self)
        self.timer.start()
        self.thread = Thread(self.test.getPrediction,self)
        self.thread.start()

    def prediction_complited(self):
        print("prediction complited at some point but not same pointer")
        self.progressBar.setValue(29)
        self.second_thread = Thread(self.test.getRanks,self)
        self.second_thread.start()

    def computing_complited(self):
        self.progressBar.setValue(70)
        self.X = self.test.x
        self.Y = self.test.y
        self.third_thread = Thread(self.test.start_custom_calculation,self)
        self.third_thread.start()
        

    def calculate_expected_keys_complited(self):
        self.progressBar.setValue(99)
        time.sleep(1)
        self.setted = True
