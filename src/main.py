#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import math
import time
from PyQt5.Qt import *
from haversine import haversine
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.font_manager import FontProperties

from win import haversineArea

def herons_formula(a, b, c):
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return area

def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

class pointsFigure(FigureCanvas):

    def __init__(self,width=5, height=4, dpi=100, font=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(pointsFigure,self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlabel('longitude, West -> East', fontproperties=font)
        self.axes.set_ylabel('latitude, South -> North')

    def plotPoints(self, longs, lats, labels):
        self.axes.scatter(longs, lats)
        self.axes.plot(longs, lats)

        for i, label in enumerate(labels):
            self.axes.annotate(label, (longs[i], lats[i]), fontsize=15)

class areaMain(QMainWindow, haversineArea.Ui_Area):

    def __init__(self, parent=None):
        super(areaMain, self).__init__(parent)
        self.setupUi(self)
        self._register_callbacks()
        self.exeTopRoot = os.getcwd()
        exeMainFile = os.path.join(self.exeTopRoot, 'src', 'main.py')
        if not os.path.isfile(exeMainFile):
            self.exeTopRoot = os.path.dirname(os.path.dirname(__file__))
        self._setUserFont()
        self.pointsGridlayout = QGridLayout(self.groupBox_points)

    def _register_callbacks(self):
        self.pushButton_calc.clicked.connect(self.callbackCalc)

    def _setUserFont( self ):
        userFontPath = os.path.abspath(os.path.join(self.exeTopRoot, 'font', 'MicrogrammaDBolExt.ttf'))
        self.font = FontProperties(fname=userFontPath)

    def callbackCalc(self):
        labels = ['p1', 'p2', 'p3', 'p4', 'p1', 'p3']

        p1long = float(self.lineEdit_p1long.text())
        p2long = float(self.lineEdit_p2long.text())
        p3long = float(self.lineEdit_p3long.text())
        p4long = float(self.lineEdit_p4long.text())

        p1lat = float(self.lineEdit_p1lat.text())
        p2lat = float(self.lineEdit_p2lat.text())
        p3lat = float(self.lineEdit_p3lat.text())
        p4lat = float(self.lineEdit_p4lat.text())

        p1 = (p1lat, p1long)
        p2 = (p2lat, p2long)
        p3 = (p3lat, p3long)
        p4 = (p4lat, p4long)

        pLongs = [p1long, p2long, p3long, p4long, p1long, p3long]
        pLats = [p1lat, p2lat, p3lat, p4lat, p1lat, p3lat]

        self.pointsFig = pointsFigure(width=1, height=1, dpi=60, font=self.font)
        self.pointsFig.plotPoints(pLongs, pLats, labels)
        clear_layout(self.pointsGridlayout)
        self.pointsGridlayout.addWidget(self.pointsFig,0,0)

        p1p2 = haversine(p1, p2, unit='m')
        self.lineEdit_p1p2.setText("{:.3f}".format(p1p2) + 'm')
        p2p3 = haversine(p2, p3, unit='m')
        self.lineEdit_p2p3.setText("{:.3f}".format(p2p3) + 'm')
        p3p4 = haversine(p3, p4, unit='m')
        self.lineEdit_p3p4.setText("{:.3f}".format(p3p4) + 'm')
        p4p1 = haversine(p4, p1, unit='m')
        self.lineEdit_p4p1.setText("{:.3f}".format(p4p1) + 'm')
        p1p3 = haversine(p1, p3, unit='m')
        self.lineEdit_p1p3.setText("{:.3f}".format(p1p3) + 'm')

        p1p2p3 = herons_formula(p1p2, p2p3, p1p3)
        p1p3p4 = herons_formula(p1p3, p3p4, p4p1)
        p1p2p3p4 = p1p2p3 + p1p3p4
        self.lineEdit_area.setText("{:.3f}".format(p1p2p3p4) + 'm2')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = areaMain(None)
    mainWin.show()

    sys.exit(app.exec_())

