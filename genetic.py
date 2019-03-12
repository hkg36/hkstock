from scipy.optimize import curve_fit
import numpy as np

def SplitPointToPersent(x):
    x=np.sort(x)
    x2=[x[0]]
    for i in range(1,x.shape[0]):
        x2.append(x[i]-x[i-1])
    x2.append(1-x[-1])
    return np.array(x2)
def profitfun(x,a,b,c):
    return a*np.power((1+b),x+c)
profit_lb=12
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
    def eval(pop):
        res=target(pop.x,dline,HSI)
        pop.p=res[0]
        pop.sq=res[1]
        return pop
    pop=[]
    for i in range(300):
        p=Pop(np.random.rand(len(names)-1))
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
                x.x[i]=np.random.normal(x.x[i],0.2)
                if x.x[i]<0:
                    x.x[i]=0
                elif x.x[i]>1:
                    x.x[i]=1

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

if __name__ == "__main__":
    import show
    import loaddata
    names,dline,HSI=loaddata.LoadData()
    champion_x=FindCmb(names,dline,HSI)
    todayx=champion_x*dline[-1,:]
    todayx=todayx/np.sum(todayx)
    indexlist=list(zip(names,todayx))
    print(indexlist)
    print(todayx)
    with open("data/cps.txt","wt") as f:
        for n,v in indexlist:
            f.write("{},{}\n".format(n,v))
    show.Show(dline,HSI,champion_x)