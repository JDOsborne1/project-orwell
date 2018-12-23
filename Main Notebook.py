
# coding: utf-8
#%%


###Project Orwell Main file
##Synopsis
'''
Script containing the core mechanics for the project, including the representation of people, objects and structures as 
distinct classes which use data structures and methods to simulate elements of life. With location and velocity being 
updated by physical accelerations provided by the environment, and things like emotions and ideologies being updated by
mental accelerations provided by the environment.
'''
##
##Imports
import numpy as np
import matplotlib.pyplot as plt
import random
##
#%%
##Function and Class definitions
#defining a custom normalization function, if a more efficient solution is found, then it can simply be inserted here, no upset
def norm(vector):
    return vector/np.linalg.norm(vector)
#

class Entity:
    '''
    defining the principle class of the objects simulated in the program, these are currently synonymous with the 'people'
    '''
    def __init__(self,name,z,y,x,velz,vely,velx,forces,maxcv=0.5):
        '''
        grav, inter, pos and vel are lists. pos and vel are 3vectors, args are expected to be a set of tuples of the gravitas' 
        and interaction strength's of the object on the set of potentials paired with a dictionary of the potentials names.
        calling the x,y,z components of the entity's position will return the integer values of the co-ordinates of the object 
        on the raster map.
        want to create a 2 dimensional array, with the vector of the position as one dimension and then the time of occurance 
        as another.
        the fatigue represents the object's tiredness with moving at it current pace. it will grow whenever it is moving above
        the max comfortable pace and decay whenever it is below. 
        '''
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.vel = np.array([velz,vely,velx],dtype='float64')
        self.pos = np.array([z,y,x],dtype='float64')
        self.rpos=self.pos.astype(int)
        self.forces = forces
        self.trajectory = self.pos
        self.fatigue = 0
        self.maxcv = maxcv
    def getForces(self,potname):
        '''Function which gets the forces tuple for the specified potential if it exists'''
        try:
            return self.forces[potname]
        except KeyError:
            return 0,0
    def update(self,pot,timestep):
        '''looks to find the potential at the six points on the field adjacent to the objects position
        initially tries to find the direction vector of the force experienced by the object. Uses a set of tuples as the 
        field indexes and wraps them according to the shape of the field
        once successful it then stacks the new position onto the trajectory matrix, extending it and thus recording the 
        positition at that time interval.
        '''
        


        self.pos += timestep * self.vel
        self.pos %= 363
        self.rpos=self.pos.astype(int)
        self.fatigueupdate()
        self.vel *= 1-self.fatigue
        self.vel += timestep * (self.getAcc(pot) + self.getQuestAcc())
        self.z,self.y,self.x = self.rpos[0],self.rpos[1],self.rpos[2]
        self.trajectory = np.vstack([self.trajectory, self.pos])
        self.checkQuest()
    def fatigueupdate(self):
        self.fatigue += (np.linalg.norm(self.vel)/self.maxcv) -1
        if self.fatigue > 1:
            self.fatigue = 1
        elif self.fatigue <0:
            self.fatigue = 0
    def getAcc(self,pot):
        try:
            r_=np.array([pot.field[tuple((self.rpos)%pot.field.shape[0])]-pot.field[tuple((self.rpos)%pot.field.shape[0])],pot.field[tuple((self.rpos+(0,1,0))%pot.field.shape[1])]-pot.field[tuple((self.rpos+(0,-1,0))%pot.field.shape[1])],pot.field[tuple((self.rpos+(0,0,1))%pot.field.shape[2])]-pot.field[tuple((self.rpos+(0,0,-1))%pot.field.shape[2])]])
        except IndexError:
            r_=np.zeros(3)
            print('indexerror')
        return self.getForces(pot.name)[1]*1*r_ 
    def getQuestAcc(self):
        try:
            dir_quest = self.objective-self.pos
            acc_quest = self. deter * dir_quest/np.linalg.norm(dir_quest)
            return acc_quest
        except AttributeError:
            return np.zeros(3)
    def setQuest(self,objective,deter):
        '''Function which introduces a directive to the object'''
        self.objective = objective # the location of the objective
        self.deter = deter # the drive/determination of the entity to get to the objective
    def checkQuest(self):
        try:
            if np.linalg.norm(self.objective-self.pos) < 0.5:
                delattr(self,'objective')
            else:
                pass
        except AttributeError:
            pass
        except NameError:
            pass
        
class Potential:
    '''this defines the class of potentials, this was used to both conform with the general style of oop for the rest of the project 
    and so that the unique evaluation method can be defined '''
    def __init__(self,name,dimz,dimy,dimx,width):
        '''
        defines the potential's name, initial dimensions, and the width parameter describing its range.
        '''
        self.name = name
        self.field = np.zeros((dimz,dimy,dimx))
        self.width = width
    def rangetest(self,entity,sensitivity):
        '''
        cannot permit zero in the cases where a field has no range, and cannot be less than zero as it would be 
        if it wouldnt be detected at the specified level at any range.
        '''
        gravitas = np.abs(entity.getForces(self.name)[0])
        if gravitas != 0:
            maxrangesquared = 2*(self.width**2)*(np.log(gravitas)-np.log(sensitivity))
        else:
            maxrangesquared = 0.0
        if maxrangesquared > 0:
            maxrange= np.sqrt(maxrangesquared)
        else:    
            maxrange = 0
        return maxrange
    def update(self,i,ran):
        '''i is an list of object, which is generating a field of that potential type
        First gets the raw, floating value of the range limitation from the rangetest method
        then rounds the value to the nearest integer and uses that as the criteria to create the cube of acceptable values
        then finds the magnitude of the difference vector between the raised co-ordinates and the co-ordinates of the entity 
        in question
        then implements the further limits on the cube of acceptable values to create the sphere of acceptable values
        then for each value in that sphere it calls up the value at those co-ords and updates it withthe new calculation                
        '''        
        self.field = np.zeros(np.shape(self.field))
        for j in i:
            r_raw=self.rangetest(j,ran)
            r = int(round(r_raw))
            for z in range(0,1):
                for y in range(j.y - r,j.y + r+1):#include the z range variance once working with 3d variables            
                    for x in range(j.x - r,j.x + r+1):
                        rp_mag = np.linalg.norm(np.array([x-j.x,y-j.y,z-j.z]))
                        if rp_mag<r_raw:
                            try:
                                self.field[z,y,x] += j.getForces(self.name)[0]*np.exp(-1*pow(rp_mag,2)/(2*pow(self.width,2)))
                            except IndexError:
                                continue
                        else:
                            continue
##

#%%


##Defining the instances of the potentials and objects

pots=[Potential('Grav',1,363,363,10),Potential('Radpres',1,363,363,3)]#formatting of z,y,x
objs = []
'''Simulating entities with outward pressure'''
for j in range(0):
    objs.append(Entity('Mount{}'.format(j),
                       0,random.randint(0,363),random.randint(0,363),
                       0,0,0,
                       {'Grav':(0,0),'Radpres':(-random.random(),0)}))
'''Simulating entities gravitating towards one another'''    
for i in range(300):
    objs.append(Entity('Person{}'.format(i),
                       0,random.randint(0,363),random.randint(0,363),
                       0,random.random(),random.random(),
                       {'Grav':(random.random(),random.random())}))

##


#%%


##Running the sim
steps=300
for t in range(steps):
    for p in pots:
        p.update(objs,0.01)
        for i in objs:
            i.update(p,0.1)
##
#%%


##Trajectory plotting on static map
for i in range(len(objs)):
    test = objs[i].trajectory.T
    plt.plot(test[1],test[2])
plt.show()
##

#%%

for i in range(1,12):
    for j in range(1,12):
         np.savetxt('C:/Users/Joe/Documents/project-orwell/field{0},{1}.csv'.format(i,j), pots[0].field[0][(i-1)*33:i*33,(j-1)*33:j*33], delimiter=',', newline='\n')


#%%
np.savetxt('C:/Users/Joe/Documents/project-orwell/field.csv', pots[0].field[0], delimiter=',', newline='\n')

