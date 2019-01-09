##Imports
import numpy as np
import vpython as vp
import matplotlib.pyplot as plt
import random
##
def norm(vector):
    return vector/np.linalg.norm(vector)
##defining the classes and their methods
#beginning with objects, which are the general class, with only physical accelerations, and the other classes can be subclasses of objects
class Entity:
    def __init__(self,name,z,y,x,velz,vely,velx,forces):#grav, inter, pos and vel are lists. pos and vel are 3vectors, args are expected to be a set of tuples of the gravitas' and interaction strength's of the object on the set of potentials paired with a dictionary of the potentials names.
        self.x = x#calling the x,y,z components of the entity's position will return the integer values of the co-ordinates of the object on the raster map
        self.y = y
        self.z = z
        self.name = name
        self.vel = np.array([velz,vely,velx],dtype='float64')
        self.pos = np.array([z,y,x],dtype='float64')
        self.rpos=self.pos.astype(int)
        self.forces = forces
        self.trajectory = self.pos# want to create a 2 dimensional array, with the vector of the position as one dimension and then the time of occurance as another.

    
    def update(self,pot,timestep):
        '''looks to find the potential at the six points on the field adjacent to the objects position'''
        try:#to find the direction vector of the force experienced by the object. Uses a set of tuples as the field indexes and wraps them according to the shape of the field
            r_=np.array([pot.field[tuple((self.rpos)%pot.field.shape[0])]-pot.field[tuple((self.rpos)%pot.field.shape[0])],
          pot.field[tuple((self.rpos+(0,1,0))%pot.field.shape[1])]-pot.field[tuple((self.rpos+(0,-1,0))%pot.field.shape[1])],
          pot.field[tuple((self.rpos+(0,0,1))%pot.field.shape[2])]-pot.field[tuple((self.rpos+(0,0,-1))%pot.field.shape[2])]])
        except IndexError:
            r_=np.zeros(3)
            print('indexerror')
        acc=self.forces[pot.name][1]*-1*r_
        self.pos += timestep * self.vel
        self.pos %= 40
        self.rpos=self.pos.astype(int)
        self.vel *=0.97
        self.vel += timestep * acc
        self.z,self.y,self.x = self.rpos[0],self.rpos[1],self.rpos[2]
        self.trajectory = np.vstack([self.trajectory, self.pos])# want to make the trajectory be appended by the most recen position after each update, therefore creating acomplete record of the positoon of the pbject at each timestep. 
    def direct(self,objective,deter):
        self.objective = objective
        self.deter = deter
        
class Structure(Entity):
    def __init__(self):# the subcalss initialisation is broken, replace
        super(Structure, self).__init__()
    def update(self,pot,timestep):
        pass
class Potential:#this defines the class of potentials, this was used to both conform with the general style of oop for the rest of the project and so that the unique evaluation method can be defined
    def __init__(self,name,dimz,dimy,dimx,width):#defines the potential's name, initial dimensions, and the width parameter describing its range.
        self.name = name
        self.field = np.zeros((dimz,dimy,dimx))
        self.width = width
    def rangetest(self,entity,sensitivity):
        gravitas = np.abs(entity.forces[self.name][0])
        if gravitas != 0: #cannot permit zero in the cases where a field has no range, and cannot be less than zero as it would be if it wouldnt be detected at the specified level at any range.
            maxrangesquared = 2*(self.width**2)*(np.log(gravitas)-np.log(sensitivity))
        else:
            maxrangesquared = 0.0
        if maxrangesquared > 0:
            maxrange= np.sqrt(maxrangesquared)
        else:
            maxrange = 0
        return maxrange
    def update(self,i,ran):#i is an list of object, which is generating a field of that potential type
        self.field = np.zeros(np.shape(self.field))
        for j in i:
            r_raw=self.rangetest(j,ran)#gets the raw, floating value of the range limitation from the rangetest method
            r = int(round(r_raw))#rounds the value to the nearest integer and uses that as the criteria to create the cube of acceptable values
            for z in range(0,1):
                for y in range(j.y - r,j.y + r+1):#remember to include the z range variance once working with 3d variables
                    for x in range(j.x - r,j.x + r+1):
                        rp_mag = np.linalg.norm(np.array([x-j.x,y-j.y,z-j.z]))#fins the magnitude of the difference vector between the raised co-ordinates and the co-ordinates of the entity in question
                        if rp_mag<r_raw:#implements the further limits on the cube of acceptable values to create the sphere of acceptable values
                            try:
                                self.field[z,y,x] -= j.forces[self.name][0]*np.exp(-1*pow(rp_mag,2)/(2*pow(self.width,2)))#calls up the value at those co-ords and updates it withthe new calculation
                            except IndexError:
                                continue
                        else:
                            continue
##

##Defining the objects for the simulation

pots=[Potential('Grav',1,40,40,4),Potential('Radpres',1,40,40,3)]#formatting of z,y,x
objs = [Entity('test1',0,15,17,0,0.4,0.05,{'Grav':(0.5,0),'Radpres':(-1,0)}),
        Entity('test2',0,16,17,0,0.3,0.025,{'Grav':(0.5,0),'Radpres':(-1,0)}),
        Entity('test3',0,15,16,0,0.2,0.1,{'Grav':(0.5,0),'Radpres':(-1,0)}),
        Entity('test4',0,16,16,0,0.1,0,{'Grav':(0.5,0),'Radpres':(-1,0)})]
'''Simulating entities with outward pressure'''
for j in range(0):
    objs.append(Entity('Mount{}'.format(j),
                       0,random.randint(0,40),random.randint(0,40),
                       0,0,0,
                       {'Grav':(0,0),'Radpres':(-random.random(),0)}))
'''Simulating entities gravitating towards one another'''    
for i in range(0):
    objs.append(Entity('Person{}'.format(i),
                       0,random.randint(0,40),random.randint(0,40),
                       0,random.random()-1,random.random()-1,
                       {'Grav':(random.random(),random.random()),'Radpres':(0,0.1)}))
			


##
##Running the sim
steps=2000
for t in range(steps):
    for p in pots:
        p.update(objs,0.01)
        for i in objs:
            i.update(p,0.1)
##
