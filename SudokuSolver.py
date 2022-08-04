from tkinter import *
import os #just to clear the console...

#usefull constants
boxes = {0:[0, 1, 2], 1:[0, 1, 2], 2:[0, 1, 2], 3:[3, 4, 5], 4:[3, 4, 5], 5:[3, 4, 5], 6:[6, 7, 8], 7:[6, 7, 8], 8:[6, 7, 8]}
#usefull methods
def clone(arr):
   #create a copy of a 2-dimension array
   narr = []
   for i in range(len(arr)):
      narr.append([])
      for j in range(len(arr[i])):
         narr[i].append(arr[i][j])
   return narr


#window setup
main = Tk();
main.title("Sudoku solver V0.1")
main.geometry("450x550")
main.resizable(width=False, height=False)
canvas = Canvas(main, width=450, height=450)
canvas.place(x=0, y=0)

#draw sidoku lines
canvas.create_line(0, 152, 450, 152, width = 2, fill = "grey")
canvas.create_line(0, 305, 450, 305, width = 2, fill = "grey")
canvas.create_line(152, 0, 152, 450, width = 2, fill = "grey")
canvas.create_line(305, 0, 305, 450, width = 2, fill = "grey")

#set up sudoku inputs
sudokuGrid = []
textHolders = []

for i in range(9):
   sudokuGrid.append([])
   textHolders.append([])
   for j in range(9):
      textHolders[i].append(Entry(main, font="Arial 30"))
      textHolders[i][j].place(x=51*i, y=51*j, width=48, height=48)
      sudokuGrid[i].append(0)

#solve and clear functions
def solveSdk():
   global iterations
   #solve the sudoku
   #get all the Inputs :
   validGrid = True
   for i in range(9):
      for j in range(9):
         text = textHolders[i][j].get()
         if(text == "" or text == " "):
            sudokuGrid[i][j] = 0
         else:
            try:
               sudokuGrid[i][j] = int(text)
            except:
               validGrid = False
               print("Please enter numbers in the grid !")
   if validGrid:
      iterations = 0
      sudoku = solveSudoku(sudokuGrid)
      if sudoku != False:
         displaySudoku(sudoku)
         print("Done !")
      else:
         print("Unable to complete sudoku")


def clearSdk():
   os.system("cls")
   for i in range(9):
      for j in range(9):
         textHolders[i][j].delete(0, "end")



#SOLVING SUDOKU
def solveSudoku(sudoku):
   global iterations
   iterations += 1
   print("Iteration {} of solving function".format(iterations))
   #start by trying to fill all simple numbers : 
   doingChanges = True
   while doingChanges:
      probabilities = createProbabilities(sudoku)
      if probabilities == False:
         return False
      doingChanges = False
      for i in range(9): #loop trought all the sudoku
         for j in range(9):
            if len(probabilities[i][j]) == 1:
               spotCanBeFilled = True #check if there is anther spot being filled with same number here
               for k in range(9):
                  if k != j and len(probabilities[i][k]) == 1 and probabilities[i][k][0] == probabilities[i][j][0]:
                     spotCanBeFilled = False
               for k in range(9):
                  if k != i and len(probabilities[k][j]) == 1 and probabilities[k][j][0] == probabilities[i][j][0]:
                     spotCanBeFilled = False
               for k in boxes[i]:
                  for l in boxes[j]:
                     if (k != i or l != j) and len(probabilities[k][l]) == 1 and probabilities[k][l][0] == probabilities[i][j][0]:
                        spotCanBeFilled = False
               if spotCanBeFilled:
                  doingChanges = True
                  print("adding a {} at position {};{}".format(probabilities[i][j][0], i, j)) #only one possibility for that spot
                  sudoku[i][j] = probabilities[i][j][0];
   if checkIfFinished(sudoku):
      print("Sudoku Solved")
      return sudoku
   #extrapolate and assumptions
   maximum = 10 #look for spot with less possibilities
   for i in range(9):
      for j in range(9):
         if len(probabilities[i][j]) != 0 and len(probabilities[i][j]) < maximum:
            extrapolateFrom = [i, j]
            maximum = len(probabilities[i][j])
   print("No obvious spot. Extrapolating from {} possibilities".format(maximum))
   tries = []
   for i in range(maximum):
      tries.append(clone(sudoku))
      tries[i][extrapolateFrom[0]][extrapolateFrom[1]] = probabilities[extrapolateFrom[0]][extrapolateFrom[1]][i]
   for i in range(maximum): 
      print("extrapolating : {}/{}".format(i + 1, maximum))  
      displaySudoku(tries[i])
      tries[i] = solveSudoku(tries[i])
      if tries[i] != False:
         print("Succeeded extrapolation. Now solving extrapolated sudoku")
         return tries[i]
   print("None of the {} tries worked. Warping back".format(maximum))
   return False
         

            
            
def checkIfFinished(sudoku):
   probabilities = createProbabilities(sudoku)
   somme = 0
   for i in range(9):
      for j in range(9):
         somme += len(probabilities[i][j])
   if somme == 0:
      return True
   else:
      return False
         
def createProbabilities(sudoku):
   probabilities = [] #the list of numbers that can go in the desire spot
   for i in range(0, 9):
      probabilities.append([])
      for j in range(0, 9):
         probabilities[i].append([])
   for i in range(0, 9): #loop trought all the sudoku
      for j in range(0, 9):
         if sudoku[i][j] == 0: #if this is a empty spot
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9] #list of possible numbers
            for k in range(9):
               try:
                  numbers.remove(sudoku[i][k]) #remove numbers already in the same row
               except:
                  pass
            #remove numbers already in the same column
            for k in range(9):
               try:
                  numbers.remove(sudoku[k][j]) #remove numbers already in the same column
               except:
                  pass
            for k in boxes[i]:
               for l in boxes[j]:
                  try:
                     numbers.remove(sudoku[k][l]) #remove numbers already in the same square
                  except:
                     pass
            if len(numbers) == 0:
               print("Unable to solve sudoku because of emplacement {};{}.".format(i, j)) # there are no possible numbers for that case
               return False
            probabilities[i][j] = numbers
         else:
            probabilities[i][j] = []
   return probabilities


def displaySudoku(sudoku):
   for i in range(9):
      for j in range(9):
         textHolders[i][j].delete(0, "end")
         if sudoku[i][j] != 0:
            textHolders[i][j].insert(0, str(sudoku[i][j]))

#set up solve and clear inputs
solveButton = Button(main, text="Solve", command=solveSdk)
solveButton.place(x=50, y=475, width=150, height=50)
clearButton = Button(main, text="Clear", command=clearSdk)
clearButton.place(x=250, y=475, width=150, height=50)

main.mainloop();




