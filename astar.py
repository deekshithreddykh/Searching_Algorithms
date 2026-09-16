import tkinter as tk
from tkinter import messagebox
import heapq
import math


class AStarVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("A* Search Visualizer")
        self.root.geometry("1150x720")
        self.root.configure(bg="#eef2f7")

        self.running = False
        self.paused = False
        self.search_finished = False

        # --------------------------------------------------
        # Graph
        # --------------------------------------------------

        self.graph = {
            "College": [("A", 2), ("B", 4)],
            "A": [("College", 2), ("C", 2), ("D", 5)],
            "B": [("College", 4), ("D", 1), ("E", 3)],
            "C": [("A", 2), ("Home", 5)],
            "D": [("A", 5), ("B", 1), ("Home", 3)],
            "E": [("B", 3), ("Home", 2)],
            "Home": [("C", 5), ("D", 3), ("E", 2)]
        }

        # Heuristic: estimated remaining distance to Home
        self.h = {
            "College": 7,
            "A": 6,
            "B": 3,
            "C": 5,
            "D": 3,
            "E": 2,
            "Home": 0
        }

        # Positions on canvas
        self.pos = {
            "College": (110, 350),
            "A": (350, 180),
            "B": (350, 520),
            "C": (600, 150),
            "D": (600, 350),
            "E": (600, 550),
            "Home": (900, 350)
        }

        self.node_radius = 42

        # Search data
        self.g = {}
        self.f = {}
        self.parent = {}
        self.open_set = []
        self.closed = set()

        self.current_node = None
        self.path = []

        self.create_ui()
        self.reset()

    # ======================================================
    # USER INTERFACE
    # ======================================================

    def create_ui(self):

        # Header
        header = tk.Frame(self.root, bg="#17202a", height=85)
        header.pack(fill="x")

        tk.Label(
            header,
            text="A* Search",
            font=("Segoe UI", 27, "bold"),
            bg="#17202a",
            fg="white"
        ).pack(pady=(12, 0))

        tk.Label(
            header,
            text="Finding an efficient path from College to Home",
            font=("Segoe UI", 11),
            bg="#17202a",
            fg="#ccd1d1"
        ).pack()

        # Main area
        main = tk.Frame(self.root, bg="#eef2f7")
        main.pack(fill="both", expand=True, padx=18, pady=18)

        # Canvas
        self.canvas = tk.Canvas(
            main,
            bg="white",
            highlightthickness=1,
            highlightbackground="#d5d8dc"
        )
        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Right panel
        panel = tk.Frame(
            main,
            width=285,
            bg="white",
            highlightthickness=1,
            highlightbackground="#d5d8dc"
        )
        panel.pack(
            side="right",
            fill="y",
            padx=(15, 0)
        )
        panel.pack_propagate(False)

        tk.Label(
            panel,
            text="A* Search",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#17202a"
        ).pack(pady=(18, 3))

        tk.Label(
            panel,
            text="f(n) = g(n) + h(n)",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2874a6"
        ).pack(pady=5)

        # Current node
        self.current_label = tk.Label(
            panel,
            text="Current Node\n—",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#17202a",
            justify="center"
        )
        self.current_label.pack(pady=12)

        # Values
        self.values_label = tk.Label(
            panel,
            text="g(n) = —\nh(n) = —\nf(n) = —",
            font=("Segoe UI", 12),
            bg="white",
            fg="#34495e",
            justify="left"
        )
        self.values_label.pack(pady=8)

        # Decision
        self.decision_label = tk.Label(
            panel,
            text="Waiting to start...",
            font=("Segoe UI", 11, "bold"),
            bg="#f8f9f9",
            fg="#566573",
            wraplength=245,
            justify="center",
            padx=10,
            pady=12
        )
        self.decision_label.pack(
            fill="x",
            padx=15,
            pady=10
        )

        # Open list
        tk.Label(
            panel,
            text="Open List",
            font=("Segoe UI", 13, "bold"),
            bg="white"
        ).pack(pady=(10, 4))

        self.open_label = tk.Label(
            panel,
            text="—",
            font=("Consolas", 10),
            bg="#f8f9f9",
            fg="#17202a",
            justify="left",
            anchor="w",
            padx=10,
            pady=8
        )
        self.open_label.pack(
            fill="x",
            padx=15
        )

        # Step
        self.step_label = tk.Label(
            panel,
            text="Step: 0",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#566573"
        )
        self.step_label.pack(pady=12)

        # Buttons
        buttons = tk.Frame(panel, bg="white")
        buttons.pack(side="bottom", pady=20)

        self.start_button = tk.Button(
            buttons,
            text="▶ Start",
            command=self.start,
            width=10,
            font=("Segoe UI", 10, "bold"),
            bg="#3498db",
            fg="white",
            relief="flat",
            pady=7
        )
        self.start_button.grid(row=0, column=0, padx=4)

        self.pause_button = tk.Button(
            buttons,
            text="⏸ Pause",
            command=self.pause_resume,
            width=10,
            font=("Segoe UI", 10, "bold"),
            bg="#f39c12",
            fg="white",
            relief="flat",
            pady=7
        )
        self.pause_button.grid(row=0, column=1, padx=4)

        self.reset_button = tk.Button(
            buttons,
            text="↻ Reset",
            command=self.reset,
            width=22,
            font=("Segoe UI", 10, "bold"),
            bg="#566573",
            fg="white",
            relief="flat",
            pady=7
        )
        self.reset_button.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=7
        )

    # ======================================================
    # DRAW GRAPH
    # ======================================================

    def draw_graph(self):

        self.canvas.delete("all")

        # Title
        self.canvas.create_text(
            500,
            30,
            text="A* Route Search: College → Home",
            font=("Segoe UI", 17, "bold"),
            fill="#17202a"
        )

        # --------------------------------------------------
        # Draw roads
        # --------------------------------------------------

        drawn_edges = set()

        for start in self.graph:

            for end, cost in self.graph[start]:

                edge = tuple(sorted([start, end]))

                if edge in drawn_edges:
                    continue

                drawn_edges.add(edge)

                x1, y1 = self.pos[start]
                x2, y2 = self.pos[end]

                color = "#bdc3c7"
                width = 3

                # Final path
                if self.path and self.is_path_edge(start, end):
                    color = "#27ae60"
                    width = 7

                # Current explored edge
                elif (
                    self.current_node is not None
                    and (
                        start == self.current_node
                        or end == self.current_node
                    )
                ):
                    color = "#3498db"
                    width = 5

                self.canvas.create_line(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    width=width
                )

                # Cost label
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2

                self.canvas.create_rectangle(
                    mx - 18,
                    my - 13,
                    mx + 18,
                    my + 13,
                    fill="white",
                    outline=""
                )

                self.canvas.create_text(
                    mx,
                    my,
                    text=f"{cost} km",
                    font=("Segoe UI", 9, "bold"),
                    fill="#566573"
                )

        # --------------------------------------------------
        # Draw nodes
        # --------------------------------------------------

        for node, (x, y) in self.pos.items():

            # Default
            fill = "#f8f9f9"
            outline = "#566573"
            width = 3

            # Start
            if node == "College":
                fill = "#d6eaf8"
                outline = "#2980b9"

            # Goal
            elif node == "Home":
                fill = "#d5f5e3"
                outline = "#229954"

            # Closed nodes
            if node in self.closed:
                fill = "#d6dbdf"

            # Current
            if node == self.current_node:
                fill = "#fdebd0"
                outline = "#e67e22"
                width = 5

            # Final path
            if node in self.path:
                fill = "#abebc6"
                outline = "#27ae60"
                width = 5

            self.canvas.create_oval(
                x - self.node_radius,
                y - self.node_radius,
                x + self.node_radius,
                y + self.node_radius,
                fill=fill,
                outline=outline,
                width=width
            )

            self.canvas.create_text(
                x,
                y - 9,
                text=node,
                font=("Segoe UI", 13, "bold"),
                fill="#17202a"
            )

            self.canvas.create_text(
                x,
                y + 13,
                text=f"h={self.h[node]}",
                font=("Segoe UI", 10),
                fill="#566573"
            )

        # Legend
        self.canvas.create_text(
            90,
            650,
            text="Road number = actual travel cost",
            font=("Segoe UI", 10),
            fill="#566573"
        )

        self.canvas.create_text(
            370,
            650,
            text="h = estimated distance to Home",
            font=("Segoe UI", 10),
            fill="#566573"
        )

        self.canvas.create_text(
            700,
            650,
            text="Green = final path",
            font=("Segoe UI", 10, "bold"),
            fill="#229954"
        )

    # ======================================================
    # A* ALGORITHM
    # ======================================================

    def start(self):

        if self.running:
            return

        self.reset_search()

        self.running = True
        self.paused = False

        self.start_button.config(state="disabled")

        self.g["College"] = 0
        self.f["College"] = self.h["College"]

        heapq.heappush(
            self.open_set,
            (self.f["College"], "College")
        )

        self.run_algorithm()

    def run_algorithm(self):

        if not self.running:
            return

        if self.paused:
            self.root.after(200, self.run_algorithm)
            return

        if not self.open_set:
            self.running = False

            self.decision_label.config(
                text="No path found."
            )

            self.start_button.config(
                state="normal"
            )

            return

        # Get lowest f(n)
        current_f, current = heapq.heappop(
            self.open_set
        )

        # Ignore outdated heap entries
        if current in self.closed:
            self.root.after(
                500,
                self.run_algorithm
            )
            return

        self.current_node = current
        self.step_label.config(
            text=f"Step: {len(self.closed) + 1}"
        )

        current_g = self.g[current]
        current_h = self.h[current]
        current_f = current_g + current_h

        self.current_label.config(
            text=f"Current Node\n{current}"
        )

        self.values_label.config(
            text=
            f"g(n) = {current_g} km\n"
            f"h(n) = {current_h} km\n"
            f"f(n) = {current_f} km"
        )

        self.decision_label.config(
            text=
            f"A* selected {current}\n"
            f"because it has the lowest f(n)."
        )

        self.update_open_list()
        self.draw_graph()

        # Goal reached
        if current == "Home":
            self.closed.add(current)

            self.running = False

            self.build_final_path()

            self.current_node = "Home"

            self.draw_graph()

            self.current_label.config(
                text="🎯 Goal Reached!\nHome"
            )

            self.values_label.config(
                text=
                f"g(Home) = {self.g['Home']} km\n"
                f"h(Home) = 0 km\n"
                f"f(Home) = {self.g['Home']} km"
            )

            self.decision_label.config(
                text=
                "Final Path:\n\n"
                + " → ".join(self.path)
                + f"\n\nTotal Cost = {self.g['Home']} km"
            )

            self.start_button.config(
                state="normal"
            )

            messagebox.showinfo(
                "A* Search Complete",
                "Goal reached!\n\n"
                f"Path:\n{' → '.join(self.path)}\n\n"
                f"Total Cost: {self.g['Home']} km"
            )

            return

        # Mark current as visited
        self.closed.add(current)

        # Examine neighbours
        for neighbour, cost in self.graph[current]:

            if neighbour in self.closed:
                continue

            new_g = self.g[current] + cost

            # If this is a better path
            if (
                neighbour not in self.g
                or new_g < self.g[neighbour]
            ):

                self.g[neighbour] = new_g
                self.parent[neighbour] = current

                self.f[neighbour] = (
                    new_g + self.h[neighbour]
                )

                heapq.heappush(
                    self.open_set,
                    (
                        self.f[neighbour],
                        neighbour
                    )
                )

        self.update_open_list()

        self.draw_graph()

        self.root.after(
            1600,
            self.run_algorithm
        )

    # ======================================================
    # BUILD FINAL PATH
    # ======================================================

    def build_final_path(self):

        path = []
        current = "Home"

        while current is not None:

            path.append(current)

            if current == "College":
                break

            current = self.parent.get(current)

        path.reverse()

        self.path = path

    # ======================================================
    # CHECK FINAL PATH EDGE
    # ======================================================

    def is_path_edge(self, a, b):

        if len(self.path) < 2:
            return False

        for i in range(len(self.path) - 1):

            if (
                self.path[i] == a
                and self.path[i + 1] == b
            ):
                return True

            if (
                self.path[i] == b
                and self.path[i + 1] == a
            ):
                return True

        return False

    # ======================================================
    # OPEN LIST DISPLAY
    # ======================================================

    def update_open_list(self):

        items = []

        for node in self.g:

            if node in self.closed:
                continue

            if node in self.f:

                items.append(
                    (
                        self.f[node],
                        node,
                        self.g[node],
                        self.h[node]
                    )
                )

        items.sort()

        if not items:
            text = "Empty"

        else:
            text = ""

            for f_value, node, g_value, h_value in items:

                text += (
                    f"{node:<8} "
                    f"g={g_value} "
                    f"h={h_value} "
                    f"f={f_value}\n"
                )

        self.open_label.config(
            text=text
        )

    # ======================================================
    # PAUSE / RESUME
    # ======================================================

    def pause_resume(self):

        if not self.running:
            return

        self.paused = not self.paused

        if self.paused:
            self.pause_button.config(
                text="▶ Resume"
            )
        else:
            self.pause_button.config(
                text="⏸ Pause"
            )

    # ======================================================
    # RESET SEARCH
    # ======================================================

    def reset_search(self):

        self.g = {}
        self.f = {}
        self.parent = {}
        self.open_set = []
        self.closed = set()

        self.current_node = None
        self.path = []

        self.search_finished = False

        self.current_label.config(
            text="Current Node\n—"
        )

        self.values_label.config(
            text=
            "g(n) = —\n"
            "h(n) = —\n"
            "f(n) = —"
        )

        self.decision_label.config(
            text="Waiting to start..."
        )

        self.open_label.config(
            text="—"
        )

        self.step_label.config(
            text="Step: 0"
        )

    # ======================================================
    # FULL RESET
    # ======================================================

    def reset(self):

        self.running = False
        self.paused = False

        self.pause_button.config(
            text="⏸ Pause"
        )

        self.start_button.config(
            state="normal"
        )

        self.reset_search()
        self.draw_graph()


# ==========================================================
# RUN
# ==========================================================

root = tk.Tk()
app = AStarVisualizer(root)
root.mainloop()
