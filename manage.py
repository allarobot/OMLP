#!/Users/jayhan/VirtualEnvs/flask_py3/bin python
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 13:18:40 2017

@author: COMAC
"""
from main import Neo4j#, Pvg, Jsw,FindFiles
#import os

IMPORT_FOLDER = "import/"
EXPORT_FOLDER = "export/"
jsw_path = "/Applications/Splunk/etc/apps/oats_admin/bin/import/"
pvg_path = "/Applications/Splunk/etc/apps/oats_admin/bin/import/"

if __name__ == "__main__":
    import datetime as dt
    t0 = dt.datetime.now()
    db = Neo4j()
    result = db.connector_status_dist()
    details={} #{connector:[PASSNumber,TestTimes,Percent]}
    for item in result:
        #print(item)
        number,status,connector = item['Number'],item['Status'],item['Connector']
        PASSNumber,TestTimes = details.get(connector,[0,0])
        if status =='HIGH':
            TestTimes += number
        elif status=='PASS':
            TestTimes += number
            PASSNumber += number
        details[connector] = [PASSNumber,TestTimes]
        
    for key in details:
        PASSNumber,TestTimes = details[key]
        Percent = PASSNumber/TestTimes*100
        details[key].append(Percent) 
    
    print(details)   
    result2 = db.connector_tested_pins()
    print(result2)
    for item in result2:
        Connector = item['Connector']
        info = details.get(Connector,[0,0,0,0])
        if len(info)==4:
            info[3] += 1
            details[Connector] = info
        elif len(info)==3:
            details[Connector].append(1)
    #print(details)
    timestr = t0.strftime("%Y-%m-%d-%Hh%Mm%Ss")
    #print(timestr)
    fp = open("wit_details_%s.csv"%timestr,'w')    
    line ="%s\t%s\t%s\t%s\t%s\n"%("Connector","PASSNumber","TestTimes","Percent","Pin_Used")
    for key in details:
        PASSNumber,TestTimes,Percent,Pin_Used = details[key]
        line ="%s\t%d\t%d\t%.2f\t%d\n"%(key,PASSNumber,TestTimes,Percent,Pin_Used)
        fp.write(line)
    fp.close()
    print("%d seconds elapsed"%(dt.datetime.now()-t0).seconds)
    
