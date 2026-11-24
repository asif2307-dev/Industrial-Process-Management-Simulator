
from scheduling import fcfs, sjf, priority_scheduling, round_robin

processes = [
    {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2},
    {"pid": "P2", "arrival": 1, "burst": 3, "priority": 1},
    {"pid": "P3", "arrival": 2, "burst": 8, "priority": 3},
    {"pid": "P4", "arrival": 3, "burst": 2, "priority": 2}
]

algorithms = {
    "FCFS": fcfs(processes),
    "SJF": sjf(processes),
    "Priority": priority_scheduling(processes),
    "Round Robin": round_robin(processes, 2)
}

for name, result in algorithms.items():
    print("\n", name)
    print("-" * 35)

    for p in result["results"]:
        print(
            p["pid"],
            "Waiting:", p["waiting"],
            "Turnaround:", p["turnaround"],
            "Completion:", p["completion"]
        )

    print("Average Waiting:", round(result["average_waiting"], 2))
    print("Average Turnaround:", round(result["average_turnaround"], 2))
