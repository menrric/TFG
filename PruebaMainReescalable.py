# Form implementation generated from reading ui file '.\PruebaMainReescalable.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1025, 637)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.textLoger = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textLoger.setAutoFillBackground(False)
        self.textLoger.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.textLoger.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.textLoger.setLineWidth(1)
        self.textLoger.setMidLineWidth(0)
        self.textLoger.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textLoger.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textLoger.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.textLoger.setObjectName("textLoger")
        self.gridLayout_2.addWidget(self.textLoger, 0, 1, 7, 1)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.RInput = QtWidgets.QPushButton(parent=self.centralwidget)
        self.RInput.setObjectName("RInput")
        self.verticalLayout.addWidget(self.RInput)

        self.ROutput = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ROutput.setObjectName("ROutput")
        self.verticalLayout.addWidget(self.ROutput)

        self.ConfClasi = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ConfClasi.setObjectName("ConfClasi")
        self.verticalLayout.addWidget(self.ConfClasi)

        self.ConfParamCompile = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ConfParamCompile.setObjectName("ConfParamCompile")
        self.verticalLayout.addWidget(self.ConfParamCompile)

        self.IniEjec = QtWidgets.QPushButton(parent=self.centralwidget)
        self.IniEjec.setObjectName("IniEjec")
        self.verticalLayout.addWidget(self.IniEjec)

        self.Grafic = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Grafic.setObjectName("Grafic")
        self.verticalLayout.addWidget(self.Grafic)

        self.gridLayout_2.addLayout(self.verticalLayout, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1025, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "hola"))
        self.RInput.setText(_translate("MainWindow", "Ruta Input"))
        self.ROutput.setText(_translate("MainWindow", "Ruta Output"))
        self.ConfClasi.setText(_translate("MainWindow", "Configurar Clasificador"))
        self.ConfParamCompile.setText(_translate("MainWindow", "Parametros del Compile"))
        self.IniEjec.setText(_translate("MainWindow", "Inicio Ejecución"))
        self.Grafic.setText(_translate("MainWindow", "Gráficas"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())