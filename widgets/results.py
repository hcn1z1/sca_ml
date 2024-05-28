import sys,os
import json
import re
import h5py
import time

from PySide6.QtWidgets import QWidget
from PySide6.QtUiTools import loadUiType
from core.customizedtest import Evolution
import pyqtgraph as PyPlot

Result_UI,_ = loadUiType("uis/results.ui")


class ResultLayout(QWidget,Result_UI):
    def __init__(self,parent = None):
        super(ResultLayout,self).__init__(parent)
        self.setupUi(self)
        self.setted = True
        self.all_expected_keys = []
        self.real_key = 0
        self.max1,self.max2 = 0,0 # high count expected keys

    def set_graph(self,X,Y):
        self.PlotWidget = PyPlot.PlotWidget()
        self.textBrowser.setText("")
        self.textBrowser.setHtml('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: "\\2610"; }\nli.checked::marker { content: "\\2612"; }\n</style></head><body style=" font-family:"Source Code Pro Medium"; font-size:10pt; font-weight:500; font-style:normal;">\n<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;">\n<li style=" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:700;">Real Key :</span> RealKey</li>\n<li style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:700;">Predicted Key Byte :</span> ExpectedKey1 </li>\n<li style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:700;">Second Predicted Key Byte :</span> ExpectedKey2</li></ul></body></html>'.replace("RealKey",str(self.real_key)).replace("ExpectedKey1",str(self.max1)).replace("ExpectedKey2",str(self.max2)))
        self.info_edit.setText(f"{int(self.all_expected_keys.count(self.max1)/len(self.all_expected_keys)*100)} %\n{int(self.all_expected_keys.count(self.max2)/len(self.all_expected_keys)*100)} %")
        self.resultLayout.addWidget(self.PlotWidget)
        self.PlotWidget.plot(X,Y)

    def set_keys(self,test:Evolution): # don't wanna add the whole object to the init
        self.all_expected_keys = test.expected_keys
        self.max1,self.max2 = test.find_max_and_second_max()
        self.real_key = test.real_key