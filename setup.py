from models.member import Member
from models.skill import Skill
from models.project import Project
from models.task import Task
from models.assignment import Assignment
import difference_checker
import random, json, pickle
import pandas as pd

random.seed(1)

staffs = dict()
staff_skills = dict()

staff_json = dict()
with open("data/staff_expertise/staff_expertise.json", "r") as f:
    staff_json = json.load(f)

# creating the list of project members
for s in staff_json:
    new_member = Member(s, staff_json[s]["salary"], staff_json[s]["efficiency"])
    staffs[s] = new_member

    # add the skillset to the new member
    new_member_skill = list()
    for s in staff_json[s]["expertise"]:
        # check if the skill already created, else create one
        skill_obj = staff_skills.get(s)
        if skill_obj:
            new_member_skill.append(skill_obj)
        else:
            new_skill = Skill(s)
            staff_skills[s] = new_skill
            new_member_skill.append(new_skill)

    new_member.skill_set = set(new_member_skill)

for s in staffs:
    member: Member = staffs[s]
    scores = staff_json[s]["scores"]

    for i, m in enumerate(staffs):
        if scores[i] != 0:
            member.add_score(staffs[m], scores[i])

tasks: list[Task] = list()
task_json = dict()
with open("data/project task/task.json", "r") as f:
    task_json = json.load(f)
for t in task_json:
    new_task = Task(t["task"], set())
    for s in t["skills_required"]:
        skill_obj = staff_skills.get(s)
        if skill_obj:
            new_task.skills.add(skill_obj)
        else:
            new_skill = Skill(s)
            staff_skills[s] = new_skill
            new_task.skills.add(new_skill)

    tasks.append(new_task)

# extracting the members and skills for easier setup
skills: list[Skill] = list(staff_skills.values())
members: list[Member] = list(staffs.values())


def low_compatibility_team():
    """create team formation with low compatibility"""
    assignments = []
    for t in tasks:
        member = random.sample(members, 5)
        new_assignment: list[Assignment] = [Assignment(t, m) for m in member]
        assignments.append(min(new_assignment, key=lambda x: x.compatibility))

    project = Project("low compatibility team", assignments)
    return project


def big_size_team():
    """create team formation with big team size"""
    assignments = []
    choosen_members = list()
    for t in tasks:
        member = random.choice([m for m in members if m not in choosen_members])
        choosen_members.append(member)
        new_assignment = Assignment(t, member)
        assignments.append(new_assignment)

    project = Project("big size team", assignments)
    return project


def high_task_load_team():
    """create team formation with high task load"""
    available_member = random.sample(members, 3)
    project = Project(
        "high task load team",
        [Assignment(t, random.choice(available_member)) for t in tasks],
    )

    return project


def low_collab_team():
    """create team formation with low collaboration score"""
    projects: list[Project] = list()
    for i in range(900):
        project = Project(
            "low collab team", [Assignment(t, random.choice(members)) for t in tasks]
        )
        projects.append(project)

    return min(projects, key=lambda x: x.collab_score)

def print_project_task():
    pd.set_option('display.max_colwidth', None)
    df = pd.DataFrame(task_json)
    print(df)

# print_project_task()

low_compatibility = low_compatibility_team()
high_load = high_task_load_team()
big_team = big_size_team()
low_collab = low_collab_team()

projects:list[Project] = [
                            low_compatibility, 
                            big_team, 
                            high_load, 
                            low_collab
                        ]

for p in projects:
    p.save_project(before=True)