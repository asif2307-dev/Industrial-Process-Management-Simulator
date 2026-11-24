
def add_process(processes, pid, arrival, burst, priority):
    if burst <= 0:
        raise ValueError("Burst time must be greater than zero")

    if arrival < 0:
        raise ValueError("Arrival time cannot be negative")

    process = {
        "pid": pid,
        "arrival": arrival,
        "burst": burst,
        "priority": priority
    }

    processes.append(process)
    return processes


def remove_process(processes, pid):
    for process in processes:
        if process["pid"] == pid:
            processes.remove(process)
            return True

    return False


def display_processes(processes):
    print("\nProcess List")
    print("-" * 45)

    for process in processes:
        print(
            process["pid"],
            "Arrival:", process["arrival"],
            "Burst:", process["burst"],
            "Priority:", process["priority"]
        )
