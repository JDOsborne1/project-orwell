import numpy as np

def remnant(Node,Type,Net,Track):
    '''
    Net is the array of connections
    Track is the tracking array which tracks the finalised values
    Function specific variables
    Node is the node in question
    '''
    l = len(Net)
    Conns = Net[Node] # Vector of connections for the specific node
    SpTrack = Track[Type] #Tracking table sliced for the remnants of the specified type

    Value = 0 #Node value for that type at that node
    for i in range(l):
        if Conns[i] != 0:
            Value += SpTrack[i]*Conns[i]/10
        
    return Value

def spillover2(Type,Net,Track):
    l = len(Net)
    remaining = True
    while remaining:
        Virtual = np.zeros(l)
        for i in range(l):
            if Track[Type][i] == 0:
                Virtual[i] = remnant(i,Type,Net,Track)

        if sum(Virtual) != 0:
            for i in np.where(Virtual == max(Virtual)):
                Track[Type][i]=Virtual[i]
        else:
            remaining = False

def pathfind(Net, Track, Destination, Location):
    #Function specific
    Vision = Track[Destination] #Slices out the remnants for the specified destination node

    while Location != Destination:
        Conns = Net[Location] #Slices out the vector of connections for the specified location node

        Seen =  Vision * Conns# The array of potentials directly seen from the location node

        Aim = np.where(Seen==max(Seen))[0][0]

        print('At {}'.format(Location))
        print('Aiming at {}'.format(Aim))
        Location = Aim

def partialPathfind(Net, Track, Destination, Location):

        Seen = Track[Destination] * Net[Location]# The array of potentials directly seen from the location node

        Aim = np.where(Seen==max(Seen))[0][0]
        return Aim