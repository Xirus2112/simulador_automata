# Simulador de Autómatas Finitos Deterministas

Proyecto de **Estructuras Discretas** · `Grupo: 6__`

- Jesus De La Hoz
- Carlos Calvo
- Brandon Navarro

Simulador de autómatas finitos deterministas (AFD) en Python y Flask. Permite crear y editar autómatas, visualizar sus transiciones, generar palabras reconocidas y probar entradas paso a paso.

**Estado del proyecto.** Este repositorio contiene el prototipo del simulador. La implementación del equipo para la entrega académica está pendiente. El alcance del uso de Codex se detalla en la sección de autoría académica.

## Instalación y ejecución en Windows

Si va a descargar el proyecto de GitHub, abra PowerShell y ejecute:

```powershell
git clone https://github.com/Xirus2112/simulador_automata.git
cd simulador_automata
```

Desde la carpeta del proyecto, ejecute los siguientes comandos. El prototipo se verificó con **Python 3.13** y requiere Python 3.10 o superior.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Abra [http://127.0.0.1:5000](http://127.0.0.1:5000). Para detener el servidor, pulse **Ctrl + C** en la terminal.

Si PowerShell bloquea la activación, puede ejecutar directamente el Python del entorno.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Si prefiere activar el entorno, puede habilitar scripts locales para su usuario y ejecutar de nuevo `Activate.ps1`.

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

La instalación inicial de los paquetes requiere acceso a PyPI. Después, el simulador funciona localmente. La gráfica usa Viz.js incluido en `static/js/vendor/`. No se requiere instalar Graphviz, configurar `dot.exe` ni usar Node.js.

## Uso de los tres módulos

1. **Construir y visualizar.** Abra **+ Nuevo autómata** e ingrese nombre, Q, Σ, δ, q₀ y F. Valide cada paso, revise el resumen y pulse **Activar autómata**. En la vista del AFD puede consultar la 5-tupla, la tabla, la gráfica y los estados alcanzables. Use **Editar autómata actual** para modificarlo o **+ Nuevo autómata** para reemplazarlo.
2. **Palabras reconocidas.** Explore hasta cinco palabras de longitud ≤ 10 ordenadas primero por longitud y después según el orden de entrada de Σ. Se muestra el recorrido de cada palabra y la causa cuando no se encuentra ninguna.
3. **Probar una palabra.** Escriba la palabra y pulse **Procesar palabra**. Deje el campo vacío para probar ε. El módulo muestra la aceptación, los pasos, la gráfica resaltada para palabras del alfabeto y el historial. Si hay un símbolo inválido, se informa su posición empezando en 1 y se muestra el recorrido parcial.

### Ejemplo de uso con A2

En **Inicio**, elija **A2 - Termina en ab** en *Ejemplos del curso* y pulse **Cargar**. En el Módulo 2 aparecen `ab`, `aab`, `bab`, `aaab` y `abab`. En el Módulo 3, `abab` se reconoce y `aba` se rechaza. Con el campo vacío se prueba ε, que A2 rechaza. Con `abc`, se detecta `c` en la tercera posición.

Para conservar el AFD, elija **Descargar AFD (.json)** en el Módulo 1. Para recuperarlo, seleccione ese archivo en Inicio, pulse **Revisar** y luego **Activar autómata**.

## Tecnologías y estructura

Python implementa las validaciones, δ, el reconocimiento y la búsqueda. Flask recibe formularios y sirve plantillas Jinja con HTML5 y CSS3. JavaScript actualiza el aviso de F vacío y Viz.js transforma el DOT generado en Python en una gráfica SVG. pytest ejecuta las pruebas.

| Ruta | Contenido |
| --- | --- |
| `app.py` | Inicio del servidor local y configuración de Flask |
| `afd/` | Modelo AFD, validación, búsqueda de palabras, generación de DOT y AFD activo |
| `routes/` | Formularios, borrador y rutas de los tres módulos |
| `templates/` y `static/` | Interfaz y copia local de Viz.js |
| `ejemplos/ejemplos.json` | Definiciones A1–A4 |
| `tests/` | Pruebas de la lógica y de Flask |
| `capturas/` | Evidencia de los tres módulos con A2 |
| `docs/` e `informes/` | Material de estudio e informe de desarrollo |

## Pruebas

Con el entorno virtual activo, ejecute:

```powershell
python -m pytest
```

Las pruebas cubren A1–A4, transiciones incompletas o inválidas, ε, caracteres fuera de Σ, orden canónico, equivalencia con fuerza bruta, edición, reemplazo y carga de JSON. También se verificó el flujo en Chrome sobre Windows con los recursos web limitados al servidor local.

## Capturas con A2

| Archivo | Contenido y cómo reproducirlo |
| --- | --- |
| [Módulo 1](capturas/01-modulo-1-a2.png) | Cargue A2 y capture la 5-tupla, la tabla de δ y la gráfica. |
| [Módulo 2](capturas/02-modulo-2-a2.png) | Abra **Palabras reconocidas** y capture las cinco palabras con sus recorridos. |
| [Módulo 3 · abab](capturas/03-modulo-3-abab.png) | Procese `abab` y capture el reconocimiento y los pasos resaltados. |
| [Módulo 3 · aba](capturas/04-modulo-3-aba.png) | Procese `aba` y capture el rechazo y el recorrido completo. |
| [Módulo 3 · ε](capturas/05-modulo-3-epsilon.png) | Procese con el campo vacío y capture el recorrido que solo contiene s0. |
| [Módulo 3 · abc](capturas/06-modulo-3-abc.png) | Procese `abc` y capture el aviso de símbolo inválido. |

## Alcance y decisiones

- El servidor está pensado para un solo usuario en el equipo local. El AFD activo, los borradores y el historial se pierden al cerrar el programa. Al activar otro AFD se vacía el historial. Los archivos exportados permiten recuperar la definición después.
- El formulario pide al menos un símbolo de un carácter en Σ. Dejar el campo de palabra completamente vacío representa ε. Escribir literalmente `ε` introduce un símbolo fuera del alfabeto.
- Se tomó el documento adjunto como especificación disponible. Sus referencias al PDF del profesor se aplicaron según las indicaciones que reproduce el adjunto.

## Material de sustentación

- [Conceptos de AFD](docs/CONCEPTOS_AFD.md)
- [Cómo funciona el código](docs/COMO_FUNCIONA_EL_CODIGO.md)
- [Algoritmo de reconocimiento](docs/ALGORITMO_RECONOCIMIENTO.md)
- [Guía de sustentación para los tres integrantes](docs/GUIA_SUSTENTACION.md)
- [Informe de desarrollo](informes/INFORME_DESARROLLO.md)

## Fuentes externas

- Manejo de formularios, plantillas y servidor de desarrollo. [Documentación de Flask](https://flask.palletsprojects.com/en/stable/quickstart/)
- Pruebas de rutas con el cliente de Flask. [Testing Flask Applications](https://flask.palletsprojects.com/en/stable/testing/)
- Sintaxis utilizada para generar la gráfica. [Lenguaje DOT de Graphviz](https://graphviz.org/doc/info/lang.html)
- API del visor y paquete incluido `@viz-js/viz` 3.31.0. [API de Viz.js](https://viz-js.com/api/), [paquete oficial en npm](https://www.npmjs.com/package/@viz-js/viz/v/3.31.0)
- Preparación y ejecución de las pruebas. [Documentación de pytest](https://docs.pytest.org/en/stable/getting-started.html)
- Automatización de la revisión en Chrome y de las capturas. [Playwright para Python](https://playwright.dev/python/docs/intro)

## Autoría académica y uso de inteligencia artificial

La sección 10 de la página 9 del enunciado exige que el programa sea obra del equipo. Permite usar IA para entender conceptos y resolver dudas sobre el lenguaje de programación. La lectura de los cinco elementos del AFD, el recorrido de una palabra y la búsqueda de palabras reconocidas deben ser escritos por el equipo. El README debe declarar el uso real de la IA y los tres integrantes deben poder explicar y modificar cualquier parte del programa.

### Uso de Codex en el prototipo

OpenAI Codex ayudó a interpretar el enunciado y escribió código del prototipo, incluida la lógica de los tres apartados indicados arriba. También diseñó y simplificó la interfaz, agregó comentarios en español, preparó y ejecutó las pruebas, generó las capturas y redactó la documentación.

### Reparto propuesto para la versión del equipo

| Responsable | Trabajo previsto | Comprobación |
| --- | --- | --- |
| Integrante 1 | Implementar la lectura y validación de Q, Σ, δ, q₀ y F desde el formulario. En el prototipo, esta parte está en [las rutas](routes/main.py) y [el validador](afd/validator.py). | Rechazar un destino fuera de Q y permitir corregir la celda conservando el resto de los datos. |
| Integrante 2 | Implementar el recorrido y la decisión de aceptación de una palabra. En el prototipo, esta parte está en [el modelo AFD](afd/automata.py). | Con A2, comprobar que `abab` termina en s2, que ε se queda en s0 y que `abc` se detiene en la posición 3. |
| Integrante 3 | Implementar la búsqueda de hasta cinco palabras por longitud y orden de Σ. En el prototipo, esta parte está en [el generador de palabras](afd/word_generator.py). | Verificar que A2 devuelve `ab`, `aab`, `bab`, `aaab` y `abab`, y que A4 devuelve cero palabras. |

El plan es escribir la versión propia a partir del enunciado y de los casos oficiales. Si se quiere reutilizar la interfaz, las pruebas u otros archivos del prototipo, corresponde consultarlo con el docente. Antes de entregar, cada integrante practicará explicar y modificar una parte escrita por otro. La declaración del README de esa versión debe reflejar lo que se hizo realmente.
