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

    durations and cost are categorized in to 3 types
    
    O: optimistic, shortest time/cost possible to complete this job
    
    E: estimated, realistic time/cost estimate needed tom complete this job
    
    P: pessimistic, longest time/cost possible to complete this job
    """
    def __init__(self, name: str, id_: int, job_type: JOB_TYPE, durations: list, costs: list, duration_weight: list = [1, 4, 1], cost_weight: list = [1, 4, 1]):
        od, ed, pd = durations
        oc, ec, pc = costs
        assert pd > ed > od, "OD must be the smallest and PD must be the largest"
        assert pc > ec > oc, "OC must be the smallest and PC must be the largest"
        self.name = name
        self.job_type = job_type
        self.durations = {
            "od": od,
            "ed": ed,
            "pd": pd
        }
        self.costs = {
            "oc": oc,
            "ec": ec,
            "pc": pc
        }
        self.duration_weight = duration_weight
        self.cost_weight = cost_weight

        self.weighted_duration = 0
        self.weighted_cost = 0

        self.calculated_weighted_duration()
        self.calculated_weighted_cost()

        self.id_ = id_

    def calculated_weighted_duration(self):
        """
        calculated weighted duration need by this job
        """
        weighted_duration = 0

        for d, w in zip(self.durations.values(), self.duration_weight):
            weighted_duration += d*w
        
        weighted_duration /= sum(self.duration_weight)
        self.weighted_duration = weighted_duration
    
    def calculated_weighted_cost(self):
        """
        calculate weighted cost needed by this job
        """
        weighted_cost = 0

        for c, w in zip(self.costs.values(), self.cost_weight):
            weighted_cost += c*w
        
        weighted_cost /= sum(self.duration_weight)
        self.weighted_cost = weighted_cost
    
    def __repr__(self) -> str:
        return str(self.id_)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "job_type": self.job_type.value,
            "durations": self.durations,
            "costs": self.costs,
            "duration_weights": self.duration_weight,
            "cost_weights": self.cost_weight,
        }
