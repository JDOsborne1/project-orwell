## Character Classes
# Object oriented classes and functions derived from the WLORS script


def get(St, func):
    try:
        Va = func(input(St) )
        return Va
    except ValueError:
        return get(St,func) 
 ## making a class which has the blueprint of the character that I'm looking for
def titleext(address):
    return address[:4]
def nameext(address):
    return address[4:10]
def monikerext(address):
    return address[11:]

class Character:
    def __init__(self, address, race, class_style, attributes, description):
        '''Address is the full phrase that someone would use to identify someone,
        ie Mr. Testy The Brave'''
        self.name = nameext(address)
        self.title = titleext(address)
        self.moniker = monikerext(address)
        self.race = race
        self.class_style = class_style
        self.attributes = attributes
        self.description = description        
        
def character_creation():
    return Character(get('Address', str),
                     get('Race',str),
                     get('Class',str),
                     {i: get(i, int) for i in ['Strength','Intelligence','Agility',
                              'Dexterity','Wisdom','Madness','Luck',
                              'Fortitude','Wits']},
                     get('Description',str))
    