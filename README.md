# Job Queue Game
allocate enough machines to run jobs with little delay while minimizing cost.


## Installation
* Install [Python 3](https://www.python.org/downloads/)
    * verify by typing python into a terminal and ensuring prompt states python 3.x
* Install [Requests](http://docs.python-requests.org/en/master/):

```bash
$ pip install requests
```

## Usage
For short game
```bash
    python job_queue.py 
```

For long game
```bash
    python job_queue.py 
```

To debug, import job_queue and instantiate a game:
```python
    import job_queue
    game = jobqueue.Game(long_game=False)
    # will print detailed information about each turn
    game.run_show(debug=True)
```

## Heuristic 
This is an NP hard problem, what heuristic have you chosen to approximate the optimal solution(s), why?

Please don't implement: What other heuristics can you think of to approximate the optimal solution(s)? How would they compare with your implementation?
Can you specify the relative cost of running a machine and a delay turn (potentially a parameter or a class that implements a strategy)?

## Implementation Details
How is the code organized? Does the code have good style? (naming, imports, comments, convention of the language, etc)
What data structures did you use? Why?
Discuss the run time complexity of your algorithm.

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

* track jobs and machines they're assigned to

for job in jobs:
* three states: running, finished, needs to run

1. if assigned: do nothing
2. if not assigned:
    a. assign to machine with smallest available memory sufficient for job ("greedy")
    b. if none are available, allocate to a new machine
3. delete any unused machines (ones with completed jobs)

* note: API doesn't register the game's state as finished untill jobs have finished running, which may occur a few turns after turn 50 for a short game or 500 for a long one.
