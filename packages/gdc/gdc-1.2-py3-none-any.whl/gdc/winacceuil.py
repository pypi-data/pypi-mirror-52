##################################
# Auteur : Christophe Palmann
# Licence : BSD-2-Clause
##################################

#coding:utf-8
import tkinter as tk
from tkinter import messagebox
from os.path import join

from .config import *
from .computestats import *

from os.path import dirname,realpath

class Accueil:
    def __init__(self,master):

        self._master = master

        #frame
        self.frame_acceuil=tk.Frame(self._master,bg=config["couleur"])
        
        # texte d'accueil
        self._label_title = tk.Label(self.frame_acceuil,text="Gestion des compétences",font=("Courrier",40),bg=config["couleur"],fg='white')

        # creation d'une image
        self._width = 370
        self._height = 370
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._logo = tk.PhotoImage(file=join(dir_path,"logo.png"))#.zoom(35).subsample(32)
        self._canvas = tk.Canvas(self.frame_acceuil, width=self._width, height=self._height,bg=config["couleur"])#,bd=0,highlightthickness=0)
        self._canvas.create_image(self._width/2,self._height/2,image=self._logo)
        
        # frame classe
        self._frame_classes=tk.Frame(self.frame_acceuil,bg=config["couleur"])

        # bouton creer/ modifier classe
        self._button_creer_classe = tk.Button(self._frame_classes,text="   Créer/modifier classe    ",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_classroom_func)

        # bouton supprimer classe
        self._button_rm_classe = tk.Button(self._frame_classes,text="Supprimer classe",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_rmclassroom_func)

        # frame évaluations
        self._frame_evaluations=tk.Frame(self.frame_acceuil,bg=config["couleur"])
        
        # bouton creer/ modifier évaluation
        self._button_new_eval = tk.Button(self._frame_evaluations,text="Créer/modifier évaluation ",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_eval_func)

        # bouton supprimer évaluation
        self._button_rm_eval = tk.Button(self._frame_evaluations,text="Supprimer évaluation",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_rmeval_func)

        # frame_cptces
        self._frame_cptces=tk.Frame(self.frame_acceuil,bg=config["couleur"])

        # bouton ajouter cptces
        self._button_add_cptces = tk.Button(self._frame_cptces,text="    Ajouter compétences   ",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_cptces_func)

        # frame_bilans
        self.frame_bilans=tk.Frame(self.frame_acceuil,bg=config["couleur"])
        
        # bouton bilan trimestriel
        self._button_bilans_trim = tk.Button(self.frame_bilans,text="      Bilans trimestriels      ",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._compute_all_stats)

        # frame_misc
        self._frame_misc=tk.Frame(self.frame_acceuil,bg=config["couleur"])

        # bouton config
        self._button_winconfig = tk.Button(self._frame_misc,text="         Configuration          ",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_config_func)

    def gridall(self):
        self.frame_acceuil.pack(expand=tk.YES,fill=tk.Y)
        self._label_title.grid(row=0,column=0,columnspan=2,pady=50)
        self._canvas.grid(row=1,column=0,rowspan=5,padx=150)
        self._frame_classes.grid(row=1,column=1,pady=10,sticky=tk.W+tk.E)
        self._button_creer_classe.grid(row=0,column=0,sticky=tk.W+tk.E)
        self._button_rm_classe.grid(row=1,column=0,sticky=tk.W+tk.E)
        self._frame_evaluations.grid(row=2,column=1,pady=10,sticky=tk.W+tk.E)
        self._button_new_eval.grid(row=0,column=0,sticky=tk.W+tk.E)
        self._button_rm_eval.grid(row=1,column=0,sticky=tk.W+tk.E)
        self._frame_cptces.grid(row=3,column=1,pady=10,sticky=tk.W+tk.E)
        self._button_add_cptces.grid(row=0,column=0,sticky=tk.W+tk.E)
        self.frame_bilans.grid(row=4,column=1,pady=10,sticky=tk.W+tk.E)
        self._button_bilans_trim.grid(row=1,column=0,columnspan=3,sticky=tk.W+tk.E)
        self._frame_misc.grid(row=5,column=1,pady=10,sticky=tk.W+tk.E)
        self._button_winconfig.grid(row=1,column=0,sticky=tk.W+tk.E)

    def register_frame_classroom(self,frame_classroom):
        self._frame_classroom = frame_classroom

    def register_frame_rmclassroom(self,frame_rmclassroom):
        self._frame_rmclassroom = frame_rmclassroom

    def register_frame_eval(self,frame_eval):
        self._frame_eval = frame_eval

    def register_lstbox_cptces(self,lstbox_cptces):
        self._lstbox_cptces = lstbox_cptces

    def register_frame_rmeval(self,frame_rmeval):
        self._frame_rmeval = frame_rmeval
        
    def register_frame_config(self,frame_config):
        self._frame_config = frame_config
        
    def register_frame_cptces(self,frame_cptces):
        self._frame_cptces = frame_cptces
        
    def register_IntVar(self,iv):
        self._v = iv

    def _frame_classroom_func(self):
        self.frame_acceuil.pack_forget()
        self._frame_classroom.pack(expand=tk.YES,fill=tk.Y)

    def _frame_rmclassroom_func(self):
        self.frame_acceuil.pack_forget()
        self._frame_rmclassroom.pack(expand=tk.YES,fill=tk.Y)

    def _frame_eval_func(self):
        self.frame_acceuil.pack_forget()
        self._frame_eval.pack(expand=tk.YES,fill=tk.Y)
        while self._lstbox_cptces.size()>0:
            self._lstbox_cptces.delete(0)

    def _frame_rmeval_func(self):
        self.frame_acceuil.pack_forget()
        self._frame_rmeval.pack(expand=tk.YES,fill=tk.Y)
        
    def _frame_config_func(self):
        self.frame_acceuil.pack_forget()
        self._frame_config.pack(expand=tk.YES,fill=tk.Y)
        
    def _frame_cptces_func(self):
        self.frame_acceuil.pack_forget()
        self._frame_cptces.pack(expand=tk.YES,fill=tk.Y)

    def _compute_all_stats(self):
        trim = "T"+str(self._v.get())
        WSevals = StatsComputer( join(config["root"],config["NOKdir"]), trim )
        if WSevals.nbevals[trim] > 0:
            WSevals.all_stats_mp()
            tk.messagebox.showinfo(title="Bilans trimestriels",message="Bilans terminés")
        else:
            tk.messagebox.showerror(title="Bilans trimestriels",message="Aucune évaluation trouvée pour le trimestre %i." % self._v.get())
        
