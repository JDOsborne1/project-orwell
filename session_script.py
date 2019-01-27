# Session Script
## Script to run on the server side to encapsulate the session of the experiment


import matplotlib.pyplot as plt
import random
import orwell_core as oc
import WLORS_classes as rsc 
import spillover2 as sp2
import get_function as get
import rng_n_roll as rng



pots=[oc.Potential('Grav',1,363,363,4),oc.Potential('Radpres',1,363,363,3)]#formatting of z,y,x
objs = []
'''Simulating entities with outward pressure'''
for j in range(0):
    objs.append(oc.Entity('Mount{}'.format(j),
                       0,random.randint(0,363),random.randint(0,363),
                       0,0,0,
                       {'Grav':(0,0),'Radpres':(-random.random(),0)}))
'''Simulating entities gravitating towards one another'''    
for i in range(100):
    objs.append(oc.Entity('Person{}'.format(i),
                       0,random.randint(0,363),random.randint(0,363),
                       0,random.random()-1,random.random()-1,
                       {'Grav':(random.random(),random.random())}))


steps=100
for t in range(steps):
    for p in pots:
        p.update(objs,0.01)
        for i in objs:
            i.update(p,0.1)


for i in range(len(objs)):
    test = objs[i].trajectory.T
    plt.plot(test[1],test[2])
plt.savefig("plots/figure1.png")