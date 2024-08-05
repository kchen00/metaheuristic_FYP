from enum import Enum

class JOB_TYPE(Enum):
    """
    type of job according to sdlc
    """
    PLANNING = 0
    ANALYSIS = 1
    DESIGN = 2
    IMPLEMENTATION = 3
    MAINTAINENCE = 4

class Job:
    """
    represent a job in a schedule
    OD: optimistic time, shortest time possible to complete this job
    ED: estimated time, realistic time estimate needed tom complete this job
    PD: pessimistic time, longest time possible to complete this job
    """
    def __init__(self, name: str, job_type: JOB_TYPE, od: float, ed: float, pd: float, weight: list = [1, 4, 1]):
        assert pd > ed > od, "OD must be the smallest and PD must be the largest"
        self.name = name
        self.job_type = job_type
        self.od = od
        self.ed = ed
        self.pd = pd
        self.weight = weight
        self.weighted_duration = 0

        self.calculated_weighted_duration()

    def calculated_weighted_duration(self):
        weighted_duration = 0

        for d, w in zip([self.od, self.ed, self.pd], self.weight):
            weighted_duration += d*w
        
        weighted_duration /= sum(self.weight)

        self.weighted_duration = weighted_duration
