# Form implementation generated from reading ui file 'PrimeraInterfaz.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

#SEGUNDA PRUEBA CON EL MANEJO DE INTERFACES E IMPLEMENTACIÓN DE LA FUNCIONALIDAD AÑADIR UNA FILA, BORRARLA O EDITAR
#UN ELEMENTO DE LA FILA


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QInputDialog, QLineEdit, QMessageBox,QTableWidgetItem


class Ui_Form(QDialog):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(564, 376)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(Form)
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
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        #ADD BUTTON
        self.pushButtonAdd = QtWidgets.QPushButton(Form)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.verticalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonAdd.clicked.connect(self.add_item)

        #EDIT BUTTON
        self.pushButtonEdit = QtWidgets.QPushButton(Form)
        self.pushButtonEdit.setObjectName("pushButtonEdit")
        self.verticalLayout.addWidget(self.pushButtonEdit)
        self.pushButtonEdit.clicked.connect(self.edit_item)

        # DELETE BUTTON
        self.pushButtonDelete = QtWidgets.QPushButton(Form)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.verticalLayout.addWidget(self.pushButtonDelete)
        self.pushButtonDelete.clicked.connect(self.remove_row)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def add_item(self):

        contador = self.tableWidget.rowCount()-1
        title = "Campo1"
        campo1, ok = QInputDialog.getText(self, title, title)
        if ok and campo1 is not None:
            self.tableWidget.setItem(contador, 0, QTableWidgetItem(campo1))
        title = "Campo2"
        campo2, ok = QInputDialog.getText(self, title, title)
        if ok and campo2 is not None:
             self.tableWidget.setItem(contador, 1, QTableWidgetItem(campo2))
        title = "Campo3"
        campo3, ok = QInputDialog.getText(self, title, title)
        if ok and campo3 is not None:
             self.tableWidget.setItem(contador, 2, QTableWidgetItem(campo3))
        title = "Campo4"
        campo4, ok = QInputDialog.getText(self, title, title)
        if ok and campo4 is not None:
            self.tableWidget.setItem(contador, 3, QTableWidgetItem(campo4))
        self.tableWidget.insertRow(contador+1)

    def edit_item(self):
        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()
        item = self.tableWidget.item(row,col)

        if item is not None:
            title = "Edit Item"
            data, ok = QInputDialog.getText(self, title,title, QLineEdit.EchoMode.Normal, item.text())
            if ok and data is not None and data != "":
                self.tableWidget.setItem(row, col, QTableWidgetItem(data))
            else:
                QMessageBox.warning(self, "Warning", "El valor no es valido")
        else:
            title = "Edit Item"
            data, ok = QInputDialog.getText(self, title, title, QLineEdit.EchoMode.Normal, "")
            if ok and data is not None and data != "":
                self.tableWidget.setItem(row, col, QTableWidgetItem(data))
            else:
                QMessageBox.warning(self, "Warning", "El valor no es valido")


    def remove_row(self):
        row = self.tableWidget.currentRow()

        reply = QMessageBox.question(self, "Borrar Fila", "¿Quieres borrar la fila .form ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.tableWidget.removeRow(row)




    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Nombre de la capa"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Seg Columna"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Cuarta Columna"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Nueva columna"))
        self.pushButtonAdd.setText(_translate("Form", "Añadir"))
        self.pushButtonEdit.setText(_translate("Form", "Editar"))
        self.pushButtonDelete.setText(_translate("Form", "Borrar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
