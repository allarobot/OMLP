#!/Users/jayhan/VirtualEnvs/flask_py3/bin python
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 13:18:40 2017

@author: COMAC
"""
from main import Neo4j, Pvg, Jsw,FindFiles
import os

db = Neo4j()
IMPORT_FOLDER = "import/"
EXPORT_FOLDER = "export/"
jsw_path = "/Applications/Splunk/etc/apps/oats_admin/bin/import/"
pvg_path = "/Applications/Splunk/etc/apps/oats_admin/bin/import/"

if __name__ == "__main__":
    import datetime as dt
    t0 = dt.datetime.now()
    paths = FindFiles(folder_in=jsw_path, fileExt='.xlsx').paths()
    print(paths)
    jsw = Jsw()
    for fp in paths:
        jsw.process(fp)
    db = Neo4j(pace=jsw.nRows//100)
    sequence = db.jsw_upload(jsw)
    print "%d seconds elapsed"%(dt.datetime.now()-t0).seconds

