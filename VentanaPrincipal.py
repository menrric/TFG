from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QDialog
from ConfiguracionClasificador import Ui_ConfiguracionClasificador


class Ui_MainWindow(QDialog):


    def setupUi(self, MainWindow):

        self.diccionario={}

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(576, 391)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(670, 560, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(385, 200, 170, 170))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        #Input path and bouton
        self.ruta=""
        self.RInput = QtWidgets.QPushButton(self.widget)
        self.RInput.setObjectName("RInput")
        self.verticalLayout.addWidget(self.RInput)
        self.RInput.clicked.connect(self.inputPath)

        #ConfPreproc button
        self.ROutput = QtWidgets.QPushButton(self.widget)
        self.ROutput.setObjectName("ROutput")
        self.verticalLayout.addWidget(self.ROutput)
        self.ROutput.clicked.connect(self.outputPath)


        #ConfiguracionClasificador button
        self.ConfClasi = QtWidgets.QPushButton(self.widget)
        self.ConfClasi.setObjectName("ConfClasi")
        self.verticalLayout.addWidget(self.ConfClasi)
        self.ConfClasi.setEnabled(bool(self.ruta))
        self.ConfClasi.clicked.connect(self.openConfClasi)

        #ConfBat button
        self.ConfBat = QtWidgets.QPushButton(self.widget)
        self.ConfBat.setObjectName("ConfBat")
        self.verticalLayout.addWidget(self.ConfBat)

        #EjecButton
        self.IniEjec = QtWidgets.QPushButton(self.widget)
        self.IniEjec.setObjectName("IniEjec")
        self.verticalLayout.addWidget(self.IniEjec)

        #Grafic button
        self.Grafic = QtWidgets.QPushButton(self.widget)
        self.Grafic.setObjectName("Grafic")
        self.verticalLayout.addWidget(self.Grafic)
        self.Grafic.setEnabled(bool(self.ruta))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 576, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    '''
    Function created to indicate the input path of the files
    '''
    def inputPath(self):
        data, ok = QInputDialog.getText(self, "Ruta Input", "Indique la ruta donde se encuentra el input", QLineEdit.EchoMode.Normal, self.ruta)
        if ok and data is not None and data != "":
            self.ruta=data
            self.ConfClasi.setEnabled(bool(self.ruta))

    '''
    Function created to indicate where to save the output  files
    '''
    def outputPath(self):
        data, ok = QInputDialog.getText(self, "Ruta Input", "Indique donde almacenar el fichero de salida", QLineEdit.EchoMode.Normal, self.ruta)
        if ok and data is not None and data != "":
            self.ruta=data
            self.Grafic.setEnabled(bool(self.ruta))

    '''
    Function that opens the ConfiguracionClasificador window when its button is selected
    '''
    def openConfClasi(self):
        self.confClasi = QtWidgets.QDialog()
        self.ui = Ui_ConfiguracionClasificador()
        self.ui.setupUi(self.confClasi)
        self.confClasi.show()
        self.confClasi.rejected.connect(self.guardarDiccionario)
        self.confClasi.show()

    def guardarDiccionario(self):
        self.diccionario = self.ui.dicCapas
        print(self.diccionario)






    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.RInput.setText(_translate("MainWindow", "Ruta Input"))
        self.ROutput.setText(_translate("MainWindow", "Ruta Output"))
        self.ConfClasi.setText(_translate("MainWindow", "Configurar clasificador"))
        self.ConfBat.setText(_translate("MainWindow", "Configurar bateria"))
        self.IniEjec.setText(_translate("MainWindow", "Inicio ejecución"))
        self.Grafic.setText(_translate("MainWindow", "Graficas"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
