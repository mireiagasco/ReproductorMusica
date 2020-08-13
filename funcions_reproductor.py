#Arxiu que conté les funcions que executen les diferents accions del reproductor
import tkinter.messagebox
from pygame import mixer
from os import *
from mutagen.mp3 import MP3
import threading
import time

#Funció que crida les funcions que toqui segons el botó pitjat
def switch(**kwargs):

    #inicialitzem el reproductor
    mixer.init()

    #simulem les variables estàtiques que necessitarem en les diferents funcions
    switch.pausat = getattr(switch, "pausat", False)
    switch.muted = getattr(switch, "muted", False)
    switch.fitxer = getattr(switch, "fitxer", None)
    switch.fil = getattr(switch, "fil", None)
    switch.playlist = getattr(switch, "playlist", [])
    switch.index = getattr(switch, "index", 0)
    switch.temps = getattr(switch, "temps", 0)

    #obtenim el valor de l'opció del diccionari d'arguments
    opcio = kwargs.get("accio", "Error")

    #cridem la funció que toqui segons el botó pitjat
    if opcio == 0:
        importar_musica(kwargs.get("listbox", None))
    elif opcio == 1:
        aturar_programa(kwargs)
    elif opcio == 2:
        pass
    elif opcio == 3:
        pass

#Lambda que mostra el missatge amb la informació
sobre_nosaltres = lambda: tkinter.messagebox.showinfo("Informació", "Aquest reproductor ha estat creat amb Python tkinter")

#funció que carrega una cançó a la llista de reproducció
def importar_musica(llista):
    switch.fitxer = tkinter.filedialog.askopenfilename()
    afegir_a_llista(switch.fitxer, llista)

#funció que afegeix una cançó a una llista
def afegir_a_llista(canço, llista):
    nom = path.basename(canço)
    llista.insert(switch.index, nom)
    switch.playlist.append(canço)
    switch.index += 1

def eliminar_detalls(d_etiq):
    #obtenim les etiquetes
    etiqueta_nom = d_etiq.get("nom", "Error")
    etiqueta_durada = d_etiq.get("durada", "Error")
    etiqueta_durada_actual = d_etiq.get("durada_actual", "Error")
    #eliminem el seu contingut
    etiqueta_nom['text'] = " "
    etiqueta_durada['text'] = " "
    etiqueta_durada_actual['text'] = " "

#funció que para la música
def stop(etiquetes):
   mixer.music.stop()
   eliminar_detalls(etiquetes)

#funció que tanca el programa
def aturar_programa(dic_etiq):
    #aturem la música
    stop(dic_etiq)
    #obtenim la finestra general i la tanquem
    finestra_general = dic_etiq.get("finestra", "Error")
    finestra_general.destroy()
