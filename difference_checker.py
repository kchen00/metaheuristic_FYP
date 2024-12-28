from models.project import Project

def print_comparison(before: Project, after: Project):
    print("Before")
    before.print_project()
    print("######################################")
    print("After")
    after.print_project()