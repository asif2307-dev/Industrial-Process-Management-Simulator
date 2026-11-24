
def fcfs(processes):
    jobs = sorted(processes, key=lambda x: x["arrival"])
    return calculate_schedule(jobs)


def sjf(processes):
    pending = processes.copy()
    completed = []
    time = 0

    while len(pending) > 0:
        available = []

        for p in pending:
            if p["arrival"] <= time:
                available.append(p)

        if len(available) == 0:
            time = min(p["arrival"] for p in pending)
            continue

        job = min(available, key=lambda x: x["burst"])
        completed.append(job)
        pending.remove(job)
        time += job["burst"]

    return calculate_schedule(completed)


def priority_scheduling(processes):
    pending = processes.copy()
    completed = []
    time = 0

    while pending:
        available = []

        for p in pending:
            if p["arrival"] <= time:
                available.append(p)

        if not available:
            time = min(p["arrival"] for p in pending)
            continue

        job = min(available, key=lambda x: x["priority"])
        completed.append(job)
        pending.remove(job)
        time += job["burst"]

    return calculate_schedule(completed)


def round_robin(processes, quantum):
    if quantum <= 0:
        raise ValueError("Quantum must be greater than zero")

    pending = sorted(processes, key=lambda x: x["arrival"])
    remaining = {p["pid"]: p["burst"] for p in processes}

    queue = []
    timeline = []
    completion = {}

    time = 0
    index = 0

    while index < len(pending) or queue:

        if not queue and index < len(pending):
            time = max(time, pending[index]["arrival"])

        while index < len(pending) and pending[index]["arrival"] <= time:
            queue.append(pending[index])
            index += 1

        if not queue:
            continue

        job = queue.pop(0)
        pid = job["pid"]

        run_time = min(quantum, remaining[pid])

        timeline.append({
            "pid": pid,
            "start": time,
            "end": time + run_time
        })

        time += run_time
        remaining[pid] -= run_time

        while index < len(pending) and pending[index]["arrival"] <= time:
            queue.append(pending[index])
            index += 1

        if remaining[pid] > 0:
            queue.append(job)
        else:
            completion[pid] = time

    return calculate_schedule(processes, timeline, completion)


def calculate_schedule(processes, timeline=None, completion=None):

    if not processes:
        raise ValueError("At least one process is required")

    if timeline is None:
        timeline = []
        time = 0

        for p in processes:
            start = max(time, p["arrival"])
            end = start + p["burst"]

            timeline.append({
                "pid": p["pid"],
                "start": start,
                "end": end
            })

            time = end

    if completion is None:
        completion = {}

        for item in timeline:
            completion[item["pid"]] = item["end"]

    results = []

    for p in processes:
        ct = completion[p["pid"]]
        tat = ct - p["arrival"]
        wt = tat - p["burst"]

        results.append({
            "pid": p["pid"],
            "completion": ct,
            "turnaround": tat,
            "waiting": wt
        })

    avg_waiting = sum(x["waiting"] for x in results) / len(results)
    avg_turnaround = sum(x["turnaround"] for x in results) / len(results)

    return {
        "timeline": timeline,
        "results": results,
        "average_waiting": avg_waiting,
        "average_turnaround": avg_turnaround
    }
