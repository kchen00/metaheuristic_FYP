import json
from models.job import Job, JOB_TYPE
from models.team import Team

json_path = "json"
job_path = f"{json_path}/jobs"
team_path = f"{json_path}/teams"

def create_job(name: str, job_type: JOB_TYPE, od: float, ed: float, pd: float, weight: list):
    """
    stores job object as jsob file
    """
    job = Job(name, 0, job_type, od, ed, pd, weight)
    with open(f"{job_path}/{name}.json", "w") as f:
        data = job.to_dict()
        json.dump(data, f)

def create_team(name: str, efficiency: float, job_focus: JOB_TYPE):
    """
    store team object as json file
    """
    team = Team(name, 0, efficiency, job_focus)
    with open(f"{team_path}/{name}.json", "w") as f:
        data = team.to_dict()
        json.dump(data, f) 

def read_job(name: str, id: int) -> Job:
    """
    open the job file and return the job

    must specify the id upon reading the file
    """
    with open(f"{job_path}/{name}.json", "r") as f:
        data = json.load(f)
        job = Job(
            name=data["name"],
            id_=id,
            job_type=JOB_TYPE(data["job_type"]),
            od=data["od"],
            ed=data["ed"],
            pd=data["pd"],
            weight=data["weight"]
        )

        return job

def read_team(name: str, id: int) -> Team:
    """
    read the team file and return the team

    must specify the id upon reading the file
    """
    with open(f"{team_path}/{name}.json", "r") as f:
        data = json.load(f)
        team = Team(
            name=data["name"],
            id_=id,
            efficiency=data["efficiency"],
            job_focus=JOB_TYPE(data["job_focus"])
        )

        return team
