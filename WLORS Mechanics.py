# -*- coding: utf-8 -*-
"""
WLORS Mechanics
"""
###stray stuff that is declared in main file
attributes = ['strength', 'Agility', 'Intelligence', 'Constitution', 'Knowledge', 'luck', 'Awareness', 'Dexterity' ]
abilities = ['Crit %', 'Accuracy', 'Hitpoints', 'Mana Pool', 'Armour', 'Madness','Speed']
affectors = attributes + abilities

itemtypes = ['Torsowear', 'Headgear', 'Necklace', 'Trouserwear','Armbands','Rings']
userlib = []
chartemp = ['name','etc','level','exp','stats','equipment','buffs','status']
'''where stats is an array of base affectors, equipment is the list of 
equipment wielded, buff is the list of buffs, and status is the final, 
current state of the character'''
itemtemp = ['entryname', 'item', 'item level', 'item type','name','boon','description']
bufftemp = ['entryname','buff','name','duration','boon','description']
import numpy as np
import random as R

###



##Experience
#creating level boundaries which scale quadratically
lvlbounds = []
for i in range(30):
    lvlbounds.append(pow(i*10,2))
#
#function which checks total player xp against the level boundaries to determine the player level
def lvlcheck(xp):
    for i in range(len(lvlbounds)):
        if xp < sum(lvlbounds[:i]):
            lvl = i-1
            break
            break
        else:
            lvl = 'max'
    return lvl
#
#Function which updates the level of a character    
def lvlupdate(char):
    char[chartemp.index('level')] = lvlcheck(char[chartemp.index('exp')])
#  
##   
##item Creation

    
#library of items
itemlib = []
#
#choosing how item affects attributes and abilities
def attributeboon():
    ab = np.zeros(len(affectors))
    for i in attributes:
        val = input('How does this item affect {0}? '.format(i))
        if len(val) == 0:
            val = 0
        val = float(val)
        ab[affectors.index(i)] = val
    return ab
def abilityboon():
    ab = np.zeros(len(affectors))
    for i in abilities:
        val = input('How does this item affect {0}? '.format(i))
        if len(val) == 0:
            val = 0
        val = float(val)
        ab[affectors.index(i)] = val
    return ab
#
#defining boons
def boondef():
    boontype = 0
    while boontype not in ['base','ability','both']:
        boontype = input('Does this affect base attributes, superficial ability or both [base/ability/both]')
        if boontype == 'base':
            boono = attributeboon()
        elif boontype == 'ability':
            boono = abilityboon()
        elif boontype == 'both':
            boon1 = attributeboon() 
            boon2 = abilityboon()
            boono = boon1 + boon2
    return boono
#    
#function ran when identifying an item
'''item expected to take the form of a list [entryname, 'item' tag, item level, 'item type','name','boon','description']'''
def itemdefine(item,lorelevel):
    print('You attempt to identifiy the {0}'.format(item[3]))
    if lorelevel >= item[2]:
        descriptor = input('How would you describe the item before you? ')
        name = input('What do you care to name this object? ')      
        boon = boondef()
                
        item.append(name)  
        item.append(boon) 
        item.append(descriptor) 
        userlib.append(item)        
    else:
        print('Alas, the mysteries of this object still elude you')
#
#function to run when making an item afresh, mostly for gamebuilding bf play        
def itemmaker(entryname,level):
    itemtype = 0
    while itemtype not in itemtypes:
        itemtype = input('what type of item is this, is it {0} or {1}? '.format(itemtypes[:-1],itemtypes[-1]))
    newitem = [entryname,'item',level,itemtype]
    '''necessary since items which are generated will have all of those values already'''
    itemdefine(newitem,30)
#
##
##Buff creation
#Template buff
bufftemp= ['entryname','buff','name of buff', ['attribute effects of buff'], 'duration of buff', 'description of buff'] 
#   
#Definition function of buffs
def buffmaker(entryname):
    desc = input('How would you describe this buff? ')
    name = input('What would you call this buff? ')
    boon = boondef()
    
    duration = input('How long does this buff last, in turns? 0 for infinite ')
    if len(duration) == 0:
        duration = 0
    duration = int(duration)
    newbuff = [entryname,'buff']
    newbuff.append(name)
    newbuff.append(duration)  
    newbuff.append(boon) 
    newbuff.append(desc)
    userlib.append(newbuff)
bufftemp = ['entryname','buff','name','duration','boon','description']
#    

##
##Combination of base state and buffs/statuses to form current state (turn based)
#testing assets
kit1 = ['kit1', 'item', 2, 'Rings','Silver Ring',np.array([1, 1, 2, 0, 0, 0, 0, -1
,0, 0, 10, 0, 2, 0,0 ]),'Simple Silver Ring']
kit2 = ['kit1', 'item', 2, 'Headgear','Gold Circlet',np.array([1, 1, 2, 0, 4, 0, 0, -1
,0, 0, 10, 0, 2, 0,0 ]),'Small golden crown']
buff1 = ['buff1','buff','Testbuff','3',np.array([1, 3, 0, 1,1, -2, 1, 3
,2, 0, 0, 0, 0, 0,3 ]),'basic testing buff']
testchar = ['test','deets',3,3000,np.array([10, 10, 12, 8, 15, 5, 18, 2 ,0,0,0,0,0,0,0]),[],[],np.zeros(len(affectors))]
#
#build function
def build(char):
    #extraction of relevant arrays
    a = char[chartemp.index('stats')]#character raw stats
    b = np.zeros(15)#Character equipment stats
    for i in char[chartemp.index('equipment')]:
        b += i[itemtemp.index('boon')]
    c = np.zeros(15)#Character Buff stats
    for i in char[chartemp.index('buffs')]:
        c += i[bufftemp.index('boon')]
    #
    #conversion of stats into abilities
    val = a+b+c
    val[affectors.index('Crit %')] += val[affectors.index('Awareness')]
    val[affectors.index('Accuracy')] += val[affectors.index('Dexterity')]
    val[affectors.index('Speed')] += 5*val[affectors.index('Agility')]
    val[affectors.index('Mana Pool')] += 50*val[affectors.index('Intelligence')]
    val[affectors.index('Madness')] += R.random()*5*val[affectors.index('Knowledge')]
    val[affectors.index('Hitpoints')] += val[affectors.index('Constitution')]
    char[chartemp.index('status')] += val
    #
#
##
##equip and buff functions acting on characters
#equip function
def equip(char,item):
    char[chartemp.index('equipment')].append(item)
#
#buff function
def buff(char,buff):
    char[chartemp.index('buffs')].append(buff)
#
##
    