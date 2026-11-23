"""Traducción de un AFD al lenguaje DOT para Viz.js."""


def _etiqueta(texto):
    # Los identificadores DOT son internos. Los nombres del usuario solo son etiquetas.
    return texto.replace("\\", "\\\\").replace('"', '\\"')


def generar_dot(afd, resultado=None):
    ids = {estado: f"n{indice}" for indice, estado in enumerate(afd.estados)}
    visitados = set()
    pasos_por_flecha = {}
    if resultado is not None:
        visitados.update(resultado.recorrido)
        # Una flecha puede aparecer varias veces en el mismo recorrido.
        for numero, (origen, _, destino) in enumerate(resultado.pasos, start=1):
            pasos_por_flecha.setdefault((origen, destino), []).append(str(numero))

    lineas = [
        "digraph AFD {",
        '  graph [rankdir=LR, bgcolor="transparent", pad=0.25, ranksep=0.85, nodesep=0.5];',
        '  node [fontname="Arial", fontsize=16, color="#526981", fontcolor="#182f3f", '
        'style=filled, fillcolor="#ffffff", width=0.58, penwidth=1.5];',
        '  edge [fontname="Arial", fontsize=13, arrowsize=0.72, color="#61758a", '
        'fontcolor="#314b62", penwidth=1.4];',
        '  inicio [shape=point, style=invis, width=0];',
    ]
    for estado in afd.estados:
        figura = "doublecircle" if estado in afd.estados_finales else "circle"
        color = ', fillcolor="#d4f4e8", color="#08745b", penwidth=2.5' if estado in visitados else ""
        lineas.append(f'  {ids[estado]} [label="{_etiqueta(estado)}", shape={figura}{color}];')
    lineas.append(f"  inicio -> {ids[afd.estado_inicial]};")

    # Juntamos los símbolos que tienen el mismo origen y destino.
    flechas = {}
    for origen in afd.estados:
        for simbolo in afd.alfabeto:
            destino = afd.transiciones[(origen, simbolo)]
            flechas.setdefault((origen, destino), []).append(simbolo)
    for (origen, destino), simbolos in flechas.items():
        etiqueta = _etiqueta(", ".join(simbolos))
        estilo = ""
        if (origen, destino) in pasos_por_flecha:
            numeros = ", ".join(pasos_por_flecha[(origen, destino)])
            etiqueta += f"\\nPasos: {numeros}"
            estilo = ', color="#08745b", fontcolor="#065641", penwidth=2.6'
        lineas.append(f'  {ids[origen]} -> {ids[destino]} [label="{etiqueta}"{estilo}];')
    lineas.append("}")
    return "\n".join(lineas)
