from scipy.optimize import curve_fit
import numpy as np

def SplitPointToPersent(x):
    x=np.sort(x)
    x2=[x[0]]
    for i in range(1,x.shape[0]):
        x2.append(x[i]-x[i-1])
    x2.append(splitsize-x[-1])
    res=np.array(x2)*splitcell
    #assert abs(np.sum(res)-1.0)<0.0000000001
    return res
def profitfun(x,a,b,c):
    return a*np.power((1+b),x+c)
profit_lb=20
splitsize=200
splitcell=1/splitsize
def target(x,dline,hsi):
    x=SplitPointToPersent(x)
    closeall=np.dot(dline,x)/hsi
    poslist=np.array(range(len(closeall)))
    try:
        popt, pcov=curve_fit(profitfun, poslist, closeall,p0=np.array([1,0,0]))
    except:
        return 0,10000000000.0
    p=((1+popt[1])**250)/1.1
    p=int((p-1)*100)

    dirline=profitfun(np.array(poslist,dtype=np.float64),*popt)
    #sqrtmean=np.sqrt(np.sum((closeall-dirline)**2/dirline))
    errorline=((closeall-dirline)/dirline)**2
    sqrtmean=np.sqrt(np.mean(errorline))+2*np.sqrt(np.max(errorline))
    if p<profit_lb:
        return p,100*(profit_lb-p)+sqrtmean
    return p,sqrtmean

def FindCmb(names,dline,HSI):
    class Pop(object):
        def __init__(self,x):
            self.x=x
            self.p=float("nan")
            self.sq=float("nan")
        def cp(self):
            return Pop(self.x.copy())
        def __eq__(self, other):
            return np.array_equal(self.x,other.x)
    def eval(pop):
        res=target(pop.x,dline,HSI)
        pop.p=res[0]
        pop.sq=res[1]
        return pop
    pop=[]
    for i in range(300):
        p=Pop(np.random.random_integers(0,splitsize,len(names)-1))
        pop.append(p)
    pop=[eval(one) for one in pop]
    def mate(x1,x2):
        newer=[]
        for s in range(4):
            param=[0]*x1.x.shape[0]
            for i in range(x1.x.shape[0]):
                if np.random.random()>0.5:
                    param[i]=x1.x[i]
                else:
                    param[i]=x2.x[i]
            newer.append(Pop(np.array(param)))
        return newer
    def mute(x):
        for i in range(x.x.shape[0]):
            if np.random.random()<0.2:
                x.x[i]=np.random.poisson(x.x[i])
                if x.x[i]<0:
                    x.x[i]=0
                elif x.x[i]>splitsize:
                    x.x[i]=splitsize

    minsq=100000000000
    keepcount=0
    while True:
        pop.sort(key=lambda o:o.sq)
        if minsq>pop[0].sq:
            minsq=pop[0].sq
            keepcount=0
            print(minsq,"  ",pop[0].p)
        else:
            keepcount+=1
            if keepcount>500:
                break
        if len(pop)>2000:
            pop=pop[:1500]
        nextpop=[]
        for i in range(50):
            nextpop.extend(mate(pop[np.random.randint(0,100)],pop[np.random.randint(0,100)]))
        for o in nextpop:
            if np.random.random()<0.2:
                mute(o)
        nextpop=list(map(eval,nextpop))
        pop.extend(nextpop)
    return SplitPointToPersent(pop[0].x)
def Cacl(dline,HSI,champion_x):
    closeall=np.dot(dline,champion_x)/HSI
    dayr=(closeall[1:]-closeall[:-1])/closeall[:-1]
    exre=dayr-0.04/250
    sharp=np.sqrt(250)*np.mean(exre)/np.std(exre)
    lasthigh=closeall[0]
    rollback=0
    for i in range(1,closeall.shape[0]):
        if closeall[i]>lasthigh:
            lasthigh=closeall[i]
        else:
            rb=(lasthigh-closeall[i])/lasthigh
            if rb>rollback:
                rollback=rb
    print("最大回撤：{}，夏普:{}".format(rollback,sharp))
if __name__ == "__main__":
    import show
    import loaddata
    import json
    import datetime
    starttime=datetime.datetime(2018,1,1)
    endtime=datetime.datetime(2019,1,10)
    pointDate=datetime.datetime(2019,1,3)
    names,dline,HSI,_=loaddata.LoadData(starttime,endtime,pointDate)
    champion_x=FindCmb(names,dline,HSI)
    todayx=champion_x#*dline[-1,:]
    #todayx=todayx/np.sum(todayx)
    indexlist=list(zip(names,todayx))
    print(indexlist)
    print(todayx)
    with open("data/cps.txt","wt") as f:
        for n,v in indexlist:
            f.write("{},{}\n".format(n,v))
    with open("data/cps.json","wt") as f:
        json.dump({"time":endtime.timestamp(),"cp":indexlist},f)
    Cacl(dline,HSI,champion_x)
    show.Show(dline,HSI,champion_x)