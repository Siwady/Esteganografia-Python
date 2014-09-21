from PIL import Image
import imghdr
import binascii
import optparse
import os
import sys, urllib, re
import urllib2
from os.path import basename
from urlparse import urlsplit

def rgb_a_hex(r,g,b):
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)

def hex_a_rgb(hex):
    return tuple(map(ord,hex[1:].decode('hex')))

def str_a_bin(message):
    binary=bin(int(binascii.hexlify(message),16))
    return binary[2:]

def bin_a_str(binary):
    message=binascii.unhexlify('%x' %(int('0b' +binary,2)))
    return message

def codificar(hex,unbinario):
    if hex[-1]in {'0','1','2','3','4','5'}:
        hex=hex[:-1]+unbinario
        return hex
    else:
        return None

def decodificar(hex):
    if hex[-1]in ('0','1'):
        return hex[-1]
    else:
        return None

def esconder(filename,mensaje):
    img=Image.open(filename)
    
    bin=str_a_bin(mensaje)+'1111111111111110'
  
    if img.mode in ('RGBA'):
        img=img.convert('RGBA')
        imgdata=img.getdata()
        
        data=[]
        pos=0
        temp=''
        for item in imgdata:
            if(pos<len(bin)):
                pix=codificar(rgb_a_hex(item[0],item[1],item[2]),bin[pos])
                if pix==None:
                    data.append(item)
                else:
                    r,g,b=hex_a_rgb(pix)
                    data.append((r,g,b,255))
                    pos+=1
            else:
                data.append(item)
        img.putdata(data)
        img.save(filename,"PNG")
        return "Se Guardo correctamente"
    return "no se pudo esconder texto."

def recuperar(filename):
    img=Image.open(filename)
    bin=''
    
    if img.mode in ('RGBA'):
        img=img.convert('RGBA')
        datas=img.getdata()

        for item in datas:
            digit=decodificar(rgb_a_hex(item[0],item[1],item[2]))
            if digit==None:
                pass
            else:
                bin=bin+digit
                if(bin[-16:]=='1111111111111110'):
                    return bin_a_str(bin[:-16])
        return bin_a_str(bin)
    return "La imagen no tiene texto oculto"

def descargarImagenes(url):
    contenido = urllib2.urlopen(url).read()

    imgUrls = re.findall('img .*?src="(.*?)"', contenido)

    for img in imgUrls:
        try:
            imgData = urllib2.urlopen(img).read()
            fileName = basename(urlsplit(img)[2])
            img2 = open(fileName,'wb')
            img2.write(imgData)
            img2.close()
        except:
            pass

def Main():
    respuesta=raw_input("esconder(1) o recuperar(2) o Pagina web(3)?: ")
    if respuesta=="1":
        direccion=raw_input("Direccion de la imagen: ")
        mensaje=raw_input("Mesaje: ")

        img=Image.open(direccion)
        f, e = os.path.splitext(direccion)
        direccion2 = f + ".png"
        if direccion != direccion2:
            ancho, largo = img.size
            img2 = img.crop((0,0,ancho,largo))
            img2 = img2.convert('RGBA')
            img2.save(direccion2,"PNG")
            print esconder(direccion2,mensaje)
        else:
            print esconder(direccion,mensaje)

    elif(respuesta=="2"):
        direccion=raw_input("Direccion de la imagen: ")
        print recuperar(direccion)
    elif(respuesta=="3"):
        url=raw_input("Url de la imagen: ")
        descargarImagenes(url);
Main()