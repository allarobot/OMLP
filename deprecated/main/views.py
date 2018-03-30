# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 13:18:40 2017

@author: COMAC
"""
from .graphData import Neo4j
from .models import FindFiles, Pgv, Jsw, Format, Save

db = Neo4j()
JSW_FOLDER = "import/JSW"
PVG_FOLDER = "import/PVG"
EXPORT_FOLDER = "export/"


def upload_jsw():
    paths = FindFiles(JSW_FOLDER, '.xlsx').path()
    for fp in paths:
        jsw1 = Jsw(fp)
        print("info_pv")
        print(jsw1.info_pv)
        print("info_g")
        print(jsw1.info_g)
        db.jsw_upload(jsw1.info_pv,'pv')
        db.jsw_upload(jsw1.info_g, 'g')



def update_ditmco():
    paths = FindFiles(PVG_FOLDER, '.txt').path()
    for fp in paths:
        pgv1 = Pgv(fp)
        print("pgv_time:", pgv1.strDateTime)
        print("pgv_info:", pgv1.pdTestLists)
        db.pgv_update(pgv1.pdTestLists)


def clear_all():
    db.clear()








