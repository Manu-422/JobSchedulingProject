from collections import deque


def topological_sort(jobs, dependencies):
    graph = {job: [] for job in jobs}
    in_degree = {job: 0 for job in jobs}

    for prerequisite, job in dependencies:
        if prerequisite not in graph or job not in graph:
            raise ValueError("Unknown job in dependency")

        graph[prerequisite].append(job)
        in_degree[job] += 1

    queue = deque(job for job in jobs if in_degree[job] == 0)
    schedule = []

    while queue:
        current = queue.popleft()
        schedule.append(current)

        for next_job in graph[current]:
            in_degree[next_job] -= 1
            if in_degree[next_job] == 0:
                queue.append(next_job)

    if len(schedule) != len(jobs):
        return None

    return schedule
