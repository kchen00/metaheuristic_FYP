from models.assignment import Assignment

#assignments is a list of Asssignment objects
def min_min(assignments: list) -> list: 
    """
    min min scheduling, arrange the job based on earliest finish time
    """
    schedule = []
    # shallow copy of assingments to avoid issue
    active_assigment = {a for a in assignments if a.active}

    # recalculate all the make span for each session of scheduling
    for a in active_assigment:
        a.calculate_make_span()
    
    # find out the type of job need to be arrange
    unique_jobs = {a.job for a in active_assigment}
    # print(f"{len(unique_jobs)} unique jobs found in assignment")
    # print("performing min min scheduling now")

    while len(unique_jobs) > 0:
        # find the option with minimum make span
        min_job:Assignment = min(active_assigment, key=lambda a: a.make_span)

        # add the min job to schedule
        schedule.append(min_job)

        # remove the min job from active assignment
        active_assigment = [a for a in active_assigment if a.job != min_job.job]

        # update the rest of the make span
        a: Assignment
        for a in active_assigment:
            # find the one with same team
            if a.team == min_job.team:
                a.make_span += min_job.make_span
            
        # remove the job from unique job set
        unique_jobs.remove(min_job.job)

    # print(f"final schedule has the make span of {max(s.make_span for s in schedule)}")
    return schedule
    