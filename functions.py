# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 00:15:09 2018

@author: Stephon
"""

from time import sleep
from sys import stdout
from math import sqrt,ceil
from random import randint
import config


###############################################################################
def userPrompt():
    while True:
        try:
            initPop = int(input("What would you like for your total population to be (25 - 500): "))
            if initPop < 25 or initPop > 500:
                raise ValueError
        except ValueError:
            print("\nYou must enter an integer between 25 and 500. Please try again.")
            continue
        else:
            return initPop
   
###############################################################################
def zombiePrompt():
    while True:
        try:
            zomPop = int(input("What would you like for your intial zombie population to be (3 - 60): "))
            if zomPop < 3 or zomPop > 60:
                raise ValueError
        except ValueError:
            print("\nYou must enter an integer between 3 and 60. Please try again.")
            continue
        else:
            return zomPop

###############################################################################
def islandPrompt():
    
    while True:
        try:
            initSize = int(input("\nEnter 1 if you like to input your own island size.\n\
Enter 2 if you would like the simulation to automatically determine it.\n\
Which option do you select? "))
            if initSize < 1 or initSize > 2:
                raise ValueError
        except ValueError:
            print("\nYou must enter either 1 or 2. Please try again.")
        else:
            return initSize

###############################################################################
def genIsland():
    """
    This function asks the user how large they would like the island to be.
    """
    while True:
        try:
            config.islandSize = int(input("The island you create will be in the shape of a square.\n\
You will be asked to enter the side length of your island. This number\n\
will be squared to determine the total area of the island.\n\n\
Please enter a side length (5 - 40): "))
            if config.islandSize < 5 or config.islandSize > 40:
                raise ValueError
        except ValueError:
        
            print("You must enter an integer between 5 and 40. Please try again.")
            continue
        else:
            config.islandSize *= config.islandSize
            print("\nYour island is " + str(config.islandSize) + " square miles.")
            break
            
###############################################################################
def delay_print(s):
    for c in s:
        stdout.write(c)
        stdout.flush()
        sleep(0.02)

###############################################################################       
def nearest_square(num):
    return (ceil(sqrt(num))-1)**2

###############################################################################
def initialize():
    print("Zombie Island Simulation v0.5\n\n\n")
    '''delay_'''
    print("\
This simulation implements a customized SIR model to predict the spread\n\
of a zombie virus on a deserted island. In a few moments you will be asked\n\
to input an initial population. A population of people of class Susceptible\n\
will be created equal to the value that you give. Please be patient as the\n\
simulation may take some time.\n\n\n")
    loop = True
    while loop:
        try:
            config.initPop = userPrompt()
            config.zombiePop = zombiePrompt()
            if config.zombiePop > config.initPop:
                raise ValueError
        except ValueError:
            print("Your zombie population is larger than your total population. Please try again.")
        else:
            loop = False
        
    config.susceptPop = config.initPop - config.zombiePop
    config.removePop = 0
    config.infectPop = 0
    config.immunePop = 0
    
    islandChoice = islandPrompt()
    
    
    if islandChoice == 2:
        config.islandSize = nearest_square(config.initPop*5)
        print("\nYour island is " + str(config.islandSize) + " square miles.")
    elif islandChoice == 1:
        genIsland()
    
        
    config.boundary = int(sqrt(config.islandSize))

###############################################################################       
def genID():
    """
    Generates an identification number for a person that includes the
    gender, age and a random five-digit integer.
    """
    gender = randint(1,2)                                                      # 1 == Male, 2 == Female
    age = randint(15,60)                                                       # Generates age between 15 and 60 years old
    randomNum = randint(10000, 99999)                                          # Generates a random 5 digit interger
    person_id = int(str(gender)+str(age)+str(randomNum))                       # Combines the gender, age, and randomNum
    return person_id

###############################################################################
def genXY():
    """
    Generates a random location on the map to assign to a person
    """
    coordinate = [randint(1,config.boundary), randint(1,config.boundary)]
    return coordinate

###############################################################################
def checkID():
    """
    Checks the current generated ID against a list of
    IDs to ensure that the same identifier is not assigned to two
    different people.
    """
    errorCheck = 0                                                             # Counts the number of errors                             
    while errorCheck < 10:                                                     # Stops after 10 errors
        id = genID()
        if id not in config.usedIDs:
            config.usedIDs.append(id)
            return id
        else:
            errorCheck += 1
    else:
        print("Err: unable to assign ID.")        

###############################################################################    
def validID(num):
    """
    Checks a user entered ID against a list of IDs to ensure that
    the same identifier is not assigned to two different people.
    """
    valid = True
    while valid:
        if num not in config.usedIDs:
            return True
        else:
            return False