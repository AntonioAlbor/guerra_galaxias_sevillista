# Clase para los mandalorianos
# 5 niveles y cada uno es mas caro y mas tocho

class Mandaloriano:
    def __init__(self, nivel, ataque, defensa, vida, velocidad, coste):
        self.nivel     = nivel
        self.tipo      = f"Mandaloriano {nivel}"
        self.ataque    = ataque
        self.defensa   = defensa
        self.vida      = vida
        self.vida_max  = vida
        self.velocidad = velocidad
        self.coste     = coste
        self.vivo      = True

    # funcion que al ser llamada resta vida al Mandaloriano en base al daño que recibe si llega a 0 muere
    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False

    # funcion que devuelve la info del objeto en string cada vez que se hace un print
    def __str__(self):
        return f"{self.tipo} (vida {self.vida}/{self.vida_max})"

# funcion que automatiza el proceso de crear un mandaloriano, si es de nivel 1 le asignará los stats de nivel 1 solo
def crear_mandaloriano(nivel):
    # nivel, ataque, defensa, vida, velocidad, coste
    datos = {
        1: (1, 20, 15, 100, 60,  800),
        2: (2, 25, 20, 120, 50, 1000),
        3: (3, 30, 25, 140, 40, 1200),
        4: (4, 35, 30, 160, 30, 1500),
        5: (5, 40, 35, 180, 20, 2000),
    }
    if nivel not in datos:
        return None
    n, atq, dfs, vid, vel, cos = datos[nivel]
    return Mandaloriano(n, atq, dfs, vid, vel, cos)


# Al crear un mandaloriano asigna ese nivel a un nombre completo, Mandaloriano de nivel 1 seria "Mandaloriano 1"
COSTE_MANDAS = {1: 800, 2: 1000, 3: 1200, 4: 1500, 5: 2000}
NOMBRES_MANDAS = {
    1: "Mandaloriano 1",
    2: "Mandaloriano 2",
    3: "Mandaloriano 3",
    4: "Mandaloriano 4",
    5: "Mandaloriano 5",
}
