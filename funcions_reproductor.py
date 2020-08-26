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
    if opcio == 0:      #importar cançó
        switch.fitxer, switch.index, switch.playlist = importar_musica(kwargs.get("listbox", None), switch.fitxer, switch.index, switch.playlist)
    elif opcio == 1:    #acabar el programa
        aturar_programa(kwargs)
    elif opcio == 2:    #play
        switch.fitxer, switch.pausat, switch.playlist, switch.seleccio = play(switch.fitxer, switch.pausat, switch.playlist,switch.seleccio, kwargs)
    elif opcio == 3:    #stop
        stop(kwargs)
    elif opcio == 4:    #pause
        mixer.music.pause()
        switch.pausat = True
    elif opcio == 5:    #següent o previ
        switch.in_rep, switch.seleccio, error = obtenir_canço(kwargs.get("list", None), switch.in_rep, switch.seleccio)
        if error:
            tkinter.messagebox.showerror("Error", "Selecciona una cançó per poder passar a la següent o a la prèvia")
        else:
            switch.fitxer, switch.in_rep, switch.seleccio = saltar(kwargs.get("list", None), switch.playlist, switch.in_rep, switch.seleccio, switch.fitxer, switch.index - 1, kwargs)
    elif opcio == 6:    #eliminar cançó
        switch.playlist, switch.index = eliminar_canço(switch.playlist, kwargs.get("listbox", None), switch.index)

#Lambda que mostra el missatge amb la info de about us
informacio = lambda: tkinter.messagebox.showinfo("Informació", "Aquest reproductor ha estat creat amb Python tkinter, Pygame Mixer i Mutagen.mp3")

#Lambda que mostra la info sobre el reproductor
sobre_nosaltres = lambda: tkinter.messagebox.showinfo("Sobre Nosaltres", "Programadora: Mireia Gasco\nAny: 2020")

#funció que carrega una cançó a la llista de reproducció
def importar_musica(llista, canço, index, playlist):
    canço = tkinter.filedialog.askopenfilename()
    index, playlist = afegir_a_llista(canço, llista, index, playlist)
    return canço, index, playlist

#funció que afegeix una cançó a una llista
def afegir_a_llista(canço, llista, i, playlist):
    nom = path.basename(canço)
    llista.insert(i, nom)
    playlist.append(canço)
    i += 1
    return i, playlist

#funció que elimina una cançó de la llista
def eliminar_canço(playlist, listbox, index):
    #obtenim l'índex de la cançó a eliminar
    t_index_canço = listbox.curselection()
    try:
        index_canço = t_index_canço[0]

        #eliminem la cançó de la llista y de la listbox
        del playlist[index_canço]
        listbox.delete(index_canço)

        #actualitzem la llargada de la llista
        index -= 1
    except IndexError:  #si no hi ha cap cançó seleccionada
        tkinter.messagebox.showerror("Error", "Selecciona la cançó que vols eliminar")

    return playlist, index

#funció que reprodueix la cançó passada i en mostra els detalls sempre que sigui .wav o .mp3
def reproduir(song, d_args):

    #obtenim les etiquetes
    etiqueta_nom = d_args.get("nom", None)
    etiqueta_durada = d_args.get("durada", None)

    #segons l'extensió obtenim la durada de diferents formes
    info = path.splitext(song)
    if info[1] == '.wav':
        canço_actual = mixer.Sound(song)
        durada_total = canço_actual.get_length()
    elif info[1] == '.mp3':
        audio = MP3(song)
        durada_total = audio.info.length
    else:
        durada_total = 0

    #si la cançó era vàlida mosrem la info i la reproduïm
    if durada_total != 0:
        #mostrem el nom
        etiqueta_nom['text'] = "Nom: {}".format(path.basename(song))
                
        #formategem la durada i la mostrem
        min, sec = format_durada(durada_total)
        etiqueta_durada['text'] = "Total: {:02d}:{:02d}".format(min, sec)

        mixer.music.load(song) #carreguem el fitxer que volem reproduir
        mixer.music.play() #reproduim la música
    else:
        tkinter.messagebox.showerror("Error", "Espero que no estiguis intentant escoltar una imatge o algo així...")

#funció que envia a reproduir la cançó seleccionada a la llista
def play(canço, pausat, playlist, seleccio, dic_args):
    #si la música estava pausada la tornem a engegar
    if pausat:
        mixer.music.unpause()
        pausat = False
    else:
        #obtenim la llista de cançons
        llista = dic_args.get("list", None)
        #si hi ha alguna cançó seleccionada
        try:
            llista.curselection()
            pos_sel = llista.curselection()
            seleccio = playlist[pos_sel[0]]
            canço = seleccio
            reproduir(canço, dic_args)
        except IndexError:
            tkinter.messagebox.showerror("Error", "Selecciona la cançó que vols reproduir")
    return canço, pausat, playlist, seleccio

#funció que atura la música
def stop(d_args):
       
    #obtenim les etiquetes
    etiqueta_nom = d_args.get("nom", "Error")
    etiqueta_durada = d_args.get("durada", "Error")

    #eliminem el seu contingut
    etiqueta_nom['text'] = " "
    etiqueta_durada['text'] = " "

    #aturem la música
    mixer.music.stop()

#funció que obté la posició i la cançó que toca reproduir
def obtenir_canço(listbox, index_actual, seleccio):
    
    if listbox.curselection():  
        #si l'índex és nul o s'ha canviat la cançó seleccionada
        posicio_actual = listbox.curselection()
        if index_actual == None or posicio_actual[0] != seleccio:
            index_actual = posicio_actual[0]
            seleccio = index_actual
        error = False
    else:
        error = True

    return index_actual, seleccio, error

#funció que salta a la cançó que toca (prèvia o següent) i la reprodueix
def saltar(llista, playlist, index_actual, seleccio, canço, llargada, d_args):
    
    if d_args.get("previ", False):  #si previ és cert (valor per defecte: fals)
        canço, index_actual = previ(playlist, index_actual, canço, llargada)
    if d_args.get("seguent", False):    #si següent és cert (valor per defecte: fals)
        canço, index_actual = seguent(playlist, index_actual, canço, llargada)

    reproduir(canço, d_args)
    return canço, index_actual, seleccio

#funció que fa que es reprodueixi la cançó prèvia
def previ(playlist, index_actual, canço, llargada,):

    #si l'índex és zero, la cançó prèvia serà la última
    if index_actual == 0:
        canço = playlist[llargada]
        index_actual = llargada

    #si l'índex següent és vàlid, carreguem la cançó prèvia
    else:
        index_actual -= 1
        canço = playlist[index_actual]
      
    return canço, index_actual

#funció que fa que es reprodueixi la següent cançó
def seguent(playlist, index_actual, canço, llargada):
         
    #si l'índex següent surt de la llista, carreguem la primera cançó
    if index_actual >= llargada:
        canço = playlist[0]
        index_actual = 0

    #si l'índex següent és vàlid, carreguem la següent cançó
    else:
        index_actual += 1
        canço = playlist[index_actual]
      
    return canço, index_actual

#funció que obté la durada de la cançó que sona
def format_durada(temps):
    min, sec = divmod(temps, 60)
    return int(min), int(sec)

#funció que modifica el volum obtingut del slider per obtenir un valor entre 0 i 1 i el passa a la funció que modifica el volum
def modif_volum(val):
    volum = float(val) / 100
    mixer.music.set_volume(volum)

#funció que canvia l'estat de la música entre muted i amb so
def mute(bt_mute,ft_mute, ft_volum, sld_volum):
    mute.muted = getattr(mute, "muted", False)
    if mute.muted: #tornem a activar el volum
        bt_mute.configure(image = ft_volum)
        mixer.music.set_volume(0.5)
        sld_volum.set(50)
        mute.muted = False
    else: #mutejem la música
        bt_mute.configure(image = ft_mute)
        mixer.music.set_volume(0)
        sld_volum.set(0)
        mute.muted = True

#funció que tanca el programa
def aturar_programa(dic_etiq):
    #aturem la música
    stop(dic_etiq)
    #obtenim la finestra general i la tanquem
    finestra_general = dic_etiq.get("finestra", "Error")
    finestra_general.destroy()
