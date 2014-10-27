"""Raghav Ramachandran 10/23/2014 Module for sudoku puzzle solving program-Insight Data Engineering Coding Challenge"""

import numpy as np
from math import *

def subsquare(xcoord,ycoord,gridsize): #calculate the subsquare (block) corresponding to each Sudoku cell
    subsquare_size=int(sqrt(gridsize))
    subsquare_number=((subsquare_size)*(floor(xcoord/subsquare_size)))+floor(ycoord/subsquare_size) 
    return subsquare_number

def sudoku_status(sudoku_grid,gridsize,rowfill,columnfill,squarefill,square_num): #figure out numbers to be filled for each row, column and subsquare (block)
    
    for i in range(gridsize):
        for j in range(gridsize):
            square_num[i][j]=subsquare(i,j,gridsize) #find subsquare (block) number corresponding to each cell
            if not(sudoku_grid[i][j]==0):
                number=sudoku_grid[i][j] #if a cell in the Sudoku puzzle has been filled 
                rowfill[i][(number-1)]=1 # mark that number as filled(1) for the corresponding row
                columnfill[j][(number-1)]=1 #and column   
                squarefill[square_num[i][j]][(number-1)]=1 # and subsquare (block)

def two_out_of_three_rule(sudoku_grid,gridsize,rowfill,columnfill,squarefill): #find cells which are the only places where a given number can fit
    subsquare_size=int(sqrt(gridsize)) #no. of rows/columns in a subsquare (block)
    for group_number in range(subsquare_size): #search for groups of rows corresponding to whole blocks
        lower=(group_number*subsquare_size) # for a 9-by-9 grid, the groups would be rows (1,2,3), (4,5,6), (7,8,9)
        upper=lower+subsquare_size #calculate the lower and upper row numbers for each group
        for num in range(gridsize): #loop through each possible number (indices start from 0)
            filled_rows=0
            cell_condition=False
            possibilities=0
            for group in range(lower,upper): #loop through each row in a group
                filled_rows=filled_rows+int((num+1) in sudoku_grid[group]) #count no. of rows in a group that have a particular number (add 1 since indices start from 0) 
                
            if (filled_rows==((subsquare_size)-1)): #if a number is missing in only one row of a group, identify the location for the number
                unfilled_row=int(lower + np.where(rowfill.transpose()[num][lower:upper]==0)[0]) #find the row missing the particular number
                square_of_interest=int(np.where(squarefill.transpose()[num][lower:upper]==0)[0]) #find the available block for the missing number
                first_column=((square_of_interest)%subsquare_size)*subsquare_size # calculate the lower and upper column numbers for the missing number
                last_column=first_column+subsquare_size
                for avail_column in range(first_column,last_column): #evaluate the possible columns for the missing number
                    cell_condition=(sudoku_grid[unfilled_row][avail_column]==0) and (columnfill[avail_column][num]==0)
                    if cell_condition==True:  #the cells in the available row and block should be empty and the number should not be present anywhere else in the columns
                        location=avail_column
                        possibilities=possibilities+1
                if possibilities==1: #only one cell for a particular number
                    sudoku_grid[unfilled_row][location]=(num+1) #update grid, row, column and block matrices every time a cell has been solved
                    rowfill[unfilled_row][num]=1
                    columnfill[location][num]=1
                    squarefill[square_of_interest][num]=1
    
    return sudoku_grid
                
def single_possibility(sudoku_grid,gridsize,rowfill,columnfill,squarefill,square_num): #identify (iteratively) unique values for individual cells
    number_choices=np.zeros(gridsize,int)

    flag=0
    iteration=1
    while ((iteration==1) or (flag==1)): #exit loop when all cells have been filled
        flag=0 #flag determining status of puzzle (solved or unsolved)
        for i in range(gridsize):
            for j in range(gridsize):
                if (sudoku_grid[i][j]==0):
                    number_choices=rowfill[i]+columnfill[j]+squarefill[square_num[i][j]] #search for unfilled (0) numbers corresponding to a cell (row,column and block)
                    choices=np.nonzero(number_choices == 0)
                    if choices[0].shape[0]==1: #only one option for unfilled cell
                        sudoku_grid[i][j]=choices[0][0]+1 #update grid, row, column and block matrices every time a cell has been solved
                        rowfill[i][choices[0][0]]=1
                        columnfill[j][choices[0][0]]=1
                        squarefill[square_num[i][j]][choices[0][0]]=1
                    else:
                        flag=1 #set flag to 1 if puzzle has not been solved
                        
        iteration=iteration+1 #start another iteration through sudoku puzzle
        i=0
        j=0 #reset for loop counters
        if iteration>=10000: #upper limit of 10000 iterations
            break
    
    print("Iterations for single possibility rule (only one option for a cell):",iteration)
    
    return sudoku_grid
