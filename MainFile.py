###Project Orwell Main file
##Synopsis
#Script containing the core mechanics for the project, including the representation of people, objects and structures as distinct classes which use data structures and methods to simulate elements of life. With location and velocity being updated by physical accelerations provided by the environment, and things like emotions and ideologies being updated by mental accelerations provided by the environment.
##
##Imports
import numpy as np
##
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
		self.forces = forces
		self.trajectory = self.pos# want to create a 2 dimensional array, with the vector of the position as one dimension and then the time of occurance as another.
	def update(self,pot,timestep):
		try:
			r_=np.array([pot.field[self.z,self.y,self.x]-pot.field[self.z,self.y,self.x],pot.field[self.z,self.y+1,self.x]-pot.field[self.z,self.y-1,self.x],pot.field[self.z,self.y,self.x+1]-pot.field[self.z,self.y,self.x-1]])
		except IndexError:
			r_=np.zeros(3)
		acc=self.forces[pot.name][1]*-1*r_
		self.pos += timestep * self.vel
		self.pos %= 40
		self.vel += timestep * acc
		self.z = int(self.pos[0])
		self.y = int(self.pos[1])
		self.x = int(self.pos[2])
		self.trajectory = np.vstack([self.trajectory, self.pos])# want to make the trajectory be appended by the most recen position after each update, therefore creating acomplete record of the positoon of the pbject at each timestep. 

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
		maxrangesquared = 2*(self.width**2)*(np.log(entity.forces[self.name][0])-np.log(sensitivity))
		return np.sqrt(maxrangesquared)
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
##Defining the Potential spaces for the accelerations

pots=[Potential('test',1,40,40,3)]#formatting of z,y,x
objs = [Entity('test2',0,15,14,0,0,0,{'test':(3,0.01)}),Entity('test3',0,15,18,0,0.2,0,{'test':(1,0.3)}),Entity('test4',0,15,17,0,0.2,0.05,{'test':(0.5,0.3)})]
			

'''
np.savetxt('C:\\Users\\theos\\Dropbox\\Documents\\PythonLibrary\\ProjectOrwell\\Field.csv',pots[0].field[0],delimiter=',',newline='\n')
'''
##
##Experimenting with some basic sets


'''
Theorise that a redesign using a system of updateing only the areas of the potential which will be affected noticably, and have the update type be applying a calculated difference.
'''

'''
suggested effciency move to not run the update code where the change would be minimal. calculate the range at which the gaussian topography becaomes effectively zero and just ignore those co-ordinates when updating. 
the magnitude of the change depends on the magnitude of the vecotr of differences in position. a constraint on that vector defines a sphere of non-sero affectation. 

the radius wil be defined by the object's gravitas and the range of the force. in the form of gravitas x exponential of 1/ twice the square of the range. this will be a positive value, which will be exponentially damped by the negative exponent of the magnitude of the difference in position. there will be a criteria where a given radius is sufficient to damp the function almost entirely to zero.

calculated for this test as the force power of 1/2 which comes from both the range and the gravitas parameters being defined as 1 for the test. it is then 1/2 * exp(-r**2) where r is the variable describing the magnitude of the positional difference. for a threshold of 1x10^-4 the inequality is then when fp*exp(-r**2) < 1x10^-4 which will be calculate by had to prduce a formula for a general force power

'''
'''Sensitivity scale test
plt.plot(np.log(np.linspace(0.001,10,100))-np.log(1e-4),label='e-4 sensitivity')
plt.plot(np.log(np.linspace(0.001,10,100))-np.log(1e-5),label='e-5 sensitivity')
plt.plot(np.log(np.linspace(0.001,10,100))-np.log(1e-6),label='e-5 sensitivity')
plt.xlabel('Force Power')
plt.ylabel('Radius squared where change is non-zero')
plt.legend()
plt.show()


'''