import tkinter as tk
from tkinter import messagebox
from collections import deque


class GraphSearchVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Search Visualizer")
        self.root.geometry("1100x700")
        self.root.configure(bg="#eef2f7")

        # ----------------------------
        # Graph
        # -----------------------------
        self.graph = {
            "Classroom": ["A", "B"],
            "A": ["Classroom", "C"],
            "B": ["Classroom", "D"],
            "C": ["A", "Library"],
            "D": ["B", "Library"],
            "Library": ["C", "D"]
        }

        # Node positions
        self.pos = {
            "Classroom": (250, 100),
            "A": (120, 270),
            "B": (380, 270),
            "C": (120, 450),
            "D": (380, 450),
            "Library": (250, 600)
        }

        self.radius = 42

        # Search variables
        self.queue = deque()
        self.visited = set()
        self.parent = {}
        self.path = []

        self.current = None
        self.running = False
        self.paused = False
        self.step = 0

        self.create_ui()
        self.draw_graph()

    # ==================================================
    # UI
    # ==================================================

    def create_ui(self):

        # Header
        header = tk.Frame(
            self.root,
            bg="#17202a",
            height=85
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="Graph Search",
            font=("Segoe UI", 27, "bold"),
            bg="#17202a",
            fg="white"
        ).pack(pady=(12, 0))

        tk.Label(
            header,
            text="Finding a path from Classroom to Library",
            font=("Segoe UI", 11),
            bg="#17202a",
            fg="#d5d8dc"
        ).pack()

        # Main area
        main = tk.Frame(
            self.root,
            bg="#eef2f7"
        )
        main.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18
        )

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
            width=300,
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
            text="Search Information",
            font=("Segoe UI", 17, "bold"),
            bg="white",
            fg="#17202a"
        ).pack(pady=(20, 12))

        self.current_label = tk.Label(
            panel,
            text="Current Node\n—",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2874a6",
            justify="center"
        )
        self.current_label.pack(pady=10)

        self.step_label = tk.Label(
            panel,
            text="Step: 0",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#566573"
        )
        self.step_label.pack(pady=5)

        # Queue
        tk.Label(
            panel,
            text="Queue",
            font=("Segoe UI", 13, "bold"),
            bg="white"
        ).pack(pady=(20, 5))

        self.queue_label = tk.Label(
            panel,
            text="Empty",
            font=("Consolas", 11),
            bg="#f8f9f9",
            fg="#17202a",
            anchor="w",
            justify="left",
            padx=10,
            pady=10
        )
        self.queue_label.pack(
            fill="x",
            padx=18
        )

        # Visited
        tk.Label(
            panel,
            text="Visited Nodes",
            font=("Segoe UI", 13, "bold"),
            bg="white"
        ).pack(pady=(20, 5))

        self.visited_label = tk.Label(
            panel,
            text="None",
            font=("Consolas", 11),
            bg="#f8f9f9",
            fg="#17202a",
            anchor="w",
            justify="left",
            padx=10,
            pady=10
        )
        self.visited_label.pack(
            fill="x",
            padx=18
        )

        # Status
        self.status_label = tk.Label(
            panel,
            text="Ready to search",
            font=("Segoe UI", 11, "bold"),
            bg="#f8f9f9",
            fg="#566573",
            wraplength=250,
            justify="center",
            padx=10,
            pady=12
        )
        self.status_label.pack(
            fill="x",
            padx=18,
            pady=18
        )

        # Buttons
        buttons = tk.Frame(
            panel,
            bg="white"
        )
        buttons.pack(
            side="bottom",
            pady=25
        )

        self.start_button = tk.Button(
            buttons,
            text="▶ Start",
            command=self.start_search,
            width=10,
            font=("Segoe UI", 10, "bold"),
            bg="#3498db",
            fg="white",
            relief="flat",
            pady=7
        )
        self.start_button.grid(
            row=0,
            column=0,
            padx=4
        )

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
        self.pause_button.grid(
            row=0,
            column=1,
            padx=4
        )

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

    # ==================================================
    # DRAW GRAPH
    # ==================================================

    def draw_graph(self):

        self.canvas.delete("all")

        # Title
        self.canvas.create_text(
            500,
            35,
            text="Classroom → Library",
            font=("Segoe UI", 18, "bold"),
            fill="#17202a"
        )

        # ----------------------------------------------
        # Draw edges
        # ----------------------------------------------

        edges = [
            ("Classroom", "A"),
            ("Classroom", "B"),
            ("A", "C"),
            ("B", "D"),
            ("C", "Library"),
            ("D", "Library")
        ]

        for start, end in edges:

            x1, y1 = self.pos[start]
            x2, y2 = self.pos[end]

            color = "#bdc3c7"
            width = 3

            # Highlight final path
            if self.is_path_edge(start, end):
                color = "#27ae60"
                width = 7

            # Highlight current node connections
            elif (
                self.current == start
                or self.current == end
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

        # ----------------------------------------------
        # Draw nodes
        # ----------------------------------------------

        for node, (x, y) in self.pos.items():

            fill = "#f8f9f9"
            outline = "#566573"
            width = 3

            # Start
            if node == "Classroom":
                fill = "#d6eaf8"
                outline = "#2980b9"

            # Goal
            if node == "Library":
                fill = "#d5f5e3"
                outline = "#229954"

            # Visited
            if node in self.visited:
                fill = "#e8e8e8"

            # Current
            if node == self.current:
                fill = "#fdebd0"
                outline = "#e67e22"
                width = 5

            # Final path
            if node in self.path:
                fill = "#abebc6"
                outline = "#27ae60"
                width = 5

            self.canvas.create_oval(
                x - self.radius,
                y - self.radius,
                x + self.radius,
                y + self.radius,
                fill=fill,
                outline=outline,
                width=width
            )

            self.canvas.create_text(
                x,
                y,
                text=node,
                font=("Segoe UI", 12, "bold"),
                fill="#17202a"
            )

        # Legend
        self.canvas.create_text(
            100,
            665,
            text="Blue = Current",
            font=("Segoe UI", 10),
            fill="#2874a6"
        )

        self.canvas.create_text(
            300,
            665,
            text="Gray = Visited",
            font=("Segoe UI", 10),
            fill="#566573"
        )

        self.canvas.create_text(
            500,
            665,
            text="Green = Final Path",
            font=("Segoe UI", 10, "bold"),
            fill="#229954"
        )

    # ==================================================
    # START SEARCH
    # ==================================================

    def start_search(self):

        if self.running:
            return

        self.queue = deque()
        self.visited = set()
        self.parent = {}
        self.path = []

        self.current = None
        self.step = 0

        self.running = True
        self.paused = False

        self.start_button.config(
            state="disabled"
        )

        # Add starting node
        self.queue.append("Classroom")
        self.visited.add("Classroom")
        self.parent["Classroom"] = None

        self.update_information()
        self.draw_graph()

        self.status_label.config(
            text="Starting search from Classroom..."
        )

        self.root.after(
            1000,
            self.search_step
        )

    # ==================================================
    # SEARCH STEP
    # ==================================================

    def search_step(self):

        if not self.running:
            return

        if self.paused:
            self.root.after(
                200,
                self.search_step
            )
            return

        # No nodes left
        if not self.queue:

            self.running = False

            self.status_label.config(
                text="No path found."
            )

            self.start_button.config(
                state="normal"
            )

            return

        # Remove first node
        current = self.queue.popleft()

        self.current = current
        self.step += 1

        self.current_label.config(
            text=f"Current Node\n{current}"
        )

        self.step_label.config(
            text=f"Step: {self.step}"
        )

        # Goal found
        if current == "Library":

            self.build_path()

            self.running = False

            self.draw_graph()
            self.update_information()

            self.current_label.config(
                text="🎯 Goal Found!\nLibrary"
            )

            self.status_label.config(
                text=
                "Search complete!\n\n"
                f"Path:\n{' → '.join(self.path)}"
            )

            self.start_button.config(
                state="normal"
            )

            messagebox.showinfo(
                "Graph Search Complete",
                "Goal found!\n\n"
                f"Path:\n{' → '.join(self.path)}"
            )

            return

        # Explore neighbours
        for neighbour in self.graph[current]:

            if neighbour not in self.visited:

                self.visited.add(neighbour)

                self.parent[neighbour] = current

                self.queue.append(neighbour)

        self.update_information()
        self.draw_graph()

        self.status_label.config(
            text=
            f"Exploring {current}\n"
            "Checking connected nodes..."
        )

        self.root.after(
            1500,
            self.search_step
        )

    # ==================================================
    # BUILD FINAL PATH
    # ==================================================

    def build_path(self):

        path = []
        node = "Library"

        while node is not None:

            path.append(node)
            node = self.parent.get(node)

        path.reverse()

        self.path = path

    # ==================================================
    # CHECK PATH EDGE
    # ==================================================

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

    # ==================================================
    # UPDATE INFORMATION
    # ==================================================

    def update_information(self):

        # Queue
        if self.queue:
            queue_text = " → ".join(self.queue)
        else:
            queue_text = "Empty"

        self.queue_label.config(
            text=queue_text
        )

        # Visited
        if self.visited:
            visited_text = "\n".join(
                self.visited
            )
        else:
            visited_text = "None"

        self.visited_label.config(
            text=visited_text
        )

    # ==================================================
    # PAUSE / RESUME
    # ==================================================

    def pause_resume(self):

        if not self.running:
            return

        self.paused = not self.paused

        if self.paused:

            self.pause_button.config(
                text="▶ Resume"
            )

            self.status_label.config(
                text="Search Paused"
            )

        else:

            self.pause_button.config(
                text="⏸ Pause"
            )

            self.status_label.config(
                text="Search Resumed"
            )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.running = False
        self.paused = False

        self.queue = deque()
        self.visited = set()
        self.parent = {}
        self.path = []

        self.current = None
        self.step = 0

        self.start_button.config(
            state="normal"
        )

        self.pause_button.config(
            text="⏸ Pause"
        )

        self.current_label.config(
            text="Current Node\n—"
        )

        self.step_label.config(
            text="Step: 0"
        )

        self.queue_label.config(
            text="Empty"
        )

        self.visited_label.config(
            text="None"
        )

        self.status_label.config(
            text="Ready to search"
        )

        self.draw_graph()


# ======================================================
# RUN PROGRAM
# ======================================================

root = tk.Tk()
app = GraphSearchVisualizer(root)
root.mainloop()
