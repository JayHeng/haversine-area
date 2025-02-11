#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import time
from PyQt5.Qt import *

from win import haversineArea

class areaMain(QMainWindow, haversineArea.Ui_Area):

    def __init__(self, parent=None):
        super(areaMain, self).__init__(parent)
        self.setupUi(self)
        self._register_callbacks()

    def _register_callbacks(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = areaMain(None)
    mainWin.show()

    sys.exit(app.exec_())

