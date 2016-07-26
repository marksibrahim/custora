# Goal 
allocate enough machines to run jobs as they come in while minimizing cost.

# Details
* each machine costs $1 and has 64 GB of memory
* game comes in two flavors: 50 turns or 500 turns

## Game Flow
1. each turn yields a batch of jobs
2. allocate enough machines (delete or add)
3. assing jobs to each machine

## Implementation Plan
* create a game class
    * instantiate with game id
    * keep track of number of machines
    * number of jobs
    * turn
    * type of game
* methods
    * create machine
    * delete machine
    * next_turn
    * assign job to a machine


