"""Enumeración en el orden longitud-lexicográfico de Σ."""

from collections import deque


def estados_que_llegan_a_final(afd):
    # Invertimos las flechas para buscar desde F qué estados pueden llegar allí.
    anteriores = {estado: [] for estado in afd.estados}
    for (origen, _), destino in afd.transiciones.items():
        anteriores[destino].append(origen)

    utiles = set(afd.estados_finales)
    pendientes = deque(afd.estados_finales)
    while pendientes:
        actual = pendientes.popleft()
        for origen in anteriores[actual]:
            if origen not in utiles:
                utiles.add(origen)
                pendientes.append(origen)
    return utiles


def generar_palabras(afd, cantidad=5, longitud_maxima=10):
    utiles = estados_que_llegan_a_final(afd)
    if afd.estado_inicial not in utiles or cantidad <= 0:
        return []

    # posibles[n] contiene los estados que llegan a F en exactamente n pasos.
    posibles = [set(afd.estados_finales)]
    for longitud in range(1, longitud_maxima + 1):
        posibles.append({
            estado for estado in utiles
            if any(
                afd.transiciones[(estado, simbolo)] in posibles[longitud - 1]
                for simbolo in afd.alfabeto
            )
        })

    def palabras_del_nivel(prefijo, estado, faltan):
        if faltan == 0:
            yield prefijo
            return
        for simbolo in afd.alfabeto:
            destino = afd.transiciones[(estado, simbolo)]
            # Extendemos el prefijo solo si todavía puede llegar a F a tiempo.
            if destino in posibles[faltan - 1]:
                yield from palabras_del_nivel(prefijo + simbolo, destino, faltan - 1)

    encontradas = []
    for longitud in range(longitud_maxima + 1):
        if afd.estado_inicial not in posibles[longitud]:
            continue
        for palabra in palabras_del_nivel("", afd.estado_inicial, longitud):
            # El Módulo 3 usa esta misma función para probar una palabra.
            resultado = afd.procesar_palabra(palabra)
            if resultado.aceptada:
                encontradas.append(resultado)
                if len(encontradas) == cantidad:
                    return encontradas
    return encontradas
