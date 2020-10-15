import socket
import time
import struct
import pickle
import cv2
import numpy
import hashlib

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 65000))
name = socket.gethostname()
ip = socket.gethostbyname(name)
hashcode = b''

def recibir(hashvalue):
    time.sleep(1)
    if hashvalue == True:
        msg = s.recv(1024)
        if len(msg) == 0:
            return True
        msg = msg.decode("Latin1")
        global hashcode
        hashcode = msg[5:]
        complete = "Recibido:   " + msg
        print(complete)
        return False
    else:
        msg = s.recv(1024)
        if len(msg) == 0:
            return True
        msg = msg.decode("Latin1")
        complete = "Recibido:   " + msg
        print(complete)
        return False

def enviar(string):
    time.sleep(1)
    string = f'{len(string):<5}' + string
    s.sendall(bytes(string, "Latin1"))
    string = "Enviado:    " + string
    print(string)

def sha2(message):
    m = hashlib.sha256()
    m.update(message)
    return m.digest()

def recibirArchivo():
    video = open('video.mp4','wb')
    inicio = time.time()
    print("Recibiendo paquetes...")
    buff = s.recv(4096)
    while (buff):
        video.write(buff)
        buff = s.recv(4096)
    video.close()
    fin = time.time()
    tiempoDeTransferencia = fin - inicio
    print("Tiempo de transferencia: " + str(tiempoDeTransferencia) + " Segundos.")
    
    
def comprobacion():
    video = open('video.mp4','rb')
    codigo = sha2(video.read()).decode("Latin1")
    print(codigo)
    if hashcode == codigo:
        print("Se recibió el archivo completo y en perfecto estado.")
    else:
        print("Sera necesario volver a descargar el archivo.")
    video.close()

enviar('[SYN] Hola, mi dirección IP es: '+ ip)
while recibir(False):
    pass
enviar('[ACK] Gracias. Estoy preparado para recibir datos.')
while recibir(False):
    pass
opcion = input()
enviar(opcion)
while recibir(True):
    pass
enviar("He recibido el hashcode: " + hashcode)
recibirArchivo()
comprobacion()
enviar("[FIN] Gracias, por todo!")