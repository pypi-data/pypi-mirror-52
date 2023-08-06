##################################
# Auteur : Christophe Palmann
# Licence : BSD-2-Clause
##################################

#coding:utf-8
import tkinter as tk
from tkinter.ttk import Combobox
from .config import *
from .utils import write_json

class Configuration:
    def __init__(self,master):

        self._master = master

        #frame
        self.frame_config=tk.Frame(self._master,bg=config["couleur"])
        
        # choix de comparer l'élève à la classe ou non
        mess = " Souhaitez-vous produire des bilans élèves en version PROFESSEUR, \n en version ELEVE, ou bien LES DEUX (production des pdf plus coûteuse en temps de calcul) ? "
        self._label_info_bilaneleve = tk.Label(self.frame_config,text=mess,font=("Courrier",11),bg="white",fg='black',bd=1,relief=tk.SUNKEN)
        
        self._combo_bilaneleve = Combobox(self.frame_config,font=("Courrier",11))
        self._combo_bilaneleve.bind("<<ComboboxSelected>>",self._update_cfg)
        self._combo_bilaneleve["values"]=("Version professeur","Version élève","Les deux")
        if config["version_bilan_eleve"]=="prof":
            self._combo_bilaneleve.current(0)
        if config["version_bilan_eleve"]=="eleve":
            self._combo_bilaneleve.current(1)
        if config["version_bilan_eleve"]=="both":
            self._combo_bilaneleve.current(2)
            
        # récupération des listes d'élèves soit par scolinfo soit par ecole directe
        mess = " Récupérez-vous vos listes d'élèves par SCOLINFO ou par ECOLE DIRECTE ? "
        self._label_info_xlstype = tk.Label(self.frame_config,text=mess,font=("Courrier",11),bg="white",fg='black',bd=1,relief=tk.SUNKEN)
        
        self._combo_xlstype = Combobox(self.frame_config,font=("Courrier",11))
        self._combo_xlstype.bind("<<ComboboxSelected>>",self._update_cfg)
        self._combo_xlstype["values"]=("Scolinfo","Ecole directe")
        if config["xlstype"]=="scolinfo":
            self._combo_xlstype.current(0)
        if config["xlstype"]=="ecoledirecte":
            self._combo_xlstype.current(1)

        # texte d'accueil
        self._label_title = tk.Label(self.frame_config,text="Configuration",font=("Courrier",40),bg=config["couleur"],fg='white')
        
        # bouton retour
        self._button_return = tk.Button(self.frame_config,text="Retour",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_acceuil_func)

        
    def gridall(self):
        self._label_title.grid(row=0,column=0,columnspan=3,pady=50)
        self._label_info_bilaneleve.grid(row=1,column=0,columnspan=2,padx=10,pady=15,sticky=tk.W+tk.E)
        self._combo_bilaneleve.grid(row=1,column=2,padx=10,pady=15,sticky=tk.W+tk.E)
        self._label_info_xlstype.grid(row=2,column=0,columnspan=2,padx=10,pady=15,sticky=tk.W+tk.E)
        self._combo_xlstype.grid(row=2,column=2,padx=10,pady=15,sticky=tk.W+tk.E)
        self._button_return.grid(row=3,column=0,padx=10,pady=25,sticky=tk.W+tk.E)
        
    def register_frame_acceuil(self,frame_acceuil):
        self._frame_acceuil = frame_acceuil
        
    def _frame_acceuil_func(self):
        self.frame_config.pack_forget()
        self._frame_acceuil.pack(expand=tk.YES,fill=tk.Y)
        
    def _update_cfg(self,event):
        # versions des bilans élèves
        if self._combo_bilaneleve.get() == "Version professeur":
            config["version_bilan_eleve"] = "prof"
        if self._combo_bilaneleve.get() == "Version élève":
            config["version_bilan_eleve"] = "eleve"
        if self._combo_bilaneleve.get() == "Les deux":
            config["version_bilan_eleve"] = "both"
        
        # xls de type scolinfo ou école directe    
        if self._combo_xlstype.get() == "Scolinfo":
            config["xlstype"] = "scolinfo"
        if self._combo_xlstype.get() == "Ecole directe":
            config["xlstype"] = "ecoledirecte"
		
        write_json(config,user_cfg_path)

