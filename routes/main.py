"""Recibe los formularios y presenta los resultados del AFD activo."""

import json
from pathlib import Path
from secrets import token_hex

from flask import Blueprint, Response, current_app, redirect, render_template, request, session, url_for

from afd import estado_app, validator
from afd.automata import AFD
from afd.graph_dot import generar_dot
from afd.validator import ErrorAFD
from afd.word_generator import generar_palabras
from routes.borrador import Borrador

rutas = Blueprint("main", __name__)
PASOS = ("Nombre", "Estados Q", "Alfabeto Σ", "Transiciones δ", "Estado inicial q₀", "Estados finales F", "Resumen")
ARCHIVO_EJEMPLOS = Path(__file__).resolve().parents[1] / "ejemplos" / "ejemplos.json"


@rutas.app_context_processor
def contexto_comun():
    return {"activo": estado_app.obtener_afd_activo()}


def _ejemplos():
    return json.loads(ARCHIVO_EJEMPLOS.read_text(encoding="utf-8"))


def _sin_afd():
    return render_template("aviso.html", mensaje="Aún no hay un autómata construido. Primero debe pasar por el Módulo 1.")


@rutas.get("/")
def inicio():
    return render_template("index.html", ejemplos=_ejemplos())


def _borradores():
    return current_app.extensions["borradores"]


def _descartar_borrador():
    _borradores().pop(session.pop("borrador", None), None)


def _iniciar_borrador(datos):
    _descartar_borrador()
    identificador = token_hex(16)
    # En la cookie guardamos el identificador. La tabla puede ser grande.
    session["borrador"] = identificador
    _borradores()[identificador] = datos
    return redirect(url_for("main.construir", paso=datos.paso))


@rutas.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "GET" and estado_app.obtener_afd_activo() is not None:
        return render_template("nuevo.html")
    if request.method == "GET":
        datos = _borradores().get(session.get("borrador"))
        if datos is not None:
            return redirect(url_for("main.construir", paso=datos.paso))
        # Entrar al Módulo 1 por GET solo abre el primer paso del formulario.
    return _iniciar_borrador(Borrador())


@rutas.post("/editar")
def editar():
    afd = estado_app.obtener_afd_activo()
    if afd is None:
        return _sin_afd()
    return _iniciar_borrador(Borrador.desde_afd(afd, "edición"))


@rutas.post("/cancelar")
def cancelar():
    _descartar_borrador()
    return redirect(url_for("main.inicio"))


def _guardar_paso(datos, paso, form, entradas):
    if paso == 1:
        entradas["texto"] = form.get("nombre", "")
        datos.nombre = validator.validar_nombre(entradas["texto"])
    elif paso == 2:
        entradas["texto"] = form.get("estados", "")
        datos.estados = validator.validar_estados(validator.leer_lista(entradas["texto"]))
        datos.ajustar_transiciones()
    elif paso == 3:
        entradas["texto"] = form.get("alfabeto", "")
        datos.alfabeto = validator.validar_alfabeto(validator.leer_lista(entradas["texto"]))
        datos.ajustar_transiciones()
    elif paso == 4:
        # Los nombres de los campos llevan la fila y la columna de la tabla.
        entradas["transiciones"] = {
            (estado, simbolo): form.get(f"delta_{i}_{j}", "").strip()
            for i, estado in enumerate(datos.estados)
            for j, simbolo in enumerate(datos.alfabeto)
        }
        validator.validar_transiciones(datos.estados, datos.alfabeto, entradas["transiciones"])
        datos.transiciones = entradas["transiciones"]
    elif paso == 5:
        entradas["inicial"] = form.get("inicial", "")
        validator.validar_inicial(datos.estados, entradas["inicial"])
        datos.inicial = entradas["inicial"]
        datos.revisar_inicial = False
    elif paso == 6:
        entradas["finales"] = form.getlist("finales")
        validator.validar_finales(datos.estados, entradas["finales"])
        datos.finales = [estado for estado in datos.estados if estado in entradas["finales"]]
        datos.finales_eliminados.clear()


@rutas.route("/construir/<int:paso>", methods=["GET", "POST"])
def construir(paso):
    datos = _borradores().get(session.get("borrador"))
    if datos is None:
        return redirect(url_for("main.nuevo"))
    if not 1 <= paso <= datos.paso:
        return redirect(url_for("main.construir", paso=datos.paso))

    entradas = {}
    error = None
    resumen = None
    try:
        if paso == len(PASOS):
            resumen = datos.construir()
            if request.method == "POST":
                # Confirmar el resumen es el paso que reemplaza el AFD activo.
                estado_app.activar_afd(resumen)
                _descartar_borrador()
                return redirect(url_for("main.automata"))
        elif request.method == "POST":
            _guardar_paso(datos, paso, request.form, entradas)
            datos.paso = paso + 1
            return redirect(url_for("main.construir", paso=datos.paso))
    except ErrorAFD as exc:
        error = str(exc)

    return render_template(
        "construir.html", datos=datos, paso=paso, pasos=PASOS, entradas=entradas,
        error=error, resumen=resumen,
    )


@rutas.get("/automata")
def automata():
    afd = estado_app.obtener_afd_activo()
    if afd is None:
        return _sin_afd()
    return render_template("automata.html", afd=afd, dot=generar_dot(afd), alcanzables=afd.estados_alcanzables())


@rutas.get("/modulo-2")
def modulo2():
    afd = estado_app.obtener_afd_activo()
    if afd is None:
        return _sin_afd()
    resultados = generar_palabras(afd)
    return render_template(
        "modulo2.html", afd=afd, resultados=resultados, alcanzables=afd.estados_alcanzables(),
    )


@rutas.route("/modulo-3", methods=["GET", "POST"])
def modulo3():
    afd = estado_app.obtener_afd_activo()
    if afd is None:
        return _sin_afd()
    mostrar_resultado = request.args.get("resultado") == "ultimo"
    if request.method == "POST":
        resultado = afd.procesar_palabra(request.form.get("palabra", ""))
        estado_app.historial.append(resultado)
        # Redirigimos para que al recargar la página no se repita el intento.
        return redirect(url_for("main.modulo3", resultado="ultimo"))
    resultado = estado_app.historial[-1] if mostrar_resultado and estado_app.historial else None
    dot = generar_dot(afd, resultado) if resultado and resultado.simbolo_invalido is None else None
    return render_template(
        "modulo3.html", afd=afd, resultado=resultado, dot=dot, historial=estado_app.historial,
    )


@rutas.post("/ejemplos")
def cargar_ejemplo():
    datos = _ejemplos().get(request.form.get("ejemplo"))
    if datos is None:
        return render_template("index.html", ejemplos=_ejemplos(), error="Seleccione un ejemplo de la lista."), 400
    estado_app.activar_afd(AFD.desde_datos(datos))
    _descartar_borrador()
    return redirect(url_for("main.automata"))


@rutas.get("/descargar")
def descargar():
    afd = estado_app.obtener_afd_activo()
    if afd is None:
        return _sin_afd()
    contenido = json.dumps(afd.a_datos(), ensure_ascii=False, indent=2) + "\n"
    return Response(
        contenido, mimetype="application/json",
        headers={"Content-Disposition": 'attachment; filename="automata.json"'},
    )


@rutas.post("/cargar")
def cargar_archivo():
    archivo = request.files.get("archivo")
    try:
        if not archivo or not archivo.filename:
            raise ErrorAFD("Seleccione un archivo JSON.")
        afd = AFD.desde_datos(json.load(archivo))
    except (json.JSONDecodeError, UnicodeDecodeError, RecursionError):
        error = "El archivo no contiene JSON válido."
    except ErrorAFD as exc:
        error = str(exc)
    else:
        return _iniciar_borrador(Borrador.desde_afd(afd, "archivo", paso=len(PASOS)))
    return render_template("index.html", ejemplos=_ejemplos(), error=error), 400
