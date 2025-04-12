import numpy as np
import copy
from dataclasses import dataclass

def sudoku_solver(sudoku):
    
    starting_sudoku = partialSudoku()
    solved_sudoku = get_final_state(starting_sudoku,sudoku)
    

    return solved_sudoku

@dataclass
class Cell:

    r:int
    c:int                                                              #objects stored in grid
    value: int  
    possible_values: set

    def __hash__(self):
        return hash((self.r,self.c,self.value))                        #<-is unique by these values
    
class partialSudoku:

    def __init__(self):
        
        self.square_corners = [[0,0],[3,0],[6,0],                      #defines all corners of the grid for checking    
                               [0,3],[3,3],[6,3],
                               [0,6],[3,6],[6,6]]                       
        self.sudoku = np.array([[Cell(r,c,0,[x for x in range(1,10)]) for c in range(9)]
                                                                         for r in range(9)])   
                                                                       #create empty board of cells

    def is_goal(self):
        for n in range(9):
            if 0 in [cell.value for cell in self.get_row(n)]:          #check all cells are filled
                return False
        return True
    
    def is_invalid(self):
                                                                       #check all rows and columns that they are 
                                                                       # unique in filled values
        for n in range(9):
            if not self.is_unique(self.get_row(n)) or not self.is_unique(self.get_column(n)):
                return True 
        for corner in self.square_corners:
            if not self.is_unique(self.get_square(corner)):            #check all values in all squares are unique
                return True  
        return False
    
    
    def is_unique(self, list):
        values = [cell.value for cell in list if cell.value != 0]
        return len(values) == len(set(values))                         #using sets to remove duplicates
    
   
    def get_column(self, column):
        return self.sudoku[:, column]                                  #slicing for rows and colmuns

    def get_row(self, row):
        return self.sudoku[row, :]
    
    def get_square(self,coords):                                        
        top_left_r = (coords[0] // 3) * 3                               #find corner of square for cell given   
        top_left_c = (coords[1] // 3) * 3

        return self.sudoku[top_left_r:top_left_r + 3, top_left_c:top_left_c + 3].flatten()
                                                                        #create as singular list

    def set_value(self,r,c,value):
        
        current_cell = self.sudoku[r][c]

        if value not in current_cell.possible_values:                  
            return False
        
        current_cell.value = value

                                                                        #union to not update a cell multiple times
        for cell in list(set(self.get_column(c)).union(self.get_row(r),self.get_square((r,c)))):
            if value in cell.possible_values:
                cell.possible_values.remove(value)                                         
                if not cell.possible_values and cell.value == 0: 
                    return False                                        #if a cell has no value and no potential value
        return True
   
    
    def pencilmark(self, initial):     
        for r in range(9):
            for c in range(9):
                value = initial[r][c]
                if value != 0:
                    if not self.set_value(r,c,value):       # setting all starting values 
                        return False                        
        return True                  

    def pick_next_cell(self):
        min = 10
        next_cell = None
        for r in range(9):                                  #find smallest possibel value list in grid
            for c in range(9):
                cell  = self.sudoku[r][c] 
                weight = len(cell.possible_values)
                if cell.value == 0 and weight < min:
                    if weight == 1:                         #save iteration by returning a cell with a single possible value
                        return cell
                    next_cell = cell
                    min = weight
        return next_cell
                    

def depth_first_search(partial_sudoku):

    cell = partial_sudoku.pick_next_cell()                                                                                     

    for value in cell.possible_values:
        new_sudoku = copy.deepcopy(partial_sudoku)                          #create branched state
        if new_sudoku.set_value(cell.r,cell.c,value):     
            if new_sudoku.is_goal():                                        #set and check grid state
                return new_sudoku    
            if not partial_sudoku.is_invalid():                         
                deep_state = depth_first_search(new_sudoku)                 #branch further as needed
                if deep_state is not None and deep_state.is_goal():                      
                    return deep_state                                       #return if branch is goal
    return None 


def get_final_state(starting_sudoku,initial):

    if starting_sudoku.pencilmark(initial):                    #handles invalid intial sudokus 
        solved_sudoku = depth_first_search(starting_sudoku)
        if solved_sudoku is not None:                          
            return np.array([[cell.value for cell in row] for row in solved_sudoku.sudoku])
                                                               #return sudoku as original numPy array not the cell object version
    
    return np.array([[-1 for _ in range(9)] for _ in range(9)])


