# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 09:44:44 2021

@author: seernox
"""
import random
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np


hp = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250]
poison = [0,1,2,3,4,5,6]
kills = 10000
spearAcc = 0.1381
spearMax = 23
swordAcc = 0.1774
swordMax = 29
results = []
X, Y = np.meshgrid(hp, poison)
Z = X*0

def simulate():
    results.clear()
    for x in range(len(hp)):
        for y in range(len(poison)):
            Z[(y,x)] = avgsimkill(kills, hp[x], poison[y])


def graph():
    if (len(results) == 0):
        print("results is empty")
        return
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})    
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    ax.set_xlabel("When to finish off with 2H")
    ax.set_ylabel("When to repoison")
    ax.set_zlabel("Average kill time (s)")
    ax.set_title("KQ kill time D2H & Dspear")
    ##fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

def simkill(threshold,pthreshold):
    random.seed()
    pcount = 2
    p = 6
    kqHP = 250
    resets = 0
    tickcount = 0
    ptimer = 30
    regen = 100
    while (kqHP > 0):
        if (tickcount > regen): ## KQ regen 1 per minute
            if (kqHP < 250):
                regen += 100
                kqHP += 1
                ##print("KQ regens 1 hp to: " + str(kqHP))
        if (tickcount > ptimer): ## poison hit one per 15 sec
            ptimer += 30
            if (p > 0):
                kqHP -= p
                pcount -= 1
                ##print("poison hit of: " + str(p) + ", KQ hp: " + str(kqHP))
                if (pcount == 0):
                    pcount = 4
                    p -= 1
        if (kqHP <= 0):
            ##print("KQ killed by poison")
            break;
        if (tickcount >= 2000): ## count if KQ been > 20 mins
            ##print("Over 20 minutes phase 2 resets")
            resets += 1
            kqHP = 250
            pcount = 2
            p = 6
            tickcount = 0
            ptimer = 30
            regen += 100
        if (kqHP <= threshold or p > pthreshold): ##2H hit
            if (random.random() < swordAcc):
                hit = random.randint(0,swordMax)
                kqHP -= hit
                ##print("2H hit of: " + str(hit) + ", KQ hp: " + str(kqHP))
        else:
            if (random.random() < spearAcc):
                hit = random.randint(0,spearMax)
                kqHP -= hit
                ##print("Spear hit of: " + str(hit) + ", KQ hp: " + str(kqHP))
                if (random.randint(0,3) == 0):
                    if (p == 0):
                        ptimer = tickcount + 30
                        p = 6
                        pcount = 4
        tickcount += 12
    return ((tickcount + (resets *2000))*0.6)

def avgsimkill(kills, threshold, pthreshold):
    result = []
    for x in range(kills):
        result.append(simkill(threshold, pthreshold))
    results.append(result)
    return (sum(result)/len(result))

def simkillconsole(threshold,pthreshold):
    random.seed()
    pcount = 2
    p = 6
    kqHP = 250
    resets = 0
    tickcount = 0
    ptimer = 30
    regen = 100
    while (kqHP > 0):
        if (tickcount > regen): ## KQ regen 1 per minute
            if (kqHP < 250):
                regen += 100
                kqHP += 1
                print("KQ regens 1 hp to: " + str(kqHP))
        if (tickcount > ptimer): ## poison hit one per 15 sec
            ptimer += 30
            if (p > 0):
                kqHP -= p
                pcount -= 1
                print("poison hit of: " + str(p) + ", KQ hp: " + str(kqHP))
                if (pcount == 0):
                    pcount = 4
                    p -= 1
        if (kqHP <= 0):
            print("KQ killed by poison")
            break;
        if (tickcount >= 2000): ## count if KQ been > 20 mins
            print("Over 20 minutes phase 2 resets")
            resets += 1
            kqHP = 250
            pcount = 2
            p = 6
            tickcount = 0
            ptimer = 30
            regen += 100
        if (kqHP <= threshold or p > pthreshold): ##2H hit
            if (random.random() < swordAcc):
                hit = random.randint(0,swordMax)
                kqHP -= hit
                print("2H hit of: " + str(hit) + ", KQ hp: " + str(kqHP))
            else:
                print("2H misses")
        else:
            if (random.random() < spearAcc):
                hit = random.randint(0,spearMax)
                kqHP -= hit
                print("Spear hit of: " + str(hit) + ", KQ hp: " + str(kqHP))
                if (random.randint(0,3) == 0):
                    print("repoisoned")
                    if (p == 0):
                        ptimer = tickcount + 30
                        p = 6
                        pcount = 4
            else:
                print("Spear misses")
        tickcount += 12
    print("KQ killed in: " + str((tickcount + (resets *2000))*0.6) + " seconds")
    return ((tickcount + (resets *2000))*0.6)

simulate()
graph()
