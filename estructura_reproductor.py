#Arxiu que conté la funció que genera el reproductor i les que controlen el volum
from pygame import mixer
from funcions_reproductor import *
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk

#Funció que genera el reproductor
def crear_reproductor():
        
    #inicialitzem el reproductor
    mixer.init()

    #generem la finestra principal
    finestra_general = tk.ThemedTk()
    finestra_general.get_themes()
    finestra_general.set_theme("breeze")

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
    submenu_info = Menu(barra_menu, tearoff = False)  #creem el submenú on aniran tots els botons
    barra_menu.add_cascade(label = "Informació", menu = submenu_info)
    submenu_info.add_command(label = "Veure info", command = informacio)
    submenu_info.add_command(label = "Sobre Nosaltres", command = sobre_nosaltres)

    #creem marcs per organitzar els botons
    marc_dret = ttk.Frame(finestra_general)
    marc_dret.pack(side = RIGHT)

    marc_esquerre = ttk.Frame(finestra_general)
    marc_esquerre.pack(side = LEFT)

    marc_superior = ttk.Frame(marc_dret)
    marc_superior.pack()

    marc_central = ttk.Frame(marc_dret)
    marc_central.pack()

    marc_inferior = ttk.Frame(marc_dret)
    marc_inferior.pack()

   

    #creem la l'etiqueta on mostrem la benvinguda
    etiqueta_benvinguda = Label(marc_superior, text = "Benvingut/da!", font = "Gabriola 20 bold")
    etiqueta_benvinguda.pack(pady = 10)

    #creem la listbox on mostrarem les cançons en cua
    llista = Listbox(marc_esquerre, height = 10, width = 25)
    llista.pack()

    #creem l'etiqueta on mostrarem el nom de la cançó
    etiqueta_nom = Label(marc_superior)
    etiqueta_nom.pack(pady = 10)

    #creem l'etiqueta amb la durada actual
    etiqueta_durada_actual = Label(marc_superior)
    etiqueta_durada_actual.pack(side = LEFT)

    #creem l'etiqueta on mostrarem la durada de la cançó
    etiqueta_durada = Label(marc_superior)
    etiqueta_durada.pack(side = RIGHT, pady = 10)

    #carreguem les fotos que utilitzarem pels botons
    foto_play = PhotoImage(file = r"icones\001-play.png")
    foto_pause = PhotoImage(file = r"icones\002-pause.png")
    foto_stop = PhotoImage(file = r"icones\003-stop.png")
    foto_seguent = PhotoImage(file = r"icones\004-next.png")
    foto_previ = PhotoImage(file = r"icones\005-previous.png")
    foto_volum = PhotoImage(file = r"icones\volum.png")
    foto_mute = PhotoImage(file = r"icones\mute.png")

    #creem els botons
    boto_previ = ttk.Button(marc_central, image = foto_previ, command = lambda: switch(accio = 5, list = llista, nom = etiqueta_nom, durada = etiqueta_durada, durada_actual = etiqueta_durada_actual, previ = True))
    boto_previ.grid(row = 0, column = 1, padx = 10, pady = 20)

    boto_pause = ttk.Button(marc_central, image = foto_pause, command = lambda: switch(accio = 4))
    boto_pause.grid(row = 0, column = 2, padx = 10, pady = 20)

    boto_stop = ttk.Button(marc_central, image = foto_stop, command = lambda: switch(accio = 3, nom = etiqueta_nom, durada = etiqueta_durada, durada_actual = etiqueta_durada_actual))
    boto_stop.grid(row = 0, column = 3, padx = 10, pady = 20)

    boto_play = ttk.Button(marc_central, image = foto_play, command = lambda: switch(accio = 2, list = llista, nom = etiqueta_nom, durada = etiqueta_durada, durada_actual = etiqueta_durada_actual))
    boto_play.grid(row = 0, column = 4, padx = 10, pady = 20)

    boto_seguent = ttk.Button(marc_central, image = foto_seguent, command = lambda: switch(accio = 5, list = llista, nom = etiqueta_nom, durada = etiqueta_durada, durada_actual = etiqueta_durada_actual, seguent = True))
    boto_seguent.grid(row = 0, column = 5, padx = 10, pady = 20)

    boto_mute = ttk.Button(marc_inferior, image = foto_volum, command = lambda: mute(boto_mute, foto_mute, foto_volum, slider_volum))
    boto_mute.grid(row = 1, column = 0, padx = 20, pady = 10)

    boto_afegir = ttk.Button(marc_esquerre, text = " Afegir ", command = lambda: switch(accio = 0, listbox = llista))
    boto_afegir.pack(side = LEFT)

    boto_eliminar = ttk.Button(marc_esquerre, text = "Eliminar", command = lambda: switch(accio = 6, listbox = llista))
    boto_eliminar.pack(side = RIGHT)

    #creem el slider del volum
    slider_volum = ttk.Scale(marc_inferior, from_ = 0, to = 100, orient = "horizontal", command = modif_volum)
    slider_volum.set(50) #establim 50 com el valor per defecte
    slider_volum.grid(pady = 10, column = 0, row = 0)

    dic = {"nom": etiqueta_nom, "durada": etiqueta_durada, "durada_actual": etiqueta_durada_actual, "finestra": finestra_general}
    finestra_general.protocol("WM_DELETE_WINDOW", lambda: aturar_programa(dic))
    finestra_general.mainloop()


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
