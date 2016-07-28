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
        * assign jobs to machine with lowest available memory sufficient for job
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
            # update current job turns
            for job in self.jobs:
                self.jobs[job]["turn"] += 1
            # add new jobs 
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
    
    def assign_job(self, job_id):
        """
        assigns job to the machine with the lowest 
        available memory sufficient for the job
        updates jobs dictionary and machine's available memory
        """
        memory_required = self.jobs[job_id]["memory_required"]
        sorted_machines = sorted(self.machines, 
                key=lambda x: self.machines[x])
        for machine in sorted_machines:
            if self.machines[machine] > memory_required:
                # assign to machine
                requests.post(Game.base_url + "/" + str(self.game_id) + 
                        "/machines/" + str(machine) + "/job_assignments",
                        data={"job_ids": [job_id]})
                # mark assignment in jobs dictionary
                self.jobs[job_id]["machine_id"] = machine
                # designate memory
                self.machines[machine] -= memory_required
        # else create a new machine and recursively call itself
        self.create_machine()
        self.assign_job(job_id)

    def manage_jobs(self):
        """
        at each turn allocates machines to jobs
        """
        pass

    def run_show(self):
        """
        runs the game
        """
        pass
        


