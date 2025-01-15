from models.skill import Skill
from models.member import Member
from models.task import Task
from models.assignment import Assignment
from models.project import Project
import random

random.seed(1)

s1 = Skill("s1")
s2 = Skill("s2")
s3 = Skill("s3")
s4 = Skill("s4")
s5 = Skill("s5")

m1 = Member("m1", 1000, 1.0, {s1, s2, s3, s4, s5})
m2 = Member("m2", 1000, 1.0, {s2, s3})
m3 = Member("m3", 1000, 1.0, {s1, s3, s4})
m4 = Member("m4", 1000, 1.0, {s2, s4})
m5 = Member("m5", 1000, 1.0, {s3})

t1 = Task("t1", {s1, s2, s3})
t2 = Task("t2", {s1, s3, s4})
t3 = Task("t3", {s1, s4})
t4 = Task("t4", {s2, s4})
t5 = Task("t5", {s3})

tasks = [t1, t2, t3, t4, t5] 
members = [m1, m2, m3, m4, m5]
rating_matric = [
    [0, 1, 3, 4, 2],
    [5, 0, 2, 3, 3],
    [4, 3, 0, 4, 5],
    [1, 3, 3, 0, 4],
    [4, 2, 3, 3, 0],
]
for i, m in enumerate(members):
    for j, other_member in enumerate(members):
        if m != other_member:
            m.add_score(other_member, rating_matric[i][j])

a1 = Assignment(t1, m3)
a2 = Assignment(t2, m3)
a3 = Assignment(t3, m3)
a4 = Assignment(t4, m4)
a5 = Assignment(t5, m5)

project = Project("Algorithm proof", [a1, a2, a3, a4, a5])