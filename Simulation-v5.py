# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 17:56:25 2018
@version: 5
@author: Stephon
"""

import config
import datetime
from math import floor
from random import randint
from matplotlib import pyplot as plt
from functions import initialize,genID,genXY,checkID,validID
from matplotlib.backends.backend_pdf import PdfPages
#from config import usedIDs,zombieList,susceptList,removeList,infectList,recoverList,immuneList

now = datetime.datetime.now()

##############################################################################
# Population Tracker Functions
##############################################################################
totalID = []
susceptID = []
zombieID = []
infectID = []
removeID = []
immuneID = []
recoverID = []

def toZombie(id):
    for x in zombieID:
        if x in susceptID:
            susceptID.remove(id)
        elif x in infectID:
            infectID.remove(id)
        elif x in removeID:
            removeID.remove(id)
        elif x in immuneID:
            immuneID.remove(id)
        elif x in recoverID:
            recoverID.remove(id)

def toSuscept(id):
    for x in susceptID:
        if x in zombieID:
            zombieID.remove(id)
        elif x in infectID:
            infectID.remove(id)
        elif x in removeID:
            removeID.remove(id)
        elif x in immuneID:
            immuneID.remove(id)
        elif x in recoverID:
            recoverID.remove(id)
            
def toInfect(id):
    for x in infectID:
        if x in zombieID:
            zombieID.remove(id)
        elif x in susceptID:
            susceptID.remove(id)
        elif x in removeID:
            removeID.remove(id)
        elif x in immuneID:
            immuneID.remove(id)
        elif x in recoverID:
            recoverID.remove(id)

def toRemove(id):
    for x in removeID:
        if x in zombieID:
            zombieID.remove(id)
        elif x in susceptID:
            susceptID.remove(id)
        elif x in infectID:
            infectID.remove(id)
        elif x in immuneID:
            immuneID.remove(id)
        elif x in recoverID:
            recoverID.remove(id)

def toImmune(id):
    for x in immuneID:
        if x in zombieID:
            zombieID.remove(id)
        elif x in susceptID:
            susceptID.remove(id)
        elif x in infectID:
            infectID.remove(id)
        elif x in removeID:
            removeID.remove(id)
        elif x in recoverID:
            recoverID.remove(id)

def toRecover(id):
    for x in recoverID:
        if x in zombieID:
            zombieID.remove(id)
        elif x in susceptID:
            susceptID.remove(id)
        elif x in infectID:
            infectID.remove(id)
        elif x in removeID:
            removeID.remove(id)
        elif x in immuneID:
            immuneID.remove(id)

##############################################################################
# Overall Superclasses
##############################################################################
class Point(object):
    def __init__(self):
        initialLocation = genXY()
        self.x = initialLocation[0]
        self.y = initialLocation[1]
    
    def __str__(self):
        return "x = {0}, y = {1}".format(self.x, self.y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

class Person(Point):
    def __init__(self):
        super().__init__()
        self.id = checkID()
        #self.__cures = 0
        
    def __str__(self):
        return "Person of class {} located at ({},{})\n".format(self.getStatus(),self.x,self.y)
    
    def __eq__(self, other):
        if isinstance(self, Person):
            return ((self.x == other.x) and (self.y == other.y))
        

    def setID(self, id):
        idCheck = validID(id)
        if idCheck == True:
            self.id = id
        if idCheck == False:
            print("Err: This id is already in use. Please try again.")

    def getID(self):
        return self.id
    
    def getAge(self):
        listID = [str(x) for x in str(self.id)]
        age = int("".join(listID[1:3]))
        return age
    
    def getGender(self):
        listID = [int(x) for x in str(self.id)]
        gender = listID[0]
        if gender == 1:
            return "Male"
        elif gender == 2:
            return "Female"
        
    def getStatus(self):
        return type(self).__name__
    
    def changeStatus(self, newStatus):
        if newStatus == "Susceptible":
            susceptID.append(self.id)
            self.__class__ = Susceptible
            toSuscept(self.id)
        elif newStatus == "Infected":
            infectID.append(self.id)
            self.__class__ = Infected
            toInfect(self.id)
        elif newStatus == "Removed":
            removeID.append(self.id)
            self.__class__ = Removed
            self.timeOfDeath = config.time
            toRemove(self.id)
        elif newStatus == "Immune":
            immuneID.append(self.id)
            self.__class__= Immune
            self.cures = 0
            toImmune(self.id)
        elif newStatus == "Recovered":
            recoverID.append(self.id)
            self.__class__ = Recovered
            toRecover(self.id)
        elif newStatus == "Zombie":
            zombieID.append(self.id)
            self.__class__ = Zombie
            toZombie(self.id)
            
    def walk(self): #**if in bounds, keep walking LOOP**
        self.x += randint(-1,1)
        self.y += randint(-1,1)
        
        if self.x < 0:
            self.x = 0
        if self.x > config.boundary:
            self.x = config.boundary
        if self.y < 0:
            self.y = 0
        if self.y > config.boundary:
            self.y = config.boundary

    def engage(self):
        pass

    def roll_die(self):
        draw = randint(1,100)
        
        if draw <= 70:
            return "Outcome 1"
        elif draw <= 90:
            return "Outcome 2"
        else:
            return "Outcome 3"

##############################################################################
# Individual State Subclasses
##############################################################################        
class Susceptible(Person):
    def __init__(self):
        super().__init__()
        self.defense = 10
        
    def buildDefense(self):
        if self.defense >= 10 and self.defense <= 90:
            multiplier = randint(1,100)
            if multiplier not in [50, 75, 100]:
                if multiplier < 50:
                    self.defense += 1
            else:
                self.defense += int(1 * multiplier/25)
        if self.defense > 80:
            self.defense = 80
            
        if self.defense < 10:
            self.defense = 10
                
    def getDefense(self):
        return self.defense
    
    def loseDefense(self, decrease):
        self.defense - decrease
        
    def resetDefense(self):
        self.defense = 10

class Infected(Person):
    def __init__(self):
        super().__init__()

    def determineFate(self):
        draw = randint(1,100)
        if draw <= 10:
            pass
        elif draw <= 90:
            self.changeStatus("Zombie")
        elif draw <= 94:
            self.changeStatus("Removed")
        else:
            self.changeStatus("Immune")

class Removed(Person):
    def __init__(self):
        super().__init__()
        self.timeOfDeath = config.time
        self.causeOfDeath = ""
        
    def setCOD(self, reason):
        self.causeOfDeath = reason
        
    def getTOD(self):
        return self.timeOfDeath
    
    def getCOD(self):
        return self.causeOfDeath

class Immune(Person):
    def __init__(self):
        super().__init__()
        #self.cures = 0
        
    def cureCount(self):
        return self.cures
        
    def developCure(self):
        draw1 = randint(1,100)
        draw2 = randint(1,100)
        val = 0
        if draw1 <= 50:
            val += 1
        if draw2 >= 50:
            val += 1
        if val == 2:
            self.cures += 1

    def heal(self, personHealed):
        draw = randint(1,100)
        if personHealed.getStatus() == "Zombie" and self.cureCount() > 0:
            if draw <= 70:
                personHealed.changeStatus("Recovered")
                self.cures -= 1
            else:
                #personHealed.changeStatus("Zombie")
                pass
        if personHealed.getStatus() == "Infected" and self.cureCount() > 0:
            if draw <= 90:
                personHealed.changeStatus("Recovered")
                self.cures -= 1
            else:
                #personHealed.changeStatus("Zombie")
                pass
            
    def locationHeal(self,personHealed):
        if (self.getY() == personHealed.getX()) and (self.getX() == personHealed.getX()) and personHealed.getStatus() == "Zombie":
            return self.heal(personHealed)
        elif personHealed.getStatus() != "Zombie":
            print("Not a Zombie!")
        else:
            print("Not in same location")

class Recovered(Person):
    
    def __init__(self):
        super().__init__()
        
    def determineFate(self):
        draw = randint(1,100)
        if draw <= 20:
            pass
        elif draw <= 90:
            self.changeStatus("Susceptible")
        else:
            self.changeStatus("Immune")
        

    def determineImmunity(self):
            draw = randint(1,100)
            if draw < 90 :
                return self.changeStatus("Susceptible")
            else:
                return self.changeStatus("Immune")

class Zombie(Person):
    def __init__(self):
        super().__init__()

    def bite(self, personBitten):
        if personBitten.getStatus() == "Susceptible":
            defense = personBitten.getDefense() 
            draw = randint(1,100)
            if draw < defense:
                personBitten.loseDefense(randint(10,40))
            elif draw < int(defense + (floor(100 - defense) * 0.95)):
                personBitten.resetDefense()
                personBitten.changeStatus("Infected")
            else:
                personBitten.changeStatus("Removed")
                personBitten.setCOD("Died of Zombie bite")
        
        if personBitten.getStatus() == "Immune":
            low = [x for x in range(15,51)]
            medium = [x for x in range(51,61)]
            draw = randint(1,100)
            if personBitten.getAge() in low:
                if draw <= 5:
                    personBitten.changeStatus("Removed")
                    personBitten.setCOD("Died of Zombie attack")
            if personBitten.getAge() in medium:
                if draw <= 15:
                    personBitten.changeStatus("Removed")
                    personBitten.setCOD("Died of Zombie attack")
            
            
    def locationBite(self,personBitten):
        if (self.getY() == personBitten.getX()) and (self.getX() == personBitten.getX()) and personBitten.getStatus() == "Susceptible":
            return self.bite(personBitten)
        elif personBitten.getStatus() != "Susceptible":
            print("Not Susceptible")
        else:
            print("Not in same location")

##############################################################################
#Zombie Simulation
##############################################################################
zombieList = []
susceptList = []
removeList = []
infectList = []
recoverList = []
immuneList = []
per= {}

def main():
    global per
    
    initialize()
    
    input("\nPress enter to generate your population: ")
    print("\n")
    
    
    per = {x:Susceptible() for x in range(1, config.initPop + 1)}
    for x in per:
        print(str(x) + ": " + str(per[x]))
    
    
    
    
    
    for x in range(1, config.initPop + 1):
        globals()["per"+str(x)] = Susceptible()
        totalID.append(globals()["per"+str(x)].getID())
        susceptID.append(globals()["per"+str(x)].getID())
        
    for y in range(1, config.zombiePop + 1):
        globals()["per"+str(y)].changeStatus("Zombie")
        
    endVal = len(totalID) + 1
    for x in range(1, endVal):
        print(str(x) + ": "+ str(globals()["per"+str(x)]))
    
    input("\nPress enter to run simulation: ")
    print("\n")
    
    config.susceptPop = len(susceptID)
    runSim = True
    while runSim:
    #while config.time < 672:
        #print("\nTime {}".format(time))
        
        for x in range(1, endVal):
            globals()["per"+str(x)].walk()
            if globals()["per"+str(x)].getStatus() == "Susceptible":
                globals()["per"+str(x)].buildDefense()
            if globals()["per"+str(x)].getStatus() == "Infected" or globals()["per"+str(x)].getStatus() == "Recovered":
                globals()["per"+str(x)].determineFate()
                if globals()["per"+str(x)].getStatus() == "Removed":
                    globals()["per"+str(x)].setCOD("Died of infection")
            if globals()["per"+str(x)].getStatus() == "Immune":
                globals()["per"+str(x)].developCure()
        
        for x in range(1,endVal):
            for y in range(1,endVal):
                if globals()["per"+str(x)] == globals()["per"+str(y)]:
                    if globals()["per"+str(x)].getStatus() == "Zombie" and globals()["per"+str(y)].getStatus() == "Susceptible":
                        globals()["per"+str(x)].bite(globals()["per"+str(y)])
                    if globals()["per"+str(x)].getStatus() == "Zombie" and globals()["per"+str(y)].getStatus() == "Immune":
                        globals()["per"+str(x)].bite(globals()["per"+str(y)])
                        
        for x in range(1,endVal):
            for y in range(1,endVal):
                if globals()["per"+str(x)] == globals()["per"+str(y)]:
                    if globals()["per"+str(x)].getStatus() == "Immune" and globals()["per"+str(y)].getStatus() == "Zombie":
                        globals()["per"+str(x)].heal(globals()["per"+str(y)])
                    if globals()["per"+str(x)].getStatus() == "Immune" and globals()["per"+str(y)].getStatus() == "Infected":
                        globals()["per"+str(x)].heal(globals()["per"+str(y)])
       
        susceptList.append(len(susceptID))
        zombieList.append(len(zombieID))
        removeList.append(len(removeID))
        infectList.append(len(infectID))
        recoverList.append(len(recoverID))
        immuneList.append(len(immuneID))
        
        config.time += 1
        if len(zombieID) == 0 and len(infectID) == 0:
            config.endScene = 1
            runSim = False
        if len(susceptID) == 0 and len(immuneID) == 0 and len(recoverID) == 0:
            config.endScene = 2
            runSim = False
        if config.time >= 1500:
            config.endScene = 3
            runSim = False
    
    for x in range(1, endVal):
        print(str(x) + ": "+ str(globals()["per"+str(x)]))
        
    input("\nPress enter to display graphs:")
    
    fileName = "simulation--{}-{}-{}--{}-{}-{}.pdf".format(now.year,now.month,now.day,now.hour,now.minute,now.second)
    pp = PdfPages(fileName)
        
    plt.plot(susceptList, label = "Susceptible")
    plt.plot(zombieList, label = "Zombie")
    plt.legend()
    plt.xlabel("Time (hours)")
    plt.ylabel("Number of People")
    pp.savefig()
    plt.show()
    
    plt.plot(immuneList, label = "Immune")
    plt.plot(removeList, label = "Removed")
    plt.legend()
    plt.xlabel("Time (hours)")
    plt.ylabel("Number of People")
    pp.savefig()
    plt.show()
    
    
    
    while True:
        try:
            summary = input("\nWould you like to view the simulation summary? (Y/N): ")
            if summary not in ['N','n','Y','y']:
                raise ValueError
        except ValueError:
            print("\nPlease enter 'Y' or 'N'\n")
        else:
            break
    
    if summary in ['N','n']:
        pp.close()
    elif summary in ['Y','y'] and config.endScene == 1:
        end = "\n\nThe simulation lasted for {} hours. It ended because the Zombie and Infected population both reached zero.\n\
There are {} people of class Immune and {} people of class Susceptible. {} {} Recovering. \n\n".format(config.time, len(immuneID), len(susceptID), len(recoverID), config.p1 if (len(recoverID) == 1) else config.p2)
        print(end)
    elif summary in ['Y','y'] and config.endScene == 2:
        end = "\n\nThe simulation lasted for {} hours. It ended because the Susceptible, Immune, and Recovering populations all reached zero.\n\
There are {} people of class Zombie and {} people of class Infected.\n\n".format(config.time, len(zombieID), len(infectID))
        print(end)
    elif summary in ['Y','y'] and config.endScene == 3:
        end = "\n\nThe simulation lasted for the maximum alloted time, {} hours.\n\
There are {} Susceptible's, {} Zombie's, {} Immune's, {} Recovered and {} Removed.".format(config.time, len(susceptID), len(zombieID), len(immuneID), len(recoverID), len(removeID))
        print(end)
    
    firstPage = plt.figure(figsize=(11.69,8.27))
    firstPage.clf()
    firstPage.text(0.5,0.5,end, transform=firstPage.transFigure, size=12, ha="center")
    pp.savefig()
    plt.close()
    pp.close()
    
    input("Press enter to end the simulation.")

main()
