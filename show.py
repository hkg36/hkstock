import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec,patches

def Show(dline,HSI,champion_x):
    tgtline=np.dot(dline,champion_x)
    diffline=tgtline-HSI
    poslist=np.array(range(len(tgtline)))

    fig=plt.figure()
    fig.subplots_adjust(top=0.98,bottom=0.02,left=0.05,right=0.98)
    fig.subplots_adjust(hspace=0.01)
    gs = gridspec.GridSpec(3, 1)
    ax = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    ax2 = plt.subplot(gs[2])

    for i in range(dline.shape[1]):
        line=dline[:,i].reshape(-1)
        ax.plot(poslist,line)
    ax1.plot(poslist,tgtline,"g")
    ax1.plot(poslist,HSI,"r--")

    ax2.plot(poslist,diffline)

    plt.show()