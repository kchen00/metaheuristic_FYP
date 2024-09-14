from models.job import Job
from models.employee import Employee

class Assignment:
    """
    represent the assigment of job and team in a schedule
    """
    def __init__(self, j: Job, e: Employee) -> None:   
        # making sure job type and employe job focus is the same
        assert j.job_type == e.job_focus
        
        self.job: Job = j
        self.employee: Employee = e
        # how much time is needed to complete the job 
        self.make_span = 0
        # how much cost is needed to complete this job
        self.cost = 0

        self.calculate_make_span()
        self.calculate_cost()
    
    def calculate_make_span(self):
        self.make_span = self.job.weighted_duration / self.employee.time_efficiency

        return self.make_span

    def calculate_cost(self):
        self.cost = self.job.weighted_cost / self.employee.cost_efficiency

        return self.cost

    def __repr__(self) -> str:
        vector = f"E{self.employee}J{self.job}"
        return vector