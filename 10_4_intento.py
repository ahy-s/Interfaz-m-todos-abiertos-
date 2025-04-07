import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget,
                             QTableWidgetItem, QFileDialog, QMessageBox, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt
from sympy import symbols, lambdify, diff, sympify, SympifyError
import mplcursors

# Implementación de los métodos numéricos
def bisection_method(f, a, b, tol, max_iter):
    results = []
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        results.append((i, c, fc))
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c, results
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    raise ValueError("Número máximo de iteraciones alcanzado.")

def newton_raphson_method(f, df, x0, tol, max_iter):
    x = x0
    results = []
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        results.append((i, x, fx))
        if abs(fx) < tol:
            return x, results
        if dfx == 0:
            raise ValueError("Derivada igual a cero. No se puede continuar.")
        x = x - fx / dfx
    raise ValueError("Número máximo de iteraciones alcanzado.")

def secant_method(f, x0, x1, tol, max_iter):
    x_prev = x1
    x = x0
    results = []
    for i in range(max_iter):
        fx = f(x)
        fx_prev = f(x_prev)
        results.append((i, x, fx))
        if abs(fx) < tol:
            return x, results
        if fx - fx_prev == 0:
            raise ValueError("División por cero en el método de la secante.")
        x_new = x - fx * (x - x_prev) / (fx - fx_prev)
        x_prev = x
        x = x_new
    raise ValueError("Número máximo de iteraciones alcanzado.")

def parse_function(expr):
    try:
        x = symbols('x')
        return sympify(expr)
    except SympifyError as e:
        raise ValueError(f"Error al analizar la expresión: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Métodos Numéricos - PyQt5")
        self.setGeometry(100, 100, 1000, 800)

        # Configurar el widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # Layout para los widgets de entrada
        self.input_layout = QVBoxLayout()
        self.create_input_widgets(self.input_layout)

        # Área de gráficos y tabla
        self.create_output_widgets(self.main_layout)

        # Conectar señales
        self.calculate_button.clicked.connect(self.calculate_root)
        self.save_button.clicked.connect(self.save_results)
        self.exit_button.clicked.connect(self.close)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.help_button.clicked.connect(self.show_help)
        self.add_function_button.clicked.connect(self.add_function_input)

        # Configuración inicial del tema
        self.is_dark_theme = False
        self.toggle_theme()

        # Agregar el layout de entrada al layout principal
        self.main_layout.addLayout(self.input_layout)

        # Aplicar estilo mejorado
        self.apply_style()

    def apply_style(self):
        if self.is_dark_theme:
            self.setStyleSheet("""
                QWidget {
                    background-color: #333;
                    color: #FFF;
                }
                QLineEdit, QComboBox {
                    background-color: #444;
                    color: #FFF;
                    border: 1px solid #555;
                    padding: 5px;
                    border-radius: 3px;
                    margin: 5px;
                }
                QPushButton {
                    background-color: #555;
                    color: #FFF;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
                QLabel {
                    color: #FFF;
                    margin: 5px;
                }
                QTableWidget {
                    gridline-color: #555;
                    color: #FFF;
                    background-color: #444;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                    color: #333;
                }
                QLineEdit, QComboBox {
                    border: 1px solid #ccc;
                    padding: 5px;
                    border-radius: 3px;
                    margin: 5px;
                }
                QPushButton {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QLabel {
                    font-weight: bold;
                    margin: 5px;
                }
                QTableWidget {
                    gridline-color: #ccc;
                }
            """)

    def create_input_widgets(self, layout):
        grid = QGridLayout()

        # Entradas de función y parámetros
        self.func_inputs = []
        self.add_function_input()

        self.a_input = QLineEdit()
        self.a_input.setPlaceholderText("Ingrese el valor de a")
        self.b_input = QLineEdit()
        self.b_input.setPlaceholderText("Ingrese el valor de b")
        self.tol_input = QLineEdit("1e-6")
        self.tol_input.setPlaceholderText("Ingrese la tolerancia")
        self.max_iter_input = QLineEdit("100")
        self.max_iter_input.setPlaceholderText("Ingrese el máximo de iteraciones")

        # Combobox para método y color
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Bisección", "Newton-Raphson", "Secante"])
        self.color_combo = QComboBox()
        self.color_combo.addItems(["blue", "green", "red", "purple"])

        # Botones
        self.calculate_button = QPushButton("Calcular Raíz")
        self.save_button = QPushButton("Guardar Resultados")
        self.exit_button = QPushButton("Salir")
        self.theme_button = QPushButton("Cambiar Tema")
        self.help_button = QPushButton("Ayuda")
        self.add_function_button = QPushButton("Agregar Función")

        # Agregar al layout
        grid.addWidget(QLabel("Funciones:"), 0, 0, 1, 2)
        for i, func_input in enumerate(self.func_inputs):
            grid.addWidget(func_input, 0, 2 + i)

        grid.addWidget(QLabel("a:"), 1, 0)
        grid.addWidget(self.a_input, 1, 1)
        grid.addWidget(QLabel("b:"), 1, 2)
        grid.addWidget(self.b_input, 1, 3)

        grid.addWidget(QLabel("Tolerancia:"), 2, 0)
        grid.addWidget(self.tol_input, 2, 1)
        grid.addWidget(QLabel("Máx iter:"), 2, 2)
        grid.addWidget(self.max_iter_input, 2, 3)

        grid.addWidget(QLabel("Método:"), 3, 0)
        grid.addWidget(self.method_combo, 3, 1)
        grid.addWidget(QLabel("Color:"), 3, 2)
        grid.addWidget(self.color_combo, 3, 3)

        grid.addWidget(self.calculate_button, 4, 0, 1, 2)
        grid.addWidget(self.save_button, 4, 2, 1, 1)
        grid.addWidget(self.exit_button, 4, 3, 1, 1)
        grid.addWidget(self.theme_button, 5, 0, 1, 2)
        grid.addWidget(self.help_button, 5, 2, 1, 1)
        grid.addWidget(self.add_function_button, 5, 3, 1, 1)

        layout.addLayout(grid)

    def add_function_input(self):
        func_input = QLineEdit()
        func_input.setPlaceholderText("Ingrese la función, ej. x**2 - 2*x + 9 o x^2 - 2*x + 9")
        self.func_inputs.append(func_input)

        # Insertar el nuevo campo de entrada justo debajo del primer campo de función
        self.input_layout.insertWidget(1, func_input)

    def create_output_widgets(self, layout):
        # Layout horizontal para gráfico y tabla
        h_layout = QHBoxLayout()

        # Área de desplazamiento para el gráfico
        scroll_area_graph = QScrollArea()
        scroll_area_graph.setWidgetResizable(True)
        scroll_content_graph = QWidget()
        scroll_layout_graph = QVBoxLayout(scroll_content_graph)

        # Gráfico de Matplotlib
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        scroll_layout_graph.addWidget(self.canvas)

        scroll_area_graph.setWidget(scroll_content_graph)
        h_layout.addWidget(scroll_area_graph, 70)  # 70% del espacio

        # Área de desplazamiento para la tabla
        scroll_area_table = QScrollArea()
        scroll_area_table.setWidgetResizable(True)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Iteración", "x", "f(x)"])
        scroll_area_table.setWidget(self.table)

        h_layout.addWidget(scroll_area_table, 30)  # 30% del espacio

        layout.addLayout(h_layout)

        # Etiqueta de resultado
        self.result_label = QLabel("Resultado: ")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.result_label)

    def validate_inputs(self):
        try:
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            tol = float(self.tol_input.text())
            max_iter = int(self.max_iter_input.text())
        except ValueError:
            QMessageBox.critical(self, "Error", "Ingrese valores numéricos válidos")
            return False, None

        if a >= b:
            QMessageBox.critical(self, "Error", "El intervalo [a, b] no es válido (a < b)")
            return False, None

        return True, (a, b, tol, max_iter)

    def calculate_root(self):
        valid, inputs = self.validate_inputs()
        if not valid:
            return

        a, b, tol, max_iter = inputs
        x0 = (a + b) / 2

        x = symbols('x')

        for func_input in self.func_inputs:
            try:
                f_expr = parse_function(func_input.text())
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))
                continue  # Continuar con la siguiente función

            try:
                f = lambdify(x, f_expr, 'numpy')
                df = lambdify(x, diff(f_expr, x), 'numpy')
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error en la función: {str(e)}")
                continue  # Continuar con la siguiente función

            method = self.method_combo.currentText()
            try:
                if method == "Bisección":
                    root, results = bisection_method(f, a, b, tol, max_iter)
                elif method == "Newton-Raphson":
                    root, results = newton_raphson_method(f, df, x0, tol, max_iter)
                elif method == "Secante":
                    root, results = secant_method(f, a, x0, tol, max_iter)

                self.result_label.setText(f"Raíz encontrada para {f_expr}: {root:.6f}")
                self.plot_function(f_expr, a, b, root)
                self.update_table(results)

            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))

    def plot_function(self, f_expr, a, b, root):
        self.ax.clear()

        x = np.linspace(a, b, 400)
        y = lambdify(symbols('x'), f_expr, 'numpy')(x)

        self.ax.plot(x, y, label=f_expr, color=self.color_combo.currentText())
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(root, color='r', linestyle='--', label=f'Raíz: {root:.4f}')
        self.ax.set_title('Gráfica de la función', fontsize=12)
        self.ax.legend()

        # Habilitar cursores interactivos
        mplcursors.cursor(self.ax, hover=True)

        # Marca de agua
        self.ax.text(0.5, -0.15, "Hecho por Roberto Isaac García Gálvez",
                    fontsize=10, color='gray', ha='center', va='center',
                    transform=self.ax.transAxes)

        self.canvas.draw()

    def update_table(self, results):
        self.table.setRowCount(len(results))
        for i, (idx, x, fx) in enumerate(results):
            self.table.setItem(i, 0, QTableWidgetItem(str(idx)))
            self.table.setItem(i, 1, QTableWidgetItem(f"{x:.6f}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"{fx:.6f}"))
        self.table.resizeColumnsToContents()

    def save_results(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar resultados", "", "Text Files (*.txt);;CSV Files (*.csv);;Excel Files (*.xlsx)")

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.result_label.text() + "\n")
                    for row in range(self.table.rowCount()):
                        items = [self.table.item(row, col).text()
                               for col in range(self.table.columnCount())]
                        f.write(",".join(items) + "\n")
                QMessageBox.information(self, "Éxito", "Resultados guardados correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_style()
        if self.is_dark_theme:
            self.theme_button.setText("Cambiar a Tema Claro")
        else:
            self.theme_button.setText("Cambiar a Tema Oscuro")

    def show_help(self):
        help_text = """
        Bienvenido a la aplicación de Métodos Numéricos.

        Instrucciones:
        - Ingrese la función en el campo "Función".
        - Ingrese los valores de a y b para el intervalo.
        - Seleccione el método numérico deseado.
        - Haga clic en "Calcular Raíz" para encontrar la raíz.
        - Utilice "Guardar Resultados" para exportar los resultados.
        - Cambie el tema con el botón "Cambiar Tema".
        """
        QMessageBox.information(self, "Ayuda", help_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
#Codigo echo por Roberto Isaac García Gálvez.