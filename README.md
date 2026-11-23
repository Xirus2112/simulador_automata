# Simulador de Autómatas Finitos Deterministas

Proyecto de **Estructuras Discretas** · `Grupo: 6__`

- Jesus De La Hoz
- Carlos Calvo
- Brandon Navarro

El simulador permite construir y modificar un AFD completo desde el navegador. El objetivo es relacionar la definición matemática con la tabla, la gráfica y el recorrido de cada palabra, de modo que los tres integrantes puedan explicar y cambiar el autómata durante la sustentación.

## Instalación y ejecución en Windows

Abra PowerShell. Se verificó con **Python 3.13**. Los requisitos permiten usar Python 3.10 o superior.

```powershell
cd "$env:USERPROFILE\Downloads\sw_ed_parcial"
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

## Uso de inteligencia artificial

Se utilizó OpenAI Codex para interpretar el enunciado, proponer la estructura, escribir y revisar código, diseñar la interfaz, preparar y ejecutar pruebas, generar capturas en el navegador y redactar la documentación técnica. Los integrantes deben ejecutar los ejemplos, explicar la lógica y practicar una modificación del AFD antes de la sustentación.
