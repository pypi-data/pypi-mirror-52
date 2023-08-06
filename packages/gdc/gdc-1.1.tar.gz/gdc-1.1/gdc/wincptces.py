##################################
# Auteur : Christophe Palmann
# Licence : BSD-2-Clause
##################################

#coding:utf-8
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from os.path import join,exists
from .utils import *
from .config import *


class Cptces:
        def __init__(self,master):

                self._master = master
                
                #frame
                self.frame_cptces=tk.Frame(self._master,bg=config["couleur"])
                
                # texte d'accueil
                self._label_title= tk.Label(self.frame_cptces,text="Importer des compétences",font=("Courrier",40),bg=config["couleur"],fg='white')    

                # Simple message d'information
                mess = " Veuillez indiquer votre discipline et ainsi qu'un fichier xls contenant les compétences associées.\n" + \
                "Remarque : si des compétences sont déjà présentes dans la base de données, cette opération les remplacera."
                self._label_info = tk.Label(self.frame_cptces,text=mess,font=("Courrier",11),bg="white",fg='black',bd=1,relief=tk.SUNKEN)
                
                # selection de la discipline
                self._combo_disc = ttk.Combobox(self.frame_cptces)
                self._combo_disc["values"]=("Anglais","Arts plastiques","E.P.S.","Espagnol","Français","Histoire-géographie","Mathématiques","Musique","Physique-Chimie","S.V.T.","Technologie")
                self._combo_disc.current(0)

                # bouton ouvrir xls
                self._button_xls = tk.Button(self.frame_cptces,text="Importer des compétences",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._load_cptces)

                # bouton retour
                self._button_return = tk.Button(self.frame_cptces,text="Retour",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_acceuil_func)

        def gridall(self):
                self._label_title.grid(row=0,column=0,columnspan=2,pady=50)
                self._label_info.grid(row=1,column=0,columnspan=2,pady=50,padx=20)
                self._combo_disc.grid(row=2,column=0,columnspan=2,pady=50,padx=20)
                self._button_xls.grid(row=3,column=0,padx=10,pady=50,sticky=tk.W+tk.E+tk.N+tk.S)
                self._button_return.grid(row=3,column=1,padx=10,pady=50,sticky=tk.W+tk.E)

        def register_frame_acceuil(self,frame_acceuil):
                self._frame_acceuil = frame_acceuil

        def _frame_acceuil_func(self):
                self.frame_cptces.pack_forget()
                self._frame_acceuil.pack(expand=tk.YES,fill=tk.Y)

        def _make_cptces_path(self):
                cptces_path = "cptces_" + config["shortcuts"][self._combo_disc.get()] + '.json'
                return join(config["root"],config["NOKdir"],cptces_path)

        def _load_cptces(self):
            cptces_path = self._make_cptces_path()
            xls_path= askopenfilename(title = "Sélectionner un fichier xls",filetypes = (("Fichier xls","*.xls"),("Tout type","*.*")))
            try:
                flag = read_cptcpes_from_xlsfiles(xls_path,cptces_path)
                if flag == 0:
                    tk.messagebox.showinfo(title="Importation des compétences",message="Les compétences ont bien été importées.")
                else:
                    if flag == -1:
                        cycle = "cycle 3"
                    else :
                        cycle = "cycle 4"
                    tk.messagebox.showinfo(title="Importation des compétences",message="Les clés de la colonne B ne sont pas uniques (voir %s)" % cycle)
                    
            except:
                tk.messagebox.showerror(title="Erreur ouverture fichier xls",message="Problème lors de l'ouverture du fichier xls.")
