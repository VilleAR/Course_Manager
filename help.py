import random

def run():

    charms=1000
    used=0
    while charms>0:
        rand=random.randint(1,10)
        if rand>3:
            charms=charms-1
        used+=1

    return used

arr=[]
for i in range (1,21):
    arr.append(run())

t=0
for r in arr:
    t=t+r
print(t/20)
