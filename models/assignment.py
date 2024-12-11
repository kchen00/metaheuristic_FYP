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
        # the risk of this job
        self.risk = self.job.risk

        # the ratio of job risk to employee rank
        # lower ratio means the job is more suited to the rank
        # high risk job assign to junior employee is bad
        self.risk_rank_ratio = self.risk / self.employee.rank

        self.calculate_make_span()
        self.calculate_cost()
    
    def calculate_make_span(self):
        self.make_span = self.job.weighted_duration / self.employee.time_efficiency

        return self.make_span

    def calculate_cost(self):
        self.cost = self.job.weighted_cost / self.employee.cost_efficiency

        return self.cost

    def __repr__(self) -> str:
        vector = f"J{self.job}E{self.employee}"
        return vector