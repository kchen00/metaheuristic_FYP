class Member:
    '''represents a team member'''
    def __init__(self, name: str, salary: float, efficiency: float, skill_set:set = set()):
        self.name = name
        self.skill_set = skill_set
        self.salary = salary
        self.efficiency = efficiency
        self.collaboration_scores = dict()
    
    def add_score(self, other_member: 'Member', score: float):
        '''add peer review score of other member'''
        self.collaboration_scores[other_member] = score