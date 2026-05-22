# servidor principal del juego

import socket
import random
import sys
import time

from clases.Nave import COSTE_NAVES, NOMBRES_NAVES
from clases.Mandaloriano import COSTE_MANDAS, NOMBRES_MANDAS
from clases.Reino import Reino, LIMITE_CREDITOS

HOST = 'localhost'
PORT = 65432

# cuando el servidor manda esto el cliente sabe que tiene que escribir algo
PIDE_INPUT = "<INPUT>"


# funcion que manda un mensaje al cliente, si falla no hace nada para que no pete el servidor
def enviar(conn, mensaje):
    try:
        conn.sendall((mensaje + "\n").encode('utf-8'))
    except Exception:
        pass


# funcion que manda una pregunta al cliente y espera que conteste
def pedir(conn, mensaje):
    try:
        conn.sendall((mensaje + "\n" + PIDE_INPUT + "\n").encode('utf-8'))
        respuesta = conn.recv(1024).decode('utf-8').strip()
        return respuesta
    except Exception:
        return ""


# igual que pedir pero comprueba que lo que manda el cliente sea un numero entero valido
def pedir_numero(conn, mensaje, minimo=0):
    while True:
        respuesta = pedir(conn, mensaje)
        try:
            numero = int(respuesta)
            if numero >= minimo:
                return numero
            else:
                enviar(conn, f"tiene que ser {minimo} o mas, prueba de nuevo")
        except ValueError:
            enviar(conn, "eso no es un numero valido, intenta otra vez")


# funcion que le pregunta al cliente cuantas naves y mandalorianos quiere y monta su reino
def configurar_reino(conn, numero):
    enviar(conn, f"\n========================================")
    enviar(conn, f" CONFIGURACION REINO {numero}")
    enviar(conn, f"========================================")

    nombre = pedir(conn, "nombre de tu Reino:")
    reino  = Reino(nombre)

    # primero elegimos las naves
    enviar(conn, "\n--- FLOTA DE NAVES ---")
    enviar(conn, "1. Estrella de la Muerte  | ataque:80  defensa:90  vida:1500  coste:4500")
    enviar(conn, "2. Ejecutor               | ataque:70  defensa:80  vida:1200  coste:4000")
    enviar(conn, "3. Halcon Milenario        | ataque:60  defensa:50  vida:800   coste:2500")
    enviar(conn, "4. Nave Real de Naboo      | ataque:40  defensa:60  vida:600   coste:2000")
    enviar(conn, "5. Caza Estelar Jedi       | ataque:50  defensa:40  vida:400   coste:1500")

    for tipo in range(1, 6):
        while True:
            disponibles = reino.creditos_disponibles()
            msg = (f"cuantas {NOMBRES_NAVES[tipo]} quieres? "
                   f"(coste {COSTE_NAVES[tipo]} c/u | creditos restantes: {disponibles})")
            cantidad = pedir_numero(conn, msg, 0)

            # comprobamos que no se pase del presupuesto antes de añadir
            if COSTE_NAVES[tipo] * cantidad > disponibles:
                maximo = disponibles // COSTE_NAVES[tipo]
                enviar(conn, f"no alcanza el presupuesto, puedes poner como mucho {maximo}")
            else:
                reino.agregar_naves(tipo, cantidad)
                enviar(conn, f"ok! creditos gastados: {reino.coste_total} / {LIMITE_CREDITOS}")
                break

    # ahora los mandalorianos
    enviar(conn, "\n--- LEGION DE MANDALORIANOS ---")
    enviar(conn, "1. Mandaloriano 1 | ataque:20  defensa:15  vida:100  coste:800")
    enviar(conn, "2. Mandaloriano 2 | ataque:25  defensa:20  vida:120  coste:1000")
    enviar(conn, "3. Mandaloriano 3 | ataque:30  defensa:25  vida:140  coste:1200")
    enviar(conn, "4. Mandaloriano 4 | ataque:35  defensa:30  vida:160  coste:1500")
    enviar(conn, "5. Mandaloriano 5 | ataque:40  defensa:35  vida:180  coste:2000")

    for nivel in range(1, 6):
        while True:
            disponibles = reino.creditos_disponibles()
            msg = (f"cuantos {NOMBRES_MANDAS[nivel]} quieres? "
                   f"(coste {COSTE_MANDAS[nivel]} c/u | creditos restantes: {disponibles})")
            cantidad = pedir_numero(conn, msg, 0)

            if COSTE_MANDAS[nivel] * cantidad > disponibles:
                maximo = disponibles // COSTE_MANDAS[nivel]
                enviar(conn, f"no alcanza el presupuesto, puedes poner como mucho {maximo}")
            else:
                reino.agregar_mandalorianos(nivel, cantidad)
                enviar(conn, f"ok! creditos gastados: {reino.coste_total} / {LIMITE_CREDITOS}")
                break

    enviar(conn, f"\nconfiguracion lista!")
    enviar(conn, f"reino '{reino.nombre}' | naves: {len(reino.naves)} | mandalorianos: {len(reino.mandalorianos)} | coste: {reino.coste_total} creditos")
    enviar(conn, "esperando al otro reino...")

    return reino


# formula del daño: ataque menos un tercio de la defensa mas algo de aleatoriedad
# el minimo es 5 para que la batalla siempre avance y no se quede colgada
def calcular_daño(atacante, defensor):
    base = atacante.ataque - (defensor.defensa // 3)
    base += random.randint(-5, 15)
    return max(5, base)


# funcion principal de la batalla, cada unidad ataca una vez por turno a un enemigo al azar
# si un ejercito tiene mas unidades lanza mas ataques ese turno, lo que da ventaja en cantidad
def simular_batalla(conn1, conn2, reino1, reino2):

    # funcion auxiliar para no repetir el enviar dos veces cada vez
    def a_todos(msg):
        enviar(conn1, msg)
        enviar(conn2, msg)

    a_todos(f"\n=== BATALLA: {reino1.nombre} vs {reino2.nombre} ===")

    turno      = 1
    max_turnos = 100  # limite por si la batalla se alarga demasiado

    while reino1.tiene_unidades() and reino2.tiene_unidades() and turno <= max_turnos:

        a_todos(f"\n--- TURNO {turno} ---")
        a_todos(f"  {reino1.nombre}: {len(reino1.naves_vivas())} naves | {len(reino1.mandas_vivos())} mandas")
        a_todos(f"  {reino2.nombre}: {len(reino2.naves_vivas())} naves | {len(reino2.mandas_vivos())} mandas")

        a_todos("  combates:")

        # cada unidad de reino1 ataca una vez a un enemigo al azar
        for atacante in reino1.naves_vivas() + reino1.mandas_vivos():
            objetivos2 = reino2.naves_vivas() + reino2.mandas_vivos()
            if not objetivos2:
                break
            defensor = random.choice(objetivos2)
            daño = calcular_daño(atacante, defensor)
            if hasattr(defensor, 'recibir_daño_nave'):
                defensor.recibir_daño_nave(daño)
            else:
                defensor.recibir_daño(daño)

            estado = f"vida: {defensor.vida}/{defensor.vida_max}" if defensor.vivo else "DESTRUIDO"
            a_todos(f"    {atacante.tipo} ({reino1.nombre}) -> {defensor.tipo} ({reino2.nombre}) | daño: {daño} | {estado}")

        # cada unidad de reino2 ataca una vez a un enemigo al azar
        for atacante in reino2.naves_vivas() + reino2.mandas_vivos():
            objetivos1 = reino1.naves_vivas() + reino1.mandas_vivos()
            if not objetivos1:
                break
            defensor = random.choice(objetivos1)
            daño = calcular_daño(atacante, defensor)
            if hasattr(defensor, 'recibir_daño_nave'):
                defensor.recibir_daño_nave(daño)
            else:
                defensor.recibir_daño(daño)

            estado = f"vida: {defensor.vida}/{defensor.vida_max}" if defensor.vivo else "DESTRUIDO"
            a_todos(f"    {atacante.tipo} ({reino2.nombre}) -> {defensor.tipo} ({reino1.nombre}) | daño: {daño} | {estado}")

        turno += 1
        time.sleep(0.3)  # pausa pequeña para que se pueda leer algo

    a_todos("\n=== RESULTADO FINAL ===")
    a_todos(f"{reino1.nombre}: {len(reino1.naves_vivas())} naves | {len(reino1.mandas_vivos())} mandas sobrevivientes")
    a_todos(f"{reino2.nombre}: {len(reino2.naves_vivas())} naves | {len(reino2.mandas_vivos())} mandas sobrevivientes")
    a_todos(f"duracion: {turno - 1} turnos")

    if not reino1.tiene_unidades() and not reino2.tiene_unidades():
        a_todos("\nEMPATE, los dos reinos han sido destruidos")
    elif not reino2.tiene_unidades():
        a_todos(f"\nGANADOR: {reino1.nombre}!")
        enviar(conn1, "tu reino ha ganado la guerra!")
        enviar(conn2, "tu reino ha perdido la guerra...")
    elif not reino1.tiene_unidades():
        a_todos(f"\nGANADOR: {reino2.nombre}!")
        enviar(conn1, "tu reino ha perdido la guerra...")
        enviar(conn2, "tu reino ha ganado la guerra!")
    else:
        a_todos("\nlimite de turnos alcanzado, la batalla termina en empate")


# funcion que gestiona la guerra, espera los dos clientes y si no llegan en 10 segundos vuelve al menu
def iniciar_guerra(srv_socket):
    print("\niniciando guerra, esperando que se conecten los dos reinos...")

    # si en 10 segundos no se conectan los dos se cancela y volvemos al menu
    srv_socket.settimeout(10.0)

    conn1 = conn2 = None

    try:
        print("esperando reino 1...")
        conn1, addr1 = srv_socket.accept()
        print(f"reino 1 conectado desde {addr1}")

        print("esperando reino 2...")
        conn2, addr2 = srv_socket.accept()
        print(f"reino 2 conectado desde {addr2}")

    except socket.timeout:
        # si salta el timeout avisamos al cliente que ya estaba conectado y cerramos
        print("timeout! los dos reinos no se conectaron en 10 segundos")
        print("volviendo al menu principal...")
        if conn1:
            enviar(conn1, "el otro reino no aparecio, se cancela la guerra")
            conn1.close()
        srv_socket.settimeout(None)
        return

    # quitamos el timeout porque ya estan los dos dentro
    srv_socket.settimeout(None)

    enviar(conn1, "conectado! esperando al segundo reino...")
    enviar(conn2, "conectado!")
    enviar(conn1, "el segundo reino se ha unido, vamos a configurar los ejercitos")
    enviar(conn2, "los dos reinos estan conectados, vamos a configurar los ejercitos")

    try:
        # configuramos los dos reinos y luego arrancamos la batalla
        reino1 = configurar_reino(conn1, 1)
        reino2 = configurar_reino(conn2, 2)

        enviar(conn1, "\nlos dos reinos estan listos, que empiece la batalla!")
        enviar(conn2, "\nlos dos reinos estan listos, que empiece la batalla!")

        simular_batalla(conn1, conn2, reino1, reino2)

    except Exception as e:
        print(f"error durante la guerra: {e}")
    finally:
        # cerramos siempre las conexiones al terminar pase lo que pase
        if conn1:
            conn1.close()
        if conn2:
            conn2.close()
        print("guerra terminada, conexiones cerradas")


def main():
    # creamos el socket con TCP (SOCK_STREAM) y lo asociamos al puerto
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR para poder reusar el puerto si reiniciamos el servidor rapido
    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_socket.bind((HOST, PORT))
    # listen(2) porque solo esperamos 2 clientes
    srv_socket.listen(2)

    print(f"servidor en marcha en {HOST}:{PORT}")

    # menu de juego
    while True:
        print("\n=== SERVIDOR - LA GUERRA DE LAS GALAXIAS (2026) ===")
        print("1. Iniciar Guerra")
        print("2. Finalizar Servidor")
        opcion = input("Seleccionar opcion para continuar: ").strip()

        if opcion == "1":
            iniciar_guerra(srv_socket)
        elif opcion == "2":
            print("cerrando servidor, hasta luego")
            srv_socket.close()
            sys.exit(0)
        else:
            print("opcion no valida, elige 1 o 2")


if __name__ == "__main__":
    main()