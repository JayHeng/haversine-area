#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import time
from PyQt5.Qt import *

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from win import haversineArea

class pointsFigure(FigureCanvas):

    def __init__(self,width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(pointsFigure,self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlabel('longitude')
        self.axes.set_ylabel('latitude')

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

    def _register_callbacks(self):
        self.pushButton_calc.clicked.connect(self.callbackCalc)

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

        pLongs = [p1long, p2long, p3long, p4long, p1long, p3long]
        pLats = [p1lat, p2lat, p3lat, p4lat, p1lat, p3lat]

        self.pointsFig = pointsFigure(width=1, height=1, dpi=50)
        self.pointsFig.plotPoints(pLongs, pLats, labels)
        self.pointsGridlayout = QGridLayout(self.groupBox_points)
        self.pointsGridlayout.addWidget(self.pointsFig,0,0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = areaMain(None)
    mainWin.show()

    sys.exit(app.exec_())

