##################################
# Auteur : Christophe Palmann
# Licence : BSD-2-Clause
##################################

#coding:utf-8
from .utils import *
from .config import *
from os.path import basename,join
from os import remove
from multiprocessing import Process
from numpy import array,arange
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileMerger


class StatsComputer:
    def __init__(self,workdir,current_trim):
        self._evals = grab_files_by_name(['eval','json'],workdir)
        self.nbevals = {"T1":0,"T2":0,"T3":0}
        for ev in self._evals:
            if "T1" in ev:
                self.nbevals["T1"] += 1
            if "T2" in ev:
                self.nbevals["T2"] += 1
            if "T3" in ev:
                self.nbevals["T3"] += 1
        
        self._current_trim = current_trim

        if self.nbevals["T1"] + self.nbevals["T2"] + self.nbevals["T3"] > 0:
            self._make_metadic()
            self._make_metadic_byclass()


    def _make_metadic(self):
        self._metadic=dict()
        self._metadic_i=dict()
        self._metadic_evstats=dict()
        self._metadic_i_evstats=dict()
        
        for ev in self._evals:
            info = self._get_info(ev)
            classe , trim , discipline = info[0] , info[1] , info[2]

            dic_cpt_cptgen = self._get_dic_cpt_cptgen(classe[0],discipline)

            eval_data = read_json(ev)
            for nom in eval_data:
                if nom != 'cptces':
                    for cpt in eval_data["cptces"]:
                        if eval_data[nom][cpt] != "-1": # non-évalué
                            # compétences (items des compétences générales
                            D1 = self._metadic.setdefault(classe,dict()).setdefault(trim,dict()).setdefault(discipline,dict()).setdefault(nom,dict())
                            D1[cpt] = D1.get(cpt,array([0.,0.])) + array([self._convert(eval_data[nom][cpt]),1.])

                            # compétences générales
                            cptgen = dic_cpt_cptgen[cpt]
                            D2 = self._metadic_i.setdefault(classe,dict()).setdefault(trim,dict()).setdefault(discipline,dict()).setdefault(nom,dict())
                            D2[cptgen] = D2.get(cptgen,array([0.,0.])) + array([self._convert(eval_data[nom][cpt]),1.])

            for c in eval_data["cptces"]:
                D1 = self._metadic_evstats.setdefault(classe,dict()).setdefault(trim,dict()).setdefault(discipline,dict())#.setdefault(c,0) + 1
                D1[c] = D1.get(c,0) + 1
                cgen = dic_cpt_cptgen[c]
                D2 = self._metadic_i_evstats.setdefault(classe,dict()).setdefault(trim,dict()).setdefault(discipline,dict())#.setdefault(cgen,0) + 1
                D2[cgen] = D2.get(cgen,0) + 1
                            
                            
    def _make_metadic_byclass(self):
        self._metadic_byclass=dict()
        for classe in self._metadic.keys():
            for trim in self._metadic[classe].keys():
                for disc in self._metadic[classe][trim].keys():
                    for nom in self._metadic[classe][trim][disc].keys():
                        for cpt in self._metadic[classe][trim][disc][nom].keys():
                            D = self._metadic_byclass.setdefault(classe,dict()).setdefault(trim,dict()).setdefault(disc,dict())
                            D[cpt] = D.get(cpt,array([0,0])) + array([self._metadic[classe][trim][disc][nom][cpt][0],self._metadic[classe][trim][disc][nom][cpt][1]])

        self._metadic_i_byclass=dict()
        for classe in self._metadic_i.keys():
            for trim in self._metadic_i[classe].keys():
                for disc in self._metadic_i[classe][trim].keys():
                    for nom in self._metadic_i[classe][trim][disc].keys():
                        for cptgen in self._metadic_i[classe][trim][disc][nom].keys():
                            D = self._metadic_i_byclass.setdefault(classe,dict()).setdefault(trim,dict()).setdefault(disc,dict())
                            D[cptgen] = D.get(cptgen,array([0,0])) + array([self._metadic_i[classe][trim][disc][nom][cptgen][0],self._metadic_i[classe][trim][disc][nom][cptgen][1]])

                    
    def _convert(self,n):
        if n=="0":
            return 10
        if n=="1":
            return 25
        if n=="2":
            return 40
        if n=="3":
            return 50


    def _get_info(self,evaluation):
        codename = basename(evaluation).split('.')[0]
        return codename.split('_')


    def _get_perfs_by_pup_full(self,classe):
        """ Bilan trimestriel par élève, avec sous-compétences et compétences"""
        for disc in self._metadic[classe][self._current_trim].keys():
            pdf_input_lst = list()
            for nom in self._metadic[classe][self._current_trim][disc].keys():
                figname = classe+"_"+self._current_trim+"_"+disc+"_"+nom+"_version_eleve.pdf"
                figpath = join(config["root"],config["NOKdir"],config["TMPdir"],figname)
                pdf_input_lst.append(figpath)
                
                scores1=list()
                cpt_lst1=list()
                lst = sorted(self._metadic[classe][self._current_trim][disc][nom].items(), key=lambda t: t[0])
                for l in lst:
                    scores1.append(l[1][0]/l[1][1])
                    cpt_lst1.append(l[0])

                scores2=list()
                cpt_lst2=list()
                lst = sorted(self._metadic_i[classe][self._current_trim][disc][nom].items(), key=lambda t: t[0])
                for l in lst:
                    scores2.append(l[1][0]/l[1][1])
                    cpt_lst2.append(l[0])
                    
                self._draw_cptces_full(scores1,cpt_lst1,scores2,cpt_lst2,figpath,"Bilan trimestriel (%s) de %s"%(self._current_trim,nom),False)
            self._merger(join(config["root"],config["OKdir"],config["Elevesdir"],classe+"_"+self._current_trim+"_"+disc+"_version_eleve.pdf"),pdf_input_lst)
            for pdf in pdf_input_lst:
                remove(pdf)  


    def _get_perfs_by_pup_vs_classe_full(self,classe):
        """ Bilan trimestriel par élève avec comparaison
        avec la classe, avec sous-compétences et compétences"""
        for disc in self._metadic[classe][self._current_trim].keys():
            pdf_input_lst = list()
            for nom in self._metadic[classe][self._current_trim][disc].keys():
                figname = classe+"_"+self._current_trim+"_"+disc+"_"+nom+"_version_prof.pdf"
                figpath = join(config["root"],config["NOKdir"],config["TMPdir"],figname)
                pdf_input_lst.append(figpath)
                
                scores_el1=list()
                scores_cl1=list()
                cpt_lst1=list()
                lst = sorted(self._metadic[classe][self._current_trim][disc][nom].items(), key=lambda t: t[0])
                for l in lst:
                    scores_el1.append(l[1][0]/l[1][1])
                    t_cl=self._metadic_byclass[classe][self._current_trim][disc][l[0]]
                    scores_cl1.append(t_cl[0]/t_cl[1])
                    cpt_lst1.append(l[0])

                scores_el2=list()
                scores_cl2=list()
                cpt_lst2=list()
                lst = sorted(self._metadic_i[classe][self._current_trim][disc][nom].items(), key=lambda t: t[0])
                for l in lst:
                    scores_el2.append(l[1][0]/l[1][1])
                    t_cl=self._metadic_i_byclass[classe][self._current_trim][disc][l[0]]
                    scores_cl2.append(t_cl[0]/t_cl[1])
                    cpt_lst2.append(l[0])
                    
                self._draw_cptces_dble_full(scores_el1,scores_cl1,cpt_lst1,scores_el2,scores_cl2,cpt_lst2,figpath,"Bilan trimestriel (%s) de %s"%(self._current_trim,nom),nom)
            self._merger(join(config["root"],config["OKdir"],config["Elevesdir"],classe+"_"+self._current_trim+"_"+disc+"_version_prof.pdf"),pdf_input_lst)
            for pdf in pdf_input_lst:
                remove(pdf)
                                            

    def _get_perfs_by_class_full(self,classe):
        """ Bilan trimestriel par classe, avec sous-compétences et compétences"""
        for disc in self._metadic_byclass[classe][self._current_trim].keys():
            figname = classe+"_"+self._current_trim+"_"+disc+"_PERFS.pdf"
            figpath = join(config["root"],config["NOKdir"],config["TMPdir"],figname)
            
            scores1=list()
            cpt_lst1=list()
            lst = sorted(self._metadic_byclass[classe][self._current_trim][disc].items(), key=lambda t: t[0])
            for l in lst:
                scores1.append(l[1][0]/l[1][1])
                cpt_lst1.append(l[0])

            scores2=list()
            cpt_lst2=list()
            lst = sorted(self._metadic_i_byclass[classe][self._current_trim][disc].items(), key=lambda t: t[0])
            for l in lst:
                scores2.append(l[1][0]/l[1][1])
                cpt_lst2.append(l[0])
                
            self._draw_cptces_full(scores1,cpt_lst1,scores2,cpt_lst2,figpath,"Bilan trimestriel (%s) de la classe %s"%(self._current_trim,classe),True)


    def _get_stats_by_class_full(self,classe):
        """ Décompte des sous-compétences et compétences évaluées"""
        for disc in self._metadic_evstats[classe][self._current_trim].keys():
            figname = classe+"_"+self._current_trim+"_"+disc+"_STATS.pdf"
            figpath = join(config["root"],config["NOKdir"],config["TMPdir"],figname)
            
            scores1=list()
            cpt_lst1=list()
            lst = sorted(self._metadic_evstats[classe][self._current_trim][disc].items(), key=lambda t: t[0])
            for l in lst:
                scores1.append(l[1])
                cpt_lst1.append(l[0])

            scores2=list()
            cpt_lst2=list()
            lst = sorted(self._metadic_i_evstats[classe][self._current_trim][disc].items(), key=lambda t: t[0])
            for l in lst:
                scores2.append(l[1])
                cpt_lst2.append(l[0])
                
            self._draw_stats_full(scores1,cpt_lst1,scores2,cpt_lst2,figpath,"Statistiques des évaluations de la classe %s (%s)"%(classe,self._current_trim))
                    

    def _get_histo_by_class_full(self,classe):
        self._get_perfs_by_class_full(classe)
        self._get_stats_by_class_full(classe)

        for disc in self._metadic_byclass[classe][self._current_trim].keys():
            figname_out = join(config["root"],config["OKdir"],config["Classesdir"],classe+"_"+self._current_trim+"_"+disc+".pdf")
            figname_in1 = join(config["root"],config["NOKdir"],config["TMPdir"],classe+"_"+self._current_trim+"_"+disc+"_PERFS.pdf")
            figname_in2 = join(config["root"],config["NOKdir"],config["TMPdir"],classe+"_"+self._current_trim+"_"+disc+"_STATS.pdf")

            self._merger(figname_out,[figname_in1,figname_in2])

            for pdf in [figname_in1,figname_in2]:
                remove(pdf)


    def all_stats_mp(self):
        lst_processes = list()
        
        for classe in self._metadic.keys():
            if config["version_bilan_eleve"] == "both":
                lst_processes.append(Process(target=self._get_perfs_by_pup_full, args=(classe,)))
                lst_processes.append(Process(target=self._get_perfs_by_pup_vs_classe_full, args=(classe,)))
            if config["version_bilan_eleve"] == "prof":
                lst_processes.append(Process(target=self._get_perfs_by_pup_vs_classe_full, args=(classe,)))
            if config["version_bilan_eleve"] == "eleve":
                lst_processes.append(Process(target=self._get_perfs_by_pup_full, args=(classe,)))

            lst_processes.append(Process(target=self._get_histo_by_class_full, args=(classe,)))
            
        for p in lst_processes:
            p.start()
            
        for p in lst_processes:
            p.join()    

        
    def _draw_cptces_full(self,scores1,cpt_lst1,scores2,cpt_lst2,figpath,titre,showscores):
        """ Utilisée par : get_perfs_by_pup_full et get_perfs_by_class_full"""
        width=0.3
        ind1 = arange(len(scores1))
        ind2 = arange(len(scores2))
        plt.clf()
        plt.figure(figsize=(8.27, 11.69), dpi=100)

        plt.subplot(2, 1, 1)
        p1 = plt.bar(ind1, scores1,   width, color='b')
        plt.xlabel('Sous-compétences')
        plt.title(titre)
        plt.xticks(ind1, cpt_lst1)
        plt.yticks([self._convert("0"),self._convert("1"),self._convert("2"),self._convert("3")], \
                   [config["convertcptces"]["0"],config["convertcptces"]["1"],config["convertcptces"]["2"],config["convertcptces"]["3"]])
        if showscores:
            for (i,s) in zip(ind1-width/2,[round(e,1) for e in scores1]):
                plt.annotate(s,(i,s+1))

        plt.subplot(2, 1, 2)
        p2 = plt.bar(ind2, scores2,   width, color='b')
        plt.xlabel('Compétences')
        plt.xticks(ind2, cpt_lst2)
        plt.yticks([self._convert("0"),self._convert("1"),self._convert("2"),self._convert("3")], \
                   [config["convertcptces"]["0"],config["convertcptces"]["1"],config["convertcptces"]["2"],config["convertcptces"]["3"]])
        if showscores:
            for (i,s) in zip(ind2-width/2,[round(e,1) for e in scores2]):
                plt.annotate(s,(i,s+1))
        
        plt.tight_layout()
        plt.savefig(figpath)
        plt.close()

        
    def _draw_cptces_dble_full(self,scores_el1,scores_cl1,cpt_lst1,scores_el2,scores_cl2,cpt_lst2,figpath,titre,nom):
        """ Utilisée par get_perfs_by_pup_vs_classe_full"""
        width=0.3
        ind1 = arange(len(scores_el1))
        ind2 = arange(len(scores_el2))
        plt.clf()
        plt.figure(figsize=(8.27, 11.69), dpi=100)

        plt.subplot(2, 1, 1)
        p1 = plt.bar(ind1 - width/2, scores_el1,   width, color='b')
        p2 = plt.bar(ind1 + width/2, scores_cl1,   width, color='r')
        plt.xlabel('Sous-compétences')
        plt.title(titre)
        plt.xticks(ind1, cpt_lst1)
        plt.yticks([self._convert("0"),self._convert("1"),self._convert("2"),self._convert("3")], \
                   [config["convertcptces"]["0"],config["convertcptces"]["1"],config["convertcptces"]["2"],config["convertcptces"]["3"]])
        plt.legend( (p1[0], p2[0]), (nom, 'Classe') )
        # affichage des scores
        for (i,s) in zip(ind1-width,[round(e,1) for e in scores_el1]):
            plt.annotate(s,(i,s+1))
        for (i,s) in zip(ind1,[round(e,1) for e in scores_cl1]):
            plt.annotate(s,(i,s+1))

        plt.subplot(2, 1, 2)
        p3 = plt.bar(ind2 - width/2, scores_el2,   width, color='b')
        p4 = plt.bar(ind2 + width/2, scores_cl2,   width, color='r')
        plt.xlabel('Compétences')
        plt.xticks(ind2, cpt_lst2)
        plt.yticks([self._convert("0"),self._convert("1"),self._convert("2"),self._convert("3")], \
                   [config["convertcptces"]["0"],config["convertcptces"]["1"],config["convertcptces"]["2"],config["convertcptces"]["3"]])
        plt.legend( (p3[0], p4[0]), (nom, 'Classe') )
        
        # affichage des scores
        for (i,s) in zip(ind2-width,[round(e,1) for e in scores_el2]):
            plt.annotate(s,(i,s+1))
        for (i,s) in zip(ind2,[round(e,1) for e in scores_cl2]):
            plt.annotate(s,(i,s+1))

        plt.tight_layout()
        plt.savefig(figpath)
        plt.close()


    def _draw_stats_full(self,scores1,cpt_lst1,scores2,cpt_lst2,figpath,titre):
        """ Utilisée par get_stats_by_class_full"""
        width=0.3
        ind1 = arange(len(scores1))
        ind2 = arange(len(scores2))
        indy1 = range(max(scores1)+1)
        indy2 = range(max(scores2)+1)
        
        plt.clf()
        plt.figure(figsize=(8.27, 11.69), dpi=100)

        plt.subplot(2, 1, 1)
        p1 = plt.bar(ind1, scores1,   width, color='b')
        plt.xlabel('Sous-compétences')
        plt.title(titre)
        plt.xticks(ind1, cpt_lst1)
        plt.yticks(indy1, [str(i) for i in indy1] )

        plt.subplot(2, 1, 2)
        p2 = plt.bar(ind2, scores2,   width, color='b')
        plt.xlabel('Compétences')
        plt.xticks(ind2, cpt_lst2)
        plt.yticks(indy2, [str(i) for i in indy2] )
        
        plt.tight_layout()
        plt.savefig(figpath)
        plt.close()


    def _make_cptces_path(self,discipline):
        cptces_name = "cptces_" + discipline + '.json'
        return os.path.join(config["root"],config["NOKdir"],cptces_name)


    def _get_dic_cpt_cptgen(self,niv,discipline):
        cptces_path = self._make_cptces_path(discipline)
        cptces = read_json(cptces_path)
        dic_cles_cptgen=dict()
        cle_cycle = "cycle4"
        if niv == "6":
            cle_cycle = "cycle3"
        for cle in cptces[cle_cycle]["clefs"]:
            dic_cles_cptgen[cle] = cptces[cle_cycle][cle][2]
        return dic_cles_cptgen


    def _merger(self,output_path, input_paths):
        pdf_merger = PdfFileMerger()
     
        for path in input_paths:
            pdf_merger.append(path)
     
        with open(output_path, 'wb') as fileh:
            pdf_merger.write(fileh)

        pdf_merger.close()
        

if __name__ == "__main__":
    from time import time
    from init import initfct
    
    initfct()

    print("Calculs des stats...")
    WSevals = StatsComputer( join(config["root"],config["NOKdir"]) )
    if WSevals.nbevals > 0:
        tps1 = time()
        WSevals.all_stats_mp()
        tps2 = time()
        print("Temps écoulé",tps2-tps1)
    
