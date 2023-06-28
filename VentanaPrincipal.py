from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QInputDialog, QLineEdit, QMainWindow, QMessageBox
from ConfiguracionClasificador import Ui_ConfiguracionClasificador
from ParamCompile import Ui_ParamCompile
from GenerarGrafica import Ui_GenerarGrafica


import errno

from keras import Sequential
from keras.layers import Dense

import numpy as np
import pandas as pd
import os
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
import xmltodict
from queue import Queue
import xml.etree.ElementTree as ET

from FuncionesEntrenamiento import ExpandDict, EntrenaYPrueba

'''
Class prepared by the student Manuel Méndez Calvo, computer engineering student at UVa. The objective of this class is
to be part of the TFG on the creation of classifiers for neural networks with data visualization.

The main objective of this window is to make a MainWindow that can serve as a common thread for the rest of the windows,
 as well as show us information about the process that the network execution follows.
'''
class Ui_MainWindow(QMainWindow):


    def setupUi(self, MainWindow):

        self.diccionario = {}
        self.font = QtGui.QFont("Helvetica", 12)
        self.ruta=""
        self.rutaOutput=""
        self.loss = None
        self.optimize = None
        self.epocas = None
        self.ConfClasiHecho = False
        self.ParamCompileHecho = False

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1025, 637)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        icon = QtGui.QIcon("CuvaCompl.png")
        pixmap = icon.pixmap(QtCore.QSize(90, 90))
        scaled_icon = QtGui.QIcon(pixmap)
        MainWindow.setWindowIcon(scaled_icon)

        #Logger
        self.textLoger = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textLoger.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.textLoger.setAutoFillBackground(False)
        self.textLoger.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.textLoger.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.textLoger.setLineWidth(1)
        self.textLoger.setMidLineWidth(0)
        self.textLoger.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textLoger.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.textLoger.setObjectName("textLoger")
        self.gridLayout_2.addWidget(self.textLoger, 0, 1, 7, 1)
        self.textLoger.setReadOnly(True)
        self.textLoger.setFont(self.font)
        self.textLoger.setStyleSheet("QTextEdit { border: 1px solid black; background-color: white; padding: 25px; }")
        self.textLoger.textChanged.connect(self.updateTextLoger)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        #Input path and bouton
        self.RInput = QtWidgets.QPushButton(parent=self.centralwidget)
        self.RInput.setObjectName("RInput")
        self.verticalLayout.addWidget(self.RInput)
        self.RInput.clicked.connect(self.inputPath)

        #Output path button
        self.ROutput = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ROutput.setObjectName("ROutput")
        self.verticalLayout.addWidget(self.ROutput)
        self.ROutput.clicked.connect(self.outputPath)


        #ConfiguracionClasificador button
        self.ConfClasi = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ConfClasi.setObjectName("ConfClasi")
        self.verticalLayout.addWidget(self.ConfClasi)
        self.ConfClasi.setEnabled(bool(self.ruta))
        self.ConfClasi.clicked.connect(self.openConfClasi)

        #ConfParamCompile button
        self.ConfParamCompile = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ConfParamCompile.setObjectName("ConfParamCompile")
        self.verticalLayout.addWidget(self.ConfParamCompile)
        self.ConfParamCompile.setEnabled(bool(self.ruta))
        self.ConfParamCompile.clicked.connect(self.openParamsCompile)


        #EjecButton
        self.IniEjec = QtWidgets.QPushButton(parent=self.centralwidget)
        self.IniEjec.setObjectName("IniEjec")
        self.verticalLayout.addWidget(self.IniEjec)
        self.IniEjec.setEnabled(False)
        self.IniEjec.clicked.connect(self.iniciarEjec)

        #Grafic button
        self.Grafic = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Grafic.setObjectName("Grafic")
        self.verticalLayout.addWidget(self.Grafic)
        self.Grafic.setEnabled(bool(self.rutaOutput))
        self.Grafic.clicked.connect(self.openGenerarGraficas)

        self.gridLayout_2.addLayout(self.verticalLayout, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

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

        self.textLoger.append('<br><font size="10"><center><b>Bienvenido</b></center></font size="10">'
                              '<br> <center>Por favor, para empezar introduzca las rutas de input y output,'
                              'después configure el clasificador y los parametros del compilador y luego inicie la ejecución</center> ')



    '''
    Function created to indicate the input path of the files
    '''

    def inputPath(self):
        data, ok = QInputDialog.getText(self, "Ruta Input", "Indique la ruta donde se encuentra el input",
                                        QLineEdit.EchoMode.Normal, self.ruta)
        if ok and data is not None and data != "":
            self.ruta = data

            if self.rutaOutput == "":
                self.textLoger.clear()

            # Verificar si existe el archivo "Todo.csv" en la ruta de entrada
            ruta_todo_csv = os.path.join(self.ruta, "Todo.csv")
            if not os.path.isfile(ruta_todo_csv):
                self.textLoger.clear()
                self.textLoger.append(
                    '<u><b>No se encontró el archivo "Todo.csv" en la ruta de input. Por favor, introduzca una nueva.</b></u><br> ')
            else:
                self.textLoger.append('<u><b>La ruta de input proporcionada es:</b></u><br><br> '
                                      + self.ruta + '<br><br>')
                self.ConfClasi.setEnabled(bool(self.ruta))
                self.ConfParamCompile.setEnabled(bool(self.ruta))
        else:
            self.textLoger.clear()
            self.textLoger.append(
                '<u><b>La ruta de input proporcionada no es válida. Por favor, introduzca una nueva.</b></u><br> ')


    '''
    Function created to indicate where to save the output  files
    '''
    def outputPath(self):
        data, ok = QInputDialog.getText(self, "Ruta Output", "Indique donde almacenar el fichero de salida", QLineEdit.EchoMode.Normal, self.rutaOutput)
        if ok and data is not None and data != "":
            self.rutaOutput=data
            self.Grafic.setEnabled(bool(self.rutaOutput))
            if self.ruta == "":
                self.textLoger.clear()
            self.textLoger.append('<u><b>La ruta de output proporcionada es: </b></u><br><br> '
                                  + self.rutaOutput + '<br><br>')
        else:
            self.textLoger.clear()
            self.textLoger.append('<u><b>La ruta de output proporcionada no es válida. Por favor, introduzca una nueva</b></u><br> ')

    '''
    Function that opens the ConfiguracionClasificador window when its button is selected
    '''
    def openConfClasi(self):
        self.confClasi = QtWidgets.QDialog()
        self.ui = Ui_ConfiguracionClasificador()
        self.ui.setupUi(self.confClasi)
        self.confClasi.rejected.connect(self.saveDiccionario)
        self.confClasi.show()

    '''
    Function that brings us the dictionary from the ConfiguracionClassificador window to the current 
    window to be able to use
    '''
    def saveDiccionario(self):
        self.diccionario = self.ui.dicCapas
        if self.diccionario:
            tabla_html = '<table border="1">'
            tabla_html += '<tr><th>Nombre</th><th>Tipo</th><th>NEP</th><th>Activación</th></tr>'

            for clave, valor in self.diccionario.items():
                nombre = valor['Nombre']
                tipo = valor['Tipo']
                nep = valor['Nep']
                activacion = valor['Activacion']

                tabla_html += '<tr>'
                tabla_html += '<td>' + nombre + '</td>'
                tabla_html += '<td>' + tipo + '</td>'
                tabla_html += '<td>' + str(nep) + '</td>'
                tabla_html += '<td>' + activacion + '</td>'
                tabla_html += '</tr>'

            tabla_html += '</table>'
            self.textLoger.append(
                "<u><b>Los valores dados para el clasificador son:</u></b> <br> " + tabla_html + "<br><br>")
            self.ConfClasiHecho = True
            if self.ConfClasiHecho and self.ParamCompileHecho and self.rutaOutput != "":
                self.IniEjec.setEnabled(True)

    '''
    Function that opens the ParamCompile window when its button is selected
    '''
    def openParamsCompile(self):
        self.ConfParamCompile = QtWidgets.QDialog()
        self.uiParams = Ui_ParamCompile()
        self.uiParams.setupUiParams(self.ConfParamCompile)
        self.ConfParamCompile.show()
        self.ConfParamCompile.accepted.connect(self.saveParamsCompile)  # Cambio en el evento conectado
        self.ConfParamCompile.show()

    '''
    Function that brings us the params from the ParamCompile window to the current 
    window to be able to use
     '''
    def saveParamsCompile(self):
        self.loss = self.uiParams.loss
        self.optimize = self.uiParams.optimize
        self.epocas = self.uiParams.epocas
        tabla_html = '<table border="1">'
        tabla_html += '<tr><th>Función Loss</th><th>Optimizador</th><th>Épocas</th></tr>'

        tabla_html += '<tr>'
        tabla_html += '<td>' + self.loss + '</td>'
        tabla_html += '<td>' + self.optimize + '</td>'
        tabla_html += '<td>' + str(self.epocas) + '</td>'
        tabla_html += '</tr>'

        tabla_html += '</table>'
        self.textLoger.append("<u><b>Los valores dados para el compilador son:</u></b> <br> " +tabla_html + "<br><br>")
        self.ParamCompileHecho = True
        if self.ConfClasiHecho == True and self.ParamCompileHecho == True:
            self.IniEjec.setEnabled(True)

    '''
    Function that opens the GenerarGrafica window when its button is selected
    '''
    def openGenerarGraficas(self):
        rutaExperimentos = os.path.join(self.rutaOutput, "Experimentos")
        self.graficasDialog = QtWidgets.QDialog()
        self.uiGraficas = Ui_GenerarGrafica()
        self.uiGraficas.setupUiGenerarGrafica(self.graficasDialog)
        if not os.path.isdir(rutaExperimentos):
            error_msg = "No se encontró la carpeta 'Experimentos' en la ruta de salida."
            QMessageBox.critical(self, "Error", error_msg)
            self.close()  # Cerrar la ventana actual
        else:
            self.graficasDialog.show()
            self.uiGraficas.setRutaOutput(self.rutaOutput)

    '''
    Function intended to update the QTextLogger so that a flow of interaction with the user is displayed
    '''
    def updateTextLoger(self):
        self.textLoger.repaint()  # Actualizar el contenido del objeto QTextEdit
        QtWidgets.QApplication.processEvents()  # Actualizar la interfaz gráfica



    '''
    Function destined to start the execution for the classifier with the given parameters
    '''
    def iniciarEjec(self):
        list_of_dicts = []

        self.textLoger.clear()
        self.textLoger.append('<br><font size="10"><center><b>'
                              ' Inicio de la ejecución '
                              '</b></center></font size="10"><br><br>')

        for key, value in self.diccionario.items():
            temp_dict = value.copy()
            list_of_dicts.append(temp_dict)


        self.textLoger.append("<b><u>"
                              "Obteniendo los ficheros de:</b></u><br><br> " + self.ruta +
                              "<br>")


        TodoDF = pd.read_csv(self.ruta +"/Todo.csv")

        TodoDF.drop(TodoDF.columns[[0]], axis=1, inplace=True)
        listaUsr = np.sort(TodoDF.NombreUsr.unique())
        listaMar = TodoDF.Marca.unique()
        listaSen = TodoDF.Sensor.unique()



        MetaModelo = list_of_dicts


        # MLPLayers is a list of dictionaries. Each item in the list is a layer described by a dictionary.
        # We start from the idea that all layers must be expanded.

        ExpandCapas = []

        for Capa in MetaModelo:
            ExpandCapas.append(ExpandDict(Capa))

        self.textLoger.append("<b><u>"
                              "Número de capas: </b></u>" + str(len(ExpandCapas)) +
                              "<br>")


        self.textLoger.append('<br><font size="10"><center><b>'
                              ' Expansión de las capas '
                              '</b></center></font size="10"><br><br>')

        for idcapa in range(len(ExpandCapas)):
            tabla_html = '<table style="border-collapse: collapse; border: 1px solid black;">'
            tabla_html += '<tr>'
            tabla_html += '<th style="border: 1px solid black;">Nombre</th>'
            tabla_html += '<th style="border: 1px solid black;">Tipo</th>'
            tabla_html += '<th style="border: 1px solid black;">NEP</th>'
            tabla_html += '<th style="border: 1px solid black;">Activación</th>'
            tabla_html += '</tr>'
            self.textLoger.append(f"<b><u>Expansiones de la capa {idcapa}</u></b>")
            for capa in ExpandCapas[idcapa]:
                nombre = capa['Nombre']
                tipo = capa['Tipo']
                nep = capa['Nep']
                activacion = capa['Activacion']

                tabla_html += '<tr>'
                tabla_html += '<td style="border: 1px solid black;">' + nombre + '</td>'
                tabla_html += '<td style="border: 1px solid black;">' + tipo + '</td>'
                tabla_html += '<td style="border: 1px solid black;">' + str(nep) + '</td>'
                tabla_html += '<td style="border: 1px solid black;">' + activacion + '</td>'
                tabla_html += '</tr>'

            tabla_html += '</table>'
            self.textLoger.append(tabla_html)
            self.textLoger.append('<br>')

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


        self.textLoger.append('<br><font size="10"><center><b>'
                              'Agrupación de capas para formar los modelos '
                              '</b></center></font size="10"><br><br>')

        contadorMod=0
        for Modelo in ListaModelos:
            tabla_html = '<table style="border-collapse: collapse; border: 1px solid black;">'
            tabla_html += '<tr>'
            tabla_html += '<th style="border: 1px solid black;">Nombre</th>'
            tabla_html += '<th style="border: 1px solid black;">Tipo</th>'
            tabla_html += '<th style="border: 1px solid black;">NEP</th>'
            tabla_html += '<th style="border: 1px solid black;">Activación</th>'
            tabla_html += '</tr>'
            self.textLoger.append(f"<b><u>Modelo {contadorMod} de la Lista de Modelos</u></b>")
            for capa in Modelo:
                nombre = capa['Nombre']
                tipo = capa['Tipo']
                nep = capa['Nep']
                activacion = capa['Activacion']

                tabla_html += '<tr>'
                tabla_html += '<td style="border: 1px solid black;">' + nombre + '</td>'
                tabla_html += '<td style="border: 1px solid black;">' + tipo + '</td>'
                tabla_html += '<td style="border: 1px solid black;">' + str(nep) + '</td>'
                tabla_html += '<td style="border: 1px solid black;">' + activacion + '</td>'
                tabla_html += '</tr>'

            tabla_html += '</table>'
            self.textLoger.append(tabla_html)
            self.textLoger.append('<br>')
            contadorMod+=1


        self.textLoger.append('<br><font size="10"><center><b>'
                              ' Generación de los directorios para cada modelo '
                              '</b></center></font size="10"><br><br>')
        i = 0

        for Modelo in ListaModelos:

            modeloMLP = Sequential()

            # The input layer is layer 0. Then layer 1 is the first hidden layer
            PrimeraCapaOculta = True
            for capa in Modelo:
                if PrimeraCapaOculta:
                    modeloMLP.add(
                        Dense(int(capa['Nep']), activation=capa['Activacion'], input_dim=240, name=capa['Nombre']))
                else:
                    modeloMLP.add(Dense(int(capa['Nep']), activation=capa['Activacion'], name=capa['Nombre']))
                PrimeraCapaOculta = False

            modeloMLP.compile(loss=self.loss, optimizer=self.optimize, metrics=['accuracy'])

            pathDir = self.rutaOutput + "/Experimentos/" + str(i)
            self.textLoger.append(f' Generando el directorio para el Modelo {i} en la ruta <b>{pathDir}</b>')
            try:
                os.makedirs(pathDir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            modeloMLP.compile(loss=self.loss, optimizer=self.optimize, metrics=['accuracy'])
            modeloMLP.save(pathDir + "/modeloMLP.mod")

            self.textLoger.append('Generando y guardando el .mod del Modelo '+ str(i) +' en <b>'+ pathDir + '/modeloMLP.mod'+ '</b>')
            DatosDict = dict({"Modelo":Modelo, "Usuarios":[]})
            Datos_xml = dicttoxml(DatosDict, attr_type=False)
            dom = parseString(Datos_xml)

            fpxml = open(pathDir + "/Experimento.xml", "w")
            fpxml.write(dom.toprettyxml())
            self.textLoger.append(f'Generando el XML con la información del modelo {i} en la ruta  <b>{pathDir}</b><br>')
            fpxml.close()

            i = i + 1

        self.textLoger.append('<br><font size="10"><center><b>'
                              ' Entrenamiento y prueba de cada modelo. 5 Repeticiones por modelo '
                              '</b></center></font size="10"><br><br>')
        i = 0
        for Modelo in ListaModelos:
            pathDir = self.rutaOutput +"/Experimentos/" + str(i)
            pathModelo = pathDir + "/modeloMLP.mod"

            ResultadosQ = Queue()
            self.textLoger.append("Iniciando modelo " + str(i))

            self.textLoger.append('<font size="4"><u>'
                                  'Modelo ' + str(i) + ' Resultados:'
                                  '</u></font size="4">')

            ResultadosTodosDF = pd.DataFrame()
            # for usr in listaUsr:     ESTE DEBERÍA SER EL BUCLE, PERO POR RAZONES DE TIEMPO SÓLO USAMOS 2 USUARIOS
            for usr in listaUsr:
                Resultados_usr = EntrenaYPrueba(pathModelo, usuario=usr, listaMar=listaMar, listaSen=listaSen,
                                                TodoDF=TodoDF, tipo=tipo, ResultadosQ=ResultadosQ, loss=self.loss,
                                                optimizer=self.optimize, epocas=self.epocas, log=self.textLoger)
                ResultadosTodosDF = pd.concat([ResultadosTodosDF, Resultados_usr])
            NuevoUsuarioXML = ET.fromstring(ResultadosTodosDF.to_xml(root_name='Usuarios', row_name='Usuario'))

            tree = ET.parse(pathDir + '/Experimento.xml')
            raizXML = tree.getroot()
            UsuariosXML = raizXML.find('Usuarios')

            for child in NuevoUsuarioXML.findall('Usuario'):
                UsuariosXML.append(child)

            fpxml = open(pathDir + '/Experimento.xml', "wb")
            tree.write(fpxml)
            fpxml.close()
            i = 1+i

        self.textLoger.append('<br><font size="10"><center><b>'
                              'Procesando resultados'
                              '</b></center></font size="10"><br><br>')
        i = 0
        ResultadosTodoDF = pd.DataFrame()
        pathDir = self.rutaOutput + "/Experimentos/"
        for subDir in next(os.walk(pathDir))[1]:
            pathDir = self.rutaOutput + "/Experimentos/" + subDir
            pathExperimento = pathDir + "/Experimento.xml"

            self.textLoger.append('<br><font size="4"><center><b>'
                                  'Procesando resultados de ' + pathExperimento+ ''
                                  '</b></center></font size="4"><br><br>')

            fpxml = open(pathExperimento, "r")
            xmlDoc = fpxml.read()
            fpxml.close()

            ExperimentoDict = xmltodict.parse(xmlDoc)

            UsuariosDF = pd.DataFrame(ExperimentoDict['root']['Usuarios']['Usuario'])
            UsuariosDF['EERlist'] = UsuariosDF['EER'].apply(lambda x: x.split())

            EERmedio = []
            for strList in UsuariosDF['EERlist']:
                EERList = [float(i) for i in strList]
                EERmedio.append(np.average(EERList))
            UsuariosDF['EERmedio'] = EERmedio
            UsuariosDF.drop('EER', axis=1, inplace=True)
            UsuariosDF.drop('EERlist', axis=1, inplace=True)
            UsuariosDF

            ModeloDict = ExperimentoDict['root']['Modelo']['item']
            # We extract all the parameters that define the model

            idCapa = 0
            for capa in ModeloDict:
                for key in capa:
                    ValorCol = capa[key]
                    UsuariosDF[key + str(idCapa)] = ValorCol
                idCapa = idCapa + 1

            ResultadosTodoDF = pd.concat([ResultadosTodoDF, UsuariosDF], ignore_index=True)


        self.textLoger.append('<br><font size="10"><center><b>'
                              'Fin de la ejecución '
                              '</b></font size="10"><br></center><br>')
        return 0


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Clasificadores UVa"))
        self.RInput.setText(_translate("MainWindow", "Ruta Input"))
        self.ROutput.setText(_translate("MainWindow", "Ruta Output"))
        self.ConfClasi.setText(_translate("MainWindow", "Configurar clasificador"))
        self.ConfParamCompile.setText(_translate("MainWindow", "Parametros del Compile"))
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
