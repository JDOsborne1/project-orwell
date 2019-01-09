from random import randint
def ran(upper,lower):
	rn = randint(upper,lower)
	return rn
def roll(DC):
	return (DC < ran(0,100))
	