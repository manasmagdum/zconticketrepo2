
import pandas as pd
import numpy as np
import math
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sklearn.metrics
import datetime
import collections
from flask import Flask,request
import json
import requests
import ast
import pickle
import psycopg2
app = Flask(__name__)

paramList=['Object','Type','Category','Issue']
IssueDict={'Software not working':1,'Software Install':2,'Accessory request':2,'System Performance':3,'Access required':4,'Work from home':5,'Network issue':6,'zCon internal issue':7}
ObjectDict={'Skype':1,'Thunderbird':2,'SQL':3,'Visual Studio':4,'NetBeans':6,'Keyboard':7,'Headphone':8,'Mouse':9,'Laptop/Machine':10,'Eclipse':11,'CVS':12,'Internet Dongle':13,'MS Office':5,'Other request':0,'Other Issue':0}
CategoryDict={'Hardware/Other':0,'Software':1}
TypeDict={'Incident':0,'Request':1}

psid = None
PAGE_ACCESS_TOKEN= 'EAAcVX4PZCfU0BABXwZAjpsXmyi8vwAZB5uyYNWDm6WeWIS0ZC9JdZC9VW86fO0FbUnsPAtVZAQZCfZCZCdTvPzWRyE8a5APy8ifFyCn81RESuY05sBUyTeZA9I7OcJGLQxyKeZBN6utgZBTj644ZAmZA7qlbeHVz8168f1sMJtsKUJSM0Wi1GfF2SsWHWi'

@app.route('/',methods=['POST'])
def JsonHandler():
    flag=0
    RequestDict={}
    ProfileDict={}
    print('Is this JSON?',request.is_json)
    #print(request.headers)
    content=request.get_json()
    #print(content)
    for k,v in content.items():
        if(k=='result'):
            for key,val in v.items():
                if (key=='parameters'):
                    for param,value in val.items():
                        if param in paramList:
                            if param=='Object':
                                RequestDict[param]=ObjectDict[value]
                                flag=1
                            if param == 'Issue':
                                RequestDict[param]=IssueDict[value]
                            if param == 'Type':
                                RequestDict[param]=TypeDict[value]
                            if param == 'Category':
                                RequestDict[param]=CategoryDict[value]




                                

        if k == 'originalRequest':
            for key,val in v.items():
                if key=='data':
                    for param,value in val.items():
                        if param=='sender':
                            psid = value['id']
                            r = requests.get("https://graph.facebook.com/v2.6/"+str(psid)+"?fields=first_name,last_name&access_token="+PAGE_ACCESS_TOKEN)
                            ProfileDict= ast.literal_eval(r.text)



    if flag==1:
        print(RequestDict)
        query= np.array([RequestDict['Issue'],RequestDict['Object'],RequestDict['Type'],RequestDict['Category']]).reshape(1,-1)
        mlpregressor=pickle.load(open("mlpregressor.pk",'rb'))
        
        prediction= mlpregressor.predict(query) 
        res = {"data":{"facebook":{"text":"Got it! From my estimation, your issue can take "+str(math.ceil(prediction))+" days to solve."}}}  
        conn =psycopg2.connect(database='d3lklpufkhie6b',user='pstoyxetkxxibj',password='5f85606ff01f0904e1ba7964db57e6256d48f5e9ad59206cdcd46206660658ca',host='ec2-174-129-26-203.compute-1.amazonaws.com',port='5432')
        print('Done')
        cur= conn.cursor()
        cur.execute("INSERT INTO TICKETPARAMETERS (ISSUEID,OBJECTID,TYPEID,CATEGORYID,TIMEREQDAYS) \
        VALUES (%s,%s,%s,%s,%s)",(RequestDict["Issue"],RequestDict["Object"],RequestDict["Type"],RequestDict["Category"],float(prediction)))
        conn.commit()
        print("commited")
        conn.close()  
        return json.dumps(res)

    elif flag==0:
        print(ProfileDict)
        res={"followupEvent":{"name":"ProbType","data":{"fname":ProfileDict["first_name"]}}}
        return json.dumps(res)


    


    
    
if __name__ == '__main__':
    app.run()

