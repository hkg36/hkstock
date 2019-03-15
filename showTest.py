import json
import datetime
import loaddata
import show
import numpy as np

with  open("data/cps.json") as f:
    data=json.load(f)
    datapoint=datetime.datetime.fromtimestamp(data["time"])
    cps=data["cp"]
    champion_x=np.array([o[1] for o in cps])

starttime=datetime.datetime(2019,1,1)
endtime=datetime.datetime(2019,3,15)
pointDate=datapoint
names,dline,HSI,_=loaddata.LoadData(starttime,endtime,pointDate)
show.Show(dline,HSI,champion_x)