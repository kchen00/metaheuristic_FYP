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
        # how much time is needed to complete the job when the job is assigned to this team?
        self.make_span = 0
        # whether this assignemnt is active or not
        self.active = False

        self.calculate_make_span()
    
    def calculate_make_span(self):
        self.make_span = self.job.weighted_duration / self.team.efficiency

        return self.make_span