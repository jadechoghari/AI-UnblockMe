from board import *
import copy

num_expand = 0

def successors_par_id_desc(successors):
    successors.sort(key=lambda x: x.parent.id, reverse=True)
    return successors       

def successors_id_desc(successors):
    successors.sort(key=lambda x: x.id, reverse=True)
    return successors

def successors_f_desc(successors):
    successors.sort(key=lambda x: (x.f + x.depth), reverse=True)
    return successors 

def a_star(init_board, hfn):
    """
    Run the A_star search algorithm given an initial board and a heuristic function.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial starting board.
    :type init_board: Board
    :param hfn: The heuristic function.
    :type hfn: Heuristic (a function that consumes a Board and produces a numeric heuristic value)
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """
    #TODO

def dfs(init_board):
    """
    Run the DFS algorithm given an initial board.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial board.
    :type init_board: Board
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """
    #TODO


def get_successors(state):
    """
    Return a list containing the successor states of the given state.
    The states in the list may be in any arbitrary order.

    :param state: The current state.
    :type state: State
    :return: The list of successor states.
    :rtype: List[State]
    """
    #TODO
    


def is_goal(state):
    """
    Returns True if the state is the goal state and False otherwise.

    :param state: the current state.
    :type state: State
    :return: True or False
    :rtype: bool
    """
    #TODO
    return exit


def get_path(state):
    """
    Return a list of states containing the nodes on the path 
    from the initial state to the given state in order.

    :param state: The current state.
    :type state: State
    :return: The path.
    :rtype: List[State]
    """
    #TODO
    return exit


def blocking_heuristic(board):
    """
    Returns the heuristic value for the given board
    based on the Blocking Heuristic function.

    Blocking heuristic returns zero at any goal board,
    and returns one plus the number of cars directly
    blocking the goal car in all other states.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """
    #TODO
    return exit


def advanced_heuristic(board):
    """
    An advanced heuristic of your own choosing and invention.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """
    goal_coord = 0
    blockedCells = [0] * 6
    blockedCellsLen = [0] * 6
    blockedCellsRow = [0] * 6
    occupied = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    
    cars = board.cars
    for car in cars:
        if car.orientation == "v":
            x_coord = car.fix_coord
            y_coord = car.var_coord
            for r in range(y_coord, y_coord + car.length):
                occupied[r][x_coord] = 1
        else:
            x_coord = car.var_coord
            y_coord = car.fix_coord
            for c in range(x_coord, x_coord + car.length):
                occupied[y_coord][c] = 1    
        if car.is_goal:
            goal_coord = car.var_coord
            if goal_coord == 4:
                return 0
        else:
            if car.orientation == "v":
                for r in range(car.length):
                    if car.var_coord + r == 2:
                        blockedCells[car.fix_coord] = 1
                        blockedCellsLen[car.fix_coord] = car.length
                        blockedCellsRow[car.fix_coord] = car.var_coord
    
    
    ret = 0
    blocked_3 = 0
    for c in range(goal_coord, 6):
        ret = ret + blockedCells[c]
        if blockedCellsLen[c] == 3:
            # must go down and takes up all the space
            blocked_cur = 0;
            for r in range(blockedCellsRow[c] + 3, 6):
                blocked_cur = blocked_cur + occupied[r][c]
            blocked_3 = max(blocked_3, blocked_cur)
            
    return ret + 1 + min(blocked_3, 1)

def main():
    boards = from_file("C:/Users/karal/Documents/School/3b/CS 486/a1_files/code_posted/jams_posted.txt")
    
    global num_expand
    
    print("\t\t|Advanced\t\t|Blocking\t\t|Advanced");
    print("Maze No.\t|Length\t|Expansion\t|Length\t|Expansion\t|Does Better");
    print("----------------+-------+---------------+-------+---------------+-----------------------");
        
    for j in range(42):
        i = j
        wrong = 0
        board = boards[i]
        num_expand = 0
        path1, cost = a_star(board,advanced_heuristic)
        adv_len = len(path1)
        adv_exp = num_expand
        num_expand = 0
        path2, cost = a_star(board,blocking_heuristic)
        blo_len = len(path2)
        blo_exp = num_expand
        print(i, end="\t\t|")
        print(adv_len, end = "\t|")
        print(adv_exp, end = "\t\t|")
        print(blo_len, end = "\t|")
        print(blo_exp, end = "\t\t|")
        better = adv_exp <= blo_exp and adv_len == blo_len
        print(adv_exp <= blo_exp and adv_len == blo_len) 
        if not better:
            wrong = wrong + 1
            for s in range(min(adv_len, blo_len)):
                print("Advanced:")
                path1[s].board.display()
                print(path1[s].f)
                print(path1[s].depth)
                print("Blocked:")
                path2[s].board.display()
                print(path2[s].f)
                print(path2[s].depth)
            for s in range(min(adv_len, blo_len), max(adv_len, blo_len)):
                if (adv_len < blo_len):
                    print("Blocked:")
                    path2[s].board.display()
                else:
                    print("Advanced:")
                    path1[s].board.display()       
                    
        
main()
