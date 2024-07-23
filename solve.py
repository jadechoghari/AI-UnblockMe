from board import *
import copy
import heapq

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
    Otherwise, it returns an empty list and -1.

    :param init_board: The initial starting board.
    :type init_board: Board
    :param hfn: The heuristic function.
    :type hfn: Heuristic (a function that consumes a Board and produces a numeric heuristic value)
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """
    #TODO
    # implement multipath pruning
    seen = {}
    #initilize the init state
    initial_state = State(board=init_board, hfn=hfn, f=0, depth=0)

    heap = []
    heapq.heappush(heap, (initial_state.f, initial_state)) # we will use initial_state.f to compare the minimum
    seen[initial_state.id] = initial_state.f
    while heap:
        # pop the node with the minimum f-value from the priority queue
        min_f_state = heapq.heappop(heap)[1] # only the state 
        if is_goal(min_f_state):
            return get_path(min_f_state), min_f_state.f
        for state in get_successors(min_f_state):
            state.f = state.depth + hfn(state.board) # cost + h
            if state.id not in seen or state.f < seen[state.id]:
                heapq.heappush(heap, (state.f, state))
                seen[state.id] = state.f
    return [], -1
    # use a heap to add neighbours and get min value


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
    # break ties by using the states ID's values
    # use multipruning search
    # At each step, DFS will add the successors to the
    # frontier in decreasing order of their IDs. In other words, DFS will expand the state with
    # the smallest ID value among the successors
    #TODO
    # implement multipath pruning
    seen = set()
    #initilize the init state
    initial_state = State(board=init_board, hfn=zero_heuristic, f=0, depth=0)

    # Create a stack for DFS 
    stack = []

    stack.append(initial_state)

    while len(stack):
        # pop from the stack the state
        current_state = stack.pop()

        if is_goal(current_state):
            return get_path(current_state), current_state.depth

        # if not, get successor and continue 

        # if not, get successors and continue
        successors = get_successors(current_state)
        successors.sort(key=lambda s: s.id, reverse=True)  # decreasing order by id

        for successor in successors:
            successor.f = successor.depth
            if successor.id not in seen:
                stack.append(successor)
                seen.add(successor.id)
    return [], -1


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
    successors = []

    for car in state.board.cars: #iterate over all cars of the boards
        if car.orientation == 'h': # horizontal can move left or right
            # try to move left
            if car.var_coord > 0 and state.board.grid[car.fix_coord][car.var_coord - 1] == '.':
                new_board = move_car(state.board, car, -1)
                new_state = State(board=new_board, hfn=state.hfn, f=state.depth + 1 + state.hfn(new_board), depth=state.depth + 1, parent=state)
                successors.append(new_state)

            #try to move right
            if car.var_coord + car.length < state.board.size and state.board.grid[car.fix_coord][car.var_coord + car.length] == '.':
                new_board = move_car(state.board, car, +1)
                new_state = State(board=new_board, hfn=state.hfn, f=state.depth + 1 + state.hfn(new_board), depth=state.depth + 1, parent=state)
                successors.append(new_state)

        elif car.orientation == 'v':
            
             # try to move up
            if car.var_coord > 0 and state.board.grid[car.var_coord - 1][car.fix_coord] == '.':
                new_board = move_car(state.board, car, -1)
                new_state = State(board=new_board, hfn=state.hfn, f=state.depth + 1 + state.hfn(new_board), depth=state.depth + 1, parent=state)
                successors.append(new_state)

            #try to move down
            if car.var_coord + car.length < state.board.size and state.board.grid[car.var_coord + car.length][car.fix_coord] == '.':
                new_board = move_car(state.board, car, +1)
                new_state = State(board=new_board, hfn=state.hfn, f=state.depth + 1 + state.hfn(new_board), depth=state.depth + 1, parent=state)
                successors.append(new_state)

    return successors


def move_car(board: Board, car: Car, move: int) -> Board:
    """
    Helper function implemented
    Return a new board with the given car moved by the given amount.
    """
    #TODO
    new_cars = []

    for c in board.cars:
        if c == car:
            if car.orientation == 'h':
                new_cars.append(Car(coord_x=car.var_coord + move, coord_y=car.fix_coord, orientation=car.orientation, length=car.length, is_goal=car.is_goal))
            elif car.orientation == 'v':
                new_cars.append(Car(coord_x=car.fix_coord, coord_y=car.var_coord + move, orientation=car.orientation, length=car.length, is_goal=car.is_goal))
        else:
            new_cars.append(c)

    new_board = Board(name=board.name, size=board.size, cars=new_cars)
    return new_board


def is_goal(state):
    """
    Returns True if the state is the goal state and False otherwise.

    :param state: the current state.
    :type state: State
    :return: True or False
    :rtype: bool
    """

    """
    • The puzzle must be on a 6 x 6 grid.
    • The goal car is in row 2 and it has a length of 2.
    • Besides the goal car, there is no other horizontal car in row 2.
    """
    #TODO
    cars = state.board.cars
    for car in cars:
        if car.is_goal:
            if car.var_coord + car.length - 1 == 5:
                return True
            return False



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
    path = [state]
    while (state.parent != None):
        path.insert(0, state.parent) #list.insert(pos, elmnt)
        state = state.parent
    return path


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
    """
    1- Identify the goal car
    2- Check if the goal car is at the exit - the heuristic value is zero
    3- Count blocking cars
    """

    goal_row = 2
    goal_car_length = 2

    # we are assuming the goal car is horizontal
    goal_car_pos = None
    for car in board.cars:
        if car.is_goal:
            goal_car_pos = car.var_coord
            break

    if goal_car_pos is None:
        raise ValueError("No goal car found on the board")
    
    # check if the goal car is already at the exit
    if goal_car_pos + goal_car_length == board.size:
        return 0
    
    # count the number of cars blocking the car's path - will be in same row 
    count = 0
    for col in range(goal_car_pos + goal_car_length, board.size):
        if board.grid[goal_row][col] != '.':
            count += 1

    return 1 + count

def advanced_heuristic(board):
    """
    An advanced heuristic of your own choosing and invention.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """
    #TODO
    goal_row = 2
    goal_car_length = 2
    # track columns with primary blockers
    primary_blocked_columns = set()

    # we are assuming the goal car is horizontal
    goal_car_pos = None
    for car in board.cars:
        if car.is_goal:
            goal_car_pos = car.var_coord
            break

    if goal_car_pos is None:
        raise ValueError("No goal car found on the board")
    
    # check if the goal car is already at the exit
    if goal_car_pos + goal_car_length == board.size:
        return 0
    
    # init the advanced heuristic param
    blocking_cars_count = 0
    total_distance = 0
    secondary_blocking_count = 0

    # check each column to the right of the goal car
    for col in range(goal_car_pos + goal_car_length, board.size):
        if board.grid[goal_row][col] != '.':
            blocking_cars_count += 1
            total_distance += (col - (goal_car_pos + goal_car_length))
            primary_blocked_columns.add(col)

    # check for secondary blockers in relevant rows and columns
    
    for car in board.cars:
        # for vertical cars we check if they block any of the columns identified as blocked by primary blockers
        if car.orientation == 'v':
            for col in primary_blocked_columns:
                if car.var_coord == col and car.fix_coord <= goal_row < car.fix_coord + car.length:
                    secondary_blocking_count += 1
                    break  # no need to check other columns for this car
                
        # for horizontal cars we check if any part of the car's length overlaps with the blocked columns
        elif car.orientation == 'h' and car.fix_coord == goal_row:
            for col in range(car.var_coord, car.var_coord + car.length):
                if col in primary_blocked_columns:
                    secondary_blocking_count += 1
                    break  # no need to check other columns for this car

     # heuristic value calculation
    heuristic_value = blocking_cars_count * 2 + total_distance + secondary_blocking_count * 2

    return heuristic_value

def main():
    # launch from here
    boards = from_file("https://github.com/jadechoghari/AI-UnblockMe/blob/main/jams_posted.txt")
    
    global num_expand
    
    print("\t\t|Advanced\t\t|Blocking\t\t|Advanced")
    print("Maze No.\t|Length\t|Expansion\t|Length\t|Expansion\t|Does Better")
    print("----------------+-------+---------------+-------+---------------+-----------------------")
        
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
