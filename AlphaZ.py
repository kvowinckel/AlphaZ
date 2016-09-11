
# coding: utf-8

# # AlphaZ #

# ## Sensor Value ##
# Ensure that the ''Arduino'' is connected to the COM3 Port

# In[1]:

import serial
import time
serArd = serial.Serial('COM3', 9600, timeout=0)
 
def getResult():
    while (_readSerial() == 0):
        time.sleep(1)
    time.sleep(1)
    return _readSerial()


def _readSerial():
    try:
        var = serArd.readline()
        if (len(var)>1):
            print (var)
            return int(float(var))
    except serArd.SerialTimeoutException:
        print('Data could not be read')
        return 0
        


# In[3]:

print ("Result: " + str(getResult()))


# ## Hardware connection ##
# Ensure that the ''OpenTrones'' is connected to the COM6 Port

# In[4]:

import serial
import time

serTro = serial.Serial('COM6', 115200, timeout=0.5)

# Use global Coords
serTro.write("G28\n")
serTro.write("G90\n")
serTro.write("GO F6000.0\n")

#serTro.send("GO X 100 Y 100 Z 0\n")
containerA1 = [156,295,96]
containerA2 = [156,315,96]
containerA3 = [156,335,96]
containerA4 = [156,355,96]
containerA5 = [156,375,96]
containerB1 = [176,295,96]
containerB2 = [176,315,96]
containerB3 = [176,335,96]
containerB4 = [176,355,96]
containerB5 = [176,375,96]
containerC1 = [196,295,96]
containerC2 = [196,315,96]
containerC3 = [196,335,96]
containerC4 = [196,355,96]
containerC5 = [196,375,96]

zyl1 = [156,275,96]
trash1 = [176,275,96]
trash2 = [196,275,96]
trash3 = [216,275,96]
trash4 = [216,315,96]
trash5 = [216,335,96]
trash6 = [216,355,96]
trash7 = [216,375,96]

time.sleep(10)

def _goToGlobalPos(pos):
    x = pos[0]
    y = pos[1]
    z = pos[2]
    serTro.write("GO X " + str(x) + " Y " + str(y) + " Z " + str(z) + " F6000.0\n")
    time.sleep(1)
    
def _pipettPushDown():
    serTro.write("GO A 12\n")
    time.sleep(1)

def _pipettPushUp():
    serTro.write("GO A 0\n")
    time.sleep(1)
    
def _moveDown():
    serTro.write("GO Z 123\n")
    time.sleep(1)
    
def _moveUp():
    serTro.write("GO Z 96\n")
    time.sleep(1)
    
def getSubstance(index, mix):
    if (index == 0):
        if (mix[0] - 5 < 0):
            _goToGlobalPos(containerA1)
        elif (mix[0] - 10 < 0):
            _goToGlobalPos(containerA2)
        elif (mix[0] - 15 < 0):
            _goToGlobalPos(containerA3)
        elif (mix[0] - 20 < 0):
            _goToGlobalPos(containerA4)
        else:
            _goToGlobalPos(containerA5)
    elif (index == 1):
        if (mix[1] - 5 < 0):
            _goToGlobalPos(containerB1)
        elif (mix[1] - 10 < 0):
            _goToGlobalPos(containerB2)
        elif (mix[1] - 15 < 0):
            _goToGlobalPos(containerB3)
        elif (mix[1] - 20 < 0):
            _goToGlobalPos(containerB4)
        else:
            _goToGlobalPos(containerB5)
    elif (index == 2):
        if (mix[2] - 5 < 0):
            _goToGlobalPos(containerC1)
        elif (mix[2] - 10 < 0):
            _goToGlobalPos(containerC2)
        elif (mix[2] - 15 < 0):
            _goToGlobalPos(containerC3)
        elif (mix[2] - 20 < 0):
            _goToGlobalPos(containerC4)
        else:
            _goToGlobalPos(containerC5)
        
    _pipettPushDown()
    _moveDown()
    _pipettPushUp()
    _moveUp()
    
def toZylinderMix(index):
    if (index == 0):
        _goToGlobalPos(zyl1)
        _moveDown()
        _pipettPushDown()
        _pipettPushUp()
        _moveUp()
        _pipettPushDown()
        _moveDown()
        _pipettPushUp()
        _moveUp()

def toZylinder(index):
    if (index == 0):
        _goToGlobalPos(zyl1)
        _moveDown()
        _pipettPushDown()
        _pipettPushUp()
        _moveUp()
        _pipettPushDown()       
        
def dumpTrash(mix):
    sum = mix[0] + mix[1] + mix[2]
    _moveUp()
    if (sum-10 < 0):
        _goToGlobalPos(trash1)
    elif (sum-20 < 0):
        _goToGlobalPos(trash2)
    elif (sum-30 < 0):
        _goToGlobalPos(trash3)
    elif (sum-40 < 0):
        _goToGlobalPos(trash4)
    elif (sum-50 < 0):
        _goToGlobalPos(trash5)
    elif (sum-60 < 0):
        _goToGlobalPos(trash6)
    else:
        _goToGlobalPos(trash7)
    _pipettPushDown()
    


def getMeasurement(index):
    return getResult()
    # TODO Measurement auch vorher im Sub. plazieren...


# ## Helpers ##

# In[5]:

import random

def norm(proA,proB,proC):
    sum = proA+proB+proC
    return [proA/sum, proB/sum, proC/sum]
    

def reward(proA, proB, proC, index):
    if (index == 0):
        proA = proA + rewardpercentage
    elif (index == 1):
        proB = proB + rewardpercentage
    elif (index == 2):
        proC = proC + rewardpercentage
    return norm(proA, proB, proC)

def punish(proA, proB, proC, index):
    if (index == 0):
        proA = proA - rewardpercentage
        if (proA < 0):
            proA = 0
    elif (index == 1):
        proB = proB - rewardpercentage
        if (proB < 0):
            proB = 0
    elif (index == 2):
        proC = proC - rewardpercentage
        if (proC < 0):
            proC = 0
    return norm(proA, proB, proC)

def getIndex(proA, proB, proC):
    sum = proA*100 + proB*100 + proC*100
    rnd = random.randint(1, 100)
    if (rnd < proA*100):
        return 0
    elif (rnd >= sum - proC*100):
        return 2
    else: 
        return 1
    


# ## Agent ##
# This is where the magic happens

# In[6]:

rewardpercentage = 0.10   # Die Belohnung/ Bestrafung der Actions
current_zyl_val = 0       # Der Füllstand des aktuellen Zylinders
current_zyl_index = 0     # Der aktuell zu befüllende Zylinder 
max_zyl_val = 50          # Der maximale Füllstand der Zylinder
sub_step = 5              # Wie viel in jedem Step vom Substr. aufgenommen wird
solution = [1,1,1]

# Initialize Action percentages with 1/3 each
proA = float(1) / 3
proB = proA
proC = proA

# Fill the first Zylinder with all substates
getSubstance(0,solution)
toZylinder(0)
getSubstance(0,solution)
toZylinder(0)
getSubstance(1,solution)
toZylinder(0)
getSubstance(1,solution)
toZylinder(0)
getSubstance(2,solution)
toZylinder(0)
getSubstance(2,solution)
toZylinder(0)

# Init. Measurement
time.sleep(50)
last_measure = getMeasurement(current_zyl_index)

step = 0
solutionArray = [solution]
percentageArray = [proA, proB, proC]
measureArray = [last_measure]
resfile = open('result.txt','w')
prefile = open('precentage.txt','w')
meafile = open('measurement.txt','w')

while step < 100:

    # Get next Substrate to add
    next_sub = getIndex(proA, proB, proC)

    # Add the Substrate
    getSubstance(next_sub, solution)
    toZylinderMix(current_zyl_index)
    
    # Add Substrate to Solution
    solution[next_sub] +=1
    solutionArray.append(solution)
    percentageArray.append([proA,proB,proC])
    print ("Current Mixture: " + str(solution))
    print ("Current AI - Procentages: " + str([proA, proB, proC]))
    
    resfile.write("%s\n" % solution)
    prefile.write("%s\n" % [proA,proB,proC])
    
    print("Tag 3")
    # Dump the Trash
    dumpTrash(solution)

    # Measure the result
    time.sleep(16)
    new_measure = getMeasurement(current_zyl_index)
    measureArray.append(new_measure)
    meafile.write("%s\n" % new_measure)

    # Reward or punish
    if (last_measure < new_measure):
        [proA, proB, proC] = reward(proA, proB, proC, next_sub)
    else:
        [proA, proB, proC] = punish(proA, proB, proC, next_sub)

    step += 1

meafile.close()
resfile.close()
prefile.close()


# In[ ]:

import numpy as np
import matplotlib.pyplot as plt

x=[]
for i in range(1,len(measureArray)+1):
    x.append(i)
    
plt.plot(x,measureArray)
plt.show()


# In[ ]:

a = [1,1,1]
a[1] += 1
solutionArray.append(a)
print (str(solutionArray))


# In[7]:

meafile.close()
resfile.close()
prefile.close()


# In[ ]:



