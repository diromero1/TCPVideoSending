import socket
import time
import hashlib
import cv2 as cv
import numpy as np
import threading

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

def enviar(string, tupla):
    time.sleep(1)
    #string = f'{len(string):<5}' + string
    s.sendto(bytes(string, "Latin1"),tupla)
    string = "Enviado:    " + string
    print(string)

def sha2(message):
    m = hashlib.sha256()
    m.update(message)
    return m.digest()

def recibirArchivo():
    contadorPaquetes = 0

    video = open('video.mp4','wb')
    inicio = time.time()
    print("Reproduciendo video...")
    buff = s.recv(1024)
    while (buff and contadorPaquetes<100000): #905
        contadorPaquetes += 1
        video.write(buff)
        buff = s.recv(1024)
    video.close()
    fin = time.time()
    tiempoDeTransferencia = fin - inicio
    print("Tiempo de transferencia: " + str(tiempoDeTransferencia) + " Segundos.")

def reproducirStream():
    cap = cv.VideoCapture('video.mp4')
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray)
        key = cv.waitKey(1)
        #if key == ord('q'):
        #    break
        if key == ord('p'):
            cv.waitKey(-1) #wait until any key is pressed
    cap.release()
    cv.destroyAllWindows()
    
    
def comprobacion(tupla):
    video = open('video.mp4','rb')
    codigo = sha2(video.read()).decode("Latin1")
    enviar("OK", tupla)
    print(codigo)
    if hashcode == codigo:
        print("Se recibió el archivo completo y en perfecto estado.")
    else:
        print("Sera necesario volver a descargar el archivo.")
    video.close()




s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    tr = threading.Thread(target = reproducirStream)
    #t.daemon = True
    s.connect((socket.gethostname(), 65000))
    name = socket.gethostname()
    ip = socket.gethostbyname(name)
    hashcode = b''
    enviar('Hola.Estoy preparado para recibir datos.', (ip,65000))
    while recibir(True):
        pass
    recibir(False)
    recibirArchivo()
    tr.start()
    comprobacion((ip, 65000))
    print("Gracias, por todo!")

except Exception as e: 
    print("something's wrong with %s:%d. Exception is %s" % (socket.gethostname(), 65000, e))