from scipy.optimize import curve_fit
import pygmo
import numpy as np

def SplitPointToPersent(x):
    x=np.sort(x)
    x2=[x[0]]
    for i in range(1,x.shape[0]):
        x2.append(x[i]-x[i-1])
    x2.append(1-x[-1])
    return np.array(x2)
def FindCmb(names,dline,HSI):
    def profitfun(x,a,b,c):
        return a*np.power((1+b),x+c)
    profit_lb=12
    def target(x):
        x=SplitPointToPersent(x)
        closeall=np.dot(dline,x)/HSI
        poslist=np.array(range(len(closeall)))
        try:
            popt, pcov=curve_fit(profitfun, poslist, closeall,p0=np.array([1,0,0]))
        except:
            return 10000000000.0
        p=int((((1+popt[1])**250)-1)*100)

        dirline=profitfun(np.array(poslist,dtype=np.float64),*popt)
        #sqrtmean=np.sqrt(np.sum((closeall-dirline)**2/dirline))
        errorline=((closeall-dirline)/dirline)**2
        sqrtmean=np.sqrt(np.mean(errorline))+2*np.sqrt(np.max(errorline))
        if p<profit_lb:
            return 100*(profit_lb-p)+sqrtmean
        return sqrtmean


    lb = [0]*(len(names)-1)
    ub = [1]*(len(names)-1)

    class Problem(object):
        def fitness(self, dv):
            return [target(dv)]
        def get_bounds(self):
            return (lb,ub)
    algo = pygmo.algorithm(pygmo.pso(gen = 100,neighb_type=4,variant=6,memory=True))
    #algo = pygmo.algorithm(pygmo.bee_colony(gen = 100, limit = 50))
    algo.set_verbosity(50)
    prob = pygmo.problem(Problem())
    pop = pygmo.population(prob, len(names)*10)

    """archi = pygmo.archipelago(n = 8, algo = algo, prob = prob, pop_size =100)
    archi.evolve()
    archi.wait()
    res = archi.get_champions_f()
    bestindex=-1
    bestres=1e15
    for i in range(len(res)):
        if res[i][0]<bestres:
            bestres=res[i][0]
            bestindex=i
    champion_x=archi.get_champions_x()[bestindex]"""
    champion_x_old=None
    while True:
        pop = algo.evolve(pop)
        champion_x=pop.champion_x[:]
        if champion_x_old is None or np.any(champion_x!=champion_x_old):
            champion_x_old=champion_x
        else:
            break
    return SplitPointToPersent(champion_x)

if __name__ == "__main__":
    import show
    import loaddata
    names,dline,HSI=loaddata.LoadData()
    champion_x=FindCmb(names,dline,HSI)
    indexlist=list(zip(names,champion_x))
    print(indexlist)
    print(champion_x)
    with open("data/cps.txt","wt") as f:
        for n,v in indexlist:
            f.write("{},{}\n".format(n,v))
    show.Show(dline,HSI,champion_x)