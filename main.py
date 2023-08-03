import glob
import threading as th
from tkinter import *
from tkinter import ttk
from winsound import *

import customtkinter as ct
import numpy as np
import sounddevice as sd

duration = 50  # en segundos


ventana = ct.CTk()
data = open("data.dat", "r")
texto = data.read()
data.close()


Ajustador_de_sensibilidad = Scale(ventana, orient=HORIZONTAL, font=20)
Ajustador_de_sensibilidad.set(int(texto))
Ajustador_de_sensibilidad.grid(column=3, row=1)


def audio_callbackt(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    sensibilidad = Ajustador_de_sensibilidad.get() + 25
    verificar = int(volume_norm)
    mostrar = ct.CTkLabel(ventana, text=str(verificar), font=("Arial",40))
    mostrar.grid(column=0, row=1)

    if verificar > sensibilidad and verificar < sensibilidad + 20:
        PlaySound(sonidos_bajos.get(), SND_FILENAME)


    elif verificar > sensibilidad and verificar < sensibilidad + 40:
        PlaySound(sonidos_medianos.get(),SND_FILENAME)

    elif verificar > sensibilidad + 50:
        PlaySound(sonidos_altos.get(),SND_FILENAME)


def escuchar():
    while True:
        stream = sd.InputStream(callback=audio_callbackt)
        with stream:
            sd.sleep(duration * 1000)


def comenzar():
    th.Thread(target=escuchar).start()


def buscar_sonidos():
    #sonidos_bajos["values"] = glob.glob('*.wav')
    sonidos_bajos.configure(values = glob.glob('*.wav'))
    #sonidos_medianos["values"] = glob.glob('*.wav')
    sonidos_medianos.configure(values = glob.glob('*.wav'))
    #sonidos_altos["values"] = glob.glob('*.wav')
    sonidos_altos.configure(values = glob.glob('*.wav'))

def guardar():
    archivo = open("data.dat", "w")
    archivo.write(str(Ajustador_de_sensibilidad.get()))
    archivo.close()


comenzar()

guardar_boton = ct.CTkButton(
    ventana, text="Guardar sensibilidad", font= ('Arial',10), command=guardar)
guardar_boton.place(x=260, y=1)

sonidos_bajos = ct.CTkComboBox(ventana, state="readonly")
sonidos_bajos.set("perro1.wav")
sonidos_bajos.place(x=160, y=120)

sonidos_medianos = ct.CTkComboBox(ventana, state="readonly")
sonidos_medianos.set("perro2.wav")
sonidos_medianos.place(x=160, y=180)

sonidos_altos = ct.CTkComboBox(ventana, state="readonly")
sonidos_altos.set("perro3.wav")
sonidos_altos.place(x=160, y=240)

buscar_sonidos()

#Labels

fuerza_sonido = ct.CTkLabel(ventana, text="Fuerza del sonido:", font=('Arial',18))
fuerza_sonido.grid(column=0, row=0)

mostrar = ct.CTkLabel(ventana, text="Sensibilidad:", font=('Arial',18))
mostrar.place(x=162, y=1)

sonidos_altos_label = ct.CTkLabel(ventana, text="Sonidos altos", font=('Arial',10))
sonidos_altos_label.place(x=170, y=210)

sonidos_medianos_label = ct.CTkLabel(ventana, text="Sonidos medianos", font=("Arial",10))
sonidos_medianos_label.place(x=170, y=150)

sonidos_bajos_label = ct.CTkLabel(ventana, text="Sonidos bajos", font=("Arial",10))
sonidos_bajos_label.place(x=170, y=90)

#Propiedades del Frame
ventana.geometry("420x400")
ventana.resizable(0, 0)
ventana.title("Sistema de alarmas")

ventana.mainloop()
