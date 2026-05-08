# Clase para nave
# 5 niveles

class Nave:
    def __init__(self, tipo, ataque, defensa, vida, velocidad, coste):
        self.tipo      = tipo
        self.ataque    = ataque
        self.defensa   = defensa
        self.vida      = vida
        self.vida_max  = vida
        self.velocidad = velocidad
        self.coste     = coste
        self.vivo      = True

    # funcion que al ser llamada resta vida a la Nave en base al daño que recibe si llega a 0 muere
    def recibir_daño_nave(self, danio):
        self.vida -= danio
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False

    # funcion que devuelve la info del objeto en string cada vez que se hace un print
    def __str__(self):
        return f"{self.tipo} (vida {self.vida}/{self.vida_max})"


# funcion que automatiza el proceso de crear una nave, si es de nivel 1 le asignará los stats de nivel 1 solo
def crear_nave(tipo):
    datos = {
        1: ("Estrella de la Muerte", 80, 90, 1500, 25, 4500),
        2: ("Ejecutor",              70, 80, 1200, 42, 4000),
        3: ("Halcon Milenario",      60, 50,  800, 70, 2500),
        4: ("Nave Real de Naboo",    40, 60,  600, 50, 2000),
        5: ("Caza Estelar Jedi",     50, 40,  400, 80, 1500),
    }
    if tipo not in datos:
        return None
    nombre, atq, dfs, vid, vel, cos = datos[tipo]
    return Nave(nombre, atq, dfs, vid, vel, cos)


# diccionarios con los costes y nombres para usarlos desde el servidor
COSTE_NAVES = {1: 4500, 2: 4000, 3: 2500, 4: 2000, 5: 1500}
NOMBRES_NAVES = {
    1: "Estrella de la Muerte",
    2: "Ejecutor",
    3: "Halcon Milenario",
    4: "Nave Real de Naboo",
    5: "Caza Estelar Jedi",
}
