import time 
import sys
import pandas as pd
import numpy as np
import Utils
from Utils import *


dfList = []
dfTables = []
graphs = []
dfInfos = []
notifications = []

def Process(unit):
    if(unit is not None):
        unit = int(unit)
    if unit == 1:     
        String()
    elif unit == 2:
        Numpy()
    return

def String():
    global dfInfos, dfList, graphs, notifications
    dataframer = DataFramer()
    htmlHelper = HTMLHelper()

    original = "Welcome to String Operations"
    notifications.append("Original String " + original)
    welcome = original[:7]
    notifications.append("original[:7] : " + welcome)
    strin = original[11:][0:6]
    notifications.append("original[11:][0:6] : " + strin)
    wel2 = original[::2]
    notifications.append("original[::2] : " + wel2)
    
    numbers = "0123456789"
    notifications.append("Numbers  " + numbers)
    evens = numbers[::2]
    notifications.append("evens numbers[::2] : " + evens)
    odds = numbers[1::2]
    notifications.append("odds numbers[1::2] : " + odds)

    likes = "Sammy likes to swim in the ocean, likes to spin up servers, and likes to smile."
    notifications.append("likes is " + likes)
    notifications.append("likes.count('likes') is " + str(likes.count("likes")))
    notifications.append("likes.find('likes') is " + str(likes.find("likes")))
    notifications.append("likes.upper() is " + likes.upper())
    notifications.append("likes.lower() is " + likes.lower())
    return

def Numpy():
    helper = Helper()
    # Create a python list
    a = ["0", 1, "two", "3", 4]

    # Print each element
    print("a[0]:", a[0])
    print("a[1]:", a[1])
    print("a[2]:", a[2])
    print("a[3]:", a[3])
    print("a[4]:", a[4])

    helper.PrintNumpy(np.array(a))

    # Create numpy array
    c = np.array([20, 1, 2, 3, 4])
    # Assign the first element to 100
    c[0] = 100
    # Assign the 5th element to 0
    c[4] = 0
    helper.PrintNumpy(c)

    # Slicing the numpy array
    d = c[1:4]
    # Set the fourth element and fifth element to 300 and 400
    c[3:5] = 300, 400
    helper.PrintNumpy(d)
    # Create the index list
    select = [0, 2, 3]
    # Use List to select elements
    d = c[select]
    # Assign the specified elements to new value
    c[select] = 100000
    helper.PrintNumpy(d)

    # Create a numpy array
    a2 = np.array([0, 1, 2, 3, 4])
    helper.PrintNumpy(a2, describe = True)
 
    # Create a numpy array
    a2 = np.array([1, -1, 1, -1, 2, 3, 4, 5])
    helper.PrintNumpy(a2, True, True)    

    u = np.array([1, 0])
    v = np.array([0, 1])
    # Numpy Array Addition
    z = u + v
    helper.PrintNumpy(z, True, True)    
    
    # Plot numpy arrays
    #Plotvec1(u, z, v)

    # Create a numpy array
    y = np.array([1, 2])
    # Numpy Array Multiplication
    z2 = 2 * y
    helper.PrintNumpy(z2, True, True)    
    
    # Create a numpy array
    u2 = np.array([1, 2])
    v2 = np.array([3, 2])
    # Calculate the production of two numpy arrays
    z3 = u2 * v2
    helper.PrintNumpy(z3, True, True)    

    # Calculate the dot product
    npdot = np.dot(u2, v2)
    print("dot product is " + str(npdot))
    
    # Create a constant to numpy array
    u4 = np.array([1, 2, 3, -1])
    # Add the constant to array
    u5 = u4 + 1
    helper.PrintNumpy(u5, True, True)    

    # Create the numpy array in radians
    x2 = np.array([0, np.pi/2 , np.pi])
    helper.PrintNumpy(x2, True, True)    
    # Calculate the sin of each elements
    y2 = np.sin(x2)
    helper.PrintNumpy(y2, True, True)    

    print("Makeup a numpy array within [-2, 2] and 5 elements")
    nlin = np.linspace(-2, 2, num=5)
    helper.PrintNumpy(nlin, True, True)    

    print("Makeup a numpy array within [-2, 2] and 9 elements")
    nlin2 = np.linspace(-2, 2, num=9)
    helper.PrintNumpy(nlin2, True, True)
    
    print("Makeup a numpy array within [0, 2π] and 100 elements") 
    nlin3 = np.linspace(0, 2*np.pi, num=100)
    helper.PrintNumpy(nlin3, True, True)
    
    # Plot the result
    #plt.plot(x, y)

    return

def Plotvec1(u, z, v):
    ax = plt.axes()
    ax.arrow(0, 0, *u, head_width=0.05, color='r', head_length=0.1)
    plt.text(*(u + 0.1), 'u')
    
    ax.arrow(0, 0, *v, head_width=0.05, color='b', head_length=0.1)
    plt.text(*(v + 0.1), 'v')
    ax.arrow(0, 0, *z, head_width=0.05, head_length=0.1)
    plt.text(*(z + 0.1), 'z')
    plt.ylim(-2, 2)
    plt.xlim(-2, 2)

def Plotvec2(a,b):
    ax = plt.axes()
    ax.arrow(0, 0, *a, head_width=0.05, color ='r', head_length=0.1)
    plt.text(*(a + 0.1), 'a')
    ax.arrow(0, 0, *b, head_width=0.05, color ='b', head_length=0.1)
    plt.text(*(b + 0.1), 'b')
    plt.ylim(-2, 2)
    plt.xlim(-2, 2)