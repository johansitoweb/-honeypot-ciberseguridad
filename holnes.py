import socket
import threading
import datetime

def manejar_conexion(cliente_socket, direccion_cliente):
    """Maneja una conexión entrante."""
    try:
        print(f"Conexión entrante de {direccion_cliente}")
        #  banner SSH
        cliente_socket.send(b"SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3\r\n")

       
        while True:
            datos = cliente_socket.recv(1024)
            if not datos:
                break
            print(f"Datos recibidos de {direccion_cliente}: {datos.decode().strip()}")
            
            cliente_socket.send(b"Acceso denegado\r\n")

    except Exception as e:
        print(f"Error al manejar la conexión de {direccion_cliente}: {e}")
    finally:
        cliente_socket.close()
        print(f"Conexión cerrada con {direccion_cliente}")

def iniciar_honeypot(puerto=2222):
    """Inicia el honeypot en el puerto especificado."""
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind(("0.0.0.0", puerto))
    servidor_socket.listen(5)
    print(f"Honeypot iniciado en el puerto {puerto}")

    try:
        while True:
            cliente_socket, direccion_cliente = servidor_socket.accept()
            hilo_cliente = threading.Thread(target=manejar_conexion, args=(cliente_socket, direccion_cliente))
            hilo_cliente.start()
    except KeyboardInterrupt:
        print("Honeypot detenido")
    finally:
        servidor_socket.close()

if __name__ == "__main__":
    iniciar_honeypot()