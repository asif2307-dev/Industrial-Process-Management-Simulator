
import tkinter as tk
from tkinter import ttk, messagebox

from modules.scheduling import (
    fcfs, sjf, priority_scheduling, round_robin
)
from modules.visualization import show_gantt_chart


def add_process():
    try:
        pid = pid_entry.get().strip()
        arrival = int(arrival_entry.get())
        burst = int(burst_entry.get())
        priority = int(priority_entry.get())

        if not pid:
            raise ValueError("Enter Process ID")

        if arrival < 0 or burst <= 0 or priority < 0:
            raise ValueError("Enter valid process details")

        for row in process_table.get_children():
            if process_table.item(row)["values"][0] == pid:
                raise ValueError("Process ID already exists")

        process_table.insert(
            "", "end",
            values=(pid, arrival, burst, priority)
        )

        pid_entry.delete(0, tk.END)
        arrival_entry.delete(0, tk.END)
        burst_entry.delete(0, tk.END)
        priority_entry.delete(0, tk.END)

    except ValueError as error:
        messagebox.showerror("Input Error", str(error))


def run_simulation():
    try:
        processes = []

        for row in process_table.get_children():
            values = process_table.item(row)["values"]

            processes.append({
                "pid": str(values[0]),
                "arrival": int(values[1]),
                "burst": int(values[2]),
                "priority": int(values[3])
            })

        if not processes:
            messagebox.showwarning(
                "Warning", "Please add at least one process."
            )
            return

        choice = algorithm.get()

        if choice == "FCFS":
            result = fcfs(processes)

        elif choice == "SJF":
            result = sjf(processes)

        elif choice == "Priority":
            result = priority_scheduling(processes)

        else:
            time_slice = int(quantum.get())

            if time_slice <= 0:
                raise ValueError("Time quantum must be positive")

            result = round_robin(processes, time_slice)

        for row in result_table.get_children():
            result_table.delete(row)

        for process in result["results"]:
            result_table.insert(
                "", "end",
                values=(
                    process["pid"],
                    process["completion"],
                    process["waiting"],
                    process["turnaround"]
                )
            )

        waiting_label.config(
            text="Average Waiting Time: "
            + str(round(result["average_waiting"], 2))
        )

        turnaround_label.config(
            text="Average Turnaround Time: "
            + str(round(result["average_turnaround"], 2))
        )

        show_gantt_chart(result["timeline"], choice)

    except Exception as error:
        messagebox.showerror("Simulation Error", str(error))


root = tk.Tk()
root.title("Industrial Process Management Simulator")
root.geometry("1000x700")

title = tk.Label(
    root,
    text="Industrial Process Management Simulator",
    font=("Arial", 20, "bold")
)
title.pack(pady=15)

input_frame = ttk.LabelFrame(root, text="Add Process")
input_frame.pack(fill="x", padx=20, pady=10)

fields = [
    "Process ID",
    "Arrival Time",
    "Burst Time",
    "Priority"
]

entries = []

for column, field in enumerate(fields):
    ttk.Label(input_frame, text=field).grid(
        row=0, column=column, padx=10, pady=5
    )

    entry = ttk.Entry(input_frame, width=15)
    entry.grid(row=1, column=column, padx=10, pady=5)
    entries.append(entry)

pid_entry, arrival_entry, burst_entry, priority_entry = entries

ttk.Button(
    input_frame,
    text="Add Process",
    command=add_process
).grid(row=1, column=4, padx=10)

process_frame = ttk.LabelFrame(root, text="Process List")
process_frame.pack(fill="x", padx=20, pady=10)

columns = ("PID", "Arrival", "Burst", "Priority")

process_table = ttk.Treeview(
    process_frame,
    columns=columns,
    show="headings",
    height=5
)

for column in columns:
    process_table.heading(column, text=column)
    process_table.column(column, width=150)

process_table.pack(fill="x", padx=10, pady=10)

control_frame = ttk.Frame(root)
control_frame.pack(pady=15)

ttk.Label(
    control_frame,
    text="Scheduling Algorithm:"
).grid(row=0, column=0, padx=5)

algorithm = ttk.Combobox(
    control_frame,
    values=["FCFS", "SJF", "Priority", "Round Robin"],
    state="readonly",
    width=18
)
algorithm.set("FCFS")
algorithm.grid(row=0, column=1, padx=5)

ttk.Label(
    control_frame,
    text="Time Quantum:"
).grid(row=0, column=2, padx=5)

quantum = ttk.Entry(control_frame, width=8)
quantum.insert(0, "2")
quantum.grid(row=0, column=3, padx=5)

ttk.Button(
    control_frame,
    text="Run Simulation",
    command=run_simulation
).grid(row=0, column=4, padx=10)

result_frame = ttk.LabelFrame(root, text="Scheduling Results")
result_frame.pack(fill="x", padx=20, pady=10)

result_columns = (
    "PID", "Completion", "Waiting", "Turnaround"
)

result_table = ttk.Treeview(
    result_frame,
    columns=result_columns,
    show="headings",
    height=5
)

for column in result_columns:
    result_table.heading(column, text=column)
    result_table.column(column, width=180)

result_table.pack(fill="x", padx=10, pady=10)

waiting_label = ttk.Label(
    root, text="Average Waiting Time: --"
)
waiting_label.pack(pady=5)

turnaround_label = ttk.Label(
    root, text="Average Turnaround Time: --"
)
turnaround_label.pack(pady=5)

root.mainloop()
