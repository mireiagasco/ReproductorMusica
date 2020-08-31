#Arxiu que conté la classe reproductor
from pygame import mixer
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
import os


#classe reproductor
class Reproductor:
    def __init__(self, *args, **kwargs):
        
        #creem els atributs del reproductor
        self.pausat = False     #indica si la música està pausada
        self.fitxer = None      #conté la cançó que s'ha de reproduir
        self.playlist = []      #llista de cançons (amb el path) per reproduir
        self.index = 0          #índex que marca quantes cançons hi ha a la llista
        self.in_rep = None      #índex que marca quina cançó s'està reproduint
        self.seleccio = None    #indica la posició de la cançó seleccionada
        self.muted = False      #indica si la música està mutejada
        
        self.dic_lang = {"ca" : 0, "es": 1, "en" : 2}   #idiomes disponibles
        self.idioma = self.dic_lang.get(kwargs.get("lang", "ca"), 0)    #selecciona com a idioma per defecte l'indicat per paràmetres o , si no s'indica res, el català

        #textos en els idiomes disponibles        
        self.text_info = (("Informació", "Aquest reproductor ha estat creat amb Python tkinter, Pygame Mixer i Mutagen.mp3"),
                          ("Información", "Este reproductor ha sido creado con Python tkinter, Pygame Mixer i Mutagen.mp3"),
                          ("Information", "This music player has been created with Python tkinter, Pygame Mixer and Mutagen.pm3"))

        self.text_about = (("Sobre Nosaltres", "Autora: Mireia Gasco\nAny: 2020\nGithub: https://github.com/mireiagasco"),
                          ("Sobre Nosotros", "Autora: Mireia Gasco\nAño: 2020\nGithub: https://github.com/mireiagasco"),
                          ("About Us", "Author: Mireia Gasco\nYear: 2020\nGithub: https://github.com/mireiagasco"))

        self.txt_er_del = (("Error", "Selecciona la cançó que vols eliminar"),
                           ("Error", "Selecciona la canción que quieres eliminar"),
                           ("Error", "Select the song you want to delete"))

        self.txt_er_inval = (("Error", "Espero que no estiguis intentant reproduir una imatge o algo així..."),
                             ("Error", "Espero que no estés intentando reproducir una imagen o algo así..."),
                             ("Error", "I hope you're not trying to listen to an image or something like that..."))

        self.txt_er_rep = (("Error", "Selecciona la cançó que vols reproduir"),
                           ("Error", "Selecciona la canción que quieres reproducir"),
                           ("Error", "Select the song you want to play"))

        self.txt_er_salt = (("Error", "Selecciona una cançó per poder passar a la següent o a la prèvia"),
                            ("Error", "Selecciona una canción para poder pasar a la siguiente o a la previa"),
                            ("Error", "Select a song in order to go to the next one or the previous one"))

        self.txt_titol = ("Reproductor de Música", "Reproductor de Música", "Music Player")
        self.txt_afegir = ("Afegir", "Añadir", "Add")
        self.txt_eliminar = ("Eliminar", "Eliminar", "Del")
        self.text_benv = ("Benvingut/da!", "Bienvenido/a!", "Welcome!")
        self.txt_rep = ("Reproductor", "Reproductor", "Player")
        self.txt_idioma = ("Idioma", "Idioma", "Language")
        self.txt_sortir = ("Sortir", "Salir", "Exit")
        self.txt_info = ("Informació", "Información", "Information")
        self.txt_vinfo = ("Veure Info", "Ver Info", "Show Info")
        self.txt_sobre = ("Sobre Nosaltres", "Sobre Nosotros", "About Us")

        #inicialitzem el reproductor
        mixer.init()

        #generem la finestra principal
        self.finestra_general = tk.ThemedTk()
        self.finestra_general.get_themes()
        self.finestra_general.set_theme("breeze")
        self.style = ttk.Style()

        self.finestra_general.title(self.txt_titol[self.idioma])
        self.finestra_general.iconbitmap(r"icones\icona_reproductor.ico")
                 
        #creem marcs per organitzar els botons
        self.marc_dret = ttk.Frame(self.finestra_general)
        self.marc_dret.pack(side = RIGHT)

        self.marc_esquerre = ttk.Frame(self.finestra_general)
        self.marc_esquerre.pack(side = LEFT)

        self.marc_superior = ttk.Frame(self.marc_dret)
        self.marc_superior.pack()

        self.marc_central = ttk.Frame(self.marc_dret)
        self.marc_central.pack()

        self.marc_inferior = ttk.Frame(self.marc_dret)
        self.marc_inferior.pack()

        #creem l'etiqueta on mostrem la benvinguda
        self.et_benv = Label(self.marc_superior, text = self.text_benv[self.idioma], font = "Gabriola 20 bold")
        self.et_benv.pack(pady = 10)

        #creem la listbox on mostrarem les cançons en cua
        self.llista = Listbox(self.marc_esquerre, height = 10, width = 25)
        self.llista.pack()

        #creem els botons d'afegir i eliminar cançons
        self.bt_afegir = ttk.Button(self.marc_esquerre, text = self.txt_afegir[self.idioma], command = self.importar_musica)
        self.bt_afegir.pack(side = LEFT)
        self.bt_eliminar = ttk.Button(self.marc_esquerre, text = self.txt_eliminar[self.idioma], command = self.eliminar_canço)
        self.bt_eliminar.pack(side = RIGHT)

        #creem el menú principal
        self.barra_menu = Menu(self.finestra_general) #creem la barra de menú
        self.finestra_general.config(menu = self.barra_menu) #la configurem per assegurar que es troba dalt de tot

        #creem els submenús
        self.canviar_idioma(self.idioma)      
       
        #creem l'etiqueta on mostrarem el nom de la cançó
        self.etiqueta_nom = Label(self.marc_superior)
        self.etiqueta_nom.pack(pady = 10)

        #creem l'etiqueta on mostrarem la durada de la cançó
        self.etiqueta_durada = Label(self.marc_superior)
        self.etiqueta_durada.pack(pady = 10)

        #carreguem les fotos que utilitzarem pels botons
        self.foto_play = PhotoImage(file = r"icones\001-play.png")
        self.foto_pause = PhotoImage(file = r"icones\002-pause.png")
        self.foto_stop = PhotoImage(file = r"icones\003-stop.png")
        self.foto_seguent = PhotoImage(file = r"icones\004-next.png")
        self.foto_previ = PhotoImage(file = r"icones\005-previous.png")
        self.foto_volum = PhotoImage(file = r"icones\volum.png")
        self.foto_mute = PhotoImage(file = r"icones\mute.png")

        #creem els botons
        ttk.Button(self.marc_central, image = self.foto_previ, command = lambda: self.saltar(opcio = 1)).grid(row = 0, column = 1, padx = 10, pady = 20)
        ttk.Button(self.marc_central, image = self.foto_pause, command = self.pause).grid(row = 0, column = 2, padx = 10, pady = 20)
        ttk.Button(self.marc_central, image = self.foto_stop, command = self.stop).grid(row = 0, column = 3, padx = 10, pady = 20)
        ttk.Button(self.marc_central, image = self.foto_play, command = self.play).grid(row = 0, column = 4, padx = 10, pady = 20)
        ttk.Button(self.marc_central, image = self.foto_seguent, command = lambda: self.saltar(opcio = 0)).grid(row = 0, column = 5, padx = 10, pady = 20)        
        self.boto_mute = ttk.Button(self.marc_inferior, image = self.foto_volum, command = self.mute)
        self.boto_mute.grid(row = 1, column = 0, padx = 20, pady = 10)

        #creem el slider del volum
        self.slider_volum = ttk.Scale(self.marc_inferior, from_ = 0, to = 100, orient = "horizontal", command = self.modif_volum)
        self.slider_volum.set(50) #establim 50 com el valor per defecte
        self.slider_volum.grid(pady = 10, column = 0, row = 0)

        #reprogramem la funció que s'executa per tancar el programa
        self.finestra_general.protocol("WM_DELETE_WINDOW", lambda: self.aturar_programa())

    #lambda que inicia el reproductor       
    iniciar = lambda self: self.finestra_general.mainloop()

    #Lambda que mostra el missatge amb la info de about us
    informacio = lambda self: tkinter.messagebox.showinfo(self.text_info[self.idioma][0], self.text_info[self.idioma][1])

    #Lambda que mostra la info sobre el reproductor
    sobre_nosaltres = lambda self: tkinter.messagebox.showinfo(self.text_about[self.idioma][0], self.text_about[self.idioma][1])

    #funció que carrega una cançó a la playlist
    def importar_musica(self):
        #obrim la finestra per buscar l'arxiu
        self.fitxer = tkinter.filedialog.askopenfilename()
        #guardem el nom de la cançó
        nom = os.path.basename(self.fitxer)
        #inserim el nom a la llista
        self.llista.insert(self.index, nom)
        #desem el path sencer a la playlist
        self.playlist.append(self.fitxer)
        self.index += 1

    #funció que elimina una cançó de la llista
    def eliminar_canço(self):
        #intentem obtenim l'índex de la cançó a eliminar        
        try:
            self.seleccio = self.llista.curselection()[0]

            #eliminem la cançó de la llista y de la listbox
            del self.playlist[self.seleccio]
            self.llista.delete(self.seleccio)

            #actualitzem la llargada de la llista
            self.index -= 1
        except IndexError:  #si no hi ha cap cançó seleccionada
            tkinter.messagebox.showerror(self.txt_er_del[self.idioma][0], self.txt_er_del[self.idioma][1])

    #funció que reprodueix una cançó i en mostra els detalls
    def mostrar_detalls_i_reproduir(self):
        
        #segons l'extensió obtenim la durada de diferents formes
        info = os.path.splitext(self.fitxer)
        if info[1] == '.wav':
            durada_total = mixer.Sound(self.fitxer).get_length()   #generem un objecte de classe Sound i n'obtenim la durada
        elif info[1] == '.mp3':
            durada_total = MP3(self.fitxer).info.length                    #generem un objecte de tipus MP3 i n'obtenim la durada
        else:
            durada_total = 0
            tkinter.messagebox.showerror(self.txt_er_inval[self.idioma][0], self.txt_er_inval[self.idioma][1])

        #si la cançó era vàlida mosrem la info i la reproduïm
        if durada_total != 0:
            #mostrem el nom
            self.etiqueta_nom['text'] = "Nom: {}".format(os.path.basename(self.fitxer))
                
            #obtenim la durda en minuts i segons i la mostrem
            min, sec = divmod(durada_total, 60)
            self.etiqueta_durada['text'] = "Total: {:02d}:{:02d}".format(int(min), int(sec))

            mixer.music.load(self.fitxer) #carreguem el fitxer que volem reproduir
            mixer.music.play() #reproduim la música

    #funció que inicia la reproducció de la cançó seleccionada
    def play(self):

        #si la música està pausada, la tornem a engegar
        if self.pausat:
            mixer.music.unpause()
            self.pausat = False
        else:
            #intentem reproduir la cançó seleccionada
            try:
                self.seleccio = self.llista.curselection()[0]
                self.fitxer = self.playlist[self.seleccio]    #la cançó seleccionada és la que es troba en la posició que ens indica curselection() en la primera posició de la tupla
                self.in_rep = self.seleccio
                self.mostrar_detalls_i_reproduir()
            except IndexError:
                tkinter.messagebox.showerror(self.txt_er_rep[self.idioma][0], self.txt_er_rep[self.idioma][1])

    #funció que para la música
    def stop(self):

        #eliminem el contingut de les etiquetes
        self.etiqueta_nom['text'] = " "
        self.etiqueta_durada['text'] = " "

        #aturem la música
        mixer.music.stop()

    #funció que pausa la música
    def pause(self):
        mixer.music.pause()
        self.pausat = True

    #funció que salta a la cançó següent o a la prèvia
    #opcio val 0 si s'ha de passar a la següent i 1 si s'ha de passar a la prèvia
    def saltar(self, opcio):
        #intentem obtenir la cançó seleccionada i, si podem, reproduim la cançó prèvia o següent segons el demanat
        try:
            sel = self.llista.curselection()[0]
            if self.seleccio != sel:
                self.in_rep, self.seleccio = sel, sel
            if opcio:
                self.previ()
            else:
                self.seguent()
            self.mostrar_detalls_i_reproduir()
        except IndexError:
            tkinter.messagebox.showerror(self.txt_er_salt[self.idioma][0], self.txt_er_salt[self.idioma][1])
    
    #funció que fa que es reprodueixi la següent cançó
    def seguent(self):
        #si la cançó seleccionada és la última de la llista
        if self.in_rep == self.index - 1:
            self.in_rep = 0
            self.fitxer = self.playlist[self.in_rep]
        else:
            self.in_rep += 1
            self.fitxer = self.playlist[self.in_rep]

    #funció que fa que es reprodueixi la següent cançó
    def previ(self):         
         #si la cançó seleccionada és la primera de la llista
        if self.in_rep == 0:
            self.in_rep = self.index - 1
            self.fitxer = self.playlist[self.in_rep]

        else:
            self.in_rep -= 1
            self.fitxer = self.playlist[self.in_rep]

    #funció que modifica el volum segons el valor del slider
    def modif_volum(self, val):
        volum = float(val) / 100
        mixer.music.set_volume(volum)

    #funció que muteja la música
    def mute(self):
        if self.muted: #tornem a activar el volum
            self.boto_mute.configure(image = self.foto_volum)
            mixer.music.set_volume(0.5)
            self.slider_volum.set(50)
            self.muted = False
        else: #mutejem la música
            self.boto_mute.configure(image = self.foto_mute)
            mixer.music.set_volume(0)
            self.slider_volum.set(0)
            self.muted = True

    #funció que canvia l'idioma del reproductor
    def canviar_idioma(self, opcio):

        self.idioma = opcio
        self.finestra_general.title(self.txt_titol[self.idioma])
        self.bt_afegir["text"] = self.txt_afegir[self.idioma]
        self.bt_eliminar["text"] = self.txt_eliminar[self.idioma]
        self.et_benv["text"] = self.text_benv[self.idioma]

        self.barra_menu.delete(0, END)
        self.submenu_reproductor = Menu(self.barra_menu, tearoff = False)  #creem el submenú on aniran tots els botons
        self.barra_menu.add_cascade(label = self.txt_rep[self.idioma], menu = self.submenu_reproductor)
        self.submenu_tema = Menu(self.submenu_reproductor, tearoff = False)
        self.submenu_reproductor.add_cascade(label = self.txt_idioma[self.idioma], menu = self.submenu_tema)
        self.submenu_tema.add_command(label = "Català", command = lambda: self.canviar_idioma(opcio = 0))
        self.submenu_tema.add_command(label = "Castellano", command = lambda: self.canviar_idioma(opcio = 1))
        self.submenu_tema.add_command(label = "English", command = lambda: self.canviar_idioma(opcio = 2))
        self.submenu_reproductor.add_command(label = self.txt_sortir[self.idioma], command = self.aturar_programa)
           
        self.submenu_info = Menu(self.barra_menu, tearoff = False)  #creem el submenú on aniran tots els botons
        self.barra_menu.add_cascade(label = self.txt_info[self.idioma], menu = self.submenu_info)
        self.submenu_info.add_command(label = self.txt_vinfo[self.idioma], command = self.informacio)
        self.submenu_info.add_command(label = self.txt_sobre[self.idioma], command = self.sobre_nosaltres)        
      
    #funció que tanca el programa
    def aturar_programa(self):
        #aturem la música
        self.stop()
        #obtenim la finestra general i la tanquem
        self.finestra_general.destroy()
