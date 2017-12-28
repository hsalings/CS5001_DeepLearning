# Hanna Salings
# CS5001 (Deep Learning) Final Project
# Due 12/13/17

# Using Q-Learning to teach Tinny Tim to find and eat donuts that randomly spawn in a corner, while avoiding running into walls or getting hit by tiles that randomly drop in certain locations

import random

# Variables
iterations = 10000000
actions = ['up','down','left','right'] # actions that Tinny Tim can perform
TDStepSize = 0.1 # set this value on own
discountRate = 0.8 # set this value on own
donutCount = 0
printCounter = 0

# Initialize map
basement = [['___' for i in range(10)] for j in range(10)]
policy = [['___' for i in range(10)] for j in range(10)]
Q = [[[0 for x in range(10)] for y in range(10)] for z in range(4)]

# Generate T, D, and wall locations (locations are given in the homework prompt)
for i in range(10):
  for j in range(10):

    # Tile spots
    if (i,j) == (1,3) or (i,j) == (2,7) or (i,j) == (3,4) or (i,j) == (5,2) or (i,j) == (6,5) or (i,j) == (6,7) or (i,j) == (7,2):
      basement[i][j] = ' T '
      policy[i][j] = ' T '

    # Walls
    elif (i == 0) or (i == 9) or (j ==0) or (j == 9) or (i,j) == (2,2) or (i,j) == (2,4) or (i,j) == (2,5) or (i,j) == (2,6) or (i,j) == (3,2) \
    or (i,j) == (4,2) or (i,j) == (4,6) or (i,j) == (5,6) or (i,j) == (6,4) or (i,j) == (6,6) or (i,j) == (7,4) or (i,j) == (8,4):
      basement[i][j] = '|||'
      policy[i][j] = '|||'

# end of for loops

# Randomize the start location
start = [random.randint(1,8), random.randint(1,8)] # didn't include 0 or 9 since those will always be walls

# while loop to check for possible starting locations landing on a wall
while True:
  if basement[start[0]][start[1]] == '|||':
    start = [random.randint(1,8), random.randint(1,8)] # re-randomize the start location if it lands on a wall
  elif basement[start[0]][start[1]] != '|||':
    timLocation = start # initialize Tinny Tim's location to the start location
    prevSpot = basement[timLocation[0]][timLocation[1]]
    policy[start[0]][start[1]] = 'TIM' # add a spot on the matrix to see where Tinny Tim is at
    break # exit while loop if it isn't on a wall

print("\nTinny Tim's Starting Location [row][column]: \n", start) # checking randomized location
print("\nNumber of iterations:", iterations)

donutCheck = False

for iteration in range(iterations):
  
  # For testing large iterations
  '''
  if printCounter == 20000000:
    print("\nCurrent Iteration: ", iteration)
    printCounter = 0
  printCounter = printCounter + 1
  '''
  # donut has a 25% chance to spawn in a corner and there can only be one donut in the basement at a time
  if donutCheck == False:
    donutChance = random.randint(1,4)
    if donutChance == 1:
      donutCheck = True;
      donutChance = random.randint(1,4)
      if donutChance == 1:
        basement[1][1] = ' D '
        #print("***** Donut spawned at [1][1] *****\n")
      elif donutChance == 2:
        basement[1][8] = ' D '
        #print("***** Donut spawned at [1][8] *****\n")
      elif donutChance == 3:
        basement[8][1] = ' D '
        #print("***** Donut spawned at [8][1] *****\n")
      elif donutChance == 4:
        basement[8][8] = ' D '
        #print("***** Donut spawned at [8][8] *****\n")

  # Default check to the 'up' action
  projectedAction = 0
  projectedReward = Q[projectedAction][timLocation[0]][timLocation[1]]

  for i in range(1,4): # run through the other three actions
    if projectedReward < Q[i][timLocation[0]][timLocation[1]]:
      projectedAction = i
      projectedReward = Q[i][timLocation[0]][timLocation[1]]

  #print("Projected action: ", projectedAction)

  # 82% chance to move in the correct direction, 6% chance for each other direction
  moveRandom = random.randint(1,100)
  if moveRandom <= 82:
    projectedAction = projectedAction
  elif moveRandom > 82 and moveRandom <= 88:
    projectedAction = (projectedAction + 1) % 4 
  elif moveRandom > 88 and moveRandom <= 94:
    projectedAction = (projectedAction + 2) % 4
  elif moveRandom > 94 and moveRandom <= 100:
    projectedAction = (projectedAction + 3) % 4

  #print("Action taken: ", projectedAction)

  # adjust location on the map depending on action
  if actions[projectedAction] == 'up':
    newLocationX = timLocation[0]
    newLocationY = timLocation[1] - 1
    policy[timLocation[0]][timLocation[1]] = ' ^ '

  elif actions[projectedAction] == 'down':
    newLocationX = timLocation[0]
    newLocationY = timLocation[1] + 1
    policy[timLocation[0]][timLocation[1]] = ' v '

  elif actions[projectedAction] == 'left':
    newLocationX = timLocation[0] - 1
    newLocationY = timLocation[1]
    policy[timLocation[0]][timLocation[1]] = ' < '

  elif actions[projectedAction] == 'right':
    newLocationX = timLocation[0] + 1
    newLocationY = timLocation[1]
    policy[timLocation[0]][timLocation[1]] = ' > '

  # Default check the max reward at the 'up' action
  maxReward = Q[0][newLocationX][newLocationY]
  # Check the other 3 directions
  for i in range(1,4):
    if maxReward < Q[i][newLocationX][newLocationY]:
      maxReward = Q[i][newLocationX][newLocationY]
  
  # Figure out immediate rewards based on the location Tim moves to
  # Wall Hit
  if basement[newLocationX][newLocationY] == '|||':
    #print("Tim hit a wall at [", newLocationX, "][",newLocationY, "], moved back to [", timLocation[0], "][", timLocation[1], "]", sep='')
    immediateReward = -1
    # Need to check for tile drop as well since Tim can both hit a wall and then be hit by a tile in some spots
    if basement[timLocation[0]][timLocation[1]] == ' T ':
      tileDrop = random.randint(1,2)
      if tileDrop == 1:
        #print("A tile hit Tim at [", timLocation[0], "][",timLocation[1], "]", sep='')
        immediateReward = immediateReward -10
  # Tile Check    
  elif basement[newLocationX][newLocationY] == ' T ':
    tileDrop = random.randint(1,2)
    if tileDrop == 1:
      #print("A tile hit Tim at [", newLocationX, "][",newLocationY, "]", sep='')
      immediateReward = -10
    elif tileDrop == 2:
      #print("No tile dropped on Tim at [", newLocationX, "][",newLocationY, "]", sep='')
      immediateReward = 0
  # Donut Get
  elif basement[newLocationX][newLocationY] == ' D ':
    #print("\n********** Tim ate a donut at [", newLocationX, "][",newLocationY, "] **********\n", sep='')
    immediateReward = 10
    donutCheck = False
    donutCount = donutCount + 1
    basement[newLocationX][newLocationY] = '___'
  else:
    immediateReward = 0
    #print("Tim moved to [", newLocationX, "][",newLocationY, "]", sep='')

  #print("Tim moved to [", newLocationX, "][",newLocationY, "]", sep='')
  #print("Immediate Reward: ", immediateReward)

  Q[projectedAction][timLocation[0]][timLocation[1]] = Q[projectedAction][timLocation[0]][timLocation[1]] + TDStepSize * (immediateReward + discountRate * maxReward - Q[projectedAction][timLocation[0]][timLocation[1]]) 

  if (basement[newLocationX][newLocationY] != '|||'):
    timLocation[0] = newLocationX
    timLocation[1] = newLocationY

# Print out the number of donuts Tinny Tim ate
print("\n\nFinal Donut Count: ", donutCount)

# Print out the basement map
print("\n--- Basement Map ---\n")
for i in basement:
  print('  '.join(map(str,i))) # nice looking outputs are the best
  print('\n') # makes it even easier to see the matrix

# Print out the policy map
print("\n--- Policy Map ---\n")
for i in policy:
  print('  '.join(map(str,i))) # nice looking outputs are the best
  print('\n') # makes it even easier to see the matrix

'''
Commented out because this prints four Q tables instead of the most recent QTable
for i in Q:
  print("\n".join(map(str,i)))
  print(' ')
'''

counter = 0

print("\n--- Expected Reward Table ---\n")

for i in range(10):
  counter = 0 # reset the counter
  for j in range(10):
    counter = counter + 1
    # output wall spots for distinction between possible 0 value spots and wall spots
    if (i == 0) or (i == 9) or (j ==0) or (j == 9) or (i,j) == (2,2) or (i,j) == (2,4) or (i,j) == (2,5) or (i,j) == (2,6) or (i,j) == (3,2) \
    or (i,j) == (4,2) or (i,j) == (4,6) or (i,j) == (5,6) or (i,j) == (6,4) or (i,j) == (6,6) or (i,j) == (7,4) or (i,j) == (8,4):
      Q[3][i][j] = '--- WALL ---'
    print('{:^24}'.format(Q[3][i][j]), end="") # had to do Q[3] because it was outputting four tables instead of just one
    # was outputting everything in a single line so this makes it so that it outputs correctly as a 10x10
    if counter == 10: 
      print(' ')
