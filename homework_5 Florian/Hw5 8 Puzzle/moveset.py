moves = {
    0 : ['u','l'],
    1 : ['r','u','l'],
    2 : ['r','u'],
    3 : ['u','l','d'],
    4 : ['r','u','l','d'],
    5 : ['r','u','d'],
    6 : ['l','d'],
    7 : ['r','l','d'],
    8 : ['r','d']
}



def position(action,oldpos):
    newpos=oldpos[:]
    if action=='r':
        newpos[x]=newpos[x-1]
        newpos[x-1]=0
        return newpos
    if action=='u':
        newpos[x]=newpos[x+3]
        newpos[x+3]=0
        return newpos
    if action=='l':
        newpos[x]=newpos[x+1]
        newpos[x+1]=0
        return newpos
    if action=='d':
        newpos[x]=newpos[x-3]
        newpos[x-3]=0
        return newpos