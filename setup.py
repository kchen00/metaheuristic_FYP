from models.member import Member
from models.skill import Skill
from models.project import Project
from models.task import Task
from models.assignment import Assignment
import random

random.seed(1)

# skills 
skill_1 = Skill("java_script")
skill_2 = Skill("python")
skill_3 = Skill("java")
skill_4 = Skill("php")
skill_5 = Skill("web_development")
skill_6 = Skill("web_scrapping")
skill_7 = Skill("ai")

skills = [
    skill_1,
    skill_2,
    skill_3,
    skill_4,
    skill_5,
    skill_6,
    skill_7,
]

# team members
member_1 = Member("member_1")
member_2 = Member("member_2")
member_3 = Member("member_3")
member_4 = Member("member_4")
member_5 = Member("member_5")

members = [
    member_1,
    member_2,
    member_3,
    member_4,
    member_5,
]

for m in members:
    random_skills = random.sample(skills, 3)
    m.skill_set = set(random_skills)

# task in the project
task_1 = Task("task_1", set(random.sample(skills, 3)))
task_2 = Task("task_2", set(random.sample(skills, 3)))
task_3 = Task("task_3", set(random.sample(skills, 3)))
task_4 = Task("task_4", set(random.sample(skills, 3)))
task_5 = Task("task_5", set(random.sample(skills, 3)))
task_6 = Task("task_6", set(random.sample(skills, 3)))
task_7 = Task("task_7", set(random.sample(skills, 3)))
task_8 = Task("task_8", set(random.sample(skills, 3)))
task_9 = Task("task_9", set(random.sample(skills, 3)))
task_10 = Task("task_10", set(random.sample(skills, 3)))

tasks = [
    task_1,
    task_2,
    task_3,
    task_4,
    task_5,
    task_6,
    task_7,
    task_8,
    task_9,
    task_10,
]

assignments = [
    Assignment(task_1, member_1),
    Assignment(task_2, member_4),
    Assignment(task_3, member_4),
    Assignment(task_4, member_4),
    Assignment(task_5, member_3),
    Assignment(task_6, member_2),
    Assignment(task_7, member_1),
    Assignment(task_8, member_4),
    Assignment(task_9, member_3),
    Assignment(task_10, member_2),
]
project = Project("itern dashboard", assignments)