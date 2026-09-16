import tkinter as tk

# =========================================================
# DFS VISUALIZER - SCHOOL TO HOME
# ========================================================

root = tk.Tk()
root.title("DFS Visualizer - School to Home")
root.geometry("950x650")
root.resizable(False, False)

# -----------------------------
# GRAPH
# -----------------------------

graph = {
    "School": ["A", "B", "C"],
    "A": ["D"],
    "B": ["E"],
    "C": ["F"],
    "D": [],          # Dead End
    "E": ["Home"],    # Correct Path
    "F": [],          # Dead End
    "Home": []
}

# Node positions
positions = {
    "School": (100, 250),

    "A": (300, 100),
    "B": (300, 250),
    "C": (300, 400),

    "D": (520, 100),
    "E": (520, 250),
    "F": (520, 400),

    "Home": (760, 250)
}

# -----------------------------
# VARIABLES
# -----------------------------

steps = []
current_step = 0
paused = False
running = False
found_path = []

# -----------------------------
# TITLE
# -----------------------------

title = tk.Label(
    root,
    text="Depth-First Search (DFS)",
    font=("Arial", 24, "bold")
)

title.pack(pady=(15, 0))

subtitle = tk.Label(
    root,
    text="DFS explores one path deeply before backtracking.",
    font=("Arial", 12)
)

subtitle.pack(pady=5)

# -----------------------------
# CANVAS
# -----------------------------

canvas = tk.Canvas(
    root,
    width=900,
    height=430,
    bg="white",
    highlightthickness=1,
    highlightbackground="#cccccc"
)

canvas.pack(pady=10)

# -----------------------------
# DRAW ARROW
# -----------------------------


def draw_connection(start, end):

    x1, y1 = positions[start]
    x2, y2 = positions[end]

    canvas.create_line(
        x1,
        y1,
        x2,
        y2,
        width=3,
        fill="#bbbbbb",
        arrow=tk.LAST,
        arrowshape=(12, 15, 5)
    )


# -----------------------------
# DRAW NODE
# -----------------------------


def draw_node(name, color="#e8e8e8"):

    x, y = positions[name]

    radius = 38

    canvas.create_oval(
        x - radius,
        y - radius,
        x + radius,
        y + radius,
        fill=color,
        outline="#333333",
        width=2,
        tags=f"node_{name}"
    )

    canvas.create_text(
        x,
        y,
        text=name,
        font=("Arial", 11, "bold"),
        tags=f"node_{name}"
    )


# -----------------------------
# DRAW GRAPH
# -----------------------------


def draw_graph():

    canvas.delete("all")

    # Connections
    draw_connection("School", "A")
    draw_connection("School", "B")
    draw_connection("School", "C")

    draw_connection("A", "D")
    draw_connection("B", "E")
    draw_connection("C", "F")

    draw_connection("E", "Home")

    # Nodes
    for node in positions:

        if node == "School":
            draw_node(node, "#90EE90")

        elif node == "Home":
            draw_node(node, "#FF9999")

        else:
            draw_node(node)

    # Labels
    canvas.create_text(
        100,
        320,
        text="START",
        font=("Arial", 10, "bold"),
        fill="green"
    )

    canvas.create_text(
        760,
        320,
        text="GOAL",
        font=("Arial", 10, "bold"),
        fill="red"
    )


# -----------------------------
# CHANGE NODE COLOR
# -----------------------------


def change_node_color(node, color):

    canvas.itemconfig(
        f"node_{node}",
        fill=color
    )


# -----------------------------
# CREATE DFS STEPS
# -----------------------------


def generate_dfs_steps():

    global steps
    global found_path

    steps = []
    found_path = []

    visited = set()

    def dfs(node, path):

        visited.add(node)

        steps.append(
            ("visit", node, list(path))
        )

        if node == "Home":

            found_path.extend(path)

            steps.append(
                ("goal", node, list(path))
            )

            return True

        for neighbour in graph[node]:

            if neighbour not in visited:

                if dfs(
                    neighbour,
                    path + [neighbour]
                ):
                    return True

        # Dead end / backtrack
        if node != "School":

            steps.append(
                ("backtrack", node, list(path))
            )

        return False

    dfs("School", ["School"])


# -----------------------------
# START DFS
# -----------------------------


def start_dfs():

    global current_step
    global paused
    global running

    if running:
        return

    draw_graph()

    generate_dfs_steps()

    current_step = 0
    paused = False
    running = True

    start_button.config(
        state="disabled"
    )

    pause_button.config(
        state="normal",
        text="Pause"
    )

    status_label.config(
        text="DFS Search Started...",
        fg="#0066cc"
    )

    process_step()


# -----------------------------
# PROCESS ANIMATION
# -----------------------------


def process_step():

    global current_step
    global running

    if not running:
        return

    if paused:
        return

    if current_step >= len(steps):

        running = False

        start_button.config(
            state="normal"
        )

        pause_button.config(
            state="disabled"
        )

        return

    action, node, path = steps[current_step]

    # VISITING NODE
    if action == "visit":

        if node != "School" and node != "Home":
            change_node_color(
                node,
                "#87CEFA"
            )

        status_label.config(
            text=f"Visiting: {node}",
            fg="#0066cc"
        )

        stack_label.config(
            text="Current Path: "
            + " → ".join(path)
        )

    # BACKTRACK
    elif action == "backtrack":

        change_node_color(
            node,
            "#ffb3b3"
        )

        status_label.config(
            text=f"Dead End at {node} → Backtracking...",
            fg="#cc6600"
        )

    # GOAL FOUND
    elif action == "goal":

        change_node_color(
            "Home",
            "#66ff66"
        )

        status_label.config(
            text="Home Found! DFS Search Complete.",
            fg="green"
        )

        stack_label.config(
            text="Path Found: "
            + " → ".join(path)
        )

        show_final_path(path)

    current_step += 1

    root.after(
        900,
        process_step
    )


# -----------------------------
# SHOW FINAL PATH
# -----------------------------


def show_final_path(path):

    for i in range(len(path) - 1):

        start = path[i]
        end = path[i + 1]

        x1, y1 = positions[start]
        x2, y2 = positions[end]

        canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            width=6,
            fill="#00aa00",
            arrow=tk.LAST
        )

    # Redraw path nodes
    for node in path:

        if node == "School":
            draw_node(node, "#66ff66")

        elif node == "Home":
            draw_node(node, "#66ff66")

        else:
            draw_node(node, "#ffff66")


# -----------------------------
# PAUSE / RESUME
# -----------------------------


def pause_resume():

    global paused

    if not running:
        return

    if paused:

        paused = False

        pause_button.config(
            text="Pause"
        )

        status_label.config(
            text="DFS Search Resumed...",
            fg="#0066cc"
        )

        process_step()

    else:

        paused = True

        pause_button.config(
            text="Resume"
        )

        status_label.config(
            text="DFS Search Paused",
            fg="#cc6600"
        )


# -----------------------------
# RESET
# -----------------------------


def reset():

    global running
    global paused
    global current_step

    running = False
    paused = False
    current_step = 0

    draw_graph()

    status_label.config(
        text="Click 'Start DFS' to begin",
        fg="black"
    )

    stack_label.config(
        text="Current Path: -"
    )

    start_button.config(
        state="normal"
    )

    pause_button.config(
        text="Pause",
        state="disabled"
    )


# -----------------------------
# INFORMATION
# -----------------------------

status_label = tk.Label(
    root,
    text="Click 'Start DFS' to begin",
    font=("Arial", 13, "bold")
)

status_label.pack()

stack_label = tk.Label(
    root,
    text="Current Path: -",
    font=("Arial", 11)
)

stack_label.pack(pady=5)

# -----------------------------
# BUTTONS
# -----------------------------

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(
    button_frame,
    text="Start DFS",
    command=start_dfs,
    width=13,
    font=("Arial", 11, "bold")
)

start_button.grid(
    row=0,
    column=0,
    padx=10
)

pause_button = tk.Button(
    button_frame,
    text="Pause",
    command=pause_resume,
    width=13,
    state="disabled",
    font=("Arial", 11, "bold")
)

pause_button.grid(
    row=0,
    column=1,
    padx=10
)

reset_button = tk.Button(
    button_frame,
    text="Reset",
    command=reset,
    width=13,
    font=("Arial", 11, "bold")
)

reset_button.grid(
    row=0,
    column=2,
    padx=10
)

# -----------------------------
# START
# -----------------------------

draw_graph()

root.mainloop()
