"""
Job Queue Class
allocates machines to run a queue of jobs with the goal of 
minimizing cost and delay until a job runs

written in Python3
"""

import requests


class Game():
    """
    creates a game instance tracking machines and jobs

    optimization heurstic:
        * track free memory at each turn
        * create/delete machines to accomodate new jobs
    """
    base_url = "http://job-queue-dev.elasticbeanstalk.com/games"
    def __init__(self, long_game=False):
        game_instance = requests.post(Game.base_url, data={"long": long_game}).json()
        self.game_id = game_instance["id"]

        # boolean indicating whether game_type is long or short
        self.short_game = game_instance["short"]
        self.total_turns = 500 if long_game else 50
        self.current_turn = 0

        self.jobs = {}
        self.machines = {}

    def next_turn(self):
        """
        moves game to the next turn, updating current_turn and jobs dictionary
        returns none if there is no next turn
        """
        turn = requests.get(Game.base_url + "/" + str(self.game_id) + "/next_turn").json()
        self.current_turn = turn["current_turn"]
        if self.current_turn > self.total_turns:
            return None
        else:
            for job in turn["jobs"]:
                self.jobs[job["id"]] = job

    def create_machine(self, n=1):
        """
        creates n new machines and updates machines dictionary
        """
        for i in range(n):
            machine = requests.post(Game.base_url + "/" + str(self.game_id) + "/machines").json()
            # add id and available memory
            self.machines[machine["id"]] =  64

    def delete_machine(self, machine_id): 
        """
        deletes machine in game
        and removes key from machines dictionary
        """
        requests.delete(Game.base_url + "/" + str(self.game_id) + "/machines/" + 
                str(machine_id))
        self.machines.pop(machine_id, None)

    def compute_available_memory(self):
        """
        updates the available memory on the machines list
        based on assigned jobs and available machines
        """
        memory = 0 
        for job in self.jobs:
            if job["turn"] <= job["turns_required"]:
                memory_needed = job

