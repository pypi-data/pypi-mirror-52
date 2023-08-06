##################################
# Auteur : Christophe Palmann
# Licence : BSD-2-Clause
##################################

#coding:utf-8
import tkinter as tk
import tkinter.ttk as ttk
from .utils import read_json,write_json
from .config import *

class SetButtons:
    def __init__(self,master,cptce,combo_names,eval_path):
        self.competence = cptce
        self.combnames = combo_names
        self.evpath = eval_path
        self.v = tk.IntVar()
        self.v.set(-1)
        self.rb1 = ttk.Radiobutton(master, text="Non évalué", variable=self.v, value=-1,command=self._update)
        self.rb2 = ttk.Radiobutton(master, text=config["convertcptces"]["0"], variable=self.v, value=0,command=self._update)
        self.rb3 = ttk.Radiobutton(master, text=config["convertcptces"]["1"], variable=self.v, value=1,command=self._update)
        self.rb4 = ttk.Radiobutton(master, text=config["convertcptces"]["2"], variable=self.v, value=2,command=self._update)
        self.rb5 = ttk.Radiobutton(master, text=config["convertcptces"]["3"], variable=self.v, value=3,command=self._update)

    def gridall(self,rowstart,colstart):
        self.rb1.grid(row=rowstart,column=colstart,padx=10,pady=5,sticky=tk.W+tk.E)
        self.rb2.grid(row=rowstart,column=colstart+1,padx=10,pady=5,sticky=tk.W+tk.E)
        self.rb3.grid(row=rowstart,column=colstart+2,padx=10,pady=5,sticky=tk.W+tk.E)
        self.rb4.grid(row=rowstart,column=colstart+3,padx=10,pady=5,sticky=tk.W+tk.E)
        self.rb5.grid(row=rowstart,column=colstart+4,padx=10,pady=5,sticky=tk.W+tk.E)

    def getv(self):
        return self.v.get()

    def setv(self,value):
        self.v.set(value)

    def getcptce(self):
        return self.competence

    def _update(self):
        eval_data = read_json(self.evpath)
        eval_data[self.combnames.get()][self.competence] = str(self.v.get())
        write_json(eval_data,self.evpath)
