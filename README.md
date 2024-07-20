# AI Unblock Me Solver

## Overview
We are building an AI that can solve the popular puzzle game "Unblock Me." Our AI leverages advanced machine learning techniques to navigate the complexities of the game, providing efficient and optimal solutions.

![DeepMind](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/DeepMind_new_logo.svg/2560px-DeepMind_new_logo.svg.png)
## Relation to Google DeepMind
This project is inspired by the breakthroughs made by Google DeepMind in solving complex problems with AI, such as their work on AlphaGo and reinforcement learning. Similar to DeepMind's approach, our AI will use sophisticated algorithms to understand and master the game of "Unblock Me."


## Get Involved
We welcome contributions from the community. Whether you're a developer, researcher, or enthusiast, join us in creating an AI that pushes the boundaries of game-solving technology.

### Advanced Heuristic Design

We will implement an advanced heuristic that not only considers the number of blocking cars but also takes into account:
1. **distance of blocking cars from the goal car** - cars closer to the goal car should contribute more to the heuristic value.
2. **secondary blocking** - cars that block the primary blockers should also be considered.
3. **freeing path length**: the number of moves required to unblock the goal car by moving the blocking cars.

### Consistency and Dominance:
- **Consistency**: A heuristic is consistent if, for every node n and each successor n' of n generated by any action a, the estimated cost of reaching the goal from n is no greater than the cost of getting from n to n' plus the estimated cost of reaching the goal from n'. This heuristic is consistent because each move made reduces the estimated distance to the goal.
- **Dominance**: This heuristic dominates the blocking heuristic because it includes all the information that the blocking heuristic uses (number of blocking cars) and adds additional factors like distance and secondary blocking.
