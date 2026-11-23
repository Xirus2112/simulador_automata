from itertools import product

import pytest

from afd.automata import AFD
from afd.graph_dot import generar_dot
from afd.validator import ErrorAFD
from afd.word_generator import generar_palabras


@pytest.mark.parametrize("clave, palabra, acepta, recorrido", [
    ("A2", "abab", True, ["s0", "s1", "s2", "s1", "s2"]),
    ("A2", "aba", False, ["s0", "s1", "s2", "s1"]),
    ("A2", "bab", True, ["s0", "s0", "s1", "s2"]),
    ("A2", "bb", False, ["s0", "s0", "s0"]),
    ("A2", "", False, ["s0"]),
    ("A1", "0110", True, ["q0", "q1", "q1", "q1", "q0"]),
    ("A1", "1011", False, ["q0", "q0", "q1", "q1", "q1"]),
    ("A1", "", True, ["q0"]),
])
def test_reconocimiento(ejemplos, clave, palabra, acepta, recorrido):
    resultado = ejemplos[clave].procesar_palabra(palabra)
    assert resultado.aceptada is acepta
    assert resultado.recorrido == recorrido
    assert resultado.estado_actual == recorrido[-1]
    assert len(resultado.pasos) == len(palabra)


@pytest.mark.parametrize("palabra, simbolo, posicion, recorrido", [
    ("abc", "c", 3, ["s0", "s1", "s2"]),
    ("a b", " ", 2, ["s0", "s1"]),
    (" ab", " ", 1, ["s0"]),
    ("ab ", " ", 3, ["s0", "s1", "s2"]),
    ("ε", "ε", 1, ["s0"]),
])
def test_simbolo_invalido(ejemplos, palabra, simbolo, posicion, recorrido):
    resultado = ejemplos["A2"].procesar_palabra(palabra)
    assert not resultado.aceptada
    assert resultado.simbolo_invalido == simbolo
    assert resultado.posicion_invalida == posicion
    assert resultado.recorrido == recorrido


def test_definicion_afd():
    afd = AFD(" Nombre ", [" y ", "x"], ["b", "a"],
              {("y", "b"): "x", ("y", "a"): "y", ("x", "b"): "y", ("x", "a"): "x"},
              "y", ["x"])
    assert afd.nombre == "Nombre"
    assert afd.estados == ["y", "x"]
    assert afd.alfabeto == ["b", "a"]
    assert afd.transiciones[("y", "b")] == "x"
    assert AFD.desde_datos(afd.a_datos()).a_datos() == afd.a_datos()


@pytest.mark.parametrize("campo, valor, mensaje", [
    ("nombre", "", "nombre"),
    ("estados", [], "al menos un elemento"),
    ("estados", ["q0", ""], "vacío"),
    ("estados", ["q0", " q0 "], "repetido"),
    ("estados", ["q0", "q 1"], "espacio interno"),
    ("estados", ["q0", "q,1"], "coma"),
    ("alfabeto", [], "al menos un elemento"),
    ("alfabeto", ["a", "a"], "repetido"),
    ("alfabeto", ["a", ","], "coma"),
    ("alfabeto", ["a", " "], "vacío"),
    ("alfabeto", ["abc", "b"], "un solo carácter"),
    ("alfabeto", ["ε", "b"], "palabra vacía"),
    ("estado_inicial", "q5", "estado inicial"),
    ("estados_finales", ["q5"], "estados finales"),
    ("estados_finales", ["s2", "s2"], "repetidos"),
])
def test_validacion(ejemplos, campo, valor, mensaje):
    datos = ejemplos["A2"].a_datos()
    datos[campo] = valor
    with pytest.raises(ErrorAFD, match=mensaje):
        AFD.desde_datos(datos)


@pytest.mark.parametrize("cambio, mensaje", [
    ("faltante", "Falta la transición"),
    ("duplicada", "más de un destino"),
    ("destino", "no pertenece a Q"),
    ("origen", "deben corresponder"),
])
def test_transicion_completa(ejemplos, cambio, mensaje):
    datos = ejemplos["A2"].a_datos()
    filas = datos["transiciones"]
    if cambio == "faltante":
        filas.pop()
    elif cambio == "duplicada":
        filas.append(filas[0].copy())
    else:
        filas[0][cambio] = "q5"
    with pytest.raises(ErrorAFD, match=mensaje):
        AFD.desde_datos(datos)


@pytest.mark.parametrize("clave, esperadas", [
    ("A1", ["", "1", "00", "11", "001"]),
    ("A2", ["ab", "aab", "bab", "aaab", "abab"]),
    ("A3", ["ab", "ba"]),
    ("A4", []),
])
def test_generacion_oficial_y_fuerza_bruta(ejemplos, clave, esperadas):
    afd = ejemplos[clave]
    bruta = []
    for longitud in range(11):
        for letras in product(afd.alfabeto, repeat=longitud):
            palabra = "".join(letras)
            if afd.es_aceptada(palabra):
                bruta.append(palabra)
    resultados = generar_palabras(afd)
    assert [resultado.palabra for resultado in resultados] == bruta[:5] == esperadas
    assert all(resultado == afd.procesar_palabra(resultado.palabra) for resultado in resultados)


def test_orden_de_alfabeto():
    afd = AFD("Todo", ["q"], ["b", "a"], {("q", "a"): "q", ("q", "b"): "q"}, "q", ["q"])
    assert [r.palabra for r in generar_palabras(afd)] == ["", "b", "a", "bb", "ba"]


def test_alfabeto_grande_con_camino_largo():
    estados = [str(i) for i in range(11)]
    simbolos = list("abcde")
    delta = {(q, s): "0" for q in estados for s in simbolos}
    for i in range(10):
        delta[(estados[i], "e")] = estados[i + 1]
    afd = AFD("Cadena", estados, simbolos, delta, "0", ["10"])
    assert [r.palabra for r in generar_palabras(afd)] == ["e" * 10]
    assert generar_palabras(afd, longitud_maxima=9) == []


def test_alcanzables_y_f_vacio(ejemplos):
    afd = ejemplos["A4"]
    assert afd.estados_alcanzables() == ["q0"]
    datos = afd.a_datos()
    datos["estados_finales"] = []
    sin_finales = AFD.desde_datos(datos)
    assert generar_palabras(sin_finales) == []
    assert not sin_finales.es_aceptada("")


def test_dot_agrupa_y_numera(ejemplos):
    dot_a3 = generar_dot(ejemplos["A3"])
    assert 'n3 -> n4 [label="a, b"]' in dot_a3
    assert 'n4 -> n4 [label="a, b"]' in dot_a3
    afd = ejemplos["A2"]
    dot_a2 = generar_dot(afd, afd.procesar_palabra("abab"))
    assert "inicio -> n0" in dot_a2 and "shape=doublecircle" in dot_a2
    assert 'n1 -> n2 [label="b\\nPasos: 2, 4"' in dot_a2
    assert 'n2 -> n1 [label="a\\nPasos: 3"' in dot_a2
