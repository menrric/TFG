import os
import xml.etree.ElementTree as ET
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xmltodict


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton

'''
Class prepared by the student Manuel Méndez Calvo, computer engineering student at UVa. The objective of this class is
to be part of the TFG on the creation of classifiers for neural networks with data visualization.

This class is responsible for displaying data. To do this, it extracts the data from the xml generated by the execution
and stores it in a dataframe that we will use later to make 5 different types of graphs. To make these graphs, 
the user must choose from a checklist the attributes that he wants to compare based on the average error. 
All the graphs follow the same structure; Each of the possible options of the chosen attribute will be compared based
on the mean error. The first one will be a bar chart, the second is a scatter chart, the third is a pie chart,
the fourth is a line chart, and finally a box and whisker chart.
'''
class Ui_GenerarGrafica(QDialog):
    def setupUiGenerarGrafica(self, GenerarGrafica):
        self.columnas = {}
        self.ResultadosTodoDF = pd.DataFrame()
        self.SeleccionResDT = pd.DataFrame()
        self.camposSeleccionados = ["EERmedio"]  # LList to store the selected fields (EERmedio selected by default)
        self.rutaOutput = ''  # Attribute to store the output path

        GenerarGrafica.setObjectName("GenerarGrafica")
        GenerarGrafica.resize(400, 300)
        self.verticalLayout = QVBoxLayout(GenerarGrafica)
        self.verticalLayout.setObjectName("verticalLayout")

        icon = QtGui.QIcon("CuvaCompl.png")
        pixmap = icon.pixmap(QtCore.QSize(90, 90))
        scaled_icon = QtGui.QIcon(pixmap)
        GenerarGrafica.setWindowIcon(scaled_icon)

        self.generateButton = QPushButton(GenerarGrafica)
        self.generateButton.setObjectName("generateButton")
        self.verticalLayout.addWidget(self.generateButton)
        self.generateButton.clicked.connect(self.extraerDatos)
        self.generateButton.clicked.connect(self.crearChecklist)

        # Button to generate bar graph
        self.barButton = QPushButton(GenerarGrafica)
        self.barButton.setObjectName("barButton")
        self.verticalLayout.addWidget(self.barButton)
        self.barButton.setEnabled(False)  # Disable button until fields are selected
        self.barButton.clicked.connect(self.generarGraficaBarras)

        # Button to generate scatter plot
        self.scatterButton = QPushButton(GenerarGrafica)
        self.scatterButton.setObjectName("scatterButton")
        self.verticalLayout.addWidget(self.scatterButton)
        self.scatterButton.setEnabled(False)  # Disable button until fields are selected
        self.scatterButton.clicked.connect(self.generarGraficaDispersion)

        # Button to generate line chart
        self.lineButton = QPushButton(GenerarGrafica)
        self.lineButton.setObjectName("lineButton")
        self.verticalLayout.addWidget(self.lineButton)
        self.lineButton.setEnabled(False)  # Disable button until fields are selected
        self.lineButton.clicked.connect(self.generarGraficaLineas)

        # Button to generate pie chart
        self.pieButton = QPushButton(GenerarGrafica)
        self.pieButton.setObjectName("pieButton")
        self.verticalLayout.addWidget(self.pieButton)
        self.pieButton.setEnabled(False)  # DDisable button until fields are selected
        self.pieButton.clicked.connect(self.generarGraficaPastel)

        # Button to generate box and whisker plot
        self.boxButton = QPushButton(GenerarGrafica)
        self.boxButton.setObjectName("boxButton")
        self.verticalLayout.addWidget(self.boxButton)
        self.boxButton.setEnabled(False)  # Disable button until fields are selected
        self.boxButton.clicked.connect(self.generarGraficaBoxplot)

        self.retranslateUi(GenerarGrafica)
        QtCore.QMetaObject.connectSlotsByName(GenerarGrafica)

    '''
    Function destined to store the path where the execution data is
    '''
    def setRutaOutput(self, rutaOutput):
        self.rutaOutput = rutaOutput

    '''
    Function designed to create the checklist that will be shown to the user so that they can choose the attributes on which they want to make the graphs
    '''
    def crearChecklist(self):
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication([])

        # Create a dialog window
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Checklist Dinámico")

        # Create a vertical layout
        layout = QtWidgets.QVBoxLayout(dialog)

        # Create checkboxes and add them to the layout
        self.checkboxes = []
        self.columnas = [col for col in self.ResultadosTodoDF.columns if
                         col in ["Usuario", "Marca", "Sensor", "EERmedio"]]

        for col in self.columnas:
            nombre_columna = self.soloLetras(col)

            # Check if a checkbox with that name already exists
            if any(nombre_columna == self.soloLetras(checkbox.text()) for checkbox in self.checkboxes):
                continue

            checkbox = QtWidgets.QCheckBox(nombre_columna)
            checkbox.setChecked(
                col in self.camposSeleccionados)  # Set the state of the checkbox according to the list of selected fields
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)

            if col == "EERmedio":
                checkbox.setCheckState(QtCore.Qt.CheckState.Checked)
                checkbox.setEnabled(False)

            checkbox.stateChanged.connect(
                self.actualizarCamposSeleccionados)



        # Disable buttons before showing dialog window
        if len(self.camposSeleccionados) <= 1:
            self.deshabilitarBotones()

        dialog.exec()

    '''
    This function is a regular expression intended to remove all non-string letters
    '''
    def soloLetras(self, texto):
        letras = re.sub('[^a-zA-Z]', '', texto)
        return letras

    '''
    Function dedicated to updating the codes selected by the user and to enabling or disabling the checklist buttons
    '''
    def actualizarCamposSeleccionados(self, state):
        checkbox = self.sender()  # Get Checkbox
        campo = checkbox.text()  # Get Checkbox Text

        if state == 2:  # Cambiar QtCore.Qt.CheckState.Checked a 2
            if campo not in self.camposSeleccionados:
                self.camposSeleccionados.append(campo)  # add item to list
        else:
            if campo in self.camposSeleccionados:
                self.camposSeleccionados.remove(campo)  # remove item if exist

        self.SeleccionResDT = self.ResultadosTodoDF[self.camposSeleccionados]

        # Check if fields were selected before enabling buttons
        if len(self.camposSeleccionados) > 1:
            self.habilitarBotones()
        else:
            self.deshabilitarBotones()

    '''
    Function destined to extract all the data from the xml to be able to make the graphs with them
    '''
    def extraerDatos(self):
        pathDir = self.rutaOutput + "/Experimentos/"
        for subDir in next(os.walk(pathDir))[1]:
            pathDir = self.rutaOutput + "/Experimentos/" + subDir
            pathExperimento = pathDir + "/Experimento.xml"


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
            # Extraemos todos los parámetros que definen el modelo

            idCapa = 0
            for capa in ModeloDict:
                for key in capa:
                    ValorCol = capa[key]
                    UsuariosDF[key + str(idCapa)] = ValorCol
                idCapa = idCapa + 1

            self.ResultadosTodoDF = pd.concat([self.ResultadosTodoDF, UsuariosDF], ignore_index=True)


    '''
    Function intended to enable buttons when conditions are met
    '''
    def habilitarBotones(self):
        self.barButton.setEnabled(True)
        self.scatterButton.setEnabled(True)
        self.lineButton.setEnabled(True)
        self.pieButton.setEnabled(True)
        self.boxButton.setEnabled(True)


    '''
    Function intended to disable buttons when conditions are met 
    '''
    def deshabilitarBotones(self):
        self.barButton.setEnabled(False)
        self.scatterButton.setEnabled(False)
        self.lineButton.setEnabled(False)
        self.pieButton.setEnabled(False)
        self.boxButton.setEnabled(False)


    '''
    Function destined to extract all the values ​​of the attributes once all the data of the xml is extracted
    '''
    def obtenerValoresAtributo(self, atributo):
        valores = []

        ruta_output = self.rutaOutput + "/Experimentos/"
        for experimento_folder in next(os.walk(ruta_output))[1]:
            experimento_path = os.path.join(ruta_output, experimento_folder)
            if os.path.isdir(experimento_path):
                xml_path = os.path.join(experimento_path, "Experimento.xml")
                if os.path.exists(xml_path):
                    tree = ET.parse(xml_path)
                    root = tree.getroot()

                    for elemento in root.iter(atributo):
                        # Get the text string with the EER values
                        valores_eer_str = elemento.text

                        # Convert the text string to a list of numbers
                        valores_eer = [float(valor) for valor in valores_eer_str.split()]

                        # Add the values to the general list
                        valores.extend(valores_eer)


        return valores

    '''
    Function intended to make the bar graph. To do this, it makes a graph based on each of the selected attributes and
    finally makes a graph where the comparison of all the attributes is put together.
    '''
    def generarGraficaBarras(self):
        NumGraficas = len(self.camposSeleccionados) - 1  # Hay tantas columnas como variables más 1 de EERmedio
        variables = [columna for columna in self.SeleccionResDT.columns if columna != "EERmedio"]

        fig_all, axes_all = plt.subplots(1, NumGraficas, figsize=(6 * NumGraficas, 6), sharey=True)
        fig_all.suptitle('Gráfico de Barras - Todas las Variables: ' + ' '.join(variables), fontsize=16,
                         fontweight='bold', y=0.95)

        if NumGraficas == 1:
            axes_all = [axes_all]  # Convertir a lista para evitar errores de índice

        for i, columna in enumerate(variables):
            fig = plt.figure(figsize=(6, 6))
            ax = fig.add_subplot(111)
            fig.suptitle('Gráfico de Barras - ' + columna, fontsize=13, fontweight='bold')

            DatosGraf = self.SeleccionResDT.loc[:, [columna, 'EERmedio']]
            xticks = []
            y = []

            for xvalor in DatosGraf[columna].unique():
                DatosSel = DatosGraf[DatosGraf[columna] == xvalor]
                xticks.append(xvalor)
                y.append(DatosSel['EERmedio'].mean())

            # Cambiar colores de las barras
            colors = plt.cm.Set3(np.linspace(0, 1, len(xticks)))
            ax.bar(xticks, y, color=colors, edgecolor='black', alpha=0.8)

            ax.set_xlabel(columna, fontsize=10)
            ax.set_xticks(range(len(xticks)))  # Establecer las marcas del eje x
            ax.set_xticklabels(xticks, rotation='vertical')  # Etiquetas del eje x con rotación vertical
            ax.tick_params(axis='both', which='major', labelsize=8)
            ax.spines['top'].set_visible(True)
            ax.spines['right'].set_visible(False)

            # Agregar etiquetas de valor a las barras
            for x, y_val in zip(xticks, y):
                ax.text(x, y_val, f'{y_val:.2f}', ha='center', va='bottom', fontsize=8)

            # Agregar error medio en la gráfica general
            axes_all[i].bar(xticks, y, color=colors, edgecolor='black', alpha=0.8)
            axes_all[i].set_title(columna, fontsize=12)
            axes_all[i].set_xlabel(columna, fontsize=10)
            axes_all[i].tick_params(axis='both', which='major', labelsize=8)
            axes_all[i].spines['top'].set_visible(True)
            axes_all[i].spines['right'].set_visible(False)

            # Agregar etiquetas de error en la gráfica general
            for bar in axes_all[i].patches:
                axes_all[i].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height():.2f}',
                                 ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        plt.show()

    '''
    Function intended to make the scatter  graph. To do this, it makes a graph based on each of the selected attributes and
    finally makes a graph where the comparison of all the attributes is put together.
    '''
    def generarGraficaDispersion(self):
        NumGraficas = len(self.camposSeleccionados) - 1  # Hay tantas columnas como variables más 1 de EERmedio
        variables = [columna for columna in self.SeleccionResDT.columns if columna != "EERmedio"]

        fig_all, axes_all = plt.subplots(NumGraficas, 1, figsize=(9, 6 * NumGraficas), sharex=True)
        fig_all.suptitle('Gráfico de Dispersión - Todas las Variables: ' + ' '.join(variables), fontsize=16,
                         fontweight='bold')

        if NumGraficas == 1:
            axes_all = [axes_all]  # Convertir a lista para evitar errores de índice

        for i, columna in enumerate(variables):
            fig, ax = plt.subplots(figsize=(9, 6))
            fig.suptitle('Gráfico de Dispersión - ' + columna, fontsize=13, fontweight='bold')

            DatosGraf = self.SeleccionResDT.loc[:, [columna, 'EERmedio']]
            x = DatosGraf[columna]
            y = DatosGraf['EERmedio']

            ax.scatter(x, y)

            ax.set_xlabel(columna, fontsize=10)
            ax.set_ylabel('EER medio', fontsize=10)
            ax.tick_params(axis='both', which='major', labelsize=8)
            ax.spines['top'].set_visible(True)
            ax.spines['right'].set_visible(False)

            plt.xticks(rotation='vertical')

            # Agregar etiquetas de valor a los puntos
            for x_val, y_val in zip(x, y):
                ax.text(x_val, y_val, f'{y_val:.2f}', ha='center', va='bottom', fontsize=8)

            # Agregar gráfica de dispersión en la gráfica general
            axes_all[i - 1].scatter(x, y)
            axes_all[i - 1].set_title(columna, fontsize=12)
            axes_all[i - 1].set_ylabel('EER medio', fontsize=10)
            axes_all[i - 1].tick_params(axis='both', which='major', labelsize=8)
            axes_all[i - 1].spines['top'].set_visible(True)
            axes_all[i - 1].spines['right'].set_visible(False)

        plt.tight_layout()
        plt.show()


    '''
    Function intended to make the lines  graph. To do this, it makes a graph based on each of the selected attributes and
    finally makes a graph where the comparison of all the attributes is put together.
    '''
    def generarGraficaLineas(self):
        NumGraficas = len(self.camposSeleccionados) - 1  # Hay tantas columnas como variables más 1 de EERmedio
        variables = [columna for columna in self.SeleccionResDT.columns if columna != "EERmedio"]

        # Definir los colores personalizados
        colors = ['#8B8878', 'green', 'darkgoldenrod']

        fig_all, axes_all = plt.subplots(1, NumGraficas, figsize=(6 * NumGraficas, 6), sharey=True)
        fig_all.suptitle('Gráfico de Líneas - Todas las Variables: ' + ' '.join(variables), fontsize=16,
                         fontweight='bold', y=0.95)

        if NumGraficas == 1:
            axes_all = [axes_all]  # Convertir a lista para evitar errores de índice

        for i, columna in enumerate(variables):
            fig = plt.figure(figsize=(6, 6))
            ax = fig.add_subplot(111)
            fig.suptitle('Gráfico de Líneas - ' + columna, fontsize=13, fontweight='bold')

            DatosGraf = self.SeleccionResDT.loc[:, [columna, 'EERmedio']]
            x = DatosGraf[columna].unique()
            y = []

            for xvalor in x:
                DatosSel = DatosGraf[DatosGraf[columna] == xvalor]
                y.append(DatosSel['EERmedio'].mean())

            y_std = []
            for xvalor in x:
                DatosSel = DatosGraf[DatosGraf[columna] == xvalor]
                y_std.append(DatosSel['EERmedio'].std())

            ax.errorbar(range(len(x)), y, yerr=y_std, fmt='o-', capsize=4, color=colors[i])
            ax.set_xticks(range(len(x)))  # Establecer las marcas del eje x
            ax.set_xticklabels(x, rotation='vertical')  # Etiquetas del eje x con rotación vertical
            ax.set_xlabel(columna, fontsize=10)
            ax.set_ylabel('EER medio', fontsize=10)
            ax.tick_params(axis='both', which='major', labelsize=8)
            ax.spines['top'].set_visible(True)
            ax.spines['right'].set_visible(False)

            # Agregar etiquetas de valor a los puntos
            for x_val, y_val in zip(range(len(x)), y):
                ax.text(x_val, y_val, f'{y_val:.2f}', ha='center', va='bottom', fontsize=8)

            # Agregar error medio en la gráfica general
            axes_all[i].errorbar(range(len(x)), y, yerr=y_std, fmt='o-', capsize=4, color=colors[i])
            axes_all[i].set_title(columna, fontsize=12)
            axes_all[i].set_xticks(range(len(x)))  # Establecer las marcas del eje x
            axes_all[i].set_xticklabels(x, rotation='vertical')  # Etiquetas del eje x con rotación vertical
            axes_all[i].set_xlabel(columna, fontsize=10)
            axes_all[i].tick_params(axis='both', which='major', labelsize=8)
            axes_all[i].spines['top'].set_visible(True)
            axes_all[i].spines['right'].set_visible(False)

        plt.tight_layout()
        plt.show()

    '''
    Function intended to make the pie  graph. To do this, it makes a graph based on each of the selected attributes and
    finally makes a graph where the comparison of all the attributes is put together.
    '''
    def generarGraficaPastel(self):
        NumGraficas = len(self.camposSeleccionados) - 1  # Hay tantas columnas como variables más 1 de EERmedio
        variables = [columna for columna in self.SeleccionResDT.columns if columna != "EERmedio"]

        fig_all, axes_all = plt.subplots(NumGraficas, 1, figsize=(9, 6 * NumGraficas), sharex=True)
        fig_all.suptitle('Gráfico de Pastel - Todas las Variables: ' + ' '.join(variables), fontsize=16,
                         fontweight='bold')

        if NumGraficas == 1:
            axes_all = [axes_all]  # Convertir a lista para evitar errores de índice

        for i, columna in enumerate(variables):
            fig, ax = plt.subplots(figsize=(9, 6))
            fig.suptitle('Gráfico de Pastel - ' + columna, fontsize=13, fontweight='bold')

            DatosGraf = self.SeleccionResDT.loc[:, [columna, 'EERmedio']]
            DatosGraf = DatosGraf.groupby(columna)['EERmedio'].mean()

            etiquetas = DatosGraf.index.tolist()
            valores = DatosGraf.values.tolist()

            colores = plt.cm.Set3(np.linspace(0, 1, len(etiquetas)))
            ax.pie(valores, labels=etiquetas, colors=colores, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')

            axes_all[i - 1].pie(valores, labels=etiquetas, colors=colores, autopct='%1.1f%%', startangle=90)
            axes_all[i - 1].set_title(columna, fontsize=12)

        plt.tight_layout()
        plt.show()

    '''
    Function intended to make the box-and-whisker plot  graph. To do this, it makes a graph based on each of
    the selected attributes. 
    It also calls another function that will do the overall graph. This is because the level of complexity of unifying
    the graphs in this type of graph is quite high.
    '''
    def generarGraficaBoxplot(self):
        variables = [columna for columna in self.SeleccionResDT.columns if columna != "EERmedio"]

        # Define los colores que deseas utilizar para los boxplots
        colores = ['#8B8878', 'green', 'darkgoldenrod']

        for i, columna in enumerate(variables):
            fig, ax = plt.subplots(figsize=(9, 6))
            fig.suptitle('Diagrama de Caja y Bigotes - ' + columna, fontsize=13, fontweight='bold')

            DatosGraf = self.SeleccionResDT.loc[:, [columna, 'EERmedio']]
            datos_por_grupo = []

            for xvalor in DatosGraf[columna].unique():
                DatosSel = DatosGraf[DatosGraf[columna] == xvalor]
                datos_por_grupo.append(DatosSel['EERmedio'])

            # Selecciona el color correspondiente al índice actual
            color_actual = colores[i % len(colores)]

            bp = ax.boxplot(datos_por_grupo, patch_artist=True, boxprops=dict(facecolor=color_actual))

            ax.set_ylabel('EER medio', fontsize=10)
            ax.set_xlabel(columna, fontsize=10)
            ax.tick_params(axis='both', which='major', labelsize=8)
            ax.spines['top'].set_visible(True)
            ax.spines['right'].set_visible(False)

            etiquetas_por_grupo = [str(xvalor) for xvalor in DatosGraf[columna].unique()]
            posiciones_xticks = range(1, len(etiquetas_por_grupo) + 1)
            ax.set_xticks(posiciones_xticks)
            ax.set_xticklabels(etiquetas_por_grupo, rotation='vertical')

            for j, datos in enumerate(datos_por_grupo):
                ax.text(posiciones_xticks[j], max(datos), f'{max(datos):.2f}', ha='center', va='bottom', fontsize=8)
                ax.text(posiciones_xticks[j], min(datos), f'{min(datos):.2f}', ha='center', va='top', fontsize=8)

        self.generarGraficaBoxplotGeneral(colores)  # Pasa la lista de colores como argumento

        plt.tight_layout()
        plt.show()

    '''
    Function in charge of making the general box and whisker plot
    '''
    def generarGraficaBoxplotGeneral(self, colores):
        variables = [columna for columna in self.SeleccionResDT.columns if columna != "EERmedio"]

        fig, ax = plt.subplots(figsize=(9, 6))
        fig.suptitle('Diagrama de Caja y Bigotes - Todas las Variables: ' + ' '.join(variables), fontsize=16,
                     fontweight='bold')

        datos_por_grupo = []
        etiquetas_por_grupo = []
        colores_por_grupo = []

        for i, columna in enumerate(variables):
            DatosGraf = self.SeleccionResDT.loc[:, [columna, 'EERmedio']]

            for xvalor in DatosGraf[columna].unique():
                DatosSel = DatosGraf[DatosGraf[columna] == xvalor]
                datos_por_grupo.append(DatosSel['EERmedio'])
                etiquetas_por_grupo.append(str(xvalor))
                colores_por_grupo.append(colores[i])  # Asignar el color correspondiente al índice actual

        bp = ax.boxplot(datos_por_grupo, patch_artist=True)

        ax.set_ylabel('EER medio', fontsize=10)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(False)

        posiciones_xticks = range(1, len(etiquetas_por_grupo) + 1)
        ax.set_xticks(posiciones_xticks)
        ax.set_xticklabels(etiquetas_por_grupo, rotation='vertical')

        for j, datos in enumerate(datos_por_grupo):
            ax.text(posiciones_xticks[j], max(datos), f'{max(datos):.2f}', ha='center', va='bottom', fontsize=8)
            ax.text(posiciones_xticks[j], min(datos), f'{min(datos):.2f}', ha='center', va='top', fontsize=8)

        # Colorear los boxplots de la gráfica general con los colores especificados
        for box, color in zip(bp['boxes'], colores_por_grupo):
            box.set(facecolor=color)

        plt.tight_layout()
        plt.show()

    def retranslateUi(self, GenerarGrafica):
        _translate = QtCore.QCoreApplication.translate
        GenerarGrafica.setWindowTitle(_translate("GenerarGrafica", "Generar Gráfica"))
        self.generateButton.setText(_translate("GenerarGrafica", "Seleccionar Campos"))
        self.barButton.setText(_translate("GenerarGrafica", "Gráfico de Barras"))
        self.scatterButton.setText(_translate("GenerarGrafica", "Gráfico de Dispersión"))
        self.lineButton.setText(_translate("GenerarGrafica", "Gráfico de Líneas"))
        self.pieButton.setText(_translate("GenerarGrafica", "Gráfico de Pastel"))
        self.boxButton.setText(_translate("GenerarGrafica", "Gráfico de Caja y Bigotes"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    GenerarGrafica = QtWidgets.QDialog()
    ui = Ui_GenerarGrafica()
    ui.setupUiGenerarGrafica(GenerarGrafica)

    GenerarGrafica.show()
    sys.exit(app.exec())
