#Arxiu que conté les funcions que executen les diferents accions del reproductor
import tkinter.messagebox
from pygame import mixer
from os import *
from mutagen.mp3 import MP3
import threading
import time

#Funció que crida les funcions que toqui segons el botó pitjat
def switch(accio = None, listbox = None):

    #simulem les variables estàtiques que necessitarem en les diferents funcions
    switch.pausat = getattr(switch, "pausat", False)
    switch.muted = getattr(switch, "muted", False)
    switch.fitxer = getattr(switch, "fitxer", None)
    switch.fil = getattr(switch, "fil", None)
    switch.playlist = getattr(switch, "playlist", [])
    switch.index = getattr(switch, "index", 0)
    switch.temps = getattr(switch, "temps", 0)

    #cridem la funció que toqui segons el botó pitjat
    if accio == 0:
        importar_musica(listbox = listbox)
    elif accio == 1:
        pass
    elif accio == 2:
        pass
    elif accio == 3:
        pass

#Lambda que mostra el missatge amb la informació
sobre_nosaltres = lambda: tkinter.messagebox.showinfo("Informació", "Aquest reproductor ha estat creat amb Python tkinter")

#funció que carrega una cançó a la llista de reproducció
def importar_musica(listbox = None):
    switch.fitxer = tkinter.filedialog.askopenfilename()
    afegir_a_llista(switch.fitxer, listbox)

#funció que afegeix una cançó a una llista
def afegir_a_llista(canço, llista):
    nom = path.basename(canço)
    llista.insert(switch.index, nom)
    switch.playlist.append(canço)
    switch.index += 1
