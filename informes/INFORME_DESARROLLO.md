# Informe de desarrollo

**Simulador de Autómatas Finitos Deterministas**  
Estructuras Discretas · `Grupo: 6__`  
Jesus De La Hoz, Carlos Calvo y Brandon Navarro

## 1. Resumen

La aplicación permite construir y activar un AFD desde el navegador, inspeccionar su definición formal y su gráfica, enumerar palabras del lenguaje y probar entradas con un recorrido verificable. El proyecto corre en Windows con un servidor Flask local.

## 2. Requerimientos

El sistema inicia sin AFD. El Módulo 1 construye, modifica y reemplaza un AFD completo. El Módulo 2 muestra hasta cinco palabras reconocidas en orden canónico y el Módulo 3 procesa una palabra cada vez, incluida ε. Ambos obtienen el AFD activo del servidor.

## 3. Arquitectura

Las rutas Flask reciben datos y preparan las vistas. La clase `AFD` y los algoritmos pueden ejecutarse por separado desde Python. Jinja genera HTML, CSS adapta la presentación y JavaScript dibuja el DOT con Viz.js.

## 4. Tecnologías

Python 3.13.5 en las pruebas, Flask 3.1.2, Jinja, HTML5, CSS3, JavaScript, Viz.js 3.31.0 y pytest 8.4.2. El navegador descarga Viz.js desde el propio servidor Flask.

## 5. Estructura

| Directorio o archivo | Responsabilidad |
| --- | --- |
| `app.py` | Punto de entrada, configuración y aplicación Flask |
| `afd/` | Modelo, validación, algoritmos, DOT y estado activo |
| `routes/` | Controladores y borrador de construcción |
| `templates/`, `static/` | Formularios, resultados, estilos y visualización |
| `ejemplos/`, `tests/` | Datos A1–A4 y pruebas automáticas |
| `docs/`, `capturas/`, `informes/` | Material académico y evidencia del funcionamiento |

## 6. Clase AFD

El constructor valida los cinco componentes. `procesar_palabra` crea un `Resultado` con la decisión y los pasos. `estados_alcanzables` usa una cola de búsqueda en anchura partiendo de q₀. Los métodos de datos transforman la definición entre el modelo de Python y JSON.

## 7. Representación de Q, Σ, δ, q₀ y F

Q y Σ son listas que conservan el orden de ingreso. δ se representa con un diccionario de claves `(estado, simbolo)`. q₀ es la cadena que identifica el estado inicial. F se almacena como lista y admite cero elementos.

## 8. Algoritmo de reconocimiento

Desde q₀, se valida cada símbolo, se consulta δ y se actualiza el estado. Si se encuentra un símbolo inválido, se devuelve su posición y el recorrido parcial. Si se consume toda la palabra, la aceptación se determina por la pertenencia del estado alcanzado a F. Para ε, el estado alcanzado es q₀.

## 9. Generación de palabras

Se construyen las transiciones inversas y se buscan los estados desde los que se puede llegar a F. Después se calculan los estados desde los que es posible llegar a F en exactamente n pasos para n de 0 a 10. La enumeración conserva el prefijo y su estado, descarta extensiones que no podrían aceptar y visita los símbolos en el orden de Σ para cada longitud. Cada candidata completa se comprueba con el método del Módulo 3.

## 10. Construcción dinámica del AFD

El asistente solicita nombre, Q, Σ, δ, q₀ y F. La tabla se genera a partir de Q y Σ. Cada celda de texto sugiere destinos de Q. El servidor valida cada paso y conserva los valores del envío al mostrar un error. En el resumen vuelve a validar la definición completa.

## 11. Edición del AFD

El borrador copia los componentes activos. Tras cambiar Q o Σ se mantienen las transiciones que aún son válidas y aparecen celdas pendientes para las demás. Si se elimina un q₀ o un final seleccionado, el asistente pide revisar ese componente.

## 12. Reemplazo del AFD activo

Al confirmar el resumen, `activar_afd` cambia la referencia de módulo y borra el historial de palabras. Abrir un borrador o cancelarlo conserva el AFD vigente. El programa mantiene un AFD activo a la vez y admite activar sucesivos AFD durante la misma ejecución. Importar un JSON válido abre el resumen antes de activar su contenido.

## 13. Generación de la gráfica

Python genera DOT con etiquetas, flecha inicial, doble círculo y aristas dirigidas. Las aristas con igual origen y destino agrupan sus símbolos y las transiciones recíprocas se muestran con dos flechas. Viz.js crea el SVG en el navegador. El Módulo 3 usa el recorrido para colorear los estados y anotar los números de paso en cada flecha.

## 14. Pruebas

Se ejecutó `python -m pytest` en Windows. Las **50 pruebas** cubren el constructor, la validación de δ, el reconocimiento, la generación canónica, la equivalencia con fuerza bruta en A1–A4, la alcanzabilidad, las rutas sin AFD, la edición y la importación/exportación. La revisión en Chrome también cubrió el formulario real, el foco después del procesamiento, el SVG, el reemplazo, el diseño a 390 px y la carga de recursos limitada al servidor local.

## 15. Resultados

| Caso | Resultado del Módulo 2 |
| --- | --- |
| A1 · Número par de ceros | ε, 1, 00, 11, 001 |
| A2 · Termina en ab | ab, aab, bab, aaab, abab |
| A3 · Solo ab y ba | ab, ba |
| A4 · Ninguna palabra | q1 es final y no es alcanzable desde q0 |

Con A2, `abab` se reconoció, `aba` y ε se rechazaron, y `abc` señaló `c` en la posición 3. Las seis capturas se encuentran en [capturas/](../capturas/).

## 16. Problemas encontrados

En la revisión visual, las anotaciones del recorrido aumentaron el ancho natural del SVG y parte de la gráfica del Módulo 3 quedó fuera del área visible. El tamaño intrínseco del diagrama podía ensanchar su columna interna.

## 17. Soluciones

Se limitó el ancho del SVG al espacio disponible y se fijó una columna que puede reducirse con el panel. Se repitió la prueba gráfica para A2 y se regeneraron las capturas. También se verificó en Chrome que el diagrama resaltado cabe dentro de su contenedor.

## 18. Instalación

En Windows, dentro de la carpeta del proyecto, cree el entorno con `python -m venv .venv`. Actívelo con `.\.venv\Scripts\Activate.ps1` e instale las dependencias con `pip install -r requirements.txt`. El README incluye el comando directo para PowerShell cuando la activación está bloqueada.

## 19. Ejecución

Con el entorno activo, ejecute `python app.py` y visite [http://127.0.0.1:5000](http://127.0.0.1:5000). Detenga el servidor con **Ctrl + C**. Descargue el AFD como JSON antes de detenerlo si desea conservarlo.

## 20. Posibles mejoras

Para una futura versión académica podrían añadirse controles para avanzar transición por transición en la gráfica y un modo de ampliación para AFD con muchos estados.

## 21. Preparación para la sustentación

La [guía para los tres integrantes](../docs/GUIA_SUSTENTACION.md) asigna la 5-tupla al integrante 1, construcción y gráfica al integrante 2, y reconocimiento y búsqueda al integrante 3. El ensayo conjunto incluye construir y editar un AFD nuevo en el navegador y comparar sus resultados con un recorrido manual.

## 22. Revisión final

| Requisito | Verificación |
| --- | --- |
| Inicio vacío y avisos en los módulos | Pruebas de las tres rutas y revisión en Chrome |
| Crear, editar y reemplazar desde la interfaz | Pruebas de formulario y recorrido real del asistente |
| Definición, tabla, gráfica y alcanzabilidad | Revisión de A2 y prueba de A4 |
| Orden canónico, límite de longitud y eficiencia | Comparación con fuerza bruta y prueba de alfabeto de cinco símbolos |
| ε, rechazo, posiciones inválidas e historial | Pruebas unitarias, de rutas y capturas con A2 |
| Gráfica resaltada y copia local de Viz.js | Revisión del SVG y carga web limitada al servidor local |
| Exportación e importación | Prueba de ida y vuelta y rechazo de JSON inválido |
| README, documentación, capturas y fuentes | Archivos incluidos en la entrega |

Se aplicaron los requisitos recogidos en el archivo adjunto. El PDF original que menciona ese archivo queda fuera de la revisión. Se interpretó que Σ debe contener al menos un símbolo y que ε se prueba dejando el campo vacío, como indica el asistente.
