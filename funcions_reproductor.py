#Arxiu que conté les funcions que executen les diferents accions del reproductor
import tkinter.messagebox
from pygame import mixer
from os import *
from mutagen.mp3 import MP3
import threading
import time

#Funció que crida les funcions que toqui segons el botó pitjat
def switch(**kwargs):

    #simulem les variables estàtiques que necessitarem en les diferents funcions
    switch.pausat = getattr(switch, "pausat", False)
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
        play(kwargs)
    elif opcio == 3:
        stop(kwargs)
    elif opcio == 4:
        pause()
    elif opcio == 5:
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

#funció que mostra els detalls de la cançó que es reprodueix
def mostrar_detalls(dic_args):

    #obtenim les etiquetes
    etiqueta_nom = dic_args.get("nom", None)
    etiqueta_durada = dic_args.get("durada", None)

    #mostrem el nom
    etiqueta_nom['text'] = "Nom: {}".format(path.basename(switch.fitxer))
    info = path.splitext(switch.fitxer)
    #segons l'extensió obtenim la durada de diferents formes
    if info[1] == '.wav':
        canço_actual = mixer.Sound(switch.fitxer)
        durada_total = canço_actual.get_length()
    elif info[1] == '.mp3':
        audio = MP3(switch.fitxer)
        durada_total = audio.info.length
    else:
        durada_total = 0

    #formategem la durada i la mostrem
    min, sec = format_durada(durada_total)
    etiqueta_durada['text'] = "Total: {:00d}:{:00d}".format(min, sec)

    #creem el thread per mostrar el temps actual
    fil = threading.Thread(target = temps_rep, args = (durada_total, dic_args,))
    fil.start()

def eliminar_detalls(d_etiq):
    #obtenim les etiquetes
    etiqueta_nom = d_etiq.get("nom", "Error")
    etiqueta_durada = d_etiq.get("durada", "Error")
    etiqueta_durada_actual = d_etiq.get("durada_actual", "Error")
    #eliminem el seu contingut
    etiqueta_nom['text'] = " "
    etiqueta_durada['text'] = " "
    etiqueta_durada_actual['text'] = " "

#funció que reprodueix una cançó prèviament seleccionada i dona error si no s'ha escollit la cançó
def play(dic_args):
    #si la música estava pausada la tornem a engegar
    if switch.pausat:
        mixer.music.unpause()
        switch.pausat = False
    else:
        #obtenim la llista de cançons
        llista = dic_args.get("list", None)
        #si hi ha alguna cançó seleccionada
        if llista.curselection():
            canço_seleccionada = llista.curselection()
            mixer.music.load(switch.playlist[canço_seleccionada[0]]) #carreguem el fitxer que volem reproduir
            mixer.music.play() #reproduim la música
            mostrar_detalls(dic_args)
        else:
            tkinter.messagebox.showerror("Error", "No s'ha seleccionat cap cançó")

#funció que para la música
def stop(etiquetes):
   mixer.music.stop()
   eliminar_detalls(etiquetes)

#funció que para temporalment la reproducció de la cançó que sona
def pause():
   mixer.music.pause()
   switch.pausat = True


#funció que obté la durada de la cançó que sona
def format_durada(temps):
    min, sec = divmod(temps, 60)
    return int(min), int(sec)

#funció que obté la durada actual de la cançó
def temps_rep(durada, d_etiq):
    #obtenim l'etiqueta
    etiqueta_durada_actual = d_etiq.get("durada_actual", None)
    while switch.temps <= durada and mixer.music.get_busy():
        if switch.pausat == False:
            min, sec = divmod(switch.temps, 60)
            etiqueta_durada_actual["text"] = "Temps: {:02d}:{:02d}".format(int(min), int(sec))
            time.sleep(1)
            switch.temps += 1

#funció que tanca el programa
def aturar_programa(dic_etiq):
    #aturem la música
    stop(dic_etiq)
    #obtenim la finestra general i la tanquem
    finestra_general = dic_etiq.get("finestra", "Error")
    finestra_general.destroy()
