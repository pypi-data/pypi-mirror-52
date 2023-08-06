##################################
# Auteur : Christophe Palmann
# Licence : BSD-2-Clause
##################################

#coding:utf-8
from os.path import join,isfile
from .utils import read_json,write_json

config=dict()
config["couleur"] = "#41B77F" #"#4065A4"
config["root"]="database"
config["OKdir"]="PUBLIC"
config["NOKdir"]="PRIVE"
config["TMPdir"]="tmp"
config["Headersdir"]="Bandeaux_évaluations"
config["Elevesdir"]="Bilans_élèves"
config["Classesdir"]="Bilans_classes"
config["convert"]={"6ème":"6","5ème":"5","4ème":"4","3ème":"3"}
config["shortcuts"]={"Anglais":"ANG","Arts plastiques":"ARTPLA","E.P.S.":"EPS","Espagnol":"ESP","Français":"FR","Histoire-géographie":"HG","Mathématiques":"MATHS","Musique":"MUS","Physique-Chimie":"PHY","S.V.T.":"SVT","Technologie":"TECH"}
config["convertcptces"]={"-1":"Non évalué","0":"Maîtrise insuffisante","1":"Maîtrise fragile","2":"Maîtrise satisfaisante","3":"Très bonne maîtrise"}
config["version_bilan_eleve"] = "both"
config["xlstype"] = "ecoledirecte"

user_cfg_path = join(config["root"],config["NOKdir"],"user_cfg.json")

def load_user_cfg():
    if isfile(user_cfg_path):
        user_cfg = read_json(user_cfg_path)
        config.update(user_cfg)
    else:
        write_json(config,user_cfg_path)
