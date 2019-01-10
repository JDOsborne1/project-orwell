## Character Classes
# Object oriented classes and functions derived from the WLORS script
import numpy as np

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
    def __init__(self, address, race, class_style, attributes, description, library):
        '''Address is the full phrase that someone would use to identify someone,
        ie Mr. Testy The Brave'''
        self.name = nameext(address)
        self.title = titleext(address)
        self.moniker = monikerext(address)
        self.race = race
        self.class_style = class_style
        self.attributes = attributes
        self.description = description       
        self.library = library
    def localise(self, locale):
        self.locale = locale 
    def updatelocale(self, newlocale):
        print(self.locale.scene)
        newlocale = get( 'where next? ',str)
        for i in self.library.locales:
            if i.scene == newlocale:
                self.locale = i
        
def character_creation():
    return Character(get('Address', str),
                     get('Race',str),
                     get('Class',str),
                     {i: get(i, int) for i in ['Strength','Intelligence','Agility',
                              'Dexterity','Wisdom','Madness','Luck',
                              'Fortitude','Wits']},
                     get('Description',str))

class Locale:
    def __init__(self, name, open_closed, coord, connectionref):
        '''
        I would want to include as an argument to initialiser a connection element
        which would indicate where it can connect to integrating with its spillover
        connections
        '''
        self.name = name 
        self.open_closed = open_closed
        self.coord = coord
        self.connectionref


    def inon(self):
        '''
        just describes if the location is enclosed or not
        ''' 
        return self.open_closed

    def scene(self):
        '''
        Currently just returns the name of the Locale, eventually would generate 
        a better description
        '''
        return 'you are' + str(self.open_closed) + self.name


def create_locale():
    return Locale(get('Locale name: ',str), 
                  get('open? : ', bool), 
                  get('co-ordinates? ', np.array), 
                  get('connection reference', str ))
# the coordinate argument can be that of a reference value in the spillover matrix.
# that reference value can also be pointed to in a dictionary with the position of 
# the locale this would also allow for the rooms to be created, their locations to
# be embedded in this dictionary, and then for a routine to run through and calculate
# the connectiveness between locales, which can be at first generated as a function
# of the terrain in between the two spaces, but then over time become a dynamic 
# connectiveness determined at least partially by traffic

class Library:
    def __init__(self, name):
        '''
        Defines the library class, which is the current format of the structure of 
        things known to an entity
        '''
        self.name = name

class Environment:
    def __init__(self, name):
        '''
        Defines the Environment class, which contains multiple locales and describes 
        and calculates their relationships with each other, consequently allowing 
        movement between them
        '''
        self.name = name