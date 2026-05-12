# servidor principal del juego

import socket
import sys

HOST = 'localhost'
PORT = 65432


# funcion que manda un mensaje al cliente, si falla no hace nada para que no pete el servidor
def enviar(conn, mensaje):
    try:
        conn.sendall((mensaje + "\n").encode('utf-8'))
    except Exception:
        pass


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

    # avisamos a cada cliente de que todo esta listo
    enviar(conn1, "conectado! esperando al segundo reino...")
    enviar(conn2, "conectado!")
    enviar(conn1, "el segundo reino se ha unido, vamos a configurar los ejercitos")
    enviar(conn2, "los dos reinos estan conectados, vamos a configurar los ejercitos")

    # aqui ira la configuracion y la batalla
    if conn1:
        conn1.close()
    if conn2:
        conn2.close()
    print("conexiones cerradas")


def main():
    # creamos el socket con TCP (SOCK_STREAM) y lo asociamos al puerto
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR para poder reusar el puerto si reiniciamos el servidor rapido
    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_socket.bind((HOST, PORT))
    # listen(2) porque solo esperamos 2 clientes
    srv_socket.listen(2)

    print(f"servidor en marcha en {HOST}:{PORT}")

    # menú de juego
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