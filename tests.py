"""
tests whether a game is correctly created and methods
(add_machine, delete_machine, next_turn) work as expected
"""
import job_queue

game = job_queue.Game()

def test_instantiation():
    # is id assigned to the game? 
    assert type(game.game_id) is int
    # default long 
    assert game.total_turns == 50
    # test long game
    long_game = job_queue.Game(long_game=True)
    assert long_game.total_turns == 500

def test_machine_creation():
    """
    ensures there are at least three machines are available after creation
    """
    game.create_machine(n=3) 
    memory = 0
    for machine in game.machines:
        memory += 64
    assert memory >= 64*3

def test_delete_machine():
    """
    tests whether machine is deleted
    """
    for machine in game.machines:
        machine_id = machine
    game.delete_machine(machine_id)
    assert machine_id not in game.machines

def test_next_turn():
    """
    test whether next turn correctly updates jobs
    assumes at least one new job appears at a turn
    """
    prev_jobs = len(game.jobs)
    if not game.next_turn():
        curr_jobs = len(game.jobs)
        assert curr_jobs > prev_jobs

def test_assign_job():
    """
    calls next_turn and assigns job to a machine
    """
    game.next_turn()
    assigned_job_id = None
    for job in game.jobs:
        if game.jobs[job]["turn"] < game.jobs[job]["turns_required"]: 
            game.assign_job(job)
            assigned_job_id = job
    assert "machine_id" in game.jobs[assigned_job_id]
    assigned_machine = game.jobs[assigned_job_id]["machine_id"]
    assert game.machines[assigned_machine] < 64

