#Arxiu que conté la classe reproductor
from pygame import mixer
from funcions_reproductor import *
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk


#   classe reproductor: inicialitza un reproductor de música (pot rebre el nom com a paràmetre) i conté la funció que 
#   inicia el loop principal de la finestra de tkinter
class Reproductor:
    def __init__(self, *args, **kwargs):
        #inicialitzem el reproductor
        mixer.init()

        #generem la finestra principal
        self.finestra_general = tk.ThemedTk()
        self.finestra_general.get_themes()
        self.finestra_general.set_theme("breeze")

        self.finestra_general.title(kwargs.get("nom", "Reproductor de Música"))
        self.finestra_general.iconbitmap(r"icones\icona_reproductor.ico")

         #creem el menú principal
        self.barra_menu = Menu(self.finestra_general) #creem la barra de menú
        self.finestra_general.config(menu = self.barra_menu) #la configurem per assegurar que es troba dalt de tot

        #creem el submenú "reproductor"
        self.submenu_reproductor = Menu(self.barra_menu, tearoff = False)  #creem el submenú on aniran tots els botons
        self.barra_menu.add_cascade(label = "Reproductor", menu = self.submenu_reproductor)
        self.submenu_reproductor.add_command(label = "Importar música", command = lambda: switch(accio = 0, listbox = self.llista))
        self.submenu_reproductor.add_command(label = "Sortir", command = lambda: switch(accio = 1, nom = self.etiqueta_nom, durada = self.etiqueta_durada, finestra = self.finestra_general))

         #creem el submenú "ajuda"
        self.submenu_info = Menu(self.barra_menu, tearoff = False)  #creem el submenú on aniran tots els botons
        self.barra_menu.add_cascade(label = "Informació", menu = self.submenu_info)
        self.submenu_info.add_command(label = "Veure info", command = informacio)
        self.submenu_info.add_command(label = "Sobre Nosaltres", command = sobre_nosaltres)

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
        self.etiqueta_benvinguda = Label(self.marc_superior, text = "Benvingut/da!", font = "Gabriola 20 bold")
        self.etiqueta_benvinguda.pack(pady = 10)

        #creem la listbox on mostrarem les cançons en cua
        self.llista = Listbox(self.marc_esquerre, height = 10, width = 25)
        self.llista.pack()

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
        self.boto_previ = ttk.Button(self.marc_central, image = self.foto_previ, command = lambda: switch(accio = 5, list = self.llista, nom = self.etiqueta_nom, durada = self.etiqueta_durada, previ = True))
        self.boto_previ.grid(row = 0, column = 1, padx = 10, pady = 20)

        self.boto_pause = ttk.Button(self.marc_central, image = self.foto_pause, command = lambda: switch(accio = 4))
        self.boto_pause.grid(row = 0, column = 2, padx = 10, pady = 20)

        self.boto_stop = ttk.Button(self.marc_central, image = self.foto_stop, command = lambda: switch(accio = 3, nom = self.etiqueta_nom, durada = self.etiqueta_durada))
        self.boto_stop.grid(row = 0, column = 3, padx = 10, pady = 20)

        self.boto_play = ttk.Button(self.marc_central, image = self.foto_play, command = lambda: switch(accio = 2, list = self.llista, nom = self.etiqueta_nom, durada = self.etiqueta_durada))
        self.boto_play.grid(row = 0, column = 4, padx = 10, pady = 20)

        self.boto_seguent = ttk.Button(self.marc_central, image = self.foto_seguent, command = lambda: switch(accio = 5, list = self.llista, nom = self.etiqueta_nom, durada = self.etiqueta_durada, seguent = True))
        self.boto_seguent.grid(row = 0, column = 5, padx = 10, pady = 20)

        self.boto_mute = ttk.Button(self.marc_inferior, image = self.foto_volum, command = lambda: mute(self.boto_mute, self.foto_mute, self.foto_volum, self.slider_volum))
        self.boto_mute.grid(row = 1, column = 0, padx = 20, pady = 10)

        self.boto_afegir = ttk.Button(self.marc_esquerre, text = " Afegir ", command = lambda: switch(accio = 0, listbox = self.llista))
        self.boto_afegir.pack(side = LEFT)

        self.boto_eliminar = ttk.Button(self.marc_esquerre, text = "Eliminar", command = lambda: switch(accio = 6, listbox = self.llista))
        self.boto_eliminar.pack(side = RIGHT)

         #creem el slider del volum
        self.slider_volum = ttk.Scale(self.marc_inferior, from_ = 0, to = 100, orient = "horizontal", command = modif_volum)
        self.slider_volum.set(50) #establim 50 com el valor per defecte
        self.slider_volum.grid(pady = 10, column = 0, row = 0)

        dic = {"nom": self.etiqueta_nom, "durada": self.etiqueta_durada, "finestra": self.finestra_general}
        self.finestra_general.protocol("WM_DELETE_WINDOW", lambda: aturar_programa(dic))
        
    def iniciar_reproduccio(self):
        self.finestra_general.mainloop()
