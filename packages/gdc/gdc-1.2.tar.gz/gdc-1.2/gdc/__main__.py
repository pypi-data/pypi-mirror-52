##################################
# Auteur : Christophe Palmann
# Licence : BSD-2-Clause
##################################

import tkinter as tk
from tkinter import messagebox
from sys import exit

from .winacceuil import *
from .winclassroom import *
from .winevals import *
from .winconfig import *
from .wincptces import *
from .init import initfct

#coding:utf-8
def main(args=None):

    # initialisation de l'arborescence
    initfct()

    # fenetre principale
    mainwin = tk.Tk()

    # personalisation
    mainwin.title("Gestion des compétences (GDC V1.2)")
    mainwin.geometry("1350x695+0+0")
    mainwin.minsize(1350,695)
    menubar = tk.Menu(mainwin)
    menufichier = tk.Menu(menubar,tearoff = 0)
    menubar.add_cascade(label="À propos", menu=menufichier)
    menufichier.add_command(label="Auteur : Christophe Palmann (cpn.math@gmail.com)")
    menufichier.add_command(label="Licence : BSD-2-Clause")
    mainwin.config(background=config["couleur"],menu=menubar)

    # instanciation des classes
    acceuil = Accueil(mainwin)
    acceuil.gridall()

    winclassroom = Classroom(mainwin)
    winclassroom.gridall()

    rmclassroom = Rmclassroom(mainwin)
    rmclassroom.gridall()

    evaluation = Eval(mainwin)
    evaluation.gridall()

    rmevaluation = Rmeval(mainwin)
    rmevaluation.gridall()
    
    configuration = Configuration(mainwin)
    configuration.gridall()
    
    competences = Cptces(mainwin)
    competences.gridall()

    # transitions et interactions entre frames
    acceuil.register_frame_classroom(winclassroom.frame_classroom)
    acceuil.register_frame_rmclassroom(rmclassroom.frame_rmclassroom)
    acceuil.register_frame_eval(evaluation.frame_eval)
    acceuil.register_lstbox_cptces(evaluation.lstbox_cptces)
    acceuil.register_frame_rmeval(rmevaluation.frame_rmeval)
    acceuil.register_frame_config(configuration.frame_config)
    acceuil.register_frame_cptces(competences.frame_cptces)

    winclassroom.register_frame_acceuil(acceuil.frame_acceuil)
    rmclassroom.register_frame_acceuil(acceuil.frame_acceuil)
    evaluation.register_frame_acceuil(acceuil.frame_acceuil)
    rmevaluation.register_frame_acceuil(acceuil.frame_acceuil)
    configuration.register_frame_acceuil(acceuil.frame_acceuil)
    competences.register_frame_acceuil(acceuil.frame_acceuil)
    
    # Radiobuttons pour sélectionner le trimestre courant
    v = tk.IntVar()
    v.set(1)
    rb1 = ttk.Radiobutton(acceuil.frame_bilans, text="Trimestre 1", variable=v, value=1)
    rb2 = ttk.Radiobutton(acceuil.frame_bilans, text="Trimestre 2", variable=v, value=2)
    rb3 = ttk.Radiobutton(acceuil.frame_bilans, text="Trimestre 3", variable=v, value=3)
    rb1.grid(row=0,column=0,sticky=tk.W+tk.E)
    rb2.grid(row=0,column=1,sticky=tk.W+tk.E)
    rb3.grid(row=0,column=2,sticky=tk.W+tk.E)
    acceuil.register_IntVar(v)

    # fermeture propre de l'application
    def on_closing():
        if tk.messagebox.askokcancel(title="Terminer l'application",message="Voulez-vous quitter l'application ?"):
            mainwin.destroy()
            exit()
    mainwin.protocol("WM_DELETE_WINDOW",on_closing)

    # lancement de l'application
    mainwin.mainloop()

if __name__ == "__main__":
    main()
