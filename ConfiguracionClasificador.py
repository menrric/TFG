from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QInputDialog, QLineEdit, QMessageBox, QTableWidgetItem



class Ui_ConfiguracionClasificador(QDialog):
    def setupUi(self, ConfiguracionClasificador):

        self.dicCapas = {}

        ConfiguracionClasificador.setObjectName("ConfiguracionClasificador")
        ConfiguracionClasificador.resize(577, 391)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ConfiguracionClasificador)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Cargar el ícono y escalarlo al tamaño deseado
        icon = QtGui.QIcon("CuvaCompl.png")
        pixmap = icon.pixmap(QtCore.QSize(90, 90))  # Ajusta el tamaño del ícono aquí
        scaled_icon = QtGui.QIcon(pixmap)
        ConfiguracionClasificador.setWindowIcon(scaled_icon)

        self.tableWidget = QtWidgets.QTableWidget(ConfiguracionClasificador)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")


        #UP ROW BUTTON
        self.pushButtonUp = QtWidgets.QPushButton(ConfiguracionClasificador)
        self.pushButtonUp.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("FlechaArriba.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonUp.setIcon(icon)
        self.pushButtonUp.setObjectName("pushButtonUp")
        self.verticalLayout.addWidget(self.pushButtonUp)
        self.pushButtonUp.clicked.connect(self.swapRowUp)

        #DOWN ROW BUTTON
        self.pushButtonDown = QtWidgets.QPushButton(ConfiguracionClasificador)
        self.pushButtonDown.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("FlechaAbajo.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonDown.setIcon(icon1)
        self.pushButtonDown.setObjectName("pushButtonDown")
        self.verticalLayout.addWidget(self.pushButtonDown)
        self.pushButtonDown.clicked.connect(self.swapRowDown)

        #SPACE LINES
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        # ADD BUTTON
        self.pushButtonAdd = QtWidgets.QPushButton(ConfiguracionClasificador)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.verticalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonAdd.clicked.connect(self.addRow)

        # EDIT BUTTON
        self.pushButtonEdit = QtWidgets.QPushButton(ConfiguracionClasificador)
        self.pushButtonEdit.setObjectName("pushButtonEdit")
        self.verticalLayout.addWidget(self.pushButtonEdit)
        self.pushButtonEdit.setEnabled(False)
        self.pushButtonEdit.clicked.connect(self.editItem)

        # DELETE BUTTON
        self.pushButtonDelete = QtWidgets.QPushButton(ConfiguracionClasificador)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.verticalLayout.addWidget(self.pushButtonDelete)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonDelete.clicked.connect(self.removeRow)

        self.retranslateUi(ConfiguracionClasificador)
        QtCore.QMetaObject.connectSlotsByName(ConfiguracionClasificador)

    def validateNep(self, nep):
        try:
            nep_list = [int(x.strip()) for x in nep.split(",")]
            return all(isinstance(x, int) and x > 0 for x in nep_list)
        except ValueError:
            return False

    def validateField(self, field, value):
        if field == "Nombre":
            return value.strip() != ""
        elif field == "Tipo":
            return value == "Dense"
        elif field == "Nep":
            return self.validateNep(value)
        elif field == "Activacion":
            return value == "sigmoid"
        else:
            return True

    '''
    ADDROW 
    addRow is used to add a new row to our table. To do this, a pop-up will be displayed that will ask us what we want
    to put in each field.
    '''

    def addRow(self):
        cell = self.tableWidget.rowCount() - 1

        fields = [
            ("Nombre", "El valor no es válido para el campo 'Nombre'"),
            ("Tipo", "El valor no es válido para el campo 'Tipo'"),
            ("Nep", "El valor no es válido para el campo 'Nep'"),
            ("Activacion", "El valor no es válido para el campo 'Activación'")
        ]

        lista = {}
        for i, (title, error_message) in enumerate(fields):
            while True:
                campo, ok = QInputDialog.getText(self, title, title)
                if not ok:
                    return  # El usuario ha cancelado, se sale del método
                if campo is not None and self.validateField(title, campo):
                    self.tableWidget.setItem(cell, i, QTableWidgetItem(campo))
                    lista[title] = campo
                    break  # Campo válido, se sale del bucle
                else:
                    QMessageBox.warning(self, "Warning", error_message)

        self.tableWidget.insertRow(cell + 1)
        self.dicCapas[self.tableWidget.rowCount() - 1] = lista
        self.pushButtonEdit.setEnabled(True)
        self.pushButtonDelete.setEnabled(True)


    '''
    EDITITEM
    editItem is used to edit a particular field in a row. To do this, click on the cell to edit and press the edit
    button
    '''

    def editItem(self):
        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()
        item = self.tableWidget.item(row, col)
        header = self.tableWidget.horizontalHeaderItem(col).text()

        if item is not None and item.text():
            title = "Edit Item " + header
            data, ok = QInputDialog.getText(self, title, title, QLineEdit.EchoMode.Normal, item.text())
            if ok and data is not None and data != "":
                if self.validateField(header, data):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(data))
                    self.dicCapas[row + 1][header] = data
                else:
                    QMessageBox.warning(self, "Warning", f"El valor no es válido para el campo '{header}'")
            else:
                QMessageBox.warning(self, "Warning", "El valor no es válido")
        else:
            QMessageBox.warning(self, "Warning", "No hay información para editar")

    '''
    REMOVEROW 
    removeRow is used to delete a specific row. To do this we must click it, hit the delete button and we will get
    a confirmation message
    button
    '''
    def removeRow(self):
        row = self.tableWidget.currentRow()

        reply = QMessageBox.question(self, "Borrar Fila", "¿Quieres borrar la fila {}?".format(row +1) ,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.tableWidget.removeRow(row)
        rowCount = self.tableWidget.rowCount()
        dataExists = False
        for row in range(rowCount):
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                if item and item.text():
                    dataExists = True
                    break
            if dataExists:
                break
        if not dataExists:
            self.pushButtonEdit.setEnabled(False)
            self.pushButtonDelete.setEnabled(False)

    def swapRows(self, row1, row2):
        rowCount = self.tableWidget.rowCount()

        if not (0 <= row1 < rowCount and 0 <= row2 < rowCount):
            QMessageBox.warning(self, "Aviso", "No es posible mover la fila")
            return

        key1 = row1 + 1
        key2 = row2 + 1

        if key1 not in self.dicCapas or key2 not in self.dicCapas:
            QMessageBox.warning(self, "Aviso", "No es posible mover la fila")
            return

        for col in range(self.tableWidget.columnCount()):
            item1 = self.tableWidget.takeItem(row1, col)
            item2 = self.tableWidget.takeItem(row2, col)
            self.tableWidget.setItem(row1, col, item2)
            self.tableWidget.setItem(row2, col, item1)

        self.dicCapas[key1]['row'], self.dicCapas[key2]['row'] = row2, row1
        self.dicCapas[key1], self.dicCapas[key2] = self.dicCapas[key2], self.dicCapas[key1]

    '''
    SWAPROWUP 
    Swap the selected row with the row above
    '''
    def swapRowUp(self):
        row = self.tableWidget.currentRow()
        self.swapRows(row, row - 1)
        self.tableWidget.setCurrentCell(row - 1, 0)

    '''
    SWAPROWUP 
    Swap the selected row with the row below
    '''
    def swapRowDown(self):
        row = self.tableWidget.currentRow()
        self.swapRows(row, row + 1)
        self.tableWidget.setCurrentCell(row + 1, 0)


    def retranslateUi(self, ConfiguracionClasificador):
        _translate = QtCore.QCoreApplication.translate
        ConfiguracionClasificador.setWindowTitle(_translate("ConfiguracionClasificador", "ConfiguracionClasificador"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("ConfiguracionClasificador", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("ConfiguracionClasificador", "Nombre"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("ConfiguracionClasificador", "Tipo"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("ConfiguracionClasificador", "Nep"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("ConfiguracionClasificador", "Activacion"))
        self.pushButtonAdd.setText(_translate("ConfiguracionClasificador", "Añadir"))
        self.pushButtonEdit.setText(_translate("ConfiguracionClasificador", "Editar"))
        self.pushButtonDelete.setText(_translate("ConfiguracionClasificador", "Borrar"))



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ConfiguracionClasificador = QtWidgets.QDialog()
    ui = Ui_ConfiguracionClasificador()
    ui.setupUi(ConfiguracionClasificador)
    ConfiguracionClasificador.show()
    sys.exit(app.exec())
