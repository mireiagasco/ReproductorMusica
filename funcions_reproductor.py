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
    switch.pausat = getattr(switch, "pausat", False)    #indica si la música està pausada
    switch.fitxer = getattr(switch, "fitxer", None)     #conté la cançó que s'ha de reproduir
    switch.playlist = getattr(switch, "playlist", [])   #llista de cançons (amb el path) per reproduir
    switch.index = getattr(switch, "index", 0)          #índex que marca quantes cançons hi ha a la llista
    switch.in_rep = getattr(switch, "in_rep", None)     #índex que marca quina cançó s'està reproduint
    switch.seleccio = getattr(switch, "seleccio", None) #indica la posició de la cançó seleccionada

    #obtenim el valor de l'opció del diccionari d'arguments
    opcio = kwargs.get("accio", "Error")

    #cridem la funció que toqui segons el botó pitjat
    if opcio == 0:
        switch.fitxer = importar_musica(kwargs.get("listbox", None), switch.fitxer)
    elif opcio == 1:
        aturar_programa(kwargs)
    elif opcio == 2:    #play
        switch.fitxer, switch.pausat, switch.playlist, switch.seleccio = play(switch.fitxer, switch.pausat, switch.playlist,switch.seleccio, kwargs)
    elif opcio == 3:    #stop
        stop(kwargs)
    elif opcio == 4:    #pause
        mixer.music.pause()
        switch.pausat = True
    elif opcio == 5:    #següent
        switch.fitxer, switch.in_rep, switch.seleccio = seguent(kwargs.get("d_llista", None), switch.playlist, switch.in_rep, switch.seleccio, switch.fitxer, kwargs)

#Lambda que mostra el missatge amb la informació
sobre_nosaltres = lambda: tkinter.messagebox.showinfo("Informació", "Aquest reproductor ha estat creat amb Python tkinter")

#funció que carrega una cançó a la llista de reproducció
def importar_musica(llista, canço):
    canço = tkinter.filedialog.askopenfilename()
    afegir_a_llista(canço, llista)
    return canço

#funció que afegeix una cançó a una llista
def afegir_a_llista(canço, llista):
    nom = path.basename(canço)
    llista.insert(switch.index, nom)
    switch.playlist.append(canço)
    switch.index += 1

#funció que mostra els detalls de la cançó que es reprodueix
def mostrar_detalls(canço, dic_args):

    #obtenim les etiquetes
    etiqueta_nom = dic_args.get("nom", None)
    etiqueta_durada = dic_args.get("durada", None)

    #mostrem el nom
    etiqueta_nom['text'] = "Nom: {}".format(path.basename(canço))
    info = path.splitext(canço)
    #segons l'extensió obtenim la durada de diferents formes
    if info[1] == '.wav':
        canço_actual = mixer.Sound(canço)
        durada_total = canço_actual.get_length()
    elif info[1] == '.mp3':
        audio = MP3(canço)
        durada_total = audio.info.length
    else:
        durada_total = 0

    #formategem la durada i la mostrem
    min, sec = format_durada(durada_total)
    etiqueta_durada['text'] = "Total: {:00d}:{:00d}".format(min, sec)

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
def play(canço, pausat, playlist, seleccio, dic_args):
    #si la música estava pausada la tornem a engegar
    if pausat:
        mixer.music.unpause()
        pausat = False
    else:
        #obtenim la llista de cançons
        llista = dic_args.get("list", None)
        #si hi ha alguna cançó seleccionada
        if llista.curselection():
            pos_sel = llista.curselection()
            seleccio = playlist[pos_sel[0]]
            canço = seleccio
            mixer.music.load(canço) #carreguem el fitxer que volem reproduir
            mixer.music.play() #reproduim la música
            mostrar_detalls(canço, dic_args)
        else:
            tkinter.messagebox.showerror("Error", "No s'ha seleccionat cap cançó")
    return canço, pausat, playlist, seleccio

#funció que atura la música
def stop(d_args):
    mixer.music.stop()
    eliminar_detalls(d_args)

#funció que fa que es reprodueixi la següent cançó
def seguent(llista, playlist, index_actual, seleccio, canço, d_args):

    #obtenim l'índex de la cançó seleccionada
    posicio_actual = llista.curselection()

    #si l'índex és nul o s'ha canviat la cançó seleccionada
    if index_actual == None or posicio_actual[0] != seleccio:
        index_actual = posicio_actual[0]
        seleccio = index_actual

    #obtenim l'índex màxim de la playlist
    llargada = len(playlist) - 1

    #si l'índex següent surt de la llista, carreguem la primera cançó
    if index_actual >= llargada:
        canço = playlist[0]
        mixer.music.load(canço)
        index_actual = 0

    #si l'índex següent és vàlid, carreguem la següent cançó
    else:
        index_actual += 1
        canço = playlist[index_actual]
        mixer.music.load(canço)

    mixer.music.play()
    
    #mostrem els detalls de la nova cançó i retornem l'índex
    mostrar_detalls(canço, d_args)
    return canço, index_actual, seleccio

#funció que obté la durada de la cançó que sona
def format_durada(temps):
    min, sec = divmod(temps, 60)
    return int(min), int(sec)

#funció que tanca el programa
def aturar_programa(dic_etiq):
    #aturem la música
    stop(dic_etiq)
    #obtenim la finestra general i la tanquem
    finestra_general = dic_etiq.get("finestra", "Error")
    finestra_general.destroy()
