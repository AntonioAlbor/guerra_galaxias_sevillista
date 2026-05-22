# cliente del juego
# se conecta al servidor, recibe los mensajes y manda las respuestas del jugador

import socket
import sys

HOST = 'localhost'
PORT = 65432

# cuando el servidor manda esto significa que quiere que el jugador escriba algo
PIDE_INPUT = "<INPUT>"


# funcion principal del cliente, conecta al servidor y se queda escuchando hasta que la guerra termine
def main():
    print("=== CLIENTE - LA GUERRA DE LAS GALAXIAS ===")
    print(f"conectando a {HOST}:{PORT}...")

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORT))
        print("conectado al servidor!\n")
    except ConnectionRefusedError:
        # si el servidor no esta arrancado no podemos conectar
        print("no se pudo conectar, asegurate de que el servidor esta corriendo primero")
        sys.exit(1)

    try:
        while True:
            datos = cliente.recv(4096).decode('utf-8')

            if not datos:
                # si llega vacio el servidor ha cerrado la conexion y la batalla ha terminado
                print("\nla guerra ha terminado")
                break

            if PIDE_INPUT in datos:
                # el servidor quiere que el jugador escriba algo
                # quitamos el marcador del texto y mostramos solo el mensaje
                mensaje = datos.replace(PIDE_INPUT, "").strip()
                if mensaje:
                    print(mensaje)
                # leemos la respuesta del jugador y la mandamos al servidor
                respuesta = input("> ")
                cliente.sendall((respuesta + "\n").encode('utf-8'))
            else:
                # si no hay PIDE_INPUT es solo informacion, la mostramos y seguimos esperando
                print(datos, end="")

    except KeyboardInterrupt:
        print("\nsaliendo...")
    except Exception as e:
        print(f"error de conexion: {e}")
    finally:
        # cerramos el socket siempre al salir pase lo que pase
        cliente.close()
        print("conexion cerrada")


if __name__ == "__main__":
    main()