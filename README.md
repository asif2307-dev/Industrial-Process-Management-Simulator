# 🏭 Industrial Process Management Simulator (OS Scheduling Architecture)

[![Python Version](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%2B-blue.svg)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/GUI-Tkinter%20%26%20TTK-cyan.svg)](https://docs.python.org/3/library/tkinter.html)
[![Visualization](https://img.shields.io/badge/Charts-Matplotlib%20(Embedded)-orange.svg)](https://matplotlib.org/)
[![Course](https://img.shields.io/badge/Course-Operating%20Systems%20PBL-emerald.svg)](#)

A high-performance, modern desktop simulator designed to model, analyze, and visualize real-time **CPU process scheduling algorithms** applied to automated industrial systems (e.g., robotic assembly, sensor telemetry, conveyor motor controllers, and quality inspection units).

---

## 📸 Key Features & Capabilities

- 🎨 **Executive Dark SCADA Interface:** Sleek, modern industrial aesthetic built with Tkinter & TTK featuring custom card containers, responsive layouts, and distinct status badges.
- 📊 **Embedded Real-Time Gantt Chart:** Live visualization of execution timelines directly embedded inside the desktop window using `FigureCanvasTkAgg`—complete with task-specific color keys, interval timestamps, and CPU IDLE detection.
- 📈 **Dynamic KPI Metrics Cards:** Instant calculation of:
  - ⏱️ **Average Waiting Time (WT)**
  - 🔄 **Average Turnaround Time (TAT)**
  - 🏁 **Total Makespan** (total simulation completion time)
  - ⚡ **CPU Efficiency / Utilization (%)**
- ⚡ **One-Click Industrial Presets:** Preloads real-world factory tasks (`ROBOT_ARM`, `TEMP_VALVE`, `CONVEYOR_BELT`, `OPTICAL_QC`, `PACKAGING_UNIT`) with non-zero arrival times and variable burst/priority constraints.
- ⌨️ **Keyboard Shortcut:** Instant simulation execution using **`F5`** or the always-visible top-header action bar.
- 📦 **Zero External Heavy Dependencies:** Pure Python standard library (`tkinter`) and `matplotlib`—runs natively out-of-the-box.

---

## 🧠 Supported Scheduling Algorithms

| Algorithm | Description | Mode | Strategy |
| :--- | :--- | :--- | :--- |
| **FCFS** | First-Come, First-Served | Non-Preemptive | Processes are executed strictly in the order of their arrival time. |
| **SJF** | Shortest Job First | Non-Preemptive | The available process with the shortest CPU burst time is prioritized. |
| **Priority** | Priority Scheduling | Non-Preemptive | Dispatches jobs based on priority levels (lower integer = higher priority). |
| **Round Robin (RR)** | Time-Sliced Execution | Preemptive | Allocates a cyclic **Time Quantum** to ready processes in a FIFO queue. |

---

## 📐 Mathematical Formulation

The simulator calculates execution metrics according to standard operating systems scheduling formulas:

1. **Turnaround Time ($TAT$):**
   $$\text{TAT} = \text{Completion Time (CT)} - \text{Arrival Time (AT)}$$

2. **Waiting Time ($WT$):**
   $$\text{WT} = \text{Turnaround Time (TAT)} - \text{Burst Time (BT)}$$

3. **Average Waiting Time ($AWT$):**
   $$\text{AWT} = \frac{1}{N} \sum_{i=1}^{N} \text{WT}_i$$

4. **Average Turnaround Time ($ATAT$):**
   $$\text{ATAT} = \frac{1}{N} \sum_{i=1}^{N} \text{TAT}_i$$

5. **CPU Efficiency / Utilization:**
   $$\text{Efficiency (\%)} = \left( \frac{\sum_{i=1}^{N} \text{Burst Time}_i}{\text{Makespan}} \right) \times 100$$

---

## 🗂️ Project Structure

```text
Industrial_Process_Simulator_OS/
│
├── main.py                     # Main application entrypoint (Dashboard UI, Canvas & Event Loop)
├── README.md                   # Comprehensive documentation and project guide
├── .gitignore                  # Git ignore definitions
│
└── modules/
    ├── scheduling.py           # Core scheduling algorithms (FCFS, SJF, Priority, Round Robin)
    ├── visualization.py        # Embedded Matplotlib Gantt chart drawing & palette mapping
    ├── process_manager.py      # Process data structure operations (add, remove, list)
    └── test_scheduling.py     # Automated unit test suite verifying algorithm correctness
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** (Tested on Python 3.11)
- **Matplotlib**

To verify your environment or install `matplotlib`:
```bash
pip install matplotlib
```

### Running the Application

1. Navigate to the project root directory:
   ```powershell
   cd "c:\Users\choud\OneDrive\Desktop\PBL, Form, etc\OS PBL\Industrial_Process_Simulator_OS"
   ```

2. Launch the desktop simulator:
   ```powershell
   python main.py
   ```

3. **Quick Walkthrough:**
   - Click **`⚡ Load Preset`** (or enter custom processes manually using the PID, Arrival, Burst, and Priority fields).
   - Select your scheduling algorithm from the dropdown (e.g., *Round Robin* with a *Time Quantum* of `2`).
   - Click the bright green **`▶ RUN SIMULATION`** button or press **`F5`**.
   - Review the generated **Gantt Chart**, **KPI Stat Badges**, and **Detailed Process Results Table**.

---

## 🧪 Running Algorithm Verification Tests

To verify the scheduling algorithm calculations independently without the GUI, run the test suite:

```powershell
python modules/test_scheduling.py
```

Sample output:
```text
 FCFS
-----------------------------------
P1 Waiting: 0 Turnaround: 5 Completion: 5
P2 Waiting: 4 Turnaround: 7 Completion: 8
P3 Waiting: 6 Turnaround: 14 Completion: 16
P4 Waiting: 13 Turnaround: 15 Completion: 18
Average Waiting: 5.75
Average Turnaround: 10.25
...
```

---

## 👥 Authors & Academic Context

- **Course:** Operating Systems (OS) Project-Based Learning (PBL)
- **Application Focus:** Industrial Automation & Process Control Scheduling
- **Tech Stack:** Python 3, Tkinter/TTK, Matplotlib TkAgg, Git
