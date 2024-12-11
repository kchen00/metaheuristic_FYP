from models.job import JOB_TYPE
from enum import Enum

class Rank(float, Enum):
    JUNIOR = 1.0
    SENIOR = 2.0

class Employee:
    """
    represents a employee
    """

    def __init__(self, name: str, id_: int, time_efficiency: float, cost_efficiency: float, job_focus: JOB_TYPE, rank: Rank) -> None:
        self.id_ = id_
        self.name = name
        self.job_focus = job_focus
        self.rank = rank
        self.time_efficiency = time_efficiency
        self.cost_efficiency = cost_efficiency

    def __repr__(self) -> str:
        return str(self.id_)
