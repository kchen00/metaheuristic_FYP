"""
some helper scripts to make my life easier
"""

from models.job import Job, JOB_TYPE
from models.team import Team
from models.assignment import Assignment

def create_random_jobs(amount:int) -> list:
    """
    returns a list of random jobs
    """
    random_jobs = []
    for i in range(amount):
        new_job = Job(f"job_{i+1}", JOB_TYPE.PLANNING, 8/(i+1), 12/(i+1), 15/(i+1))
        random_jobs.append(new_job)

    return random_jobs

def create_random_team(amount: int) -> list:
    """
    returns a list of random team
    """
    random_teams = []
    for i in range(amount):
        new_team = Team(f"team_{i+1}", 0.5, JOB_TYPE.PLANNING)
        random_teams.append(new_team)

    return random_teams


def calculate_make_span(schedule: list) -> tuple:
    """
    given the schedule, return the team with highest make span and the make span
    
    Returns:
        (Team, make_span)
    """
    teams = {s.team for s in schedule}
    make_span = {}

    for t in teams:
        make_span[t] = sum([s.make_span for s in schedule if s.active and s.team == t])
    
    max_team = max(make_span, key=make_span.get)
    
    return max_team, make_span[max_team]


def print_schedule(schedule: list):
    schedule.sort(key=lambda x: x.make_span)
    teams = list({s.team for s in schedule})
    teams.sort(key=lambda x: x.name)

    team, make_span = calculate_make_span(schedule)

    print(f"Make span: {make_span:.2f}")
    print(f"Team {team.name} has the highest make span")
    t: Team
    for t in teams:
        print(f"{t.name} | {[s.job.name for s in schedule if s.active and s.team == t]} | {sum([s.make_span for s in schedule if s.active and s.team == t])}")
    
