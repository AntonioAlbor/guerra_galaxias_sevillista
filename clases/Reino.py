# Clase para reino

from clases.Nave import crear_nave, COSTE_NAVES
from clases.Mandaloriano import crear_mandaloriano, COSTE_MANDAS

LIMITE_CREDITOS = 100000  # limite dinero 


class Reino:
    # constructor crea el objeto e inicializa los valores
    def __init__(self, nombre):
        self.nombre        = nombre
        self.naves         = []
        self.mandalorianos = []
        self.coste_total   = 0

    # funcion para agregar las naves con tipo y cantidad para guardarlas en self.naves
    def agregar_naves(self, tipo, cantidad):
        for _ in range(cantidad):
            self.naves.append(crear_nave(tipo))
        self.coste_total += COSTE_NAVES[tipo] * cantidad

    # funcion para agregar los mandalorianos con tipo y cantidad para guardarlas en self.mandalorianos
    def agregar_mandalorianos(self, nivel, cantidad):
        for _ in range(cantidad):
            self.mandalorianos.append(crear_mandaloriano(nivel))
        self.coste_total += COSTE_MANDAS[nivel] * cantidad

    # funcion para filtrar las naves que siguen vivas
    def naves_vivas(self):
        return [n for n in self.naves if n.vivo]

    # funcion para filtrar los mandalorianos que siguen vivos
    def mandas_vivos(self):
        return [m for m in self.mandalorianos if m.vivo]

    # comprobacion para saber si aun quedan unidades
    def tiene_unidades(self):
        return len(self.naves_vivas()) > 0 or len(self.mandas_vivos()) > 0

    # comprobacion para no pasarse del limite de dinero
    def creditos_disponibles(self):
        return LIMITE_CREDITOS - self.coste_total
