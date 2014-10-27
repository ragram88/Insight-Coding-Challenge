"""Raghav Ramachandran 10/21/2014 Main program to solve Sudoku-Insight Data Engineering Code Challenge"""

import sudoku
import csv
import numpy as np
from math import *

def readfile():
    inputfname=input("Please enter the full name of the csv file containing the unsolved Sudoku puzzle: ")
        
    try:
        inputfile=open(inputfname,'r')
    except IOError:
        print("Cannot open file",inputfname)
        quit()
    return inputfile

def main():

    inputfile=readfile() # input file storing unsolved Sudoku puzzle   
    sudoku_grid=[] #2D list storing unsolved Sudoku puzzle (sudoku grid)
    for line in inputfile:
        row=line.rstrip('\n').split(',')
        sudoku_grid.append(row)
    sudoku_grid=np.array(sudoku_grid,int) #convert Sudoku grid from 2D list to 2D array for easier data retrieval
    print("Original Sudoku matrix: ",'\n',sudoku_grid)

    gridsize=sudoku_grid.shape[0] #the sudoku (square) grid length must be a perfect square
    if not(sudoku_grid.shape[0]==sudoku_grid.shape[1]):
        print("Invalid grid dimensions. Grid must be square in shape.")
        quit()
    if not(round(sqrt(gridsize))==sqrt(gridsize)):
        print("Invalid grid length. Length of grid must be a perfect square.")
        quit()

    rowfill=np.zeros((gridsize,gridsize),int)
    columnfill=np.zeros((gridsize,gridsize),int)
    squarefill=np.zeros((gridsize,gridsize),int)
    square_num=np.zeros((gridsize,gridsize),int)

    board_status=sudoku.sudoku_status(sudoku_grid,gridsize,rowfill,columnfill,squarefill,square_num)
    board_solution=sudoku.single_possibility(sudoku_grid,gridsize,rowfill,columnfill,squarefill,square_num)
    if (0 in board_solution):
        board_solution=sudoku.two_out_of_three_rule(board_solution,gridsize,rowfill,columnfill,squarefill) #call two out of three rule to find the only places for a particular number
        board_solution=sudoku.single_possibility(board_solution,gridsize,rowfill,columnfill,squarefill,square_num)
        print("Sudoku puzzle has not been fully solved. The partially solved puzzle is shown below.") 
    print("Sudoku solution matrix: ",'\n',board_solution)

    outputfname=input("Please enter the desired full name of the csv file containing the solved Sudoku puzzle: ")
    outputfile=csv.writer(open(outputfname,'w',newline=''),delimiter=",") #output file storing solved Sudoku puzzle
    for count in range(gridsize):
        outputfile.writerow(board_solution[count])
    inputfile.close()
    
if __name__=="__main__":
    main()
