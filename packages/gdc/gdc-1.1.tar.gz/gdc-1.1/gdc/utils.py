##################################
# Auteur : Christophe Palmann
# Licence : BSD-2-Clause
##################################

#coding:utf-8
import os,stat
from shutil import copyfile
from os.path import join
import json
import xlrd

def RecursiveDirectoriesListing(top="."):
    """ List directories recursively"""
    names = os.listdir(top)
    files = []
    for name in names:
        try:
            st = os.lstat(join(top,name))
        except os.error:
            continue
        if stat.S_ISDIR(st.st_mode):
            for(newtop,children) in RecursiveDirectoriesListing(join(top,name)):
                yield newtop,children
        else:
            files.append(name)

    yield top,files

def grab_files_by_name(list_cond,path1):
    found_files=[]
    for (dir1,files1) in RecursiveDirectoriesListing(path1):
        for file1 in files1:
            found = True
            for c in list_cond:
                if c not in file1:
                    found = False
                    break
            if found:
                found_files.append(join(dir1,file1))
    return found_files

def read_json(path):
    try:
        with open(path, "r") as read_file:
            data = json.load(read_file)
            return data
    except:
        print("Problème lors de la lecture du fichier %s" % path)

def write_json(data,path):
    try:
        with open(path, "w") as write_file:
            json.dump(data,write_file)
    except:
        print("Problème lors de l'écriture du fichier %s" % path)
        
def read_cptcpes_from_xlsfiles(path,json_path):
    flag = 0 # tout s'est bien passé
    
    dic=dict()
    dic["cycle3"]=dict()
    dic["cycle3"]["clefs"]=list()
    dic["cycle4"]=dict()
    dic["cycle4"]["clefs"]=list()
    
    try:
        workbook = xlrd.open_workbook(path)
        
        worksheet1 = workbook.sheet_by_index(0)
        for i in range(worksheet1.nrows):
            cle = worksheet1.cell(i,1).value
            dic["cycle3"]["clefs"].append(cle)
            dic["cycle3"][cle] = (str(worksheet1.cell(i,2).value).strip(),"",str(worksheet1.cell(i,0).value).strip())
            
        # Vérification
        testcles=list()
        for c in dic["cycle3"]["clefs"]:
            if c not in testcles:
                testcles.append(c)
            else:
                flag = -1
            
        worksheet2 = workbook.sheet_by_index(1)
        for i in range(worksheet2.nrows):
            cle = worksheet2.cell(i,1).value
            dic["cycle4"]["clefs"].append(cle)
            dic["cycle4"][cle] = (str(worksheet2.cell(i,2).value).strip(),"",str(worksheet2.cell(i,0).value.strip()))
            
        # Vérification
        testcles=list()
        for c in dic["cycle4"]["clefs"]:
            if c not in testcles:
                testcles.append(c)
            else:
                flag = -2
    except:
        print("Problème lors de l'ouverture du fichier %s" % path)
    
    if flag == 0:
        write_json(dic,json_path)
        
    return flag



		
