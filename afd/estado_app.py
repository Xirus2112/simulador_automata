"""Estado compartido del simulador local durante la ejecución."""

afd_activo = None
historial = []


def obtener_afd_activo():
    return afd_activo


def activar_afd(nuevo_afd):
    global afd_activo
    afd_activo = nuevo_afd
    # Las pruebas anteriores se hicieron con la definición que estaba activa.
    historial.clear()
