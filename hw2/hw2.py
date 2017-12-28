# Hanna Salings
# Deep Learning HW 2
# Due 10/24/17

from random import * # used for creating random value later
import math

with open ("pizzacatdata.txt") as file:
  pizzaData = file.read().split() # read in data from pizzacatdata.txt and split it

# ----- Variables -----
eta = 0.050 # learning rate

exampleCount = int(len(pizzaData) / 5) # examples n (divided by 5 to get size of one column)

pepperoni = pizzaData[0::5] # pepperoni, takes in the first column of pizzaData
sausage = pizzaData[1::5] # sausage, takes in the second column of pizzaData
mushroom = pizzaData[2::5] # mushroom, takes in the third column of pizzaData
cheese = pizzaData[3::5] # cheese, takes in the fourth column of pizzaData
catAccept = pizzaData[4::5] # y value, takes in the fifth column of pizzaData

w = [0] * 5 # weights w0, w1, w2, w3, and w4
for i in range(5):
  w[i] = randint(-100, 100) # gets a random int between -100 and 100

yCap = 0
error = 0
error_Sum = 0 # Sum of squares error
sigmoid = 0

iterations = 5000

for i in range(iterations): # repeat 1500 times
  for k in range(exampleCount): # goes through all examples in a column
    yCap = w[0] + (w[1] * int(pepperoni[k])) + (w[2]*int(sausage[k])) + (w[3]*int(mushroom[k])) + (w[4]*int(cheese[k]))
    
    try:
      sigmoid = 1 / (1 + (math.e**-yCap))
    except OverflowError:
      sigmoid = 1

    error = (int(catAccept[k]) - yCap)

    # Update weights
    w[0] = w[0] + (eta * error)
    w[1] = w[1] + (eta * error * int(pepperoni[k]))
    w[2] = w[2] + (eta * error * int(sausage[k]))
    w[3] = w[3] + (eta * error * int(mushroom[k]))
    w[4] = w[4] + (eta * error * int(cheese[k]))
  # end of 'for k in range(exampleCount)' loop
# end of 'for i in range(iterations)' loop

# Get sum of errors using the final weights
for k in range(exampleCount):
  yCap = (w[0]) + (w[1] * int(pepperoni[k])) + (w[2]*int(sausage[k])) + (w[3]*int(mushroom[k])) + (w[4]*int(cheese[k]))
  sigmoid = 1 / (1 + (math.e**-yCap))
  error = (int(catAccept[k]) - yCap)
  error_Sum = error_Sum + (error**2)

print("CS-5001 : HW#2 : Logistic Regression.\nProgrammer: Hanna Salings")
print("No cats were hurt gathering this data.\n")
print("Using learning rate eta = ", eta)
print("After", iterations, "iterations:")
print("Sum of Squares Errors = ", error_Sum)
print("Weights:")
for i in range(5):
  print("w", i, " = ", w[i], sep='')
