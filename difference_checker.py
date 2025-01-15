from models.project import Project
import pandas as pd

def calculate_improvement(before: dict, after: dict, key: str):
    if before[key] == 0:
        return f"absolute improvement: {after[key]:.2f}" 
    
    improvement = (after[key] - before[key]) / before[key]
    return f"{improvement * 100:.2f}%"

def print_improvement(before: Project, after: Project):
    before_metrics = before.formation_metrics()
    after_metrics = after.formation_metrics()
    data = {
        "before": before_metrics,
        "after": after_metrics,
        "improvement": {
            key: calculate_improvement(before_metrics, after_metrics, key) for key in before_metrics
            },
    }

    df = pd.DataFrame(data)
    print(df)

def print_member_changes(before: Project, after: Project):
    data = {
        "before": before.assingment_member(),
        "after": after.assingment_member(),
    }

    df = pd.DataFrame(data)
    print(df)

def print_difference(before: Project, after: Project):
    print("=====================================================================")
    print(f"Scenario:  {before.name}")
    print_member_changes(before, after)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print_improvement(before, after)
    print("=====================================================================")