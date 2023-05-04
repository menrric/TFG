import subprocess

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QDialog
from ConfiguracionClasificador import Ui_ConfiguracionClasificador


import errno

from keras import Sequential
from keras.layers import Dense

from sklearn.metrics import roc_curve
import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
import os

from FuncionesEntrenamiento import ExpandDict, split_sequences, CalculaEER


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
        self.rutaOutput=""
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
        self.IniEjec.clicked.connect(self.iniciarEjec)

        #Grafic button
        self.Grafic = QtWidgets.QPushButton(self.widget)
        self.Grafic.setObjectName("Grafic")
        self.verticalLayout.addWidget(self.Grafic)
        self.Grafic.setEnabled(bool(self.rutaOutput))

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
        data, ok = QInputDialog.getText(self, "Ruta Output", "Indique donde almacenar el fichero de salida", QLineEdit.EchoMode.Normal, self.rutaOutput)
        if ok and data is not None and data != "":
            self.rutaOutput=data
            self.Grafic.setEnabled(bool(self.rutaOutput))

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

    def iniciarEjec(self):
        list_of_dicts = []

        for key, value in self.diccionario.items():
            temp_dict = value.copy()
            list_of_dicts.append(temp_dict)

        print(list_of_dicts)


        print("Obteniendo los ficheros de " + self.ruta)

        EntrenDF = pd.read_csv(self.ruta +"/Entren_v1.csv")
        PruebaDF = pd.read_csv(self.ruta +"/Prueba_v1.csv")

        X_train, y_train = split_sequences(np.array(EntrenDF), 80)

        X_test, y_test = split_sequences(np.array(PruebaDF), 80)

        # Este ejemplo se crea para un MLP, por lo que vamos a poner en
        # cada entrada una ventana de 80 muestras, cada muestra con 3 datos-dimensiones.
        # Es decir, las entradas son vectores de 240 componentes.
        X_train = X_train.reshape(-1, 240)
        X_test = X_test.reshape(-1, 240)

        EPOCAS = 5

        MetaModelo = list_of_dicts


        # CapasMLP es una lista de diccionarios. Cada item de la lista es una capa
        # descrita por un diccionario.
        # Partimos de la idea de que hay que expandir todas las capas.

        ExpandCapas = []

        for Capa in MetaModelo:
            ExpandCapas.append(ExpandDict(Capa))

        print("Número de capas: ", len(ExpandCapas))

        for idcapa in range(len(ExpandCapas)):
            for capa in ExpandCapas[idcapa]:
                print("Expansiones de la capa ", idcapa, capa)
            print("")

        NumCapas = len(ExpandCapas)
        Pares0 = ExpandCapas[0]

        for Actual in range(NumCapas - 1):
            Pares = []
            for previo in Pares0:
                for sig in ExpandCapas[Actual + 1]:
                    if Actual == 0:
                        Pares.append([previo.copy()] + [sig.copy()])
                    else:
                        Pares.append(previo.copy() + [sig.copy()])
            Pares0 = Pares

        ListaModelos = Pares

        for Modelo in ListaModelos:
            print("Modelo")
            for capa in Modelo:
                print(capa)

        i = 0
        for Modelo in ListaModelos:

            modeloMLP = Sequential()

            # La capa de entrada es la capa 0. Luego, la capa 1 es la primera capa oculta
            PrimeraCapaOculta = True
            for capa in Modelo:
                if PrimeraCapaOculta:
                    modeloMLP.add(
                        Dense(int(capa['nep']), activation=capa['activacion'], input_dim=240, name=capa['nombre']))
                else:
                    modeloMLP.add(Dense(int(capa['nep']), activation=capa['activacion'], name=capa['nombre']))
                PrimeraCapaOculta = False

            modeloMLP.compile(loss='binary_crossentropy', optimizer="adam", metrics=['accuracy'])
            # modeloMLP.summary()

            pathDir = self.rutaOutput + "/Experimentos/" + str(i)
            try:
                os.makedirs(pathDir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            modeloMLP.save(pathDir + "/modeloMLP.mod")
            i = i + 1

        # Ahora vamos, modelo por modelo, entrenando y probando

        i = 0
        for Modelo in ListaModelos:
            pathModelo = pathDir + "/modeloMLP.mod"
            modelo = tf.keras.models.load_model(pathModelo)

            modelo.summary()

            modelo.fit(X_train, y_train, batch_size=64, epochs=EPOCAS, verbose=0)

            Salida_red = modelo.predict(X_test)
            Salida_red = Salida_red.reshape(-1, 1)

            # Evaluamos

            EER = CalculaEER(Salida_red, y_test.reshape(-1, 1))

            print("Finaliza EER = ", EER)
            i = i + 1


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
