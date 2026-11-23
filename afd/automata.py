"""Representación de la 5-tupla y recorrido de una palabra."""

from collections import deque
from dataclasses import dataclass

from afd import validator


@dataclass
class Resultado:
    palabra: str
    recorrido: list[str]
    pasos: list[tuple[str, str, str]]
    aceptada: bool = False
    simbolo_invalido: str | None = None
    posicion_invalida: int | None = None

    @property
    def estado_actual(self):
        return self.recorrido[-1]


class AFD:
    def __init__(self, nombre, estados, alfabeto, transiciones, estado_inicial, estados_finales):
        self.nombre = validator.validar_nombre(nombre)
        self.estados = validator.validar_estados(estados)
        self.alfabeto = validator.validar_alfabeto(alfabeto)
        validator.validar_transiciones(self.estados, self.alfabeto, transiciones)
        validator.validar_inicial(self.estados, estado_inicial)
        validator.validar_finales(self.estados, estados_finales)
        self.transiciones = transiciones.copy()
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales.copy()

    def procesar_palabra(self, palabra):
        actual = self.estado_inicial
        # El recorrido empieza en q0, incluso cuando la palabra está vacía.
        resultado = Resultado(palabra, [actual], [])
        for posicion, simbolo in enumerate(palabra, start=1):
            if simbolo not in self.alfabeto:
                resultado.simbolo_invalido = simbolo
                resultado.posicion_invalida = posicion
                return resultado
            # Buscamos en la fila del estado actual y la columna del símbolo.
            siguiente = self.transiciones[(actual, simbolo)]
            resultado.pasos.append((actual, simbolo, siguiente))
            resultado.recorrido.append(siguiente)
            actual = siguiente
        resultado.aceptada = actual in self.estados_finales
        return resultado

    def es_aceptada(self, palabra):
        return self.procesar_palabra(palabra).aceptada

    def estados_alcanzables(self):
        """BFS desde q0; devolver el resultado en el orden de Q."""
        visitados = {self.estado_inicial}
        pendientes = deque([self.estado_inicial])
        while pendientes:
            actual = pendientes.popleft()
            for simbolo in self.alfabeto:
                destino = self.transiciones[(actual, simbolo)]
                # Si hay un bucle, el estado ya visitado queda fuera de la cola.
                if destino not in visitados:
                    visitados.add(destino)
                    pendientes.append(destino)
        return [estado for estado in self.estados if estado in visitados]

    def a_datos(self):
        # JSON no permite tuplas como claves. Guardamos una fila por transición.
        return {
            "nombre": self.nombre,
            "estados": self.estados.copy(),
            "alfabeto": self.alfabeto.copy(),
            "estado_inicial": self.estado_inicial,
            "estados_finales": self.estados_finales.copy(),
            "transiciones": [
                {"origen": origen, "simbolo": simbolo, "destino": destino}
                for (origen, simbolo), destino in self.transiciones.items()
            ],
        }

    @classmethod
    def desde_datos(cls, datos):
        """Convertir una lista JSON de transiciones a pares (estado, símbolo)."""
        try:
            filas = datos["transiciones"]
            if not isinstance(filas, list):
                raise TypeError
            transiciones = {}
            for fila in filas:
                origen, simbolo, destino = (fila[campo] for campo in ("origen", "simbolo", "destino"))
                if not all(isinstance(valor, str) for valor in (origen, simbolo, destino)):
                    raise TypeError
                par = (origen, simbolo)
                if par in transiciones:
                    raise validator.ErrorAFD(f"Hay más de un destino para δ({origen}, {simbolo}).")
                transiciones[par] = destino
            return cls(
                datos["nombre"], datos["estados"], datos["alfabeto"], transiciones,
                datos["estado_inicial"], datos["estados_finales"],
            )
        except (KeyError, TypeError):
            raise validator.ErrorAFD("El JSON debe usar el formato de un AFD exportado.") from None
