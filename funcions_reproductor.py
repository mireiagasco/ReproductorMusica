#Arxiu que conté les funcions que executen les diferents accions del reproductor
import tkinter.messagebox
from pygame import mixer
from os import *
from mutagen.mp3 import MP3
import threading
import time

#Lambda que mostra el missatge amb la informació
sobre_nosaltres = lambda: tkinter.messagebox.showinfo("Informació", "Aquest reproductor ha estat creat amb Python tkinter")