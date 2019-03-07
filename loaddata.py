import pymongo
import datetime
import numpy as np

def LoadData():
    starttime=datetime.datetime(2018,3,1)
    endtime=datetime.datetime(2019,3,1)
    dbclient=pymongo.MongoClient("mongodb://192.168.31.24:27017/")
    db=dbclient["hk_D"]
    with open("data/hsilist.csv",encoding="utf8") as f:
        lines=f.readlines()
        lines=[one.strip() for one in lines]
        lines=[one[-4:] for one in lines if len(one)>0]

    dline=[]
    for one in lines:
        res=db[one].find({"_id":{"$gte":starttime.timestamp(),"$lte":endtime.timestamp()}}).sort("_id",1)
        his=[]
        for line in res:
            his.append(line["adj close"])
        dline.append(his)
    dline=np.array(dline).T
    dline/=dline[0,:]

    HSI=[]
    res=db["HSI"].find({"_id":{"$gte":starttime.timestamp(),"$lte":endtime.timestamp()}}).sort("_id",1)
    for one in res:
        HSI.append(one["close"])
    HSI=np.array(HSI)
    HSI=HSI/HSI[0]
    return lines,dline,HSI