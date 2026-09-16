import tkinter as tk
from tkinter import messagebox
import time


# ----------------------------
# Greedy Best-First Search Demo
# -----------------------------

class GreedyBestFirstGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Greedy Best-First Search")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f4f6f8")

        self.running = False
        self.paused = False
        self.step = 0

        # Nodes and heuristic values
        self.nodes = {
            "School": {"h": None},
            "A": {"h": 6},
            "B": {"h": 3},
            "C": {"h": 2},
            "Home": {"h": 0}
        }

        # Graph
        self.graph = {
            "School": ["A", "B", "C"],
            "A": ["Home"],
            "B": ["Home"],
            "C": ["Home"],
            "Home": []
        }

        # Coordinates
        self.pos = {
            "School": (130, 320),
            "A": (380, 150),
            "B": (380, 320),
            "C": (380, 490),
            "Home": (750, 320)
        }

        self.create_ui()
        self.draw_graph()

    # -----------------------------
    # UI
    # -----------------------------
    def create_ui(self):

        title = tk.Label(
            self.root,
            text="Greedy Best-First Search",
            font=("Arial", 26, "bold"),
            bg="#f4f6f8",
            fg="#17202a"
        )
        title.pack(pady=(15, 3))

        subtitle = tk.Label(
            self.root,
            text="Choose the node that looks closest to the goal",
            font=("Arial", 13),
            bg="#f4f6f8",
            fg="#5d6d7e"
        )
        subtitle.pack()

        main = tk.Frame(self.root, bg="#f4f6f8")
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # Canvas
        self.canvas = tk.Canvas(
            main,
            width=700,
            height=540,
            bg="white",
            highlightthickness=1,
            highlightbackground="#d5d8dc"
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        # Right panel
        panel = tk.Frame(
            main,
            width=250,
            bg="white",
            highlightbackground="#d5d8dc",
            highlightthickness=1
        )
        panel.pack(side="right", fill="y", padx=(15, 0))
        panel.pack_propagate(False)

        tk.Label(
            panel,
            text="Search Information",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#17202a"
        ).pack(pady=(20, 15))

        self.current_label = tk.Label(
            panel,
            text="Current Node:\nSchool",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#2874a6"
        )
        self.current_label.pack(pady=10)

        self.h_label = tk.Label(
            panel,
            text="h(n): —",
            font=("Arial", 14),
            bg="white",
            fg="#17202a"
        )
        self.h_label.pack(pady=5)

        self.choice_label = tk.Label(
            panel,
            text="Next Choice:\n—",
            font=("Arial", 13),
            bg="white",
            fg="#229954",
            justify="center"
        )
        self.choice_label.pack(pady=15)

        tk.Label(
            panel,
            text="Heuristic Values",
            font=("Arial", 13, "bold"),
            bg="white"
        ).pack(pady=(10, 5))

        self.values_label = tk.Label(
            panel,
            text="A = 6\nB = 3\nC = 2\nHome = 0",
            font=("Arial", 12),
            bg="white",
            justify="left"
        )
        self.values_label.pack()

        self.step_label = tk.Label(
            panel,
            text="Step: 0",
            font=("Arial", 12, "bold"),
            bg="white"
        )
        self.step_label.pack(pady=15)

        # Buttons
        button_frame = tk.Frame(panel, bg="white")
        button_frame.pack(side="bottom", pady=25)

        self.start_button = tk.Button(
            button_frame,
            text="▶ Start",
            width=9,
            command=self.start_search,
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            relief="flat",
            padx=5,
            pady=5
        )
        self.start_button.grid(row=0, column=0, padx=4, pady=5)

        self.pause_button = tk.Button(
            button_frame,
            text="⏸ Pause",
            width=9,
            command=self.pause_resume,
            font=("Arial", 11, "bold"),
            bg="#f39c12",
            fg="white",
            relief="flat",
            padx=5,
            pady=5
        )
        self.pause_button.grid(row=0, column=1, padx=4, pady=5)

        self.reset_button = tk.Button(
            button_frame,
            text="↻ Reset",
            width=19,
            command=self.reset,
            font=("Arial", 11, "bold"),
            bg="#566573",
            fg="white",
            relief="flat",
            padx=5,
            pady=5
        )
        self.reset_button.grid(row=1, column=0, columnspan=2, pady=5)

    # -----------------------------
    # Draw Graph
    # -----------------------------
    def draw_graph(self, active=None, path=None):

        self.canvas.delete("all")

        # Draw edges
        edges = [
            ("School", "A"),
            ("School", "B"),
            ("School", "C"),
            ("A", "Home"),
            ("B", "Home"),
            ("C", "Home")
        ]

        for start, end in edges:
            x1, y1 = self.pos[start]
            x2, y2 = self.pos[end]

            color = "#2c3e50"
            width = 2

            if path and (start, end) in zip(path, path[1:]):
                color = "#27ae60"
                width = 5

            self.canvas.create_line(
                x1, y1,
                x2, y2,
                fill=color,
                width=width,
                arrow=tk.LAST,
                arrowshape=(12, 15, 6)
            )

        # Draw nodes
        for node, (x, y) in self.pos.items():

            if node == "School":
                fill = "#d6eaf8"
            elif node == "Home":
                fill = "#d5f5e3"
            else:
                fill = "#f8f9f9"

            if node == active:
                fill = "#f9e79f"

            radius = 48

            self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=fill,
                outline="#34495e",
                width=3
            )

            self.canvas.create_text(
                x,
                y - 8,
                text=node,
                font=("Arial", 15, "bold"),
                fill="#17202a"
            )

            if self.nodes[node]["h"] is not None:
                self.canvas.create_text(
                    x,
                    y + 18,
                    text=f"h(n) = {self.nodes[node]['h']}",
                    font=("Arial", 11),
                    fill="#566573"
                )

        # Heading inside canvas
        self.canvas.create_text(
            350,
            40,
            text="Finding Your Way Home",
            font=("Arial", 18, "bold"),
            fill="#17202a"
        )

    # -----------------------------
    # Start Search
    # -----------------------------
    def start_search(self):

        if self.running:
            return

        self.running = True
        self.paused = False
        self.step = 0

        self.start_button.config(state="disabled")

        self.search_steps = [
            ("School", ["A", "B", "C"], "C"),
            ("C", ["Home"], "Home")
        ]

        self.run_step()

    # -----------------------------
    # Search Steps
    # -----------------------------
    def run_step(self):

        if not self.running:
            return

        if self.paused:
            self.root.after(200, self.run_step)
            return

        if self.step >= len(self.search_steps):
            self.finish_search()
            return

        current, choices, selected = self.search_steps[self.step]

        # Highlight current node
        self.draw_graph(active=current)

        self.current_label.config(
            text=f"Current Node:\n{current}"
        )

        if self.nodes[current]["h"] is not None:
            self.h_label.config(
                text=f"h(n) = {self.nodes[current]['h']}"
            )
        else:
            self.h_label.config(text="h(n): Start")

        # Show choices
        if len(choices) > 1:

            values = []

            for node in choices:
                values.append(
                    f"{node}: h({node}) = {self.nodes[node]['h']}"
                )

            self.choice_label.config(
                text="Comparing:\n" + "\n".join(values)
            )

        else:
            self.choice_label.config(
                text=f"Next Choice:\n{selected}"
            )

        self.step_label.config(
            text=f"Step: {self.step + 1}"
        )

        # Move to selected node after delay
        self.root.after(
            1800,
            lambda: self.select_node(selected)
        )

    # -----------------------------
    # Select Node
    # -----------------------------
    def select_node(self, selected):

        if not self.running:
            return

        if self.paused:
            self.root.after(
                200,
                lambda: self.select_node(selected)
            )
            return

        self.draw_graph(active=selected)

        self.current_label.config(
            text=f"Selected:\n{selected}"
        )

        self.h_label.config(
            text=f"h({selected}) = {self.nodes[selected]['h']}"
        )

        self.choice_label.config(
            text=f"Greedy chooses:\n{selected}\n\n"
                 f"Smallest h(n)"
        )

        self.step += 1

        self.root.after(1800, self.run_step)

    # -----------------------------
    # Finish
    # -----------------------------
    def finish_search(self):

        self.running = False

        final_path = ["School", "C", "Home"]

        self.draw_graph(
            active="Home",
            path=final_path
        )

        self.current_label.config(
            text="Goal Reached!\nHome"
        )

        self.h_label.config(
            text="h(Home) = 0"
        )

        self.choice_label.config(
            text="Final Path:\n\nSchool → C → Home"
        )

        self.step_label.config(
            text="Search Complete"
        )

        self.start_button.config(
            state="normal"
        )

        messagebox.showinfo(
            "Search Complete",
            "Greedy Best-First Search reached Home!\n\n"
            "Final Path:\nSchool → C → Home"
        )

    # -----------------------------
    # Pause / Resume
    # -----------------------------
    def pause_resume(self):

        if not self.running:
            return

        self.paused = not self.paused

        if self.paused:
            self.pause_button.config(text="▶ Resume")
        else:
            self.pause_button.config(text="⏸ Pause")

    # -----------------------------
    # Reset
    # -----------------------------
    def reset(self):

        self.running = False
        self.paused = False
        self.step = 0

        self.pause_button.config(text="⏸ Pause")
        self.start_button.config(state="normal")

        self.current_label.config(
            text="Current Node:\nSchool"
        )

        self.h_label.config(text="h(n): —")

        self.choice_label.config(
            text="Next Choice:\n—"
        )

        self.step_label.config(
            text="Step: 0"
        )

        self.draw_graph()


# -----------------------------
# Run Program
# -----------------------------

root = tk.Tk()
app = GreedyBestFirstGUI(root)
root.mainloop()
