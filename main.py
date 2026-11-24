import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.scheduling import (
    fcfs, sjf, priority_scheduling, round_robin
)
from modules.visualization import plot_gantt_chart

# ---------------------------------------------------------
# UI Color Palette & Design Tokens (Modern Industrial Dark)
# ---------------------------------------------------------
THEME = {
    "bg_root": "#0b0f19",        # Main root background (deep obsidian)
    "bg_card": "#151d30",        # Card surface background
    "bg_card_inner": "#1c263e",  # Secondary inner container
    "border": "#273552",         # Border outline
    "text_primary": "#f8fafc",   # High-contrast text
    "text_secondary": "#94a3b8", # Muted label text
    "accent_blue": "#2563eb",    # Primary action blue
    "accent_blue_hover": "#1d4ed8",
    "accent_cyan": "#06b6d4",    # Industrial cyan
    "accent_green": "#10b981",   # Success / Run green
    "accent_green_hover": "#059669",
    "accent_amber": "#f59e0b",   # Warning / metrics
    "accent_purple": "#8b5cf6",  # TAT metric
    "accent_red": "#ef4444",     # Delete action
    "accent_red_hover": "#dc2626",
    "input_bg": "#0f172a",       # Field background
    "input_fg": "#f8fafc",
}

FONT_FAMILY = "Segoe UI"


def create_btn(parent, text, command, bg, hover_bg, fg="#ffffff", font_size=9, pad_x=10, pad_y=5):
    """Creates a modern flat button with dynamic hover state."""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=hover_bg,
        activeforeground=fg,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=(FONT_FAMILY, font_size, "bold"),
        padx=pad_x,
        pady=pad_y
    )

    def on_enter(e):
        btn.config(bg=hover_bg)

    def on_leave(e):
        btn.config(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


# ---------------------------------------------------------
# Application Core Logic
# ---------------------------------------------------------
class IndustrialSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Industrial Process Management Simulator | OS Scheduling")
        
        # Adaptive window geometry that fits nicely even on 1366x768 screens
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w = min(1240, max(1040, screen_w - 60))
        win_h = min(740, max(620, screen_h - 80))
        pos_x = max(10, (screen_w - win_w) // 2)
        pos_y = max(10, (screen_h - win_h) // 2)
        self.root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        self.root.minsize(1020, 600)
        self.root.configure(bg=THEME["bg_root"])

        self.setup_ttk_styles()
        self.build_ui()

        # Keyboard shortcut: F5 to run simulation
        self.root.bind("<F5>", lambda e: self.run_simulation())

        # Load Industrial Presets by default on launch so the user has immediate data
        self.load_presets()

        # Initial Empty Chart State
        self.update_gantt([])

    def setup_ttk_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=THEME["bg_root"])
        style.configure("Card.TFrame", background=THEME["bg_card"])

        style.configure(
            "TLabel",
            background=THEME["bg_root"],
            foreground=THEME["text_primary"],
            font=(FONT_FAMILY, 9)
        )
        style.configure(
            "Card.TLabel",
            background=THEME["bg_card"],
            foreground=THEME["text_primary"],
            font=(FONT_FAMILY, 9)
        )

        # Treeview styling (Tables)
        style.configure(
            "Treeview",
            background=THEME["bg_card_inner"],
            foreground=THEME["text_primary"],
            fieldbackground=THEME["bg_card_inner"],
            rowheight=25,
            font=(FONT_FAMILY, 9),
            borderwidth=0
        )
        style.map(
            "Treeview",
            background=[("selected", THEME["accent_blue"])],
            foreground=[("selected", "#ffffff")]
        )
        style.configure(
            "Treeview.Heading",
            background="#222f4c",
            foreground="#ffffff",
            relief="flat",
            font=(FONT_FAMILY, 8, "bold"),
            padding=4
        )
        style.map("Treeview.Heading", background=[("active", "#2d3e64")])

        # Combobox styling
        style.configure(
            "TCombobox",
            fieldbackground=THEME["input_bg"],
            background=THEME["border"],
            foreground="#ffffff",
            arrowcolor="#ffffff",
            padding=4
        )

    def build_ui(self):
        # ------------------- Top Header Bar -------------------
        header = tk.Frame(self.root, bg=THEME["bg_card"], height=56)
        header.pack(fill="x", side="top")

        separator = tk.Frame(self.root, bg=THEME["border"], height=1)
        separator.pack(fill="x", side="top")

        header_content = tk.Frame(header, bg=THEME["bg_card"], padx=18, pady=8)
        header_content.pack(fill="x")

        # Left brand & titles
        title_box = tk.Frame(header_content, bg=THEME["bg_card"])
        title_box.pack(side="left")

        top_line = tk.Frame(title_box, bg=THEME["bg_card"])
        top_line.pack(anchor="w")

        brand_badge = tk.Label(
            top_line,
            text="🏭 INDUSTRIAL OS",
            bg="#1e3a8a",
            fg="#93c5fd",
            font=(FONT_FAMILY, 8, "bold"),
            padx=6,
            pady=1
        )
        brand_badge.pack(side="left", padx=(0, 8))

        title_lbl = tk.Label(
            top_line,
            text="Process Management Simulator",
            bg=THEME["bg_card"],
            fg=THEME["text_primary"],
            font=(FONT_FAMILY, 13, "bold")
        )
        title_lbl.pack(side="left")

        subtitle_lbl = tk.Label(
            title_box,
            text="Multi-Algorithm CPU Scheduling & Resource Execution Analytics",
            bg=THEME["bg_card"],
            fg=THEME["text_secondary"],
            font=(FONT_FAMILY, 8)
        )
        subtitle_lbl.pack(anchor="w")

        # Right status indicator & Header Run Shortcut Button
        right_header = tk.Frame(header_content, bg=THEME["bg_card"])
        right_header.pack(side="right")

        self.status_pill = tk.Label(
            right_header,
            text="● Engine Ready",
            bg="#064e3b",
            fg="#6ee7b7",
            font=(FONT_FAMILY, 8, "bold"),
            padx=10,
            pady=4
        )
        self.status_pill.pack(side="right", padx=(8, 0))

        # Always-visible header Run button
        btn_header_run = create_btn(
            right_header,
            text="▶ Run Simulation (F5)",
            command=self.run_simulation,
            bg=THEME["accent_green"],
            hover_bg=THEME["accent_green_hover"],
            font_size=9,
            pad_x=12,
            pad_y=4
        )
        btn_header_run.pack(side="right")

        # ------------------- Main Dashboard Layout -------------------
        main_container = tk.Frame(self.root, bg=THEME["bg_root"], padx=14, pady=10)
        main_container.pack(fill="both", expand=True)

        # Left Column (fixed width ~430px)
        left_panel = tk.Frame(main_container, bg=THEME["bg_root"], width=430)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        # Right Column (Analytics & Gantt Canvas)
        right_panel = tk.Frame(main_container, bg=THEME["bg_root"])
        right_panel.pack(side="right", fill="both", expand=True)

        self.build_left_panel(left_panel)
        self.build_right_panel(right_panel)

    def build_left_panel(self, parent):
        # ========================================================
        # 1. ALGORITHM & SIMULATION CONTROLS CARD (PROMINENT AT TOP)
        # ========================================================
        control_card = tk.Frame(
            parent,
            bg=THEME["bg_card"],
            highlightbackground=THEME["border"],
            highlightthickness=1,
            padx=14,
            pady=10
        )
        control_card.pack(fill="x", pady=(0, 8))

        ctrl_head = tk.Frame(control_card, bg=THEME["bg_card"])
        ctrl_head.pack(fill="x", pady=(0, 6))

        tk.Label(
            ctrl_head,
            text="⚙️ Scheduler Configuration",
            bg=THEME["bg_card"],
            fg=THEME["accent_amber"],
            font=(FONT_FAMILY, 10, "bold")
        ).pack(side="left")

        ctrl_grid = tk.Frame(control_card, bg=THEME["bg_card"])
        ctrl_grid.pack(fill="x")

        # Algorithm picker
        algo_box = tk.Frame(ctrl_grid, bg=THEME["bg_card"])
        algo_box.pack(side="left", fill="x", expand=True, padx=(0, 8))

        tk.Label(
            algo_box,
            text="Algorithm",
            bg=THEME["bg_card"],
            fg=THEME["text_secondary"],
            font=(FONT_FAMILY, 8, "bold")
        ).pack(anchor="w")

        self.algorithm = ttk.Combobox(
            algo_box,
            values=["FCFS", "SJF", "Priority", "Round Robin"],
            state="readonly",
            font=(FONT_FAMILY, 9)
        )
        self.algorithm.set("FCFS")
        self.algorithm.pack(fill="x", pady=(2, 0))
        self.algorithm.bind("<<ComboboxSelected>>", self.on_algo_changed)

        # Quantum Entry
        self.quantum_box = tk.Frame(ctrl_grid, bg=THEME["bg_card"])
        self.quantum_box.pack(side="right")

        tk.Label(
            self.quantum_box,
            text="Quantum (ms)",
            bg=THEME["bg_card"],
            fg=THEME["text_secondary"],
            font=(FONT_FAMILY, 8, "bold")
        ).pack(anchor="w")

        self.quantum_entry = tk.Entry(
            self.quantum_box,
            bg=THEME["input_bg"],
            fg=THEME["input_fg"],
            insertbackground="#ffffff",
            width=8,
            relief="flat",
            highlightbackground=THEME["border"],
            highlightcolor=THEME["accent_blue"],
            highlightthickness=1,
            font=(FONT_FAMILY, 9),
            bd=3
        )
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.pack(fill="x", pady=(2, 0))
        self.quantum_entry.config(state="disabled")

        # Prominent Simulation Action Button
        self.btn_run = create_btn(
            control_card,
            text="▶ RUN SIMULATION",
            command=self.run_simulation,
            bg=THEME["accent_green"],
            hover_bg=THEME["accent_green_hover"],
            font_size=10,
            pad_y=7
        )
        self.btn_run.pack(fill="x", pady=(8, 2))

        # ========================================================
        # 2. ADD PROCESS CARD (COMPACT)
        # ========================================================
        input_card = tk.Frame(
            parent,
            bg=THEME["bg_card"],
            highlightbackground=THEME["border"],
            highlightthickness=1,
            padx=14,
            pady=10
        )
        input_card.pack(fill="x", pady=(0, 8))

        header_lbl = tk.Label(
            input_card,
            text="➕ Register Process",
            bg=THEME["bg_card"],
            fg=THEME["accent_cyan"],
            font=(FONT_FAMILY, 10, "bold")
        )
        header_lbl.pack(anchor="w", pady=(0, 6))

        grid_frame = tk.Frame(input_card, bg=THEME["bg_card"])
        grid_frame.pack(fill="x")

        self.inputs = {}
        fields = [
            ("PID", "pid", "P6"),
            ("Arrival", "arrival", "0"),
            ("Burst", "burst", "4"),
            ("Priority", "priority", "1")
        ]

        for idx, (label_text, key, placeholder) in enumerate(fields):
            cell = tk.Frame(grid_frame, bg=THEME["bg_card"])
            cell.grid(row=0, column=idx, padx=3, pady=2, sticky="ew")
            grid_frame.columnconfigure(idx, weight=1)

            lbl = tk.Label(
                cell,
                text=label_text,
                bg=THEME["bg_card"],
                fg=THEME["text_secondary"],
                font=(FONT_FAMILY, 8, "bold")
            )
            lbl.pack(anchor="w")

            ent = tk.Entry(
                cell,
                bg=THEME["input_bg"],
                fg=THEME["input_fg"],
                insertbackground="#ffffff",
                relief="flat",
                highlightbackground=THEME["border"],
                highlightcolor=THEME["accent_cyan"],
                highlightthickness=1,
                font=(FONT_FAMILY, 9),
                bd=3
            )
            ent.insert(0, placeholder)
            ent.pack(fill="x", pady=(1, 0))
            self.inputs[key] = ent

        btn_add = create_btn(
            input_card,
            text="+ Add Process to Queue",
            command=self.add_process,
            bg=THEME["accent_cyan"],
            hover_bg="#0891b2",
            fg="#0f172a",
            font_size=9,
            pad_y=4
        )
        btn_add.pack(fill="x", pady=(8, 0))

        # ========================================================
        # 3. PROCESS QUEUE CARD (WITH FIXED HEIGHT TREEVIEW)
        # ========================================================
        queue_card = tk.Frame(
            parent,
            bg=THEME["bg_card"],
            highlightbackground=THEME["border"],
            highlightthickness=1,
            padx=14,
            pady=10
        )
        queue_card.pack(fill="both", expand=True)

        q_head = tk.Frame(queue_card, bg=THEME["bg_card"])
        q_head.pack(fill="x", pady=(0, 6))

        q_title = tk.Label(
            q_head,
            text="📋 Execution Queue",
            bg=THEME["bg_card"],
            fg=THEME["text_primary"],
            font=(FONT_FAMILY, 10, "bold")
        )
        q_title.pack(side="left")

        self.queue_count_lbl = tk.Label(
            q_head,
            text="0 tasks",
            bg="#1e293b",
            fg=THEME["text_secondary"],
            font=(FONT_FAMILY, 8, "bold"),
            padx=6,
            pady=1
        )
        self.queue_count_lbl.pack(side="right")

        tree_container = tk.Frame(queue_card, bg=THEME["bg_card_inner"])
        tree_container.pack(fill="both", expand=True)

        cols = ("PID", "Arrival", "Burst", "Priority")
        self.process_table = ttk.Treeview(
            tree_container,
            columns=cols,
            show="headings",
            selectmode="browse",
            height=6
        )
        col_widths = {"PID": 120, "Arrival": 75, "Burst": 75, "Priority": 75}
        for c in cols:
            self.process_table.heading(c, text=c)
            self.process_table.column(c, width=col_widths[c], anchor="center")

        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.process_table.yview)
        self.process_table.configure(yscrollcommand=scrollbar.set)

        self.process_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action bar under Queue
        btn_bar = tk.Frame(queue_card, bg=THEME["bg_card"])
        btn_bar.pack(fill="x", pady=(8, 0))

        btn_preset = create_btn(
            btn_bar,
            text="⚡ Load Preset",
            command=self.load_presets,
            bg="#334155",
            hover_bg="#475569",
            pad_x=8, pad_y=4, font_size=8
        )
        btn_preset.pack(side="left", padx=(0, 4))

        btn_delete = create_btn(
            btn_bar,
            text="🗑️ Delete",
            command=self.delete_selected,
            bg="#334155",
            hover_bg=THEME["accent_red"],
            pad_x=8, pad_y=4, font_size=8
        )
        btn_delete.pack(side="left", padx=4)

        btn_clear = create_btn(
            btn_bar,
            text="🧹 Clear All",
            command=self.clear_all,
            bg="#334155",
            hover_bg=THEME["accent_red"],
            pad_x=8, pad_y=4, font_size=8
        )
        btn_clear.pack(side="right")

    def build_right_panel(self, parent):
        # 1. Metric Stat Cards Row
        stats_frame = tk.Frame(parent, bg=THEME["bg_root"])
        stats_frame.pack(fill="x", pady=(0, 8))

        self.stat_cards = {}
        metrics = [
            ("Avg Waiting Time", "avg_waiting", "-- ms", THEME["accent_cyan"], "⏱️"),
            ("Avg Turnaround Time", "avg_turnaround", "-- ms", THEME["accent_purple"], "🔄"),
            ("Total Makespan", "makespan", "-- ms", THEME["accent_amber"], "🏁"),
            ("CPU Efficiency", "efficiency", "-- %", THEME["accent_green"], "⚡")
        ]

        for title, key, default_val, accent_color, icon in metrics:
            card = tk.Frame(
                stats_frame,
                bg=THEME["bg_card"],
                highlightbackground=THEME["border"],
                highlightthickness=1,
                padx=12,
                pady=8
            )
            card.pack(side="left", fill="both", expand=True, padx=3)

            top_row = tk.Frame(card, bg=THEME["bg_card"])
            top_row.pack(fill="x")

            lbl_title = tk.Label(
                top_row,
                text=title,
                bg=THEME["bg_card"],
                fg=THEME["text_secondary"],
                font=(FONT_FAMILY, 8, "bold")
            )
            lbl_title.pack(side="left")

            lbl_icon = tk.Label(
                top_row,
                text=icon,
                bg=THEME["bg_card"],
                font=(FONT_FAMILY, 9)
            )
            lbl_icon.pack(side="right")

            lbl_val = tk.Label(
                card,
                text=default_val,
                bg=THEME["bg_card"],
                fg=accent_color,
                font=(FONT_FAMILY, 14, "bold")
            )
            lbl_val.pack(anchor="w", pady=(2, 0))

            self.stat_cards[key] = lbl_val

        # 2. Embedded Gantt Chart Card
        chart_card = tk.Frame(
            parent,
            bg=THEME["bg_card"],
            highlightbackground=THEME["border"],
            highlightthickness=1,
            padx=14,
            pady=8
        )
        chart_card.pack(fill="x", pady=(0, 8))

        chart_head = tk.Frame(chart_card, bg=THEME["bg_card"])
        chart_head.pack(fill="x", pady=(0, 4))

        chart_title = tk.Label(
            chart_head,
            text="📊 Real-Time CPU Execution Timeline (Gantt Chart)",
            bg=THEME["bg_card"],
            fg=THEME["text_primary"],
            font=(FONT_FAMILY, 10, "bold")
        )
        chart_title.pack(side="left")

        # Matplotlib Embedded Canvas
        self.figure = Figure(figsize=(7.5, 2.5), dpi=100)
        self.figure.patch.set_facecolor(THEME["bg_card"])
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_card)
        self.canvas.get_tk_widget().pack(fill="x", expand=True)

        # 3. Results Table Card
        results_card = tk.Frame(
            parent,
            bg=THEME["bg_card"],
            highlightbackground=THEME["border"],
            highlightthickness=1,
            padx=14,
            pady=8
        )
        results_card.pack(fill="both", expand=True)

        res_head = tk.Frame(results_card, bg=THEME["bg_card"])
        res_head.pack(fill="x", pady=(0, 4))

        res_title = tk.Label(
            res_head,
            text="📑 Process Performance Metrics",
            bg=THEME["bg_card"],
            fg=THEME["text_primary"],
            font=(FONT_FAMILY, 10, "bold")
        )
        res_title.pack(side="left")

        res_table_container = tk.Frame(results_card, bg=THEME["bg_card_inner"])
        res_table_container.pack(fill="both", expand=True)

        res_cols = ("PID", "Arrival", "Burst", "Priority", "Completion", "Turnaround", "Waiting")
        self.result_table = ttk.Treeview(
            res_table_container,
            columns=res_cols,
            show="headings",
            selectmode="browse",
            height=6
        )

        col_configs = {
            "PID": 110,
            "Arrival": 85,
            "Burst": 85,
            "Priority": 85,
            "Completion": 105,
            "Turnaround": 105,
            "Waiting": 95
        }
        for c in res_cols:
            self.result_table.heading(c, text=c)
            self.result_table.column(c, width=col_configs[c], anchor="center")

        res_scrollbar = ttk.Scrollbar(
            res_table_container, orient="vertical", command=self.result_table.yview
        )
        self.result_table.configure(yscrollcommand=res_scrollbar.set)

        self.result_table.pack(side="left", fill="both", expand=True)
        res_scrollbar.pack(side="right", fill="y")

    # ---------------------------------------------------------
    # UI Event Handlers
    # ---------------------------------------------------------
    def on_algo_changed(self, event=None):
        if self.algorithm.get() == "Round Robin":
            self.quantum_entry.config(state="normal")
        else:
            self.quantum_entry.config(state="disabled")

    def add_process(self):
        try:
            pid = self.inputs["pid"].get().strip()
            arr_val = self.inputs["arrival"].get().strip()
            bst_val = self.inputs["burst"].get().strip()
            pri_val = self.inputs["priority"].get().strip()

            if not pid:
                raise ValueError("Please provide a Process ID.")

            arrival = int(arr_val)
            burst = int(bst_val)
            priority = int(pri_val)

            if arrival < 0:
                raise ValueError("Arrival time cannot be negative.")
            if burst <= 0:
                raise ValueError("Burst time must be greater than zero.")
            if priority < 0:
                raise ValueError("Priority cannot be negative.")

            for row in self.process_table.get_children():
                if self.process_table.item(row)["values"][0] == pid:
                    raise ValueError(f"Process ID '{pid}' already exists.")

            self.process_table.insert(
                "", "end",
                values=(pid, arrival, burst, priority)
            )

            # Suggest next PID
            curr_count = len(self.process_table.get_children())
            self.inputs["pid"].delete(0, tk.END)
            self.inputs["pid"].insert(0, f"P{curr_count + 1}")

            self.update_queue_count()

        except ValueError as err:
            messagebox.showerror("Input Validation Error", str(err))

    def update_queue_count(self):
        count = len(self.process_table.get_children())
        self.queue_count_lbl.config(text=f"{count} tasks")

    def load_presets(self):
        self.clear_all()
        industrial_tasks = [
            ("ROBOT_ARM", 0, 5, 2),
            ("TEMP_VALVE", 1, 3, 1),
            ("CONVEYOR_BELT", 2, 7, 3),
            ("OPTICAL_QC", 4, 4, 1),
            ("PACKAGING_UNIT", 6, 2, 2)
        ]
        for pid, arrival, burst, priority in industrial_tasks:
            self.process_table.insert(
                "", "end",
                values=(pid, arrival, burst, priority)
            )
        self.update_queue_count()
        self.status_pill.config(
            text="● Loaded Presets",
            bg="#1e3a8a",
            fg="#93c5fd"
        )

    def delete_selected(self):
        selected = self.process_table.selection()
        if not selected:
            messagebox.showinfo("Selection Required", "Please select a process row to delete.")
            return
        for item in selected:
            self.process_table.delete(item)
        self.update_queue_count()

    def clear_all(self):
        for row in self.process_table.get_children():
            self.process_table.delete(row)
        for row in self.result_table.get_children():
            self.result_table.delete(row)

        self.update_queue_count()
        self.update_gantt([])
        self.stat_cards["avg_waiting"].config(text="-- ms")
        self.stat_cards["avg_turnaround"].config(text="-- ms")
        self.stat_cards["makespan"].config(text="-- ms")
        self.stat_cards["efficiency"].config(text="-- %")

        self.status_pill.config(
            text="● Queue Cleared",
            bg="#374151",
            fg="#9ca3af"
        )

    def update_gantt(self, timeline, title="CPU Execution Timeline"):
        plot_gantt_chart(self.ax, timeline, title=title, dark_mode=True)
        self.figure.tight_layout()
        self.canvas.draw()

    def run_simulation(self):
        try:
            processes = []
            process_meta = {}

            for row in self.process_table.get_children():
                values = self.process_table.item(row)["values"]
                pid = str(values[0])
                arr = int(values[1])
                bst = int(values[2])
                pri = int(values[3])

                processes.append({
                    "pid": pid,
                    "arrival": arr,
                    "burst": bst,
                    "priority": pri
                })
                process_meta[pid] = {"arrival": arr, "burst": bst, "priority": pri}

            if not processes:
                messagebox.showwarning(
                    "Empty Queue", "Please add at least one process to run the simulation."
                )
                return

            choice = self.algorithm.get()

            if choice == "FCFS":
                result = fcfs(processes)
            elif choice == "SJF":
                result = sjf(processes)
            elif choice == "Priority":
                result = priority_scheduling(processes)
            elif choice == "Round Robin":
                quantum_val = int(self.quantum_entry.get().strip())
                if quantum_val <= 0:
                    raise ValueError("Time quantum must be a positive integer.")
                result = round_robin(processes, quantum_val)
            else:
                raise ValueError("Unsupported algorithm selected.")

            # Clear previous results
            for row in self.result_table.get_children():
                self.result_table.delete(row)

            # Insert updated result rows
            for p in result["results"]:
                pid = p["pid"]
                meta = process_meta.get(pid, {"arrival": "-", "burst": "-", "priority": "-"})
                self.result_table.insert(
                    "", "end",
                    values=(
                        pid,
                        meta["arrival"],
                        meta["burst"],
                        meta["priority"],
                        p["completion"],
                        p["turnaround"],
                        p["waiting"]
                    )
                )

            # Calculate makespan & CPU efficiency
            total_burst = sum(p["burst"] for p in processes)
            timeline = result.get("timeline", [])
            makespan = timeline[-1]["end"] if timeline else total_burst
            efficiency = round((total_burst / makespan) * 100, 1) if makespan > 0 else 100.0

            # Update Stat Cards
            self.stat_cards["avg_waiting"].config(
                text=f"{round(result['average_waiting'], 2)} ms"
            )
            self.stat_cards["avg_turnaround"].config(
                text=f"{round(result['average_turnaround'], 2)} ms"
            )
            self.stat_cards["makespan"].config(
                text=f"{makespan} ms"
            )
            self.stat_cards["efficiency"].config(
                text=f"{efficiency} %"
            )

            # Update embedded Gantt Chart
            chart_title = f"{choice} Execution Timeline"
            if choice == "Round Robin":
                chart_title += f" (Quantum = {self.quantum_entry.get()} ms)"
            self.update_gantt(timeline, title=chart_title)

            # Status pill update
            self.status_pill.config(
                text=f"● Executed {choice}",
                bg="#065f46",
                fg="#34d399"
            )

        except Exception as error:
            messagebox.showerror("Simulation Execution Error", str(error))


if __name__ == "__main__":
    app_root = tk.Tk()
    app = IndustrialSimulatorApp(app_root)
    app_root.mainloop()
