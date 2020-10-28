import socket
import time
import hashlib
import threading
import logging


def recibir():
    time.sleep(1)
    msg, address = s.recvfrom(1024)
    msg= msg.decode("Latin1")
    if len(msg)==0:
        return True
    global opcion
    string = "Recibido de: "+str(address) + " El mensaje:    "+ msg 
    print(string)
    return False

def enviar(add, string):
    time.sleep(1)
    msg = string
    msg = f'{len(msg):<5}' + msg
    s.sendto(bytes(msg, "Latin1"),add)
    msg = "Enviado a:  " + str(add[0]) + " El mensaje:    "+ msg
    print(msg)

def sha2(message):
    m = hashlib.sha256()
    m.update(message)
    return m.digest()

def confirmacion(add):
    msg, address = s.recvfrom(1024)
    msg= msg.decode("Latin1")
    if msg =="OK":
        print("El cliente " + add[0]+ " recibió el mensaje correctamente")
    else:
        print("El cliente " + add[0]+ " no recibió el mensaje correctamente")

    print("Gracias, por todo!")
   
def enviar_archivo_eleccion( address):
    b.wait()
    if opcion == "1":
        logging.debug("Se enviará archivo 1. Tamaño: 100MiB")
        enviarHash( address, 1)
        time.sleep(5)
        enviar(address,"Comienza")
        print("Enviando paquetes...")
        enviarArchivo100( address)
    if opcion == "2":
        logging.debug("Se enviará archivo 2. Tamaño: 250MiB")
        enviarHash( address, 2)
        time.sleep(5)
        enviar(address,"Comienza")
        print("Enviando paquetes...")
        enviarArchivo250( address)

def enviarHash(add, archive):
    if archive == 1:
        fil = open('100Mb.mp4','rb')
        hashcode = sha2(fil.read())
        enviar(add, hashcode.decode("Latin1"))
        fil.close()
    if archive == 2:
        fil = open('250Mb.mp4','rb')
        hashcode = sha2(fil.read())
        enviar(add, hashcode.decode("Latin1"))
        fil.close()

def enviarArchivo100(add):
    contadorPaquetes = 0
    video = open('100Mb.mp4','rb')
    print('Enviando paquetes a ',str(add[0]),'...')
    buff = video.read(1024)
    inicio = time.time()
    while (buff):
        contadorPaquetes += 1
        s.sendto(buff,add)
        buff = video.read(1024)
    video.close()
    fin = time.time()
    tiempoEnvio = fin - inicio
    print("Envío completado.")
    print(contadorPaquetes)
    print("Tiempo de envío: " + str(tiempoEnvio) + " Segundos.")

def enviarArchivo250(add):
    contadorPaquetes = 0
    video = open('250Mb.mp4','rb')
    print('Enviando paquetes a ',str(add[0]),'...')
    buff = video.read(1024)
    inicio = time.time()
    while (buff):
        contadorPaquetes += 1
        s.sendto(buff,add)
        buff = video.read(1024)
    video.close()
    fin = time.time()
    tiempoEnvio = fin - inicio
    print("Envío completado.")
    print("Tiempo de envío: " + str(tiempoEnvio) + " Segundos.")

def atenderCliente(data, add):
    mensaje = data.decode("Latin1")
    clientMsg = "Message from Client:{}".format(mensaje)
    clientIP  = "Client IP Address:{}".format(add)
    print(clientMsg)
    print(clientIP)
    enviar_archivo_eleccion(add)
    confirmacion(add)
    s.shutdown(socket.SHUT_WR)
    s.close()


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((socket.gethostname(), 65000))
opcion = 0
n=0   
logging.basicConfig(filename='tmp.log',
                    format='%(levelname)s %(asctime)s :: %(message)s',
                    level=logging.DEBUG) 
n =  int(input ("¿A cuántos clientes quiere atender hoy?"))
opcion = input("Seleccione la opción del archivo que quiere enviar hoy: \n1. Archivo 100 Mib\n2. Archivo 250 MiB\n--->")   
b = threading.Barrier(n)
    
def wait_for_client(s):
    try:
        while True: # keep alive
            try: # receive request from client
                data, client_address = s.recvfrom(1024)
                if data.decode("Latin1") == "Hola.Estoy preparado para recibir datos.":
                    c_thread = threading.Thread(target = atenderCliente,
                                            args = (data, client_address))
                    c_thread.daemon = True
                    c_thread.start()
            except OSError as err:
                s.printwt(err)
    except KeyboardInterrupt:
        s.shutdown_server()


wait_for_client(s)
#while True:
#    t = threading.Thread(target = atenderCliente)
#    t.start()




