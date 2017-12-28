# Hanna Salings
# Deep Learning HW 1
# Due 10/12/17

from random import * # used for creating random value later

with open ("zData.txt") as file:
  zData = file.read().split() # read in data from zData.txt and split it

# Variables
eta = 0.001
exampleCount = int(len(zData) / 2) # examples n (divided by 2 to get size of one column)
customers_X = zData[0::2] # x value, takes in the first column of zData
calories_Y = zData[1::2] # y value, takes in the second column of zData
w = [0] * 2 # weights w[0,1]
wErr = [0] * 2 # wErr[0,1] error per weight, initialized to 0
yCap = 0
LLE = 0 # Least Squares Error
LLE_Sum = 0 # Sum of squares error

w[0] = randint(0,20000) # gets a random int between 0 and 20000
w[1] = randint(0,20000)

for i in range(1500): # repeat 1500 times
  for k in range(exampleCount): #goes through all examples
    yCap = (w[0]) + (w[1] * int(customers_X[k])) # no x[0] because it is 1

    LLE = (int(calories_Y[k]) - yCap) ** 2
    LLE_Sum = LLE_Sum + LLE

    wErr[0] = wErr[0] + (int(calories_Y[k]) - yCap) # don't need x[0] since it is 1
    wErr[1] = wErr[1] + (int(calories_Y[k]) - yCap) * int(customers_X[k])
    # end of 'for k in range(0, exampleCount)'

  # Normalize each weights error
  wErr[0] = (1/exampleCount) * wErr[0]
  wErr[1] = (1/exampleCount) * wErr[1]

  # Update neuron's weights
  w[0] = w[0] + eta * wErr[0]
  w[1] = w[1] + eta * wErr[1]
  # end of 'for i in range(0,1500)'

print("CS-5001 : HW#1 : Regression with one variable.\nProgrammer: Hanna Salings\n")
print("Learning rate eta = ", eta)
print("After 1500 iterations:")
print("Sum of Squares Errors = ", LLE_Sum)
print("Weights:")
print("w0 = ", w[0])
print("w1 = ", w[1])