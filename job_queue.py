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

        self.jobs = []

    def next_turn(self):
        """
        moves game to the next turn, updating current_turn and jobs
        returns none if there is no next turn
        """
        turn = requests.get(base_url + "/" + self.game_id + "/next_turn").json()
        self.current_turn = turn["current_turn"]
        if self.current_turn > self.total_turns:
            return None
        else:
            self.jobs += turn["jobs"]

    def create_machine(self, n=1):
        """
        creates n new machines
        """
        for i in range(n):
            requests.post(Game.base_url + "/" + self.game_id + "/machines")

    def delete_machine(self, machine_id): 
        requests.delete(Game.base_url + "/" + self.game_id + "/machines/" + 
                machine_id)

    def compute_memory_required(self):       
        """
        returns the total memory required for active jobs
        """
        memory = 0
        for job in self.jobs:
            if job["turn"] <= job["turns_required"]:
                memory += job["memory_required"]
        return memory

    def compute_available_memory(self):
        """
        returns available memory of current machines
        in GB
        """
        game_info = requests.get(Game.base_url + "/" + self.game_id)
        return game_info["machines_running"]*64

    def assign_jobs(self, job):
        """
        assigns jobs to the machine with the lowest available memory
        sufficient for the job
        does nothing if job is already assigned
        """
        pass

    def manage_machines(self):
        """
        runs the show
        """
        for turn in range(self.total_turns):
            self.next_turn()
            memory_needed = self.compute_memory_required()
            memory_available = compute_available_memory()
            memory_deficit = memory_needed - memory_available
            # create machines
            if memory_deficit > 0:
                create_machine(n=((memory_deficit // 64) + 1))
            # assign jobs






