# RESOLUCIÓN DE ECUACIONES NO LINEALES: IMPLEMENTACIÓN DE MÉTODOS NUMÉRICOS CON INTERFAZ GRÁFICA

# Autor: Roberto Isaac García Gálvez
# Instituto Tecnológico de Tuxtla Gutiérrez
## Ingeniería Mecatrónica
## 16 de Abril 2025

## Resumen

Este proyecto presenta una implementación práctica de los métodos numéricos de Secante y Newton-Raphson para la resolución de ecuaciones no lineales, incorporando el método de Bisección como referencia comparativa. El objetivo principal fue desarrollar una herramienta computacional con interfaz gráfica que permita no solo obtener soluciones, sino también visualizar gráficamente el comportamiento de los métodos. Utilicé Python como lenguaje de programación base junto con PyQt5 para la interfaz gráfica, complementado con bibliotecas como NumPy, Matplotlib y SymPy para cálculos matemáticos y visualización de resultados. La aplicación resultante permite al usuario ingresar funciones matemáticas, definir parámetros como intervalos y tolerancia, y obtener soluciones aproximadas junto con representaciones gráficas que facilitan la comprensión del proceso iterativo.

## Introducción

Las ecuaciones no lineales son herramientas matemáticas fundamentales para modelar fenómenos físicos complejos en ingeniería mecatrónica, como sistemas de control, dinámica de fluidos o comportamiento estructural, donde las relaciones entre variables no siguen patrones lineales simples. A diferencia de las ecuaciones lineales, estas ecuaciones generalmente no pueden resolverse mediante métodos analíticos directos, lo que hace imprescindible el uso de técnicas numéricas para encontrar soluciones aproximadas.

En este contexto, los métodos de Secante y Newton-Raphson representan dos enfoques poderosos y ampliamente utilizados para abordar este tipo de problemas. El método de Newton-Raphson destaca por su rápida convergencia cuadrática cuando las condiciones iniciales son favorables, mientras que el método de la Secante ofrece una alternativa práctica que no requiere el cálculo explícito de derivadas, lo que resulta ventajoso en funciones complejas.

La implementación de estos métodos mediante una interfaz gráfica presenta múltiples ventajas:

1. Facilita la visualización del comportamiento de las funciones y la convergencia de los métodos, lo que mejora significativamente la comprensión conceptual.
2. Permite experimentar con diferentes funciones y parámetros, promoviendo un aprendizaje interactivo.
3. Proporciona un entorno para comparar la eficiencia y precisión de distintas técnicas numéricas.
4. Ofrece una herramienta práctica que podemos aplicar en problemas reales de ingeniería.

El objetivo general de este proyecto fue desarrollar una aplicación computacional que implemente los métodos de Secante y Newton-Raphson para la resolución de ecuaciones no lineales, con una interfaz gráfica intuitiva que permita visualizar tanto el proceso iterativo como la solución final. Adicionalmente, se incluyó el método de Bisección como referencia comparativa para evaluar el rendimiento de los métodos principales.

## Fundamento Teórico

### 4.1 Método de la Secante

El método de la Secante es una técnica iterativa para encontrar las raíces de una función continua. Su nombre proviene del uso de la secante (línea que corta una curva en dos puntos) como aproximación a la tangente utilizada en el método de Newton-Raphson.

#### Ecuación base y fórmulas

La fórmula iterativa del método de la Secante viene dada por:

$$x_{n+1} = x_n - f(x_n) \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$

Esta ecuación puede interpretarse como una aproximación al método de Newton-Raphson donde la derivada se reemplaza por una diferencia finita:

$$f'(x_n) \approx \frac{f(x_n) - f(x_{n-1})}{x_n - x_{n-1}}$$

#### Condiciones de aplicación

Para aplicar el método de la Secante se requiere:
- Una función continua en el intervalo de interés
- Dos valores iniciales $x_0$ y $x_1$, que idealmente deben estar cerca de la raíz buscada
- Un criterio de tolerancia para detener el proceso iterativo

#### Convergencia

El método de la Secante tiene una tasa de convergencia superlineal con orden aproximado de 1.618 (número áureo), que lo sitúa entre la convergencia lineal del método de bisección y la cuadrática del método de Newton-Raphson. Esta característica lo hace atractivo cuando:

- El cálculo de derivadas es complicado o costoso computacionalmente
- Se dispone de dos aproximaciones iniciales razonables
- Se busca un equilibrio entre velocidad de convergencia y simplicidad de implementación

Sin embargo, al igual que el método de Newton-Raphson, puede diverger en ciertas situaciones si los valores iniciales no son adecuados.

### 4.2 Método de Newton-Raphson

El método de Newton-Raphson es uno de los métodos iterativos más potentes para encontrar raíces de funciones diferenciables.

#### Derivación de la fórmula

La idea fundamental consiste en aproximar la función por su recta tangente en un punto y tomar el punto donde esta recta cruza el eje x como la siguiente aproximación. Matemáticamente:

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

Esta fórmula puede derivarse a partir de la expansión de Taylor de primer orden de la función $f(x)$ alrededor del punto $x_n$:

$$f(x) \approx f(x_n) + f'(x_n)(x - x_n)$$

Al hacer $f(x) = 0$ y despejar $x$, obtenemos la siguiente aproximación $x_{n+1}$.

#### Hipótesis de funcionamiento

El método de Newton-Raphson se basa en las siguientes hipótesis:
- La función $f(x)$ debe ser continuamente diferenciable en el entorno de la raíz
- La derivada $f'(x)$ no debe anularse en la vecindad de la raíz
- El valor inicial $x_0$ debe estar "suficientemente cerca" de la raíz buscada

#### Riesgos de divergencia

A pesar de su rapidez de convergencia, el método presenta varias limitaciones:
1. Si la derivada se anula o es muy pequeña en algún punto del proceso iterativo, el método puede diverger o producir divisiones por números muy pequeños
2. En funciones con múltiples raíces o puntos de inflexión, la convergencia depende críticamente del punto inicial
3. Cuando la función tiene comportamientos asintóticos o variaciones bruscas, puede producirse un "salto" a regiones lejanas, perdiendo la convergencia

Estos riesgos hacen necesario implementar mecanismos de control como límites en el número de iteraciones y criterios robustos de convergencia.

## Diseño de la Interfaz

### 5.1 Herramientas y tecnologías utilizadas

Para este proyecto utilicé un conjunto de tecnologías modernas que me permitieron crear una aplicación robusta y funcional:

1. **Python**: Como lenguaje base por su flexibilidad, legibilidad y amplio soporte para cálculos científicos.

2. **PyQt5**: Framework para el desarrollo de la interfaz gráfica, que ofrece componentes nativos del sistema operativo y alto rendimiento visual.

3. **Bibliotecas de apoyo**:
   - **NumPy**: Para operaciones numéricas eficientes y manejo de arrays
   - **SymPy**: Para cálculo simbólico, especialmente en la evaluación y derivación de funciones
   - **Matplotlib**: Para la visualización gráfica de funciones y resultados
   - **mplcursors**: Para añadir interactividad a los gráficos

### 5.2 Estructura general de la GUI

La interfaz gráfica está organizada en cuatro secciones principales:

1. **Panel de entrada de datos**: 
   - Campos para ingresar funciones matemáticas (con posibilidad de agregar múltiples funciones)
   - Entradas para los valores del intervalo [a, b]
   - Configuración de tolerancia y número máximo de iteraciones
   - Selección del método numérico y opciones de visualización

2. **Panel de gráficos**:
   - Representación visual de la función
   - Indicación de la raíz encontrada
   - Opciones interactivas para explorar los valores de la función

3. **Tabla de resultados**:
   - Muestra las iteraciones del método seleccionado
   - Valores de x en cada iteración
   - Valores de f(x) correspondientes

4. **Barra de controles**:
   - Botones para calcular, guardar resultados y salir
   - Opciones adicionales como cambio de tema y ayuda

### 5.3 Diagrama de flujo de interacción

El flujo de interacción del usuario con la aplicación sigue esta secuencia:

1. El usuario ingresa la función matemática y los parámetros necesarios
2. Selecciona el método numérico deseado (Bisección, Newton-Raphson o Secante)
3. Al hacer clic en "Calcular Raíz", la aplicación:
   - Valida las entradas del usuario
   - Ejecuta el algoritmo seleccionado
   - Genera la gráfica de la función
   - Actualiza la tabla con los resultados de las iteraciones
   - Muestra la raíz encontrada
4. El usuario puede:
   - Guardar los resultados en un archivo
   - Modificar los parámetros para nueva ejecución
   - Cambiar el tema de la interfaz
   - Solicitar ayuda sobre el uso de la aplicación

## Desarrollo del Código

### 6.1 Lógica de ingreso de datos

La validación de entradas es crucial para garantizar el correcto funcionamiento de los métodos numéricos. Implementé las siguientes validaciones:

```python
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
```

Este código asegura que:
- Los valores ingresados sean numéricos
- El intervalo [a, b] sea válido (a < b)
- La tolerancia y el número máximo de iteraciones tengan valores apropiados

Para la interpretación de funciones matemáticas, utilicé la biblioteca SymPy que permite manejar expresiones simbólicas:

```python
def parse_function(expr):
    try:
        x = symbols('x')
        return sympify(expr)
    except SympifyError as e:
        raise ValueError(f"Error al analizar la expresión: {str(e)}")
```

Esta función convierte la expresión ingresada por el usuario en un objeto matemático que puede ser evaluado y derivado simbólicamente.

### 6.2 Implementación del método de la Secante

El método de la Secante se implementó siguiendo su formulación matemática:

```python
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
```

Aspectos importantes de esta implementación:
1. La función recibe dos puntos iniciales x0 y x1
2. En cada iteración, calcula un nuevo punto usando la fórmula del método
3. Almacena los resultados intermedios para mostrarlos en la tabla
4. Implementa manejo de errores para casos de división por cero
5. Limita el número de iteraciones con un valor máximo

### 6.3 Implementación del método de Newton-Raphson

La implementación del método de Newton-Raphson requiere calcular tanto el valor de la función como su derivada:

```python
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
```

Características clave:
1. Recibe funciones f(x) y su derivada df(x)
2. Utiliza SymPy para calcular automáticamente la derivada de la función ingresada
3. Verifica si la derivada se anula durante el proceso
4. Aplica el criterio de convergencia basado en la tolerancia especificada

El cálculo simbólico de la derivada se realiza con:

```python
f_expr = parse_function(func_input.text())
f = lambdify(x, f_expr, 'numpy')
df = lambdify(x, diff(f_expr, x), 'numpy')
```

### 6.4 Salida de resultados y gráficas

La visualización es un componente fundamental de este proyecto. Para representar gráficamente la función y la raíz encontrada:

```python
def plot_function(self, f_expr, a, b, root):
    self.ax.clear()

    x = np.linspace(a, b, 400)  # 400 puntos entre a y b
    y = lambdify(symbols('x'), f_expr, 'numpy')(x)

    self.ax.plot(x, y, label=f_expr, color=self.color_combo.currentText())
    self.ax.axhline(0, color='black', linewidth=0.5)  # Eje X
    self.ax.axvline(root, color='r', linestyle='--', label=f'Raíz: {root:.4f}')
    self.ax.set_title('Gráfica de la función', fontsize=12)
    self.ax.legend()

    # Habilitar cursores interactivos
    mplcursors.cursor(self.ax, hover=True)

    self.canvas.draw()
```

Este código:
1. Genera una serie de puntos en el intervalo [a, b]
2. Evalúa la función para esos puntos
3. Traza la gráfica con el color seleccionado
4. Añade líneas para los ejes y para marcar la raíz encontrada
5. Habilita cursores interactivos para explorar los valores

Para mostrar los resultados en forma tabular:

```python
def update_table(self, results):
    self.table.setRowCount(len(results))
    for i, (idx, x, fx) in enumerate(results):
        self.table.setItem(i, 0, QTableWidgetItem(str(idx)))
        self.table.setItem(i, 1, QTableWidgetItem(f"{x:.6f}"))
        self.table.setItem(i, 2, QTableWidgetItem(f"{fx:.6f}"))
    self.table.resizeColumnsToContents()
```

## Ejemplos y Pruebas

Para evaluar el desempeño de los métodos implementados, realicé varias pruebas con funciones de diferente complejidad. A continuación, presento algunos casos representativos:

### Caso 1: Función polinómica simple
- Función: $f(x) = x^2 - 4$
- Intervalo: [0, 5]
- Raíz esperada: 2

Esta función tiene una raíz fácilmente identificable y permite verificar el funcionamiento básico de los métodos.

### Caso 2: Función trigonométrica
- Función: $f(x) = \sin(x) - 0.5$
- Intervalo: [0, π]
- Raíz esperada: π/6 ≈ 0.5236

Las funciones trigonométricas representan un buen caso de prueba para evaluar la precisión de los métodos con funciones no polinómicas.

### Caso 3: Función con múltiples raíces
- Función: $f(x) = \sin(x) \cdot \cos(x)$
- Intervalo: [-π, π]
- Raíces esperadas: 0, ±π/2, ±π

Este caso permite evaluar cómo los diferentes métodos convergen a distintas raíces dependiendo de los valores iniciales.

### Caso 4: Función con comportamiento complejo
- Función: $f(x) = x^3 - 2x^2 + 4x - 8$
- Intervalo: [1, 3]
- Raíz esperada: 2

Esta función polinómica de grado 3 presenta variaciones en su pendiente que pueden afectar la convergencia de los métodos.

En cada prueba, comparé los tres métodos (Bisección, Newton-Raphson y Secante) considerando:
- Número de iteraciones hasta la convergencia
- Precisión de la raíz encontrada
- Comportamiento ante diferentes valores iniciales

## Resultados y Discusión

Tras realizar numerosas pruebas con diferentes funciones, observé patrones consistentes en el comportamiento de los métodos implementados:

### Método de Bisección
- **Ventajas**: Convergencia garantizada si f(a) y f(b) tienen signos opuestos
- **Desventajas**: Convergencia lenta, especialmente en intervalos grandes
- **Comportamiento**: Redujo el intervalo de búsqueda a la mitad en cada iteración, mostrando convergencia lineal

### Método de Newton-Raphson
- **Ventajas**: Convergencia cuadrática cuando las condiciones son favorables
- **Desventajas**: Sensible al valor inicial; puede diverger si la derivada se aproxima a cero
- **Comportamiento**: Mostró la convergencia más rápida en la mayoría de los casos, pero falló en situaciones donde la función tenía comportamientos complejos cerca de la raíz

### Método de la Secante
- **Ventajas**: No requiere el cálculo de derivadas; convergencia superlineal
- **Desventajas**: Necesita dos valores iniciales; puede diverger si estos no son adecuados
- **Comportamiento**: Ofreció un equilibrio entre la robustez del método de bisección y la velocidad del método de Newton-Raphson

En términos de usabilidad de la interfaz, la implementación con PyQt5 demostró ser intuitiva y funcional. Los usuarios pueden:
1. Ingresar fácilmente diferentes funciones y parámetros
2. Visualizar claramente la función y la ubicación de la raíz
3. Analizar el proceso iterativo a través de la tabla de resultados
4. Guardar los resultados para análisis posteriores

El componente gráfico resultó ser especialmente valioso para comprender visualmente el comportamiento de los métodos y la naturaleza de las funciones analizadas.

## Conclusiones

A través del desarrollo de este proyecto, he logrado implementar con éxito una aplicación que integra métodos numéricos para la resolución de ecuaciones no lineales con una interfaz gráfica interactiva. Las principales conclusiones derivadas de este trabajo son:

1. Los métodos de Newton-Raphson y Secante ofrecen aproximaciones eficientes para encontrar raíces de ecuaciones no lineales, cada uno con sus propias ventajas y limitaciones dependiendo del contexto de aplicación.

2. La visualización gráfica de los resultados mejora significativamente la comprensión del comportamiento de los métodos y facilita la interpretación de los resultados numéricos.

3. La biblioteca SymPy proporciona herramientas poderosas para el manejo simbólico de expresiones matemáticas, permitiendo evaluar funciones y calcular derivadas de manera robusta.

4. La combinación de PyQt5 con Matplotlib ofrece un entorno flexible para desarrollar aplicaciones científicas con interfaces gráficas profesionales.

5. El método de Newton-Raphson generalmente converge más rápido que los otros métodos probados, pero requiere condiciones iniciales más favorables y puede fallar en casos donde la derivada se aproxima a cero.

6. El método de la Secante representa un buen compromiso entre velocidad de convergencia y facilidad de implementación, siendo una alternativa práctica cuando el cálculo de derivadas es complicado.

7. La interfaz gráfica desarrollada proporciona un entorno accesible para experimentar con diferentes funciones y parámetros, facilitando el aprendizaje y la experimentación.

El trabajo realizado también presenta algunas limitaciones que podrían abordarse en futuras mejoras:

1. Se podrían implementar métodos adicionales como el método de punto fijo o el método de la regula falsi.

2. La aplicación actual se limita a funciones de una variable; una extensión natural sería abordar sistemas de ecuaciones no lineales.

3. Se podría añadir funcionalidad para analizar y visualizar la velocidad de convergencia de los diferentes métodos.

4. La integración con otras bibliotecas de computación simbólica podría expandir las capacidades para manejar expresiones matemáticas más complejas.

Este proyecto ha sido una valiosa oportunidad para aplicar conocimientos de programación, matemáticas y diseño de interfaces en la creación de una herramienta práctica para la resolución de problemas de ingeniería.

## Referencias

1. Burden, R. L., & Faires, J. D. (2011). *Numerical Analysis* (9th ed.). Brooks/Cole, Cengage Learning.

2. Chapra, S. C., & Canale, R. P. (2015). *Numerical Methods for Engineers* (7th ed.). McGraw-Hill Education.

3. Kiusalaas, J. (2015). *Numerical Methods in Engineering with Python 3*. Cambridge University Press.

4. Documentación oficial de PyQt5: https://www.riverbankcomputing.com/static/Docs/PyQt5/

5. Documentación de NumPy: https://numpy.org/doc/

6. Documentación de SymPy: https://docs.sympy.org/

7. Documentación de Matplotlib: https://matplotlib.org/stable/contents.html

8. Summerfield, M. (2018). *Python in Practice: Create Better Programs Using Concurrency, Libraries, and Patterns*. Addison-Wesley Professional.

9. Qt Documentation: https://doc.qt.io/

## Anexos

### Código fuente completo

El código fuente completo está organizado en un único archivo Python que contiene todas las clases y funciones necesarias para la ejecución de la aplicación. Los componentes principales incluyen:

1. Implementación de los métodos numéricos (bisección, Newton-Raphson y secante)
2. Función para procesar expresiones matemáticas
3. Clase principal de la interfaz gráfica (MainWindow)
4. Funciones auxiliares para visualización y manejo de datos

El código se ha estructurado siguiendo buenas prácticas de programación orientada a objetos, con comentarios explicativos que facilitan su comprensión y mantenimiento.

### Manual de usuario

#### Requisitos previos
- Python 3.6 o superior
- PyQt5
- NumPy
- Matplotlib
- SymPy
- mplcursors

#### Instalación de dependencias
```
pip install numpy matplotlib sympy PyQt5 mplcursors
```

#### Uso de la aplicación
1. Ejecute el programa con el nobre que lo guardastes
2. Ingrese la función matemática en el campo correspondiente
3. Proporcione los valores de a y b para el intervalo
4. Ajuste la tolerancia y el número máximo de iteraciones si es necesario
5. Seleccione el método numérico deseado
6. Haga clic en "Calcular Raíz"
7. Observe la gráfica y los resultados en la tabla
8. Utilice el botón "Guardar Resultados" para exportar los datos si lo desea

#### Funcionalidades adicionales
- Puede añadir múltiples funciones utilizando el botón "Agregar Función"
- Cambie el tema de la interfaz con el botón "Cambiar Tema"
- Acceda a la ayuda mediante el botón correspondiente
