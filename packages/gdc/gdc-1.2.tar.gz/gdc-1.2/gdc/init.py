##################################
# Auteur : Christophe Palmann
# Licence : BSD-2-Clause
##################################

#coding:utf-8
from os.path import join,isdir
from os import mkdir
from .config import *

def initfct():
	
	full_root = join(config["root"])
	if not isdir(full_root):
		mkdir(full_root)	
	
	full_OKdir = join(config["root"],config["OKdir"])
	if not isdir(full_OKdir):
		mkdir(full_OKdir)
	
	full_NOKdir = join(config["root"],config["NOKdir"])
	if not isdir(full_NOKdir):
		mkdir(full_NOKdir)

	full_TMPdir = join(config["root"],config["NOKdir"],config["TMPdir"])
	if not isdir(full_TMPdir):
		mkdir(full_TMPdir)

	full_headersdir = join(config["root"],config["OKdir"],config["Headersdir"])
	if not isdir(full_headersdir):
		mkdir(full_headersdir)

	full_elevesdir = join(config["root"],config["OKdir"],config["Elevesdir"])
	if not isdir(full_elevesdir):
		mkdir(full_elevesdir)

	full_classesdir = join(config["root"],config["OKdir"],config["Classesdir"])
	if not isdir(full_classesdir):
		mkdir(full_classesdir)

	# mise à jour de la config
	load_user_cfg()
