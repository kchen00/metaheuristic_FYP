from setup import project
from models.project import Project

def check_difference(new_solution: list):
    old_compatibiltiy = sum([a.compatibility for a in project.assignments])
    new_compatibility = sum([a.compatibility for a in new_solution])

    compatibility_diff = (new_compatibility - old_compatibiltiy) / old_compatibiltiy

    old_team_size = len(set([a.member for a in project.assignments]))
    new_team_size = len(set([a.member for a in new_solution]))
    team_size_diff = (new_team_size - old_team_size) / old_team_size

    print("")
    print(f"Compatibility improvement:  {old_compatibiltiy} -> {new_compatibility} ({compatibility_diff})")
    print(f"Team size improvement:  {old_team_size} -> {new_team_size} ({team_size_diff})")