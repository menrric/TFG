from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, \
    QMessageBox, QFileDialog
from PyQt6.QtGui import QIcon
import os
import sys


class MainWindow(QMainWindow):
    def __init__(self, output_path):
        super().__init__()
        self.setWindowTitle("Generar Gráficas")
        self.setGeometry(100, 100, 400, 200)

        # Ruta de salida
        self.output_path = output_path

        # Crear componentes de la interfaz
        self.label_output = QLabel("Ruta de salida: ")
        self.label_output_value = QLabel(self.output_path)

        self.btn_graficas = QPushButton("Generar Gráficas")
        self.btn_graficas.setEnabled(True)
        self.btn_graficas.clicked.connect(self.generate_graphs)

        self.label_campos = QLabel("Campos:")
        self.combo_campos = QComboBox()
        self.combo_campos.addItem("EER")
        # Agrega más campos aquí

        # Diseño de la ventana principal
        layout = QVBoxLayout()
        layout.addWidget(self.label_output)
        layout.addWidget(self.label_output_value)
        layout.addWidget(self.btn_graficas)
        layout.addWidget(self.label_campos)
        layout.addWidget(self.combo_campos)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def generate_graphs(self):
        # Obtener el campo seleccionado
        campo = self.combo_campos.currentText()

        # Comprobar la existencia de la carpeta de experimentos
        experimentos_path = os.path.join(self.output_path, "Experimentos")
        if not os.path.exists(experimentos_path):
            QMessageBox.critical(self, "Error", "La carpeta de experimentos no existe.")
            return

        # Obtener las carpetas de experimentos
        carpetas_experimentos = [carpeta for carpeta in os.listdir(experimentos_path) if
                                 os.path.isdir(os.path.join(experimentos_path, carpeta))]

        # Comprobar si existen carpetas de experimentos
        if not carpetas_experimentos:
            QMessageBox.critical(self, "Error", "No hay carpetas de experimentos disponibles.")
            return

        # Procesar los archivos XML de cada experimento
        for carpeta in carpetas_experimentos:
            experimento_path = os.path.join(experimentos_path, carpeta)
            xml_path = os.path.join(experimento_path, "Experimento.xml")
            if not os.path.exists(xml_path):
                QMessageBox.critical(self, "Error", f"No se encontró el archivo XML en la carpeta {experimento_path}.")
                continue

            # Aquí puedes agregar la lógica para procesar el archivo XML y generar las gráficas
            # Puedes usar la variable "campo" para determinar qué campos procesar

        QMessageBox.information(self, "Éxito", "Gráficas generadas correctamente.")


if __name__ == "__main__":
    app = QApplication([])
    output_path = "Ruta de salida desde VentanaPrincipal"
    window = MainWindow(output_path)
    window.show()
    sys.exit(app.exec())