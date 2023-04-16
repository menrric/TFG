# Form implementation generated from reading ui file 'SegundaInterfaz.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QInputDialog, QLineEdit, QMessageBox, QTableWidgetItem



class Ui_Form(QDialog):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(577, 391)
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


        #UP ROW BUTTON
        self.pushButtonUp = QtWidgets.QPushButton(Form)
        self.pushButtonUp.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("FlechaArriba.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonUp.setIcon(icon)
        self.pushButtonUp.setObjectName("pushButtonUp")
        self.verticalLayout.addWidget(self.pushButtonUp)
        self.pushButtonUp.clicked.connect(self.swap_row_up)

        #DOWN ROW BUTTON
        self.pushButtonDown = QtWidgets.QPushButton(Form)
        self.pushButtonDown.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("FlechaAbajo.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonDown.setIcon(icon1)
        self.pushButtonDown.setObjectName("pushButtonDown")
        self.verticalLayout.addWidget(self.pushButtonDown)
        self.pushButtonDown.clicked.connect(self.swap_row_down)

        #SPACE LINES
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        # ADD BUTTON
        self.pushButtonAdd = QtWidgets.QPushButton(Form)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.verticalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonAdd.clicked.connect(self.add_row)

        # EDIT BUTTON
        self.pushButtonEdit = QtWidgets.QPushButton(Form)
        self.pushButtonEdit.setObjectName("pushButtonEdit")
        self.verticalLayout.addWidget(self.pushButtonEdit)
        self.pushButtonEdit.clicked.connect(self.edit_item)

        # DELETE BUTTON
        self.pushButtonDelete = QtWidgets.QPushButton(Form)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.verticalLayout.addWidget(self.pushButtonDelete)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.pushButtonDelete.clicked.connect(self.remove_row)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    '''ADD_ROW 
    add_row is used to add a new row to our table. To do this, a pop-up will be displayed that will ask us what we want
    to put in each field.
    '''
    def add_row(self):

        cell = self.tableWidget.rowCount()-1
        for col in range(self.tableWidget.columnCount()):

            title = "Campo" + str(col)
            campo1, ok = QInputDialog.getText(self, title, title)
            if ok and campo1 is not None:
                self.tableWidget.setItem(cell, col, QTableWidgetItem(campo1))
            print(cell)
        self.tableWidget.insertRow(cell + 1)


    '''EDIR_ROW 
    edit_row is used to edit a particular field in a row. To do this, click on the cell to edit and press the edit
     button
    '''
    def edit_item(self):
        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()
        item = self.tableWidget.item(row, col)

        if item is not None:
            title = "Edit Item"
            data, ok = QInputDialog.getText(self, title, title, QLineEdit.EchoMode.Normal, item.text())
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

    '''REMOVE_ROW 
    remove_row is used to delete a specific row. To do this we must click it, hit the delete button and we will get
     a confirmation message
     button
    '''
    def remove_row(self):
        row = self.tableWidget.currentRow()

        reply = QMessageBox.question(self, "Borrar Fila", "¿Quieres borrar la fila .form ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.tableWidget.removeRow(row)

    '''SWAP_ROWS 
    swap_rows is used to swap two rows, which have to be passed as an argument. In this project, it is used to be called
    in the swap_row_up and swap_row_down functions.
    '''
    def swap_rows(self, row1, row2):
        for col in range(self.tableWidget.columnCount()):
            item1 = self.tableWidget.takeItem(row1, col)
            item2 = self.tableWidget.takeItem(row2, col)
            self.tableWidget.setItem(row1, col, item2)
            self.tableWidget.setItem(row2, col, item1)

    '''SWAP_ROW_UP 
    Swap the selected row with the row above
    '''
    def swap_row_up(self):
        row = self.tableWidget.currentRow()
        if row > 0:
            self.swap_rows(row, row - 1)
            self.tableWidget.setCurrentCell(row - 1, 0)


    '''SWAP_ROW_UP 
    Swap the selected row with the row below
    '''
    def swap_row_down(self):
        row = self.tableWidget.currentRow()
        if row < self.tableWidget.rowCount() - 1:
            self.swap_rows(row, row + 1)
            self.tableWidget.setCurrentCell(row + 1, 0)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Nº Capa"))
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