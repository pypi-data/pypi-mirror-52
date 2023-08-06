##################################
# Auteur : Christophe Palmann
# Licence : BSD-2-Clause
##################################

#coding:utf-8
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import os.path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .config import *
from .utils import *
from .setbuttonsclass import *


class Eval:
    def __init__(self,master):
        
        self._master = master

        #frame
        self.frame_eval=tk.Frame(self._master,bg=config["couleur"])

        # texte d'accueil
        self._label_title= tk.Label(self.frame_eval,text="Nouvelle évaluation",font=("Courrier",40),bg=config["couleur"],fg='white')

        # selection de la discipline
        self._combo_discipline = ttk.Combobox(self.frame_eval,height=11)
        self._combo_discipline["values"]=("Anglais","Arts plastiques","E.P.S.","Espagnol","Français","Histoire-géographie","Mathématiques","Musique","Physique-Chimie","S.V.T.","Technologie")
        self._combo_discipline.current(0)
        self._combo_discipline.bind("<<ComboboxSelected>>",self._label_info_update_and__reset_lstbox_cptces)

        # selection du niveau
        self._combo_niveau = ttk.Combobox(self.frame_eval)
        self._combo_niveau["values"]=("6ème","5ème","4ème","3ème")
        self._combo_niveau.current(0)
        self._combo_niveau.bind("<<ComboboxSelected>>",self._label_info_update_and__reset_lstbox_cptces)

        # selection du nom
        self._combo_nom = ttk.Combobox(self.frame_eval,height=16)
        self._combo_nom["values"]=("A","B","C","D","E","F","G","H","1","2","3","4","5","6","7","8")
        self._combo_nom.current(0)
        self._combo_nom.bind("<<ComboboxSelected>>",self._label_info_update_func)

        # selection du trimestre
        self._combo_trim = ttk.Combobox(self.frame_eval,height=3)
        self._combo_trim["values"]=("T1","T2","T3")
        self._combo_trim.current(0)
        self._combo_trim.bind("<<ComboboxSelected>>",self._label_info_update_func)

        # selection du numéro de l'eval
        self._combo_numeval = ttk.Combobox(self.frame_eval,height=10)
        self._combo_numeval["values"]=("eval1","eval2","eval3","eval4","eval5","eval6","eval7","eval8","eval9","eval10")
        self._combo_numeval.current(0)

        # listbox pour les compétences et défilement horizontal et vertical
        self._yDefilB = tk.Scrollbar(self.frame_eval, orient='vertical')
        self._xDefilB = tk.Scrollbar(self.frame_eval, orient='horizontal')
        self.lstbox_cptces = tk.Listbox(self.frame_eval,xscrollcommand=self._xDefilB.set,yscrollcommand=self._yDefilB.set,activestyle=tk.DOTBOX,selectmode='multiple',font=("Courrier",10),width=100)
        self._xDefilB['command'] = self.lstbox_cptces.xview
        self._yDefilB['command'] = self.lstbox_cptces.yview

        # bouton afficher compétences
        self._disp_cptces = tk.Button(self.frame_eval,text="Afficher les\ncompétences",font=("Courrier",12),bg='white',fg=config["couleur"],command=self._new_eval_fill_cptces)

        # bouton suivant
        self._button_next = tk.Button(self.frame_eval,text="Suivant",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_next_func)

        # bouton retour
        self._button_return = tk.Button(self.frame_eval,text="Retour",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_acceuil_func)

        # message d'information
        self._label_info_v = tk.StringVar()
        self._label_info = tk.Label(self.frame_eval,textvariable=self._label_info_v,font=("Courrier",10),bg="white",fg='black',bd=1,relief=tk.SUNKEN,width=90)	
        self._label_info_v.set("\n\n")
        self._label_info_update_func(None)

        ###next
        self._frame_lst_next=list()
        self._frame_lst_next.append(tk.Frame(self._master,bg=config["couleur"]))
        self._next_lst_combo_names = list()
        self._next_lst_combo_names.append(ttk.Combobox(self._frame_lst_next[0],height=10))
        self._next_lst_setbuttons = list()
        
    def gridall(self):
        self._label_title.grid(row=0,column=0,columnspan=6,pady=25)
        self._combo_discipline.grid(row=1,column=0,pady=50,padx=10)
        self._combo_niveau.grid(row=1,column=1,pady=50,padx=10)
        self._combo_nom.grid(row=1,column=2,pady=50,padx=10)
        self._combo_trim.grid(row=1,column=3,pady=50,padx=10)
        self._combo_numeval.grid(row=1,column=4,pady=50,padx=10)
        self.lstbox_cptces.grid(row=2,column=0,columnspan=6,sticky=tk.W+tk.E)
        self._xDefilB.grid(row=3, column=0, columnspan=6, sticky=tk.W+tk.E)
        self._yDefilB.grid(row=2, column=6, sticky=tk.N+tk.S)
        self._disp_cptces.grid(row=1,column=5,pady=50,padx=10,sticky=tk.W+tk.E)
        self._button_next.grid(row=4,column=0,padx=10,pady=50,sticky=tk.W+tk.E)
        self._button_return.grid(row=4,column=1,padx=10,pady=50,sticky=tk.W+tk.E)
        self._label_info.grid(row=4,column=2,columnspan=4,padx=10,pady=50,sticky=tk.W+tk.E)

    def register_frame_acceuil(self,frame_acceuil):
        self._frame_acceuil = frame_acceuil

    def _frame_acceuil_func(self):
        self.frame_eval.pack_forget()
        self._label_info_update_and__reset_lstbox_cptces(None)
        self._frame_acceuil.pack(expand=tk.YES,fill=tk.Y)

    def _frame_eval_to_frame_next(self):
        self.frame_eval.pack_forget()
        self._frame_lst_next[0].pack(expand=tk.YES,fill=tk.Y)

    def _frame_next_to_frame_accueil(self):
        self._label_info_update_and__reset_lstbox_cptces(None)
        self._frame_lst_next[0].pack_forget()
        
        self._frame_acceuil.pack(expand=tk.YES,fill=tk.Y)

    def _reset_lstbox_cptces(self):
        while self.lstbox_cptces.size()>0:
            self.lstbox_cptces.delete(0)        

    def _frame_next_func(self):
        """
        Fonction appelée par le bouton suivant
        Lance l'affichage de la frame next si les conditions sont réunies
        """
        index_cptces=self.lstbox_cptces.curselection()
        if len(index_cptces)==0:
                tk.messagebox.showerror(title="Compétences sélectionnées",message="Vous n'avez sélectionné aucune compétence")
        else:
                classe_path = self._make_classe_path()
                if not os.path.exists(classe_path):
                        tk.messagebox.showerror(title="Classe inconnue",message="La classe que vous souhaitez évaluer n'existe pas.")
                else:
                        lst_keys=list()
                        mess = "Vous avez choisi les compétences suivantes:\n\n"
                        for i in index_cptces:
                                lst_keys.append(self.lstbox_cptces.get(i).split()[0])
                                mess += self.lstbox_cptces.get(i) + '\n\n'      
                        mess += "\nPour commencer l'évaluation cliquez sur OK, ou sinon cliquez sur Annuler"
                        ok_next=tk.messagebox.askokcancel(title="Commencer l'évaluation",message=mess)
                        if ok_next:
                                eval_path = self._make_eval_path()
                                self._init_eval(eval_path,classe_path,lst_keys)
                                self._clean_next()
                                self._frame_eval_to_frame_next()
                                self._build_next(index_cptces,lst_keys,read_json(classe_path))

    def _make_cptces_path(self):
        cptces_name = "cptces_"+ config["shortcuts"][self._combo_discipline.get()] + '.json'
        return os.path.join(config["root"],config["NOKdir"],cptces_name)

    def _get_cptces(self,niv,json_path): 
        cptces = read_json(json_path)

        lst_cptces=list()
        cle_cycle = "cycle4"
        if niv == "6":
            cle_cycle = "cycle3"
        for cle in cptces[cle_cycle]["clefs"]:
            lst_cptces.append(cle + ' - ' + cptces[cle_cycle][cle][0])
        
        return lst_cptces

    def _make_classe_path(self):
        classe_name = config["convert"][self._combo_niveau.get()] +'-'+ self._combo_nom.get() + '.json'
        return os.path.join(config["root"],config["NOKdir"],classe_name)

    def _make_eval_path(self):
        eval_name = config["convert"][self._combo_niveau.get()] + '-' + self._combo_nom.get() + '_' + self._combo_trim.get() + '_' \
                    + config["shortcuts"][self._combo_discipline.get()] + '_' + self._combo_numeval.get() + '.json'
        return os.path.join(config["root"],config["NOKdir"],eval_name)

    def _new_eval_fill_cptces(self):
        """
        Fonction appelée par le bouton "Afficher les compétences"
        Remplissage de self.lstbox_cptces avec les compétences
        Peut éventuellement lancer l'affichage de la frame next si les conditions sont réunies (évaluation déjà existante notamment)
        """
        cptces_path = self._make_cptces_path()

        if not os.path.exists(cptces_path):
                tk.messagebox.showerror(title="Afficher les compétences",message="Les compétences pour ce cycle et cette discipline n'ont pas été trouvées")
        else:
                self._reset_lstbox_cptces()
                
                lst_cptces=self._get_cptces(config["convert"][self._combo_niveau.get()],cptces_path)
                
                eval_path = self._make_eval_path()
                if os.path.exists(eval_path):
                        
                        eval_data = read_json(eval_path)
                        mess = "L'évaluation n°%s du trimestre %s pour la classe %s %s et pour la discipline '%s' existe déjà et concerne les compétences suivantes:\n\n" \
                        % (self._combo_numeval.get()[-1],self._combo_trim.get()[-1],self._combo_niveau.get(),self._combo_nom.get(),self._combo_discipline.get())
                        for i,c in enumerate(lst_cptces):
                                self.lstbox_cptces.insert(tk.END,c)
                                for k in eval_data["cptces"]:
                                        if k in c[:8]:
                                                self.lstbox_cptces.select_set(i)
                                                mess += c + '\n\n'      
                        mess += "\nPour reprendre ou modifier l'évaluation cliquez sur OK, ou sinon cliquez sur Annuler"
                        
                        modifier = tk.messagebox.askokcancel(title="Evaluation existante",message=mess)

                        if modifier:
                                self._clean_next()
                                self._frame_eval_to_frame_next()
                                names_lst = list()
                                for k in eval_data.keys():
                                        if k != "cptces":
                                                names_lst.append(k)
                                names_lst.sort()
                                self._build_next(self.lstbox_cptces.curselection(),eval_data["cptces"],names_lst)
                
                        else:
                                self._reset_lstbox_cptces()

                else:
                        for c in lst_cptces:
                                self.lstbox_cptces.insert(tk.END,c)

    def _make_eval_basename(self,niveau,nom,trim,discipline):
        eval_basename = config["convert"][niveau] + '-' + nom + '_' + trim + '_' + config["shortcuts"][discipline] + '_eval'
        return eval_basename
            
    def _label_info_update_func(self,event):
        """
        Permet à l'utilisateur de connaître le numéro des évaluations déjà enregistrées
        """
        bn = self._make_eval_basename(self._combo_niveau.get(),self._combo_nom.get(),self._combo_trim.get(),self._combo_discipline.get())
        lst_eval = grab_files_by_name([bn],os.path.join(config["root"],config["NOKdir"]))

        num_eval=list()
        for e in lst_eval:
                num_eval.append(e.split(".json")[0][-1])
        num_eval.sort()

        if len(num_eval)>0:
            if len(num_eval)==1:
                mess = "Pour la discipline '%s', la classe de %s %s et le trimestre %s, seule l'évaluation n°%s a été trouvée.\n" \
                        % (self._combo_discipline.get(),self._combo_niveau.get(),self._combo_nom.get(),self._combo_trim.get()[-1],num_eval[0])
            else:
                mess = "Pour la discipline '%s', la classe de %s %s et le trimestre %s, les évaluations suivantes ont été trouvées:\nN°" \
                        % (self._combo_discipline.get(),self._combo_niveau.get(),self._combo_nom.get(),self._combo_trim.get()[-1])
                for i in range(len(num_eval)-1):
                               mess += num_eval[i] + ' '
                mess += 'et ' + num_eval[-1] +'.'
        else:
                mess = "Pour la discipline '%s', la classe de %s %s et le trimestre %s, aucune évaluation n'a été trouvée.\n" \
                        % (self._combo_discipline.get(),self._combo_niveau.get(),self._combo_nom.get(),self._combo_trim.get()[-1])
                         
        self._label_info_v.set(mess)

    def _label_info_update_and__reset_lstbox_cptces(self,event):
        self._label_info_update_func(event)
        self._reset_lstbox_cptces()

        ###next

    def _init_eval(self,eval_path,classe_path,lst_keys):
        noms = read_json(classe_path)
        
        data={}
        for n in noms:
            data[n]={}
            for k in lst_keys:
                data[n][k]="-1"

        data["cptces"]=list()
        for k in lst_keys:
            data["cptces"].append(k)
	
        write_json(data,eval_path)
        
    def _clean_next(self):
        if len(self._frame_lst_next)>0:
                self._frame_lst_next[0].destroy()
                self._frame_lst_next.pop()
                self._frame_lst_next.append(tk.Frame(self._master,bg=config["couleur"]))
                
                self._next_lst_combo_names.pop()
                self._next_lst_combo_names.append(ttk.Combobox(self._frame_lst_next[0],height=10))
                self._next_lst_combo_names[0].bind("<<ComboboxSelected>>",self._update_next_lst_combo_names)

                self._next_lst_setbuttons = list()

    def _build_next(self,index_cptces,lst_keys,names_lst):
        eval_path = self._make_eval_path()
        
        # texte d'accueil
        label_title_ne= tk.Label(self._frame_lst_next[0],text="Evaluation",font=("Courrier",40),bg=config["couleur"],fg='white')
        label_title_ne.grid(row=0,column=0,columnspan=7,pady=50)

        # sélection des élèves
        self._next_lst_combo_names[0].grid(row=1,column=0,pady=50,padx=10,sticky=tk.W+tk.E)

        # bouton élève précédent
        next_backward = tk.Button(self._frame_lst_next[0],text="Elève précédent",font=("Courrier",12),bg='white',fg=config["couleur"],command=self._move_back_next_combo_names)
        next_backward.grid(row=1,column=1,padx=10,pady=50,sticky=tk.E)

        # bouton élève suivant
        next_forward = tk.Button(self._frame_lst_next[0],text=" Elève suivant ",font=("Courrier",12),bg='white',fg=config["couleur"],command=self._move_fwd_next_combo_names)
        next_forward.grid(row=1,column=2,padx=10,pady=50,sticky=tk.W+tk.E)

        # récapitulation des compétences + placement des boutons d'évaluation
        next_lst_stringvar = list()
        next_lst_labels = list()
        for i,k in enumerate(index_cptces) :
                next_lst_stringvar.append(tk.StringVar())
                next_lst_labels.append(tk.Label(self._frame_lst_next[0],textvariable=next_lst_stringvar[-1],font=("Courrier",10),bg="white",fg='black',bd=1,relief=tk.SUNKEN,width=70))
                text = self.lstbox_cptces.get(k)
                if len(text)>90:
                        text = text[:87]+'...'
                next_lst_stringvar[-1].set(text)
                next_lst_labels[-1].grid(row=2+i,column=0,columnspan=2,padx=10,pady=5,sticky=tk.W+tk.E)

                self._next_lst_setbuttons.append(SetButtons(self._frame_lst_next[0],lst_keys[i],self._next_lst_combo_names[0],eval_path))
                self._next_lst_setbuttons[-1].gridall(2+i,2)

        # placement des boutons de génération des bandeaux et retour                        
        nb_cmptces = len(next_lst_labels)
        next_genheaders = tk.Button(self._frame_lst_next[0],text="Générer les bandeaux",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._make_headers)
        next_genheaders.grid(row=nb_cmptces+2,column=0,padx=10,pady=50,sticky=tk.W+tk.E)
        next_return = tk.Button(self._frame_lst_next[0],text="Retour",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_next_to_frame_accueil)
        next_return.grid(row=nb_cmptces+2,column=1,padx=10,pady=50,sticky=tk.W+tk.E)

        # liste des élèves
        classe_path = self._make_classe_path()
        self._next_lst_combo_names[0]["values"] = names_lst
        self._next_lst_combo_names[0].current(0)

        # mise à jour premier élève
        self._update_next_lst_combo_names(None)

    def _move_back_next_combo_names(self):
        val = self._next_lst_combo_names[0].current()
        
        if val > 0 :
                self._next_lst_combo_names[0].current(val-1)
                self._update_next_lst_combo_names(None)
                
    def _move_fwd_next_combo_names(self):
        val = self._next_lst_combo_names[0].current()
        nbeleves = len(self._next_lst_combo_names[0]["values"])
        
        if val+1 < nbeleves :
                self._next_lst_combo_names[0].current(val+1)
                self._update_next_lst_combo_names(None)


    def _update_next_lst_combo_names(self,event):
        nom = self._next_lst_combo_names[0].get()
        eval_path = self._make_eval_path()
        eval_data = read_json(eval_path)
        for setb in self._next_lst_setbuttons:
                cptce = setb.getcptce()
                setb.setv(eval_data[nom][cptce])

    def _make_headers(self):
        header_name = config["convert"][self._combo_niveau.get()] + '-' + self._combo_nom.get() + '_' + self._combo_trim.get() + '_' \
                    + config["shortcuts"][self._combo_discipline.get()] + '_' + self._combo_numeval.get() + '.pdf'
        header_path = os.path.join(config["root"],config["OKdir"],config["Headersdir"],header_name)
        canv = canvas.Canvas(header_path, bottomup=0, pagesize=A4)
        canv.setFont("Helvetica",12)

        eval_path = self._make_eval_path()
        eval_data = read_json(eval_path)

        # calcul du nombre d'eleves par pages
        nb_lignes_par_eleve = 2 + len(eval_data['cptces'])
        nb_lignes_par_page = 56
        nb_eleves_par_page = nb_lignes_par_page // nb_lignes_par_eleve
        
        startx,starty,stepy = 10,15,15
        linex,liney = startx,starty

        try:
            numeleve = 0
            for n in eval_data.keys():
                if n != 'cptces':
                    canv.drawString(linex,liney,n)
                    liney += stepy
                    for cpt in eval_data[n].keys():
                        mess = cpt + " : " + config["convertcptces"][eval_data[n][cpt]]
                        canv.drawString(linex,liney,mess)
                        liney += stepy
                    canv.drawString(0,liney,"-"*150)
                    liney += stepy
                    numeleve += 1
                    if numeleve >= nb_eleves_par_page:
                        numeleve = 0
                        liney = starty
                        canv.showPage()
            canv.save()
        except:
            tk.messagebox.showerror(title="Génération des bandeaux", \
                                    message="La génération des bandeaux a échoué.")
        else:
            tk.messagebox.showinfo(title="Génération des bandeaux", \
                                    message="Les bandeaux ont bien été générés\n(voir fichier %s)" % header_name)
        
            



class Rmeval:

    def __init__(self,master):

        self._master = master

        #frame
        self.frame_rmeval=tk.Frame(self._master,bg=config["couleur"])

        # texte d'accueil
        self._label_title= tk.Label(self.frame_rmeval,text="Supprimer une évaluation",font=("Courrier",40),bg=config["couleur"],fg='white')

        # selection de la discipline
        self._combo_discipline = ttk.Combobox(self.frame_rmeval,height=11)
        self._combo_discipline["values"]=("Anglais","Arts plastiques","E.P.S.","Espagnol","Français","Histoire-géographie","Mathématiques","Musique","Physique-Chimie","S.V.T.","Technologie")
        self._combo_discipline.current(0)
        self._combo_discipline.bind("<<ComboboxSelected>>",self._label_info_update_func)

        # selection du niveau
        self._combo_niveau = ttk.Combobox(self.frame_rmeval)
        self._combo_niveau["values"]=("6ème","5ème","4ème","3ème")
        self._combo_niveau.current(0)
        self._combo_niveau.bind("<<ComboboxSelected>>",self._label_info_update_func)

        # selection du nom
        self._combo_nom = ttk.Combobox(self.frame_rmeval,height=16)
        self._combo_nom["values"]=("A","B","C","D","E","F","G","H","1","2","3","4","5","6","7","8")
        self._combo_nom.current(0)
        self._combo_nom.bind("<<ComboboxSelected>>",self._label_info_update_func)

        # selection du trimestre
        self._combo_trim = ttk.Combobox(self.frame_rmeval,height=3)
        self._combo_trim["values"]=("T1","T2","T3")
        self._combo_trim.current(0)
        self._combo_trim.bind("<<ComboboxSelected>>",self._label_info_update_func)

        # selection du numéro de l'eval
        self._combo_numeval = ttk.Combobox(self.frame_rmeval,height=10)
        self._combo_numeval["values"]=("eval1","eval2","eval3","eval4","eval5","eval6","eval7","eval8","eval9","eval10")
        self._combo_numeval.current(0)

        # bouton supprimer
        self._button_rmeval = tk.Button(self.frame_rmeval,text="Supprimer",font=("Courrier",20),bg='white',fg=config["couleur"])#,command=self._rm_classroom)

        # bouton retour
        self._button_return = tk.Button(self.frame_rmeval,text="Retour",font=("Courrier",20),bg='white',fg=config["couleur"],command=self._frame_acceuil_func)

        # message d'information
        self._label_info_v = tk.StringVar()
        self._label_info = tk.Label(self.frame_rmeval,textvariable=self._label_info_v,font=("Courrier",10),bg="white",fg='black',bd=1,relief=tk.SUNKEN,width=90)	
        self._label_info_v.set("\n\n")
        self._label_info_update_func(None)

    def gridall(self):
        self._label_title.grid(row=0,column=0,columnspan=6,pady=25)
        self._combo_discipline.grid(row=1,column=0,pady=50,padx=10)
        self._combo_niveau.grid(row=1,column=1,pady=50,padx=10)
        self._combo_nom.grid(row=1,column=2,pady=50,padx=10)
        self._combo_trim.grid(row=1,column=3,pady=50,padx=10)
        self._combo_numeval.grid(row=1,column=4,pady=50,padx=10)
        self._label_info.grid(row=2,column=0,columnspan=6,padx=10,pady=50,sticky=tk.W+tk.E)
        self._button_rmeval.grid(row=3,column=0,padx=10,pady=50,sticky=tk.W+tk.E)
        self._button_return.grid(row=3,column=1,padx=10,pady=50,sticky=tk.W+tk.E)

    def register_frame_acceuil(self,frame_acceuil):
        self._frame_acceuil = frame_acceuil

    def _frame_acceuil_func(self):
        self.frame_rmeval.pack_forget()
        self._frame_acceuil.pack(expand=tk.YES,fill=tk.Y)

    def _make_eval_basename(self,niveau,nom,trim,discipline):
        eval_basename = config["convert"][niveau] + '-' + nom + '_' + trim + '_' + config["shortcuts"][discipline] + '_eval'
        return eval_basename

    def _label_info_update_func(self,event):
        """
        Permet à l'utilisateur de connaître le numéro des évaluations déjà enregistrées
        """
        bn = self._make_eval_basename(self._combo_niveau.get(),self._combo_nom.get(),self._combo_trim.get(),self._combo_discipline.get())
        lst_eval = grab_files_by_name([bn],os.path.join(config["root"],config["NOKdir"]))

        num_eval=list()
        for e in lst_eval:
                num_eval.append(e.split(".json")[0][-1])
        num_eval.sort()

        if len(num_eval)>0:
            if len(num_eval)==1:
                mess = "Pour la discipline '%s', la classe de %s %s et le trimestre %s, seule l'évaluation n°%s a été trouvée.\n" \
                        % (self._combo_discipline.get(),self._combo_niveau.get(),self._combo_nom.get(),self._combo_trim.get()[-1],self._combo_numeval.get()[-1])
            else:
                mess = "Pour la discipline '%s', la classe de %s %s et le trimestre %s, les évaluations suivantes ont été trouvées:\nN°" \
                        % (self._combo_discipline.get(),self._combo_niveau.get(),self._combo_nom.get(),self._combo_trim.get()[-1])
                for i in range(len(num_eval)-1):
                               mess += num_eval[i] + ' '
                mess += 'et ' + num_eval[-1] +'.'
        else:
                mess = "Pour la discipline '%s', la classe de %s %s et le trimestre %s, aucune évaluation n'a été trouvée.\n" \
                        % (self._combo_discipline.get(),self._combo_niveau.get(),self._combo_nom.get(),self._combo_trim.get()[-1])
                         
        self._label_info_v.set(mess)
