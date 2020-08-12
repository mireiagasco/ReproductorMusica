from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from pygame import mixer
from os import *
from mutagen.mp3 import MP3

#generem la finestra principal
finestra_general = Tk()
finestra_general.title("Reproductor de Música")
finestra_general.iconbitmap(r"icones\icona_reproductor.ico")

#inicialitzem el reproductor
mixer.init()

#definim les variables globals
pausat = False
muted = False
fitxer = None

#definim totes les funcions que necessitarem------------------------------------------------------

#funció que mostra els detalls de la cançó que es reprodueix
def mostrar_detalls():
    #mostrem el nom
    etiqueta_nom['text'] = "Nom: {}".format(path.basename(fitxer))
    info = path.splitext(fitxer)
    #segons l'extensió obtenim la durada de diferents formes
    if info[1] == '.wav':
        canço_actual = mixer.Sound(fitxer)
        durada_total = canço_actual.get_length()
    elif info[1] == '.mp3':
        audio = MP3(fitxer)
        durada_total = audio.info.length
    else:
        durada_total = 0
    #formategem la durada i la mostrem
    min, sec = format_durada(durada_total)
    etiqueta_durada['text'] = "Durada: {:00d}:{:00d}".format(min, sec)

#funció que elimina els detalls quan es deixa de reproduir una cançó
def eliminar_detalls():
    etiqueta_nom['text'] = " "
    etiqueta_durada['text'] = " "

#funció que reprodueix una cançó prèviament seleccionada i dona error si no s'ha escollit la cançó
def play():
    global pausat
    global fitxer
    if pausat:
        mixer.music.unpause()
        pausat = False
    else:
        if fitxer:
            mixer.music.load(fitxer) #carreguem el fitxer que volem reproduir
            mixer.music.play() #reproduim la música
            mostrar_detalls()
        else:
            tkinter.messagebox.showerror("Error", "No s'ha pogut reproduir l'arxiu")

#funció que para temporalment la reproducció de la cançó que sona
def pause():
   global pausat
   mixer.music.pause()
   pausat = True

#funció que para la música
def stop():
   mixer.music.stop()
   eliminar_detalls()

#funció que fa que es reprodueixi la següent cançó
def seguent():
    pass

#funció que fa que es reprodueixi la cançó prèvia
def previ():
    pass

#funció que modifica el volum obtingut del slider per obtenir un valor entre 0 i 1 i el passa a la funció
#que modifica el volum (aquesta només accepta valors fins a 1)
def modif_volum(val):
    volum = int(val) / 100
    mixer.music.set_volume(volum)

#funció que canvia l'estat de la música entre muted i amb so
def mute():
    global muted
    if muted: #tornem a activar el volum
        boto_mute.configure(image = foto_volum)
        mixer.music.set_volume(0.5)
        slider_volum.set(50)
        muted = False
    else: #mutejem la música
        boto_mute.configure(image = foto_mute)
        mixer.music.set_volume(0)
        slider_volum.set(0)
        muted = True


#funció que obre un buscador per importar els arxius de música que volguem
def cercar_musica():
    global fitxer
    fitxer = tkinter.filedialog.askopenfilename()

#funció que obté la durada de la cançó que sona
def format_durada(temps):
    min, sec = divmod(temps, 60)
    return int(min), int(sec)

#-----------------------------------------------------------------------------------------------------

#creem el menú
nom = "Reproductor de Música"
autora = "Mireia Gasco"
any = "2020"
missatge = "{}\n{}\n{}".format(nom, autora, any)
sobre_nosaltres = lambda: tkinter.messagebox.showinfo("Informació", missatge)

barra_menu = Menu(finestra_general) #creem la barra de menú
finestra_general.config(menu = barra_menu) #la configurem per assegurar que es troba dalt de tot

submenu_arxiu = Menu(barra_menu, tearoff = False)  #creem el submenú on aniran tots els botons
barra_menu.add_cascade(label = "Reproductor", menu = submenu_arxiu)
submenu_arxiu.add_command(label = "Importar música", command = cercar_musica)
submenu_arxiu.add_command(label = "Sortir", command = finestra_general.destroy)

submenu_ajuda = Menu(barra_menu, tearoff = False)  #creem el submenú on aniran tots els botons
barra_menu.add_cascade(label = "Ajuda", menu = submenu_ajuda)
submenu_ajuda.add_command(label = "Sobre Nosaltres", command = sobre_nosaltres)

#creem marcs per organitzar els botons
marc_superior = Frame(finestra_general)
marc_superior.pack()

marc_central = Frame(finestra_general)
marc_central.pack()

marc_inferior = Frame(finestra_general)
marc_inferior.pack()

#creem la l'etiqueta on mostrem la benvinguda
etiqueta_benvinguda = Label(marc_superior, text = "Benvingut/da!", pady = 10)
etiqueta_benvinguda.pack()

#creem l'etiqueta on mostrarem el nom de la cançó
etiqueta_nom = Label(marc_superior, pady = 10)
etiqueta_nom.pack()

#creem l'etiqueta on mostrarem la durada de la cançó
etiqueta_durada = Label(marc_superior, pady = 10)
etiqueta_durada.pack()

#carreguem les fotos que utilitzarem pels botons
foto_play = PhotoImage(file = r"icones\001-play.png")
foto_pause = PhotoImage(file = r"icones\002-pause.png")
foto_stop = PhotoImage(file = r"icones\003-stop.png")
foto_seguent = PhotoImage(file = r"icones\004-next.png")
foto_previ = PhotoImage(file = r"icones\005-previous.png")
foto_volum = PhotoImage(file = r"icones\volum.png")
foto_mute = PhotoImage(file = r"icones\mute.png")

#creem els botons
boto_previ = Button(marc_central, image = foto_previ, borderwidth = 0, command = previ)
boto_previ.grid(row = 0, column = 1, padx = 10, pady = 20)

boto_pause = Button(marc_central, image = foto_pause, borderwidth = 0, command = pause)
boto_pause.grid(row = 0, column = 2, padx = 10, pady = 20)

boto_stop = Button(marc_central, image = foto_stop, borderwidth = 0, command = stop)
boto_stop.grid(row = 0, column = 3, padx = 10, pady = 20)

boto_play = Button(marc_central, image = foto_play, borderwidth = 0, command = play)
boto_play.grid(row = 0, column = 4, padx = 10, pady = 20)

boto_seguent = Button(marc_central, image = foto_seguent, borderwidth = 0, command = seguent)
boto_seguent.grid(row = 0, column = 5, padx = 10, pady = 20)

boto_mute = Button(marc_inferior, image = foto_volum, borderwidth = 0, command = mute)
boto_mute.grid(row = 1, column = 0, padx = 20)

#creem el slider del volum
slider_volum = Scale(marc_inferior, from_ = 0, to = 100, orient = "horizontal", label = "         Volum", command = modif_volum)
slider_volum.set(50) #establim 50 com el valor per defecte
slider_volum.grid(pady = 20, column = 0, row = 0)

finestra_general.mainloop()
