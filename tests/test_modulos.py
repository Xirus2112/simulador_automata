from io import BytesIO

import pytest


@pytest.mark.parametrize("ruta", ["/automata", "/modulo-2", "/modulo-3"])
def test_aviso_sin_afd(cliente, ruta):
    respuesta = cliente.get(ruta)
    assert respuesta.status_code == 200
    assert "Aún no hay un autómata construido" in respuesta.text
    assert 'href="/nuevo">Ir al Módulo 1' in respuesta.text


def enviar_paso(cliente, numero, datos):
    respuesta = cliente.post(f"/construir/{numero}", data=datos)
    assert respuesta.location == f"/construir/{numero + 1}"


def test_crear_validar_y_activar(cliente):
    assert "Sin autómata activo" in cliente.get("/").text
    assert cliente.get("/nuevo").location == "/construir/1"
    enviar_paso(cliente, 1, {"nombre": "Binario de prueba"})
    fallo = cliente.post("/construir/2", data={"estados": "z, z"}).text
    assert "está repetido en Q" in fallo and 'value="z, z"' in fallo
    enviar_paso(cliente, 2, {"estados": "z, u"})
    enviar_paso(cliente, 3, {"alfabeto": "1, 0"})
    destinos = {"delta_0_0": "u", "delta_0_1": "z", "delta_1_0": "z", "delta_1_1": "u"}
    fallo = cliente.post("/construir/4", data={**destinos, "delta_0_1": "q5"}).text
    assert "Error en δ(z, 0)" in fallo and 'value="q5"' in fallo
    assert 'name="delta_1_0" value="z"' in fallo
    enviar_paso(cliente, 4, destinos)
    enviar_paso(cliente, 5, {"inicial": "z"})
    enviar_paso(cliente, 6, {"finales": "u"})
    revision = cliente.get("/construir/7").text
    assert "M = ({z, u}, {1, 0}, δ, z, {u})" in revision
    assert "Sin autómata activo" in revision
    activado = cliente.post("/construir/7", follow_redirects=True).text
    assert "Binario de prueba" in activado
    assert "Diagrama de estados" in activado


def test_editar_y_regenerar_tabla(cliente):
    cliente.post("/ejemplos", data={"ejemplo": "A2"})
    cliente.post("/editar")
    enviar_paso(cliente, 1, {"nombre": "A2 editado"})
    enviar_paso(cliente, 2, {"estados": "s0, s2, s3"})
    enviar_paso(cliente, 3, {"alfabeto": "b, c"})
    tabla = cliente.get("/construir/4").text
    assert 'name="delta_0_0" value="s0"' in tabla
    assert 'name="delta_1_0" value="s0"' in tabla
    assert 'name="delta_0_1" value=""' in tabla
    assert 'name="delta_2_0" value=""' in tabla
    assert tabla.count('class="pendiente"') == 4
    assert 'name="delta_1_1" value=""' in tabla
    enviar_paso(cliente, 4, {"delta_0_0": "s0", "delta_0_1": "s2", "delta_1_0": "s0",
                              "delta_1_1": "s0", "delta_2_0": "s3", "delta_2_1": "s3"})
    assert 'value="s0" selected' in cliente.get("/construir/5").text
    enviar_paso(cliente, 5, {"inicial": "s0"})
    assert 'value="s2" checked' in cliente.get("/construir/6").text
    enviar_paso(cliente, 6, {"finales": "s2"})
    cliente.post("/construir/7")
    assert "M = ({s0, s2, s3}, {b, c}, δ, s0, {s2})" in cliente.get("/automata").text
    assert '<code class="palabra">c</code>' in cliente.get("/modulo-2").text


def test_edicion_pide_inicial_y_finales_eliminados(cliente):
    cliente.post("/ejemplos", data={"ejemplo": "A2"})
    cliente.post("/editar")
    enviar_paso(cliente, 1, {"nombre": "Otro A2"})
    enviar_paso(cliente, 2, {"estados": "s1"})
    enviar_paso(cliente, 3, {"alfabeto": "a, b"})
    tabla = cliente.get("/construir/4").text
    assert 'name="delta_0_0" value="s1"' in tabla
    assert 'name="delta_0_1" value=""' in tabla
    enviar_paso(cliente, 4, {"delta_0_0": "s1", "delta_0_1": "s1"})
    assert "El estado inicial anterior fue eliminado" in cliente.get("/construir/5").text
    enviar_paso(cliente, 5, {"inicial": "s1"})
    finales = cliente.get("/construir/6").text
    assert "Se eliminaron de Q los estados finales s2" in finales
    assert "No se han definido estados finales" in finales
    enviar_paso(cliente, 6, {})
    cliente.post("/construir/7")
    assert "No se definieron estados finales" in cliente.get("/modulo-2").text


def test_modulos_siguen_activo_y_limpian_historial(cliente):
    cliente.post("/ejemplos", data={"ejemplo": "A2"})
    respuesta = cliente.post("/modulo-3", data={"palabra": "abab"}, follow_redirects=True)
    assert "✓ Palabra reconocida" in respuesta.text and "Recorrido en la gráfica" in respuesta.text
    assert "Historial de palabras" in respuesta.text
    assert "¿Desea crear un nuevo autómata?" in cliente.get("/nuevo").text
    cliente.post("/nuevo")
    assert "A2 - Termina en ab" in cliente.get("/modulo-2").text
    cliente.post("/ejemplos", data={"ejemplo": "A4"})
    assert "Ningún estado final es alcanzable" in cliente.get("/modulo-2").text
    assert "Historial de palabras" not in cliente.get("/modulo-3").text
    assert "Σ = {a}" in cliente.get("/modulo-3").text


def test_epsilon_y_error_en_interfaz(cliente):
    cliente.post("/ejemplos", data={"ejemplo": "A1"})
    pagina = cliente.post("/modulo-3", data={"palabra": ""}, follow_redirects=True).text
    assert '<code class="palabra">ε</code>' in pagina and "✓ Palabra reconocida" in pagina
    cliente.post("/ejemplos", data={"ejemplo": "A2"})
    pagina = cliente.post("/modulo-3", data={"palabra": "abc"}, follow_redirects=True).text
    assert "El símbolo «c», ubicado en la posición 3" in pagina
    assert "✗ Palabra no reconocida" in pagina


def test_importar_exportar_json(cliente):
    cliente.post("/ejemplos", data={"ejemplo": "A2"})
    archivo = cliente.get("/descargar")
    assert archivo.is_json and "attachment" in archivo.headers["Content-Disposition"]
    cliente.post("/ejemplos", data={"ejemplo": "A1"})
    malo = cliente.post("/cargar", data={"archivo": (BytesIO(b"{n"), "invalido.json")})
    assert malo.status_code == 400 and "JSON válido" in malo.text
    assert "A1 - Número par de ceros" in cliente.get("/automata").text
    cargado = cliente.post("/cargar", data={"archivo": (BytesIO(archivo.data), "afd.json")})
    assert cargado.location == "/construir/7"
    assert "Revisar autómata importado" in cliente.get(cargado.location).text
    cliente.post(cargado.location)
    assert cliente.get("/descargar").json == archivo.json
