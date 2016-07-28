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
