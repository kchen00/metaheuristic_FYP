from models.job import JOB_TYPE

class Team:
    """
    represents a team on a schedule
    """
    def __init__(self, name: str, id_: int, time_efficiency: float, cost_efficieny: float, job_focus: JOB_TYPE) -> None:
        assert time_efficiency <= 1.0, "efficiency must be lesser than 1.0, unless you have superman"
        assert cost_efficieny <= 1.0, "efficiency must be lesser than 1.0, unless you have superman"
        self.name = name
        self.job_focus = job_focus
        self.time_efficiency = time_efficiency
        self.cost_efficieny = cost_efficieny

        self.id_ = id_
    
    def __repr__(self) -> str:
        return str(self.id_)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "time_efficiency": self.time_efficiency,
            "cost_efficieny": self.cost_efficieny,
            "job_focus": self.job_focus.value
        }