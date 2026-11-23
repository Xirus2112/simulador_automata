"""Validaciones compartidas por el formulario, los ejemplos y los archivos."""


class ErrorAFD(ValueError):
    """Un dato del autómata necesita corrección."""


def validar_nombre(nombre):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ErrorAFD("Ingrese un nombre para el autómata.")
    return nombre.strip()


def leer_lista(texto):
    """Separar por comas sin ocultar los elementos vacíos."""
    return texto.split(",")


def _validar_lista(valores, conjunto):
    if not isinstance(valores, list) or not valores:
        raise ErrorAFD(f"Ingrese al menos un elemento para {conjunto}.")
    # Quitamos espacios externos y dejamos los elementos en el orden de entrada.
    limpios = []
    for valor in valores:
        if not isinstance(valor, str) or not valor.strip():
            raise ErrorAFD(f"Hay un elemento vacío en {conjunto}. Revise las comas.")
        valor = valor.strip()
        if "," in valor or any(caracter.isspace() for caracter in valor):
            raise ErrorAFD(f"«{valor}» en {conjunto} contiene una coma o un espacio interno.")
        if valor in limpios:
            raise ErrorAFD(f"«{valor}» está repetido en {conjunto}.")
        limpios.append(valor)
    return limpios


def validar_estados(estados):
    return _validar_lista(estados, "Q")


def validar_alfabeto(alfabeto):
    simbolos = _validar_lista(alfabeto, "Σ")
    for simbolo in simbolos:
        if len(simbolo) != 1:
            raise ErrorAFD(f"«{simbolo}» no es válido. Cada símbolo debe tener un solo carácter.")
        if simbolo == "ε":
            raise ErrorAFD("ε representa la palabra vacía. Elija otro símbolo para Σ.")
    return simbolos


def validar_transiciones(estados, alfabeto, transiciones):
    # La tabla debe tener un destino para cada par de Q y Σ.
    esperadas = {(estado, simbolo) for estado in estados for simbolo in alfabeto}
    if not isinstance(transiciones, dict) or transiciones.keys() - esperadas:
        raise ErrorAFD("Las transiciones deben corresponder a estados de Q y símbolos de Σ.")
    for estado in estados:
        for simbolo in alfabeto:
            destino = transiciones.get((estado, simbolo))
            if not destino:
                raise ErrorAFD(f"Falta la transición δ({estado}, {simbolo}). Escriba su destino.")
            if destino not in estados:
                lista = ", ".join(estados)
                raise ErrorAFD(
                    f"Error en δ({estado}, {simbolo}). El estado «{destino}» "
                    f"no pertenece a Q = {{{lista}}}."
                )


def validar_inicial(estados, inicial):
    if inicial not in estados:
        raise ErrorAFD(f"El estado inicial «{inicial or 'sin seleccionar'}» no pertenece a Q.")


def validar_finales(estados, finales):
    if not isinstance(finales, list):
        raise ErrorAFD("F debe ser una lista de estados.")
    if any(final not in estados for final in finales):
        raise ErrorAFD("Todos los estados finales deben pertenecer a Q.")
    if len(dict.fromkeys(finales)) != len(finales):
        raise ErrorAFD("Hay estados finales repetidos en F.")
