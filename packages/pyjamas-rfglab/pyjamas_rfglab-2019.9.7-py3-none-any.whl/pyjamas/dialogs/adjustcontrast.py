"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import numpy
from PyQt5 import QtCore, QtWidgets

from pyjamas.dialogs.matplotlibdialog import MatplotlibDialog
from pyjamas.external.qrangeslider import QRangeSlider
from pyjamas.pjscore import PyJAMAS


class AdjustContrastDialog(object):
    def __init__(self, pjs: PyJAMAS):
        super().__init__()

        self.pjs = pjs
        self.image: numpy.ndarray = self.pjs.slices[self.pjs.curslice]
        self.preview_window: MatplotlibDialog = None

    def setupUi(self, Dialog, min_percentile = None, max_percentile = None):

        if min_percentile is None or min_percentile is not False:
            min_percentile = self.pjs.min_pix_percentile

        if max_percentile is None or max_percentile is not False:
            max_percentile = self.pjs.max_pix_percentile

        self.dialog = Dialog
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(221, 245)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dialog.sizePolicy().hasHeightForWidth())
        self.dialog.setSizePolicy(sizePolicy)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-150, 200, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox_3 = QtWidgets.QGroupBox(self.dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 120, 181, 71))
        self.groupBox_3.setObjectName("groupBox_3")
        self.sbdilation = QtWidgets.QSpinBox(self.groupBox_3)
        self.sbdilation.setGeometry(QtCore.QRect(5, 40, 48, 24))
        self.sbdilation.setObjectName("sbdilation")
        self.sbdilation_2 = QtWidgets.QSpinBox(self.groupBox_3)
        self.sbdilation_2.setGeometry(QtCore.QRect(130, 40, 48, 24))
        self.sbdilation_2.setObjectName("sbdilation_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(55, 37, 71, 32))
        self.pushButton.setObjectName("pushButton")
        self.horizontalSlider = QRangeSlider(self.groupBox_3)
        self.horizontalSlider.setGeometry(QtCore.QRect(4, 20, 171, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

        self.retranslateUi()
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def accept(self):
        #self.close_preview_window()
        self.dialog.accept()

    def reject(self):
        #self.close_preview_window()
        self.dialog.reject()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("Dialog", "Adjust contrast"))
        self.groupBox_3.setTitle(_translate("Dialog", "Min and max"))
        self.pushButton.setText(_translate("Dialog", "Auto"))


