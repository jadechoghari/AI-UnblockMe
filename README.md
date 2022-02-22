# Unblock Me

Built an AI that solves the game of Unblock Me with the goal of optimizing the number of steps it takes.

## Depth First Search
DFS does not take costs into account. Its goal is to simply find a solution by expanding the most recently added successor.

## A*
In A*, we minimize the total cost and heuristic value when choosing a successor to expand from a frontier. This could ensure that we find our solution using minimum number of steps.

### Cost Function
The total cost is determined by number of steps it has taken.

### Consistent Heuristic Function 1 - Number of cars blocking the exit plus 1
At any state, it takes at least 1 step for us to decrease the number of blocking cars by 1, and at least 1 step for us to move the goal car to the exit. Therefore, by induction, it must take at least `m + 1` steps for us to remove `m` blocking cars and move the goal car to the exit at any states. Therefore, we know that this is a consistent heuristic function.

### Consistent Heuristic Function 2 - Number of cars blocing the exit plus number of cars blocking the blocking cars plus 1
What's different between this function and the previous function is that, we are also adding one if there are cars under any blocking cars of length 3. This is because any blocking cars of length 3 must be moved to the bottom for the goal car to pass through. Similar to the above, it takes at least 1 step to remove all cars under blocking cars of length 3 at any state. Therefore, it's another consistent heuristic function. Furthermore, this function must give a value at least the value of the function 1. Therefore, this function dominates function 1.

## Multi-Path Pruning
In order to minimize the number repeating expansion, multi-path pruning is used. Since our heuristic functions are consistent, multi-path pruning would not remove the solution that takes the least amount of steps.

