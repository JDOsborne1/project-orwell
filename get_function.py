
def get(self,St, func):
    try:
        Va = func(input(St) )
        return Va
    except ValueError:
        return get(St,func) 

def get2(self, string, func, bounds):
    try:
        value = func(input(string))
        if value in bounds:
            return value
        else:
            return get(string, func, bounds)
    except ValueError:
        return get(string, func, bounds)
