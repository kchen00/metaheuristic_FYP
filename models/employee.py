from models.job import JOB_TYPE

class Employee:
    """
    represents a employee
    """
    def __init__(self, name: str, id_: int, time_efficiency:float, cost_efficiency: float, job_focus: JOB_TYPE) -> None:
        self.id_ = id_
        self.name = name
        self.job_focus = job_focus
        self.time_efficiency = time_efficiency
        self.cost_efficiency = cost_efficiency

    def __repr__(self) -> str:
        return str(self.id_)