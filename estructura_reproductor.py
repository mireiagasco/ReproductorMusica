#Arxiu que conté la funció que genera el reproductor i les que controlen el volum
from pygame import mixer
from funcions_reproductor import *
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog

#Funció que genera el reproductor
def crear_reproductor():
        
    #inicialitzem el reproductor
    mixer.init()

    #generem la finestra principal
    finestra_general = Tk()
    finestra_general.title("Reproductor de Música")
    finestra_general.iconbitmap(r"icones\icona_reproductor.ico")

    #creem el menú principal
    barra_menu = Menu(finestra_general) #creem la barra de menú
    finestra_general.config(menu = barra_menu) #la configurem per assegurar que es troba dalt de tot

    #creem el submenú "reproductor"
    submenu_reproductor = Menu(barra_menu, tearoff = False)  #creem el submenú on aniran tots els botons
    barra_menu.add_cascade(label = "Reproductor", menu = submenu_reproductor)
    submenu_reproductor.add_command(label = "Importar música", command = lambda: switch(accio = 0, listbox = llista))
    submenu_reproductor.add_command(label = "Sortir", command = lambda: switch(accio = 1, nom = etiqueta_nom, durada = etiqueta_durada, durada_actual = etiqueta_durada_actual, finestra = finestra_general))

    #creem el submenú "ajuda"
    submenu_ajuda = Menu(barra_menu, tearoff = False)  #creem el submenú on aniran tots els botons
    barra_menu.add_cascade(label = "Informació", menu = submenu_ajuda)
    submenu_ajuda.add_command(label = "Veure info", command = sobre_nosaltres)

    #creem marcs per organitzar els botons
    marc_dret = Frame(finestra_general)
    marc_dret.pack(side = RIGHT)

    marc_superior = Frame(marc_dret)
    marc_superior.pack()

    marc_central = Frame(marc_dret)
    marc_central.pack()

    marc_inferior = Frame(marc_dret)
    marc_inferior.pack()

    marc_esquerre = Frame(finestra_general)
    marc_esquerre.pack(side = LEFT)

    #creem la l'etiqueta on mostrem la benvinguda
    etiqueta_benvinguda = Label(marc_superior, text = "Benvingut/da!", pady = 10)
    etiqueta_benvinguda.pack()

    #creem la listbox on mostrarem les cançons en cua
    llista = Listbox(marc_esquerre, height = 10, width = 25)
    llista.grid(row = 0, column = 0, columnspan = 2, pady = 10)

    #creem l'etiqueta on mostrarem el nom de la cançó
    etiqueta_nom = Label(marc_superior, pady = 10)
    etiqueta_nom.pack()

    #creem l'etiqueta amb la durada actual
    etiqueta_durada_actual = Label(marc_superior)
    etiqueta_durada_actual.pack(side = LEFT)

    #creem l'etiqueta on mostrarem la durada de la cançó
    etiqueta_durada = Label(marc_superior, pady = 10)
    etiqueta_durada.pack(side = RIGHT)

    #carreguem les fotos que utilitzarem pels botons
    foto_play = PhotoImage(file = r"icones\001-play.png")
    foto_pause = PhotoImage(file = r"icones\002-pause.png")
    foto_stop = PhotoImage(file = r"icones\003-stop.png")
    foto_seguent = PhotoImage(file = r"icones\004-next.png")
    foto_previ = PhotoImage(file = r"icones\005-previous.png")
    foto_volum = PhotoImage(file = r"icones\volum.png")
    foto_mute = PhotoImage(file = r"icones\mute.png")

    #creem els botons
    boto_previ = Button(marc_central, image = foto_previ, borderwidth = 0, command = lambda: switch(accio = 5, list = llista, nom = etiqueta_nom, durada = etiqueta_durada, durada_actual = etiqueta_durada_actual, previ = True))
    boto_previ.grid(row = 0, column = 1, padx = 10, pady = 20)

    boto_pause = Button(marc_central, image = foto_pause, borderwidth = 0, command = lambda: switch(accio = 4))
    boto_pause.grid(row = 0, column = 2, padx = 10, pady = 20)

    boto_stop = Button(marc_central, image = foto_stop, borderwidth = 0, command = lambda: switch(accio = 3, nom = etiqueta_nom, durada = etiqueta_durada, durada_actual = etiqueta_durada_actual))
    boto_stop.grid(row = 0, column = 3, padx = 10, pady = 20)

    boto_play = Button(marc_central, image = foto_play, borderwidth = 0, command = lambda: switch(accio = 2, list = llista, nom = etiqueta_nom, durada = etiqueta_durada, durada_actual = etiqueta_durada_actual))
    boto_play.grid(row = 0, column = 4, padx = 10, pady = 20)

    boto_seguent = Button(marc_central, image = foto_seguent, borderwidth = 0, command = lambda: switch(accio = 5, list = llista, nom = etiqueta_nom, durada = etiqueta_durada, durada_actual = etiqueta_durada_actual, seguent = True))
    boto_seguent.grid(row = 0, column = 5, padx = 10, pady = 20)

    boto_mute = Button(marc_inferior, image = foto_volum, borderwidth = 0, command = lambda: mute(boto_mute, foto_mute, foto_volum, slider_volum))
    boto_mute.grid(row = 1, column = 0, padx = 20, pady = 10)

    boto_afegir = Button(marc_esquerre, text = " Afegir ", command = lambda: switch(accio = 0, listbox = llista))
    boto_afegir.grid(row = 1, column = 0, pady = 10, padx = 10)

    boto_eliminar = Button(marc_esquerre, text = "Eliminar")
    boto_eliminar.grid(row = 1, column = 1, pady = 10, padx = 10)

    #creem el slider del volum
    slider_volum = Scale(marc_inferior, from_ = 0, to = 100, orient = "horizontal", label = "         Volum", command = modif_volum)
    slider_volum.set(50) #establim 50 com el valor per defecte
    slider_volum.grid(pady = 10, column = 0, row = 0)

    dic = {"nom": etiqueta_nom, "durada": etiqueta_durada, "durada_actual": etiqueta_durada_actual, "finestra": finestra_general}
    finestra_general.protocol("WM_DELETE_WINDOW", lambda: aturar_programa(dic))
    finestra_general.mainloop()


#funció que modifica el volum obtingut del slider per obtenir un valor entre 0 i 1 i el passa a la funció que modifica el volum
def modif_volum(val):
    volum = int(val) / 100
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
