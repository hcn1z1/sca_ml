import os
import h5py

from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtUiTools import loadUiType

Dataset_UI,_ = loadUiType("uis/dataset.ui")

class DatasetLayout(QWidget,Dataset_UI):
    def __init__(self,parent = None):
        super(DatasetLayout,self).__init__(parent)
        self.setupUi(self)
        self.warning.hide()
        self.setted = False
        self.labels,self.metadata,self.traces = 0,0,0
        self.start_index_ = 0
        self.amount_ = 5 # least possible
        self.amount.textChanged.connect(self.check_amount)
        self.start_index.textChanged.connect(self.chack_index_value)
        self.path_edit.textChanged.connect(self.textChanged)
        self.browser_btn.clicked.connect(self.custom_dataset)
        self.display_info(False)
        self.path = None

    def check_amount(self):
        edited:str = self.amount.toPlainText()
        if edited.isnumeric() and self.start_index_ + int(edited) <= self.traces:
            self.amount_ = int(edited)
            self.setted = True
        else : 
            self.setted = False

    def chack_index_value(self):
        edited = self.start_index.toPlainText()
        if edited.isnumeric() and self.amount_ + int(edited) <= self.traces:
            self.start_index_ = int(edited)
            self.setted = True

        else: 
            self.setted = False

    def textChanged(self):
        path = self.path_edit.toPlainText()
        self.check_path(path)

    def custom_dataset(self):
        options = QFileDialog.Options()
        file_filter = "HDF5 Files (*.h5 *.hd5);;All Files (*)"
        model = QFileDialog.getOpenFileName(self,"Dataset","",file_filter,options=options)
        try:
            path = model[0]
            self.check_path(path)
        except:
            self.setted = False

    def check_path(self,edited):
        if os.path.exists(edited) and ("hd5" in edited or "h5" in edited):
            self.labels,self.metadata,self.traces = self.get_metadata(edited)
            self.path = edited
            if not (self.labels == None):
                self.warning.hide()
                self.display_info(True)
                self.info_edit.setText(f"{self.traces}\n{self.metadata}\n{self.labels}")
                return True
            else:
                self.warning.show()
                self.display_info(False)
        else:
            self.warning.show()
            self.display_info(False)
        return False

    def display_info(self,boolean):
        if boolean:
            self.info.show()
            self.info_edit.show()
            self.textBrowser.show()
            self.start_index.show()
            self.amount.show()
        else: 
            self.info.hide()
            self.info_edit.hide()
            self.textBrowser.hide()
            self.start_index.hide()
            self.amount.hide()
    def get_metadata(self,file):
        f = h5py.File(file)
        try:
            metadata = len(f["Attack_traces"]["metadata"])
            traces = len(f["Attack_traces"]["traces"])
            labels = len(f["Attack_traces"]["labels"])
        except:
            metadata,traces,labels = None, None, None
        
        return labels,metadata,traces