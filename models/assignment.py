from models.job import Job
from models.team import Team

class Assignment:
    """
    represent the assigment of job and team in a schedule
    """
    def __init__(self, j: Job, t: Team) -> None:
        # making sure that both job type and job focus is the same
        assert j.job_type == t.job_focus
        
        self.job: Job = j
        self.team: Team = t
        # how much time is needed to complete the job 
        self.make_span = 0
        # how much cost is needed to complete this job
        self.cost = 0

        self.calculate_make_span()
        self.calculate_cost()
    
    def calculate_make_span(self):
        self.make_span = self.job.weighted_duration / self.team.time_efficiency

        return self.make_span

    def calculate_cost(self):
        self.cost = self.job.weighted_cost / self.team.cost_efficieny

        return self.cost

    def __repr__(self) -> str:
        vector = f"T{self.team}J{self.job}"
        return vector