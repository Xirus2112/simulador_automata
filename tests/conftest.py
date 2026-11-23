import json
from pathlib import Path

import pytest

from afd import estado_app
from afd.automata import AFD
from app import crear_app


@pytest.fixture(scope="session")
def ejemplos():
    archivo = Path(__file__).resolve().parents[1] / "ejemplos" / "ejemplos.json"
    datos = json.loads(archivo.read_text(encoding="utf-8"))
    return {clave: AFD.desde_datos(afd) for clave, afd in datos.items()}


@pytest.fixture
def cliente():
    estado_app.activar_afd(None)
    app = crear_app()
    app.config["TESTING"] = True
    with app.test_client() as cliente:
        yield cliente
    estado_app.activar_afd(None)
