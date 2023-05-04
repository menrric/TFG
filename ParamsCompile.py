from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ParamCompile(object):

    def setupUi(self, ParamCompile):

        self.loss_value = None
        self.optimize = None
        self.epocas = None


        ParamCompile.setObjectName("ParamCompile")
        ParamCompile.resize(537, 59)
        self.tableWidget = QtWidgets.QTableWidget(parent=ParamCompile)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 531, 241))
        self.tableWidget.setMidLineWidth(0)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.tableWidget.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.comboBoxLoss = QtWidgets.QComboBox(parent=ParamCompile)
        self.comboBoxLoss.setGeometry(QtCore.QRect(80, 30, 131, 22))
        self.comboBoxLoss.setObjectName("comboBoxLoss")
        self.comboBoxLoss.addItem("mean_squared_error")
        self.comboBoxLoss.addItem("categorical_crossentropy")
        self.comboBoxLoss.addItem("binary_crossentropy")
        self.comboBoxLoss.addItem("mean_absolute_error")
        self.comboBoxLoss.addItem("mean_squared_logarithmic_error")
        self.comboBoxLoss.addItem("kullback_leibler_divergence")
        self.comboBoxLoss.currentTextChanged.connect(self.setLossValue)


        self.comboBoxOptimizers = QtWidgets.QComboBox(parent=ParamCompile)
        self.comboBoxOptimizers.setGeometry(QtCore.QRect(250, 30, 91, 22))
        self.comboBoxOptimizers.setObjectName("comboBoxOptimizers")
        self.comboBoxOptimizers.addItem("SGD")
        self.comboBoxOptimizers.addItem("RMSprop")
        self.comboBoxOptimizers.addItem("Adam")
        self.comboBoxOptimizers.currentTextChanged.connect(self.setOptimizerValue)


        self.lineEditEpocas = QtWidgets.QLineEdit(parent=ParamCompile)
        self.lineEditEpocas.setGeometry(QtCore.QRect(390, 30, 121, 20))
        self.lineEditEpocas.setObjectName("lineEditEpocas")
        self.lineEditEpocas.textChanged.connect(self.setEpocasValue)

        self.retranslateUi(ParamCompile)
        QtCore.QMetaObject.connectSlotsByName(ParamCompile)

    '''
    setLossValue 
    Function to use to store the value of loss
    '''
    def setLossValue(self, text):
        self.loss = text

    '''
    setOptimizerValue 
    Function to use to store the value of optimize
    '''
    def setOptimizerValue(self, text):
        self.optimize = text

    '''
    setEpocasValue 
    Function to use to store the value of epocas
    '''
    def setEpocasValue(self, new_text):
        self.epocas = int(new_text)



    def retranslateUi(self, ParamCompile):
        _translate = QtCore.QCoreApplication.translate
        ParamCompile.setWindowTitle(_translate("ParamCompile", "Dialog"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("ParamCompile", "Parametros"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("ParamCompile", "Función Loss"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("ParamCompile", "Optimizers"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("ParamCompile", "Epocas"))
        self.comboBoxLoss.setItemText(0, _translate("ParamCompile", "mean_squared_error"))
        self.comboBoxLoss.setItemText(1, _translate("ParamCompile", "categorical_crossentropy"))
        self.comboBoxLoss.setItemText(2, _translate("ParamCompile", "binary_crossentropy"))
        self.comboBoxLoss.setItemText(3, _translate("ParamCompile", "mean_absolute_error"))
        self.comboBoxLoss.setItemText(4, _translate("ParamCompile", "mean_squared_logarithmic_error"))
        self.comboBoxLoss.setItemText(5, _translate("ParamCompile", "kullback_leibler_divergence"))
        self.comboBoxOptimizers.setItemText(0, _translate("ParamCompile", "SGD"))
        self.comboBoxOptimizers.setItemText(1, _translate("ParamCompile", "RMSprop"))
        self.comboBoxOptimizers.setItemText(2, _translate("ParamCompile", "Adam"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ParamCompile = QtWidgets.QDialog()
    ui = Ui_ParamCompile()
    ui.setupUi(ParamCompile)
    ParamCompile.show()
    sys.exit(app.exec())
