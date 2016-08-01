"""
Job Queue Class
allocates machines to run a queue of jobs with the goal of 
minimizing cost and delay until a job runs

written in Python3
"""

import requests
import sys


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
        if long_game:
            game_instance = requests.post(Game.base_url, data={"long": True}).json()
        else:
            game_instance = requests.post(Game.base_url).json()
        self.game_id = game_instance["id"]

        # boolean indicating whether game_type is long or short
        self.short_game = game_instance["short"]
        self.total_turns = 500 if long_game else 50
        self.current_turn = 0

        # {job_id: {"turn": 2, "turns_required": 6, "memory_required": 20, "machine_id": 202}}
        self.jobs = {}
        # {machine_id: memory_free}
        self.machines = {}
        
        self.jobs_delayed = 0


    def next_turn(self):
        """
        moves game to the next turn, updating jobs dictionary
        returns none if there is no next turn
        """
        turn = requests.get(Game.base_url + "/" + str(self.game_id) + "/next_turn").json()

        if turn["current_turn"] > self.total_turns:
            return None
        else:
            # add new jobs 
            for job in turn["jobs"]:
                self.jobs[job["id"]] = job
            return turn

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
    
    def assign_job(self, job_id, delay=True):
        """
        assigns job to the machine with the lowest 
        available memory sufficient for the job
            if delay is true, then job is assigned to machine with largest
            available memory 
            if false, then job is assigned to a new machine
        updates jobs dictionary and machine's available memory
        """
        memory_required = self.jobs[job_id]["memory_required"]
        sorted_machines = sorted(self.machines, 
                key=lambda x: self.machines[x])
        assigned = False
        for i, machine in enumerate(sorted_machines):
            if self.machines[machine] > memory_required or ((i + 1 == len(sorted_machines)) and delay):
                # assign to machine
                response = requests.post(Game.base_url + "/" + str(self.game_id) + 
                        "/machines/" + str(machine) + "/job_assignments",
                        data={"job_ids": "[" + str(job_id) + "]"})
                # throws exception if bad http request
                response.raise_for_status()
                # mark assignment in jobs dictionary
                self.jobs[job_id]["machine_id"] = machine
                # designate memory
                self.machines[machine] = self.machines.get(machine, 0) -memory_required
                if i + 1 == len(sorted_machines):
                    self.jobs_delayed += 1
                assigned = True
                break
        if not assigned:
            # create a new machine and recursively call itself
            self.create_machine()
            self.assign_job(job_id)

    def terminate_free_machines(self):
        """
        deletes machines without any jobs assigned to them
        """
        occupied_machines = {}
        for job in self.jobs:
            if "machine_id" in self.jobs[job]:
                occupied_machines[self.jobs[job]["machine_id"]] = True
        unoccupied_machines = [k for k in self.machines if k not in occupied_machines]
        for occupied_machine in occupied_machines:
            self.machines.pop(occupied_machine, None)
            requests.delete(Game.base_url + "/" + str(self.game_id) + 
                "/machines/" + str(occupied_machine))

    def terminate_all_machines(self):        
        """
        terminates all running machines
        """
        for machine in self.machines:
            requests.delete(Game.base_url + "/" + str(self.game_id) + 
                    "/machines/" + str(machine))
        self.machines = {}

    def manage_jobs(self, delay=False):
        """
        at each turn allocates machines to jobs
        """
        for job in self.jobs:
            # check whether job is finished
            try:
                finished = self.jobs[job]["finished"]
            except KeyError:
                self.jobs[job]["finished"] = False
                finished = False
            # not assigned
            if "machine_id" not in self.jobs[job]: 
                self.assign_job(job, delay=delay)
            # job finished running
            elif self.current_turn - self.jobs[job]["turn"] >  self.jobs[job]["turns_required"] and not finished:
                # free machine's memory
                machine_id = self.jobs[job]["machine_id"]
                memory = self.jobs[job]["memory_required"]
                self.machines[machine_id] = self.machines.get(machine_id, 0) + memory
                self.jobs[job]["finished"] = True

    def run_show(self, debug=False, delay=False):
        """
        runs the game by advancing turns and calling manage_jobs
        debug = True prints game status after each turn
        """
        self.manage_jobs(delay=delay)
        next_turn = self.next_turn()
        i = 1
        while next_turn:
            i += 1
            print("turn: ", i)
            self.manage_jobs(delay=delay)
            self.terminate_free_machines()
            if debug: 
                print("======")
                print("======")
                print(next_turn)
                print("======")
                for job in self.jobs:
                    print(job, self.jobs[job]["machine_id"], 
                            self.jobs[job]["memory_required"])
                print("======")
                for machine in self.machines:
                    print(machine, self.machines[machine])
                print("======")
            next_turn = self.next_turn()

        self.terminate_all_machines() 
        game_info = requests.get(Game.base_url + "/" + str(self.game_id)).json()
        # advance game until all jobs are complete 
            # requires more than 50 or 500 turns until jobs finish running
        while not game_info["completed"]:
            self.next_turn()
            i +=1 
            print("turn: ", i)
            game_info = requests.get(Game.base_url + "/" + str(self.game_id)).json()
        return game_info

# if file is executed not imported:
if __name__ == "__main__":        
    args = sys.argv
    try:
        if args[1] == "long":
            long_game = True
            print("starting long game")
    except IndexError:
        long_game = False
        print("starting short game")
    game = Game(long_game=long_game)
    print(game.run_show())

