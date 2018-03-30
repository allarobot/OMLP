# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 10:40:53 2017
@author: jayHan

Modified 2018.1.4,15:44pm
function demonstration

"""
from py2neo import Graph, Node, Relationship
import numpy as np
import pandas as pd
from functools import reduce
unicode = str ### set during python3 enviornment

class Neo4j(object):
    try:
        _graph = Graph('bolt://127.0.0.1:7687',user="neo4j",password='comac.123')
    except:
        print("Please check database Neo4j!")
        exit(-1);

    _node_lables = ["pin"]
    _rel_labeles = ["continuity","insulation"]
    _jsw_columns = ['connector1','pin1','connector2','pin2','chapter','pin1Type','pin2Type']
    _pgv_columns = [u'connector1',u'pin1',u'connector2',u'pin2',u'testType',u'status',u'value',u'unit',u'addr1',u'addr2']
    def jsw_upload(self,info,pvg):
        '''
        upload new node and relationship to data base
        :param info: DataFrame with column name = _jsw_columns
        :return: True/False
        '''
        col = info.columns
        if not reduce(lambda x,y:x and y,col==Neo4j._jsw_columns):
            print("improper data format, please check!")
            return False
        try:
            #self.clear()
            print("to be")
            #set constraint
        except:
            print("Please check connection of Neo4j Database!")
            return False
        row,col = info.shape
        node_gnd = Node(Neo4j._node_lables[0],connectorName='GND', pinIndex='', fullName='GND',pinType='auto')
        for r in range(row):
            print("{0}/{1}".format(r+1,row))
            cntName1,pin1,cntName2,pin2,chapter,pin1Type,pin2Type = info.iloc[r]
            lable1,lable2 = Neo4j._rel_labeles[0],Neo4j._rel_labeles[1]
            if pin1 is np.nan or not pin1:
               fullName1 = unicode(cntName1)
            else:
               fullName1 = unicode(cntName1)+'-'+unicode(pin1)
            if pin2 is np.nan or not pin2:
               fullName2 = unicode(cntName2)
            else:
               fullName2 = unicode(cntName2)+'-'+unicode(pin2)
            node1 =Node(Neo4j._node_lables[0],connectorName=cntName1,pinIndex=pin1,fullName=fullName1,pinType=pin1Type)
            node2 =Node(Neo4j._node_lables[0],connectorName=cntName2,pinIndex=pin2,fullName=fullName2,pinType=pin2Type)
            if pvg =='pv':
                rel1 = Relationship(node1, lable1, node2, chapter=chapter, status='NULL',times=0,sequence= r)
                Neo4j._graph.merge(node1)
                Neo4j._graph.merge(node2)
                Neo4j._graph.merge(node_gnd)
                Neo4j._graph.merge(rel1)
                rel2 = Relationship(node1, lable2, node_gnd, chapter=chapter, status='NULL', times=0, sequence=row+r)
                Neo4j._graph.merge(rel2)
            elif pvg =='g':
                Neo4j._graph.merge(node1)
                Neo4j._graph.merge(node2)
                rel1 = Relationship(node1, lable1, node2, chapter=chapter, status='NULL', times=0, sequence=r)
                Neo4j._graph.merge(rel1)
        return True


    def pgv_update(self,info):
        '''
        Only modify property of existing relationship
        :param info:DataFrame with column name = _pvg_columns
        :return:False/True
        '''
        col = info.columns
        colName=["connector1","pin1","connector2","pin2","testType","status","value","unit","pin1_addr","pin2_addr"]
        if not reduce(lambda x,y:x and y,col==colName):
            print("improper data format, please check!")
            return False
        try:
    #       ping database?
            print("to be ")
        except:
            print("Please check connection of Neo4j Database!")
            return False
        row,col = info.shape
        high_count = 0
        for r in range(row):
            cntName1,pin1,cntName2,pin2,testType,status,val,unit,addr1,addr2 = info.iloc[r]
            if status == "HIGH":
                high_count += 1
            if pin1 is np.nan or not pin1:
               fullName1 = unicode(cntName1)
            else:
               fullName1 = unicode(cntName1)+'-'+unicode(pin1)
            if pin2 is np.nan or not pin2:
               fullName2 = unicode(cntName2)
            else:
               fullName2 = unicode(cntName2)+'-'+unicode(pin2)

            query='''
            MATCH (pin1:pin)-[rel]->(pin2:pin)
            WHERE pin1.fullName = {name1} and pin2.fullName = {name2}
            WITH rel,pin1,pin2,rel.times as t
            SET rel.times = t+1,rel.status = {status},rel.value = {value},rel.unit = {unit},pin1.addr= {addr1},pin2.addr = {addr2}
            RETURN pin1,rel,pin2
            '''
            data = Neo4j._graph.run(query,name1=fullName1,name2=fullName2,\
                                 status=status,value=val,unit=unit,addr1=addr1,addr2=addr2)
            if not data:
                print("NOT FOUND:",fullName1,fullName2,status,val,unit,addr1,addr2)
        print("high count:",high_count)
        return True

    def clear(self):
        Neo4j._graph.delete_all()


    def stats(self):
        '''
        stats. total number of 'HIGH','PASS' and 'NULL' status of test relationship
        :return: {"HIGH":n,"PASS":m,"NULL":p}
        '''
        result = {"HIGH":0,"PASS":0,"NULL":0}
        query = '''
        match(n1)-[rel1:continuity|insulation]-(n2)
        where rel1.status='HIGH'
        return count(rel1) as NUMBER
        '''
        data1 = Neo4j._graph.run(query).data()
        print(data1)
        result["HIGH"] = data1[0]['NUMBER']
        query = '''
        match(n1)-[rel1:continuity|insulation]-(n2)
        where rel1.status='PASS'
        return count(rel1) as NUMBER
        '''
        data2 = Neo4j._graph.run(query).data()
        result["PASS"] = data2[0]['NUMBER']
        query = '''
        match(n1)-[rel1:continuity|insulation]-(n2)
        where rel1.status='NULL'
        return count(rel1) as NUMBER
        '''
        data3 = Neo4j._graph.run(query).data()
        result["NULL"] = data3[0]['NUMBER']
        return result

    def prog(self, label):
        '''
        :label: label type of relationship,eg. continuity,insulation
        :return: (json objects)
        '''
        query='''
        MATCH (pin1:pin)-[rel:{label}]->(pin2:pin)
        WHERE rel.status='HIGH'
        RETURN pin1.fullName AS PIN1,pin2.fullName AS PIN2,rel.chapter as CHAPTER
        ORDER BY rel.sequence
        '''
        query = query.format(label=label)
        data = Neo4j._graph.run(query).data()

        return data

    def connector_status_dist(self):
        '''

        :return: json objects
        '''
        query = '''
        MATCH (pin1:pin)-[rel]->(pin2:pin)
        WHERE rel.status='HIGH'
        WITH pin1.connectorName as cnm
        MATCH (pin3:pin)-[rel2]->(pin4:pin)
        WHERE pin3.connectorName = cnm
        RETURN count(rel2.status) as NUMBER,rel2.status as STATUS,cnm as CONNECTOR
        ORDER by count(rel2.status) DESC
        '''
        data = Neo4j._graph.run(query).data()
        if not data:
            data = [{'NUMBER':0, 'STATUS':'NULL', 'CONNECTOR':None}]

        return data


    def test1(self):
        query = '''
        match (n1:pin)
        return n1.connectorName as ConnectorName, count(n1.connectorName) as PinNumber
        order by n1.connectorName'''
        data1 = Neo4j._graph.run(query).data()
        query = '''
        match (n1:pin)-[:continuity]-()
        return n1.connectorName as ConnectorName,count(n1.connectorName) as TestingTimes
        order by n1.connectorName'''
        data2 = Neo4j._graph.run(query).data()
        query = '''
        match  (n1:pin)-[rel:continuity{status:'HIGH'}]-(n2:pin)
        return n1.connectorName as ConnectorName1,n2.connectorName as ConnectorName2,count(rel) as HighTimes
        order by n1.connectorName'''
        data3 = Neo4j._graph.run(query).data()
        Connector={}
        for info in data1:
            Name = info[u'ConnectorName']
            Connector[Name]={u'PinNumber':info[u'PinNumber']}
        for info in data2:
            Name = info[u'ConnectorName']
            Connector[Name][u'TestingTimes']= info[u'TestingTimes']

        for info in data3:
            cnt1,cnt2,high_num =info[u'ConnectorName1'],info[u'ConnectorName2'],info[u'HighTimes']
            pin_number1, test_times1 = Connector[cnt1][u'PinNumber'],Connector[cnt1][u'TestingTimes']
            pin_number2, test_times2 = Connector[cnt2][u'PinNumber'], Connector[cnt2][u'TestingTimes']
            info[u'PinNumber1'],info[u'TestingTimes1'] = Connector[cnt1][u'PinNumber'],Connector[cnt1][u'TestingTimes']
            info[u'PinNumber2'],info[u'TestingTimes2'] = Connector[cnt2][u'PinNumber'], Connector[cnt2][u'TestingTimes']
            outtext = "%20s%20s%20s%20s%20s%20s%20s\n"%(cnt1,pin_number1,test_times1,cnt2,pin_number2,test_times2,high_num)
            print(outtext)
        pd_data = pd.DataFrame(data3)
        with pd.ExcelWriter("High_RelationShip.xlsx") as writer:
            pd_data.to_excel(writer, index=False)

        print(data3)