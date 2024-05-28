import json
import re

from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtUiTools import loadUiType

Model_UI,_ = loadUiType("uis/model.ui")

class ModelLayout(QWidget,Model_UI):
    def __init__(self,parent=None):
        super(ModelLayout,self).__init__(parent)
        self.models_json = json.load(open("models/models.json","r"))
        self.models = ["Model : Nc {}, Pa {} , Bs {} / {}".format(model["epoches"],model["learning_rate"],model["batche"],model["model"]) for model in self.models_json]
        self.setupUi(self)
        self.info.hide()
        self.info_edit.hide()
        self.comboBox.addItems(self.models)
        self.comboBox.currentIndexChanged.connect(self.set_path)
        self.browser_btn.clicked.connect(self.custom_model)
        self.setted = False
        self.path = None
    
    def custom_model(self):
        options = QFileDialog.Options()
        file_filter = "HDF5 Files (*.h5 *.hd5);;All Files (*)"
        model = QFileDialog.getOpenFileName(self,"Model","",file_filter,options=options)
        try:
            self.path = model[0]
            self.setted = True
            self.info.show()
            self.info_edit.show()
        except:
            self.setted = False
            self.info_edit.setText("{}\n{}\n{}".format("?","?","?"))
                                            

    def set_path(self):
        self.path = self.comboBox.currentText().split("/ ")[1]
        self.setted = True
        self.info.show()
        self.info_edit.show()
        infos = ModelLayout.re_info(self.comboBox.currentText())
        self.info_edit.setText("{}\n{}\n{}".format(infos["Nc"][0],infos["Bs"][0],infos["Pa"][0]))

    @staticmethod
    def re_info(text):
        pattern = r"(Nc\s+([\d\*\-\+eE]+))|(Pa\s+([\d\*\-\+eE]+))|(Bs\s+([\d\*\-\+eE]+))"
        matches = re.findall(pattern, text)
        positions = {
            'Nc': [],
            'Pa': [],
            'Bs': []
        }
        for match in matches:
            for i, label in enumerate(['Nc', 'Pa', 'Bs']):
                value = match[i * 2 + 1]
                if value:
                    positions[label].append(value)
        
        return positions