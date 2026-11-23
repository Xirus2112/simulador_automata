"""Datos temporales del asistente y conservación de sus transiciones."""

from dataclasses import dataclass, field

from afd.automata import AFD


@dataclass
class Borrador:
    nombre: str = ""
    estados: list[str] = field(default_factory=list)
    alfabeto: list[str] = field(default_factory=list)
    transiciones: dict[tuple[str, str], str] = field(default_factory=dict)
    inicial: str = ""
    finales: list[str] = field(default_factory=list)
    paso: int = 1
    modo: str = "nuevo"
    revisar_inicial: bool = False
    finales_eliminados: list[str] = field(default_factory=list)

    @classmethod
    def desde_afd(cls, afd, modo, paso=1):
        return cls(
            afd.nombre, afd.estados.copy(), afd.alfabeto.copy(),
            afd.transiciones.copy(), afd.estado_inicial, afd.estados_finales.copy(), paso, modo,
        )

    def ajustar_transiciones(self):
        # Al cambiar Q o Σ, conservamos las celdas que todavía se pueden usar.
        self.transiciones = {
            (origen, simbolo): destino
            for (origen, simbolo), destino in self.transiciones.items()
            if origen in self.estados and simbolo in self.alfabeto and destino in self.estados
        }
        if self.inicial and self.inicial not in self.estados:
            self.inicial = ""
            self.revisar_inicial = True
        for final in self.finales:
            if final not in self.estados and final not in self.finales_eliminados:
                self.finales_eliminados.append(final)
        self.finales = [final for final in self.finales if final in self.estados]

    def construir(self):
        return AFD(
            self.nombre, self.estados, self.alfabeto, self.transiciones, self.inicial, self.finales,
        )
