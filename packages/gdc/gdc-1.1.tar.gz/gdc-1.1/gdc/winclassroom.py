##################################
# Auteur : Christophe Palmann
# Licence : BSD-2-Clause
##################################

#coding:utf-8
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
import xlrd
from os.path import join,exists
from .utils import *
from .config import *


class Classroom:
        def __init__(self,master):

                self._master = master
                
                #frame
                self.frame_classroom=tk.Frame(self._master,bg=config["couleur"])
                
                # texte d'accueil
                self._label_title= tk.Label(self.frame_classroom,text="Nouvelle classe",font=("Courrier",40),bg=config["couleur"],fg='white')    
                
                # Simple message d'information
                mess = " La liste des élèves d'une classe doit être récupérée depuis un fichier xls fourni par Ecole Directe ou bien Scolinfo.\n" + \
                "Remarque : pensez à indiquer la provenance de ce fichier dans la fenêtre de configuration."
                self._label_info = tk.Label(self.frame_classroom,text=mess,font=("Courrier",11),bg="white",fg='black',bd=1,relief=tk.SUNKEN)
                
                # selection du niveau
                self._combo_niveau = ttk.Combobox(self.frame_classroom)
                self._combo_niveau["values"]=("6ème","5ème","4ème","3ème")
                self._combo_niveau.current(0)

                # selection du nom
                self._combo_nom = ttk.Combobox(self.frame_classroom,height=16)
                self._combo_nom["values"]=("A","B","C","D","E","F","G","H","1","2","3","4","5","6","7","8")
                self._combo_nom.current(0)

                # bouton ouvrir liste noms
                self._button_noms = tk.Button(self.frame_classroom,text="Importer noms",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._new_class_grab_names)

                # bouton retour
                self._button_return = tk.Button(self.frame_classroom,text="Retour",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_acceuil_func)

        def gridall(self):
                self._label_title.grid(row=0,column=0,columnspan=2,pady=50)
                self._label_info.grid(row=1,column=0,columnspan=2,pady=50)
                self._combo_niveau.grid(row=2,column=0,pady=50,padx=20)
                self._combo_nom.grid(row=2,column=1,pady=50,padx=20)
                self._button_noms.grid(row=3,column=0,padx=10,pady=50,sticky=tk.W+tk.E+tk.N+tk.S)
                self._button_return.grid(row=3,column=1,padx=10,pady=50,sticky=tk.W+tk.E)

        def register_frame_acceuil(self,frame_acceuil):
                self._frame_acceuil = frame_acceuil

        def _frame_acceuil_func(self):
                self.frame_classroom.pack_forget()
                self._frame_acceuil.pack(expand=tk.YES,fill=tk.Y)

        def _make_classe_path(self):
                classe_name = config["convert"][self._combo_niveau.get()] +'-'+ self._combo_nom.get() + '.json'
                return join(config["root"],config["NOKdir"],classe_name)

        def _save_class(self,filename,data):
                write_json(data,filename)

        def _grab_names(self,filename):
                data=list()

                #Ouverture du fichier via une boite de dialogue
                liste_noms= askopenfilename(initialdir = join("C:","Users","Utilisateur","Downloads"),title = "Sélectionner un fichier xls",filetypes = (("Fichier xls","*.xls"),("Tout type","*.*")))
                try:
                        workbook = xlrd.open_workbook(liste_noms)
                        worksheet = workbook.sheet_by_index(0)
                except:
                        tk.messagebox.showerror(title="Erreur ouverture fichier xls",message="Problème lors de l'ouverture du fichier xls.")
                else:
                        # Récupération des noms et prénoms version scolinfo
                        if config["xlstype"] == "scolinfo":
                            i=7
                            while worksheet.cell(i,3).value != "":
                                    data.append(worksheet.cell(i,3).value + ' ' + worksheet.cell(i,8).value)
                                    i+=1
                                    
                        # Récupération des noms et prénoms version ecoledirecte
                        if config["xlstype"] == "ecoledirecte":
                            for i in range(7,worksheet.nrows):
                                data.append(worksheet.cell(i,0).value)
                                    
                return data
                

        def _new_class_grab_names(self):
                classe_path = self._make_classe_path()

                grab = True
                if exists(classe_path):
                        grab = tk.messagebox.askyesno(title="Remplacer classe existante",message="Cette classe est déjà dans la base de données; voulez-vous la remplacer ?")

                if grab :
                        data = self._grab_names(classe_path)#,new_class_combo_discipline.get())
                        if len(data)>0:
                                mess = "Nombre d'élèves dans la classe = %i \nPremier élève : %s  Dernier élève : %s \n\n" % (len(data),data[0],data[-1])
                                mess = mess + "Si ces informations sont correctes, cliquez sur Ok. Sinon, cliquez sur Annuler"
                                ok_save_class=tk.messagebox.askokcancel(title="Ouverture du fichier .xls",message=mess)
                                if ok_save_class:
                                        self._save_class(classe_path,data)
                        else:
                                mess = "Échec / abandon de l'ouverture du fichier .xls"
                                tk.messagebox.showerror(title="Ouverture du fichier .xls",message=mess)
                
        
class Rmclassroom:
        def __init__(self,master):

                self._master = master
                
                #frame
                self.frame_rmclassroom=tk.Frame(self._master,bg=config["couleur"])

                # texte d'accueil
                self._label_title = tk.Label(self.frame_rmclassroom,text="Supprimer une classe",font=("Courrier",40),bg=config["couleur"],fg='white')

                # selection du niveau
                self._combo_niveau = ttk.Combobox(self.frame_rmclassroom)
                self._combo_niveau["values"]=("6ème","5ème","4ème","3ème")
                self._combo_niveau.current(0)

                # selection du nom
                self._combo_nom = ttk.Combobox(self.frame_rmclassroom,height=16)
                self._combo_nom["values"]=("A","B","C","D","E","F","G","H","1","2","3","4","5","6","7","8")
                self._combo_nom.current(0)

                # bouton supprimer
                self._button_rmclass = tk.Button(self.frame_rmclassroom,text="Supprimer",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._rm_classroom)

                # bouton retour
                self._button_return = tk.Button(self.frame_rmclassroom,text="Retour",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_acceuil_func)

        def gridall(self):
                self._label_title.grid(row=0,column=0,columnspan=2,pady=50)
                self._combo_niveau.grid(row=1,column=0,pady=50,padx=20)
                self._combo_nom.grid(row=1,column=1,pady=50,padx=20)
                self._button_rmclass.grid(row=2,column=0,padx=10,sticky=tk.W+tk.E)
                self._button_return.grid(row=2,column=1,padx=10,sticky=tk.W+tk.E)

        def register_frame_acceuil(self,frame_acceuil):
                self._frame_acceuil = frame_acceuil

        def _frame_acceuil_func(self):
                self.frame_rmclassroom.pack_forget()
                self._frame_acceuil.pack(expand=tk.YES,fill=tk.Y)

        def _grab_levname(self,list_cond,path):
                return grab_files_by_name([list_cond[0]+"-"+list_cond[1]],path)

        def _rm_classroom(self):
                lst_files = self._grab_levname([config["convert"][self._combo_niveau.get()],self._combo_nom.get()],join(config["root"]))
                if len(lst_files)==0:
                        tk.messagebox.showerror(title="Supprimer classe",message="Pas de classe à supprimer")
                else :
                        supp = tk.messagebox.askyesno(title="Supprimer classe", message="Êtes-vous sûr(e) de vouloir effacer la classe de %s ? \n\nCela supprimera aussi les fichiers liés : évaluations, comptes-rendus..." \
                                                      % (self._combo_niveau.get()+' '+self._combo_nom.get()))
                        if supp :
                                mess= "Les fichiers suivants ont été supprimés : \n"
                                for f in lst_files:
                                        os.remove(f)
                                        mess += f + "\n"
                                tk.messagebox.showinfo(title="Supprimer classe",message=mess)
                        else :
                                tk.messagebox.showinfo(title="Supprimer classe",message="Suppression annulée")



