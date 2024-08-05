from models.job import JOB_TYPE

class Team:
    """
    represents a team on a schedule
    """
    def __init__(self, name: str, efficiency: float, job_focus: JOB_TYPE) -> None:
        assert efficiency <= 1.0, "efficiecy must be lesser than 1.0, unless you have superman"
        self.name = name
        self.job_focus = job_focus
        self.efficiency = efficiency