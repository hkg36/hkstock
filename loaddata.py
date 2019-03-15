import pymongo
import datetime
import numpy as np

def LoadData(starttime=datetime.datetime(2018,3,1),endtime=datetime.datetime(2019,3,1),pointDate=datetime.datetime(2019,3,1)):
    dbclient=pymongo.MongoClient("mongodb://192.168.31.24:27017/")
    db=dbclient["hk_D"]
    with open("data/hsilist.csv",encoding="utf8") as f:
        lines=f.readlines()
        lines=[one.strip() for one in lines]
        lines=[one[-4:] for one in lines if len(one)>0]

    dline=[]
    point=0
    for one in lines:
        res=list(db[one].find({"_id":{"$gte":starttime.timestamp(),"$lte":endtime.timestamp()}}).sort("_id",1))
        his=[]
        for il in range(len(res)):
            line=res[il]
            his.append(line["adj close"])
            if  point==0 and pointDate.timestamp()==line["_id"]:
                point=il
        dline.append(his)
    dline=np.array(dline).T
    dline/=dline[point,:]

    HSI=[]
    res=db["HSI"].find({"_id":{"$gte":starttime.timestamp(),"$lte":endtime.timestamp()}}).sort("_id",1)
    for one in res:
        HSI.append(one["close"])
    HSI=np.array(HSI)
    HSI=HSI/HSI[point]
    return lines,dline,HSI,point