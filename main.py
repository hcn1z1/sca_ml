# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Qt
from core.timer import Timer
from img_rc import *
from widgets.model import ModelLayout
from widgets.dataset import DatasetLayout
from widgets.test import TestLayout
from widgets.results import ResultLayout


from ui_form import Ui_Form

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.cls.clicked.connect(lambda b:self.close())
        self.ui.mnm.clicked.connect(lambda g:self.showMinimized())
        self.progress_buttons = [self.ui.model_btn,self.ui.dataset_btn,self.ui.testing_btn,self.ui.results_btn]
        self.widgets = [ModelLayout(),DatasetLayout(),TestLayout(),ResultLayout()]
        self.progress_index = 0
        self.last_widget_index = 0
        self.progressed_styleSheet = self.ui.model_btn.styleSheet()
        self.default_btn_styleSheet = self.ui.dataset_btn.styleSheet()
        [self.ui.stackedWidget.addWidget(widget) for widget in self.widgets]
        self.ui.stackedWidget.setCurrentWidget(self.widgets[0])
        self.ui.next_btn.clicked.connect(self.connect_next_window)
        self.ui.previous_btn.clicked.connect(self.connect_previous_window)
        self.ui.reload_btn.clicked.connect(self.reload_everything)
        self.thread = Timer(Dialog.enable_or_disable_next_button,self) # A timer
        self.thread.run()

    def connect_next_window(self):
        self.progress_index +=1
        self.progress_index %=4
        self.set_on_progress()
        
    
    def connect_previous_window(self):
        self.progress_index -=1
        self.progress_index %=4
        self.set_on_progress()

    def enable_or_disable_next_button(self):
        if self.progress_index == 2:
            if self.widgets[self.progress_index].setted:
                self.connect_next_window()
        else : 
            self.ui.next_btn.setDisabled(not self.widgets[self.progress_index].setted)
        

    def set_on_progress(self):
        button = self.progress_buttons[self.progress_index%4]
        last_progress = self.progress_buttons[(self.progress_index-1)%4]
        next_progress = self.progress_buttons[(self.progress_index+1)%4]
        button.setStyleSheet(self.progressed_styleSheet)
        last_progress.setStyleSheet(self.default_btn_styleSheet)
        next_progress.setStyleSheet(self.default_btn_styleSheet)
        self.ui.stackedWidget.setCurrentWidget(self.widgets[self.progress_index])
        self.ui.next_btn.setDisabled(not self.widgets[self.progress_index].setted)        
        
        if self.progress_index == 0:
            self.ui.previous_btn.hide()
        
        elif self.progress_index == 2: # waiting 
            self.widgets[self.progress_index].model = self.widgets[0] # set dynamic data
            self.widgets[self.progress_index].dataset = self.widgets[1] # this way we inherit all data without webserver
            self.widgets[self.progress_index].start_thread()
            self.ui.next_btn.hide()
            self.ui.previous_btn.hide()

        elif self.progress_index == 3:
            self.widgets[self.progress_index].set_keys(self.widgets[2].test)
            self.widgets[self.progress_index].set_graph(self.widgets[2].X,self.widgets[2].Y) # get X and Y from TestLayout

        else:
            self.ui.next_btn.show()
            self.ui.previous_btn.show()
    
    def reload_everything(self):
        [self.ui.stackedWidget.removeWidget(widget) for widget in self.widgets]
        self.widgets = [ModelLayout(),DatasetLayout(),TestLayout(),ResultLayout()]
        [self.ui.stackedWidget.addWidget(widget) for widget in self.widgets]
        self.ui.stackedWidget.setCurrentWidget(self.widgets[0])
        self.progress_index = 0
        self.set_on_progress()
        self.ui.next_btn.show()
        self.ui.previous_btn.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Dialog()
    widget.show()
    sys.exit(app.exec())
