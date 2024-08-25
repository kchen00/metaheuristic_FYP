"""
config contains the jobs and teams
"""

from models.job import Job, JOB_TYPE
from models.team import Team
from helpers.helper import kahn_sort
import random

random.seed(1)

cost_weights = [1, 6, 1]
make_span_weights = [1, 6, 1]

# planning jobs
job_1 = Job("Define Project Scope", 1, JOB_TYPE.PLANNING, [2, 5, 10], [1.0, 5.0, 5.5], 0.7, make_span_weights, cost_weights)
job_2 = Job("Identify Stakeholders", 2, JOB_TYPE.PLANNING, [2, 3, 5], [1.0, 3.0, 5.5], 0.3, make_span_weights, cost_weights)
job_3 = Job("Create Project Timeline", 3, JOB_TYPE.PLANNING, [2, 4, 10], [2.0, 4.0, 4.5], 0.6, make_span_weights, cost_weights)
job_4 = Job("Risk Assessment", 4, JOB_TYPE.PLANNING, [2, 3, 10], [2.5, 3.5, 4.5], 0.4, make_span_weights, cost_weights)
job_5 = Job("Budget Estimation", 5, JOB_TYPE.PLANNING, [2, 4, 10], [2.5, 4.5, 5.0], 0.8, make_span_weights, cost_weights)
# analysis job
job_6 = Job("Requirements Gathering", 6, JOB_TYPE.ANALYSIS, [8, 10, 20], [8.0, 10.0, 12.0], 0.7, make_span_weights, cost_weights)
job_7 = Job("Feasibility Study", 7, JOB_TYPE.ANALYSIS, [5, 7, 10], [5.0, 7.0, 9.5], 0.5, make_span_weights, cost_weights)
job_8 = Job("Requirement Specification", 8, JOB_TYPE.ANALYSIS, [5, 8, 10], [3.5, 5.5, 6.5], 0.4, make_span_weights, cost_weights)
job_9 = Job("Stakeholder Analysis", 9, JOB_TYPE.ANALYSIS, [2, 4, 6], [1.0, 4, 4.5], 0.3, make_span_weights, cost_weights)
job_10 = Job("Process Modeling", 10, JOB_TYPE.ANALYSIS, [2, 6, 10], [5.5, 6, 8.0], 0.4, make_span_weights, cost_weights)
# design jobs
job_11 = Job("System Architecture Design", 11, JOB_TYPE.DESIGN, [8, 10, 15], [10.0, 12.0, 14.0], 0.6, make_span_weights, cost_weights)
job_12 = Job("Database Design", 12, JOB_TYPE.DESIGN, [5, 7, 10], [6.5, 8.0, 10.0], 0.5, make_span_weights, cost_weights)
job_13 = Job("User Interface Design", 13, JOB_TYPE.DESIGN, [6, 8, 10], [8.5, 9.0, 12.0], 0.4, make_span_weights, cost_weights)
job_14 = Job("Component Design", 14, JOB_TYPE.DESIGN, [4, 6, 10], [5.5, 6.5, 9.5], 0.5, make_span_weights, cost_weights)
job_15 = Job("Security Design", 15, JOB_TYPE.DESIGN, [5, 7, 10], [8.0, 8.5, 10.0], 0.8, make_span_weights, cost_weights)
# implementation jobs
job_16 = Job("Code Development", 16, JOB_TYPE.IMPLEMENTATION, [18, 20, 30], [20.0, 25.0, 40.0], 0.7, make_span_weights, cost_weights)
job_17 = Job("Unit Testing", 17, JOB_TYPE.IMPLEMENTATION, [3, 5, 7], [4.0, 5.0, 8.0], 0.3, make_span_weights, cost_weights)
job_18 = Job("Code Review", 18, JOB_TYPE.IMPLEMENTATION, [2, 4, 10], [2.0, 4.0, 5.5], 0.4, make_span_weights, cost_weights)
job_19 = Job("Integration Testing", 19, JOB_TYPE.IMPLEMENTATION, [5, 7, 10], [6.0, 7.5, 10.0], 0.5, make_span_weights, cost_weights)
job_20 = Job("Deployment", 20, JOB_TYPE.IMPLEMENTATION, [2, 3, 4], [2.0, 3.5, 4.0], 0.8, make_span_weights, cost_weights)
# maintainence job
job_21 = Job("Bug Fixing", 21, JOB_TYPE.MAINTAINENCE, [2, 5, 10], [4.5, 5, 7.0], 0.4, make_span_weights, cost_weights)
job_22 = Job("Performance Optimization", 22, JOB_TYPE.MAINTAINENCE, [2, 6, 10], [6.5, 7.0, 8.0], 0.6, make_span_weights, cost_weights)
job_23 = Job("Software Updates", 23, JOB_TYPE.MAINTAINENCE, [2, 5, 10], [4.0, 6.0, 8.0], 0.5, make_span_weights, cost_weights)
job_24 = Job("User Support", 24, JOB_TYPE.MAINTAINENCE, [2, 5, 10], [4.0, 10.0, 11.0], 0.3, make_span_weights, cost_weights)
job_25 = Job("Documentation Update", 25, JOB_TYPE.MAINTAINENCE, [2, 4, 10], [2.0, 4.0, 4.5], 0.2, make_span_weights, cost_weights)

jobs = [
    job_1,
    job_2,
    job_3,
    job_4,
    job_5,
    job_6,
    job_7,
    job_8,
    job_9,
    job_10,
    job_11,
    job_12,
    job_13,
    job_14,
    job_15,
    job_16,
    job_17,
    job_18,
    job_19,
    job_20,
    job_21,
    job_22,
    job_23,
    job_24,
    job_25
]

teams = [
    Team("XGWGK", 1, 0.80, 0.83, JOB_TYPE.PLANNING),
    Team("WLLXJ", 2, 0.84, 0.86, JOB_TYPE.PLANNING),
    Team("GSHJX", 3, 0.80, 0.89, JOB_TYPE.PLANNING),
    Team("GTCSM", 6, 0.81, 0.86, JOB_TYPE.ANALYSIS),
    Team("YNTVI", 7, 0.92, 0.82, JOB_TYPE.ANALYSIS),
    Team("TVFKY", 8, 0.88, 0.96, JOB_TYPE.ANALYSIS),
    Team("TJXNS", 11, 0.88, 0.83, JOB_TYPE.DESIGN),
    Team("YGQXC", 12, 0.84, 0.93, JOB_TYPE.DESIGN),
    Team("JDDQZ", 13, 0.86, 0.87, JOB_TYPE.DESIGN),
    Team("TFFUA", 16, 0.74, 0.85, JOB_TYPE.IMPLEMENTATION),
    Team("JBCDP", 17, 0.96, 0.81, JOB_TYPE.IMPLEMENTATION),
    Team("ZFMUR", 18, 0.92, 0.89, JOB_TYPE.IMPLEMENTATION),
    Team("OWTEW", 21, 0.87, 0.83, JOB_TYPE.MAINTAINENCE),
    Team("NERGG", 22, 0.85, 0.77, JOB_TYPE.MAINTAINENCE),
    Team("FJQHF", 23, 0.95, 0.82, JOB_TYPE.MAINTAINENCE),
]

# building job dependency
dependencies = [
    (job_2, [job_1]),
    (job_4, [job_1, job_2]),
    (job_5, [job_4, job_3]),
    (job_3, [job_1]),
    (job_6, [job_3, job_5]),
    (job_7, [job_6]),
    (job_8, [job_6]),
    (job_10, [job_7, job_8]),
    (job_9, [job_7]),
    (job_11, [job_10]),
    (job_12, [job_9, job_11]),
    (job_13, [job_12]),
    (job_14, [job_12]),
    (job_15, [job_12]),
    (job_22, [job_13, job_14, job_15, job_20, job_21]),
    (job_16, [job_15]),
    (job_17, [job_16]),
    (job_18, [job_16]),
    (job_19, [job_17, job_18]),
    (job_20, [job_19]),
    (job_21, [job_20]),
    (job_23, [job_22]),
    (job_24, [job_22]),
    (job_25, [job_23, job_24]),
]

j: Job
for j, d in dependencies:
    j.depends_on(d)

# topo_order = kahn_sort(jobs)
# print(topo_order)