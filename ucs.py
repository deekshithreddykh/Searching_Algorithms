import tkinter as tk
import heapq

# ==========================================================
# UNIFORM COST SEARCH - VISUAL DEMO
# =========================================================

root = tk.Tk()
root.title("Uniform Cost Search - School to Home")
root.geometry("1100x750")
root.configure(bg="white")
root.resizable(False, False)

# ==========================================================
# GRAPH
# ==========================================================

graph = {
    "School": [("A", 20), ("B", 50), ("C", 30)],
    "A": [("Home", 40)],
    "B": [("Home", 10)],
    "C": [("Home", 20)],
    "Home": []
}

# Positions
pos = {
    "School": (120, 350),
    "A": (380, 150),
    "B": (380, 350),
    "C": (380, 550),
    "Home": (820, 350)
}

roads = [
    ("School", "A", 20),
    ("School", "B", 50),
    ("School", "C", 30),
    ("A", "Home", 40),
    ("B", "Home", 10),
    ("C", "Home", 20)
]

# ==========================================================
# VARIABLES
# ==========================================================

running = False
paused = False

car = None

exploration = []
explore_index = 0

final_path = []
final_cost = 0

# ==========================================================
# CANVAS
# ==========================================================

canvas = tk.Canvas(
    root,
    width=1050,
    height=580,
    bg="white",
    highlightthickness=0
)

canvas.pack(pady=10)

# ==========================================================
# DRAW ROADS
# ==========================================================

road_lines = {}


def draw_roads():

    for start, end, cost in roads:

        x1, y1 = pos[start]
        x2, y2 = pos[end]

        line = canvas.create_line(
            x1, y1,
            x2, y2,
            fill="#cbd5e1",
            width=8
        )

        road_lines[(start, end)] = line

        # Cost position
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        canvas.create_rectangle(
            mx - 35,
            my - 20,
            mx + 35,
            my + 20,
            fill="white",
            outline="#94a3b8",
            width=2
        )

        canvas.create_text(
            mx,
            my,
            text=f"₹{cost}",
            font=("Arial", 12, "bold"),
            fill="#111827"
        )


# ==========================================================
# DRAW NODES
# ==========================================================

def draw_nodes():

    for node, (x, y) in pos.items():

        if node == "School":
            fill = "#16a34a"
            text = "SCHOOL"

        elif node == "Home":
            fill = "#dc2626"
            text = "HOME"

        else:
            fill = "#e2e8f0"
            text = node

        canvas.create_oval(
            x - 50,
            y - 50,
            x + 50,
            y + 50,
            fill=fill,
            outline="#334155",
            width=3
        )

        canvas.create_text(
            x,
            y,
            text=text,
            font=("Arial", 12, "bold"),
            fill="white" if node in ["School", "Home"] else "#111827"
        )


# ==========================================================
# HIGHLIGHT ROAD
# ==========================================================

def highlight_road(a, b, color="#2563eb"):

    if (a, b) in road_lines:

        canvas.itemconfig(
            road_lines[(a, b)],
            fill=color,
            width=12
        )


def reset_roads():

    for line in road_lines.values():

        canvas.itemconfig(
            line,
            fill="#cbd5e1",
            width=8
        )


# ==========================================================
# UCS
# ==========================================================

def calculate_ucs():

    queue = [(0, "School", ["School"])]

    visited = set()

    steps = []

    while queue:

        cost, current, path = heapq.heappop(queue)

        if current in visited:
            continue

        visited.add(current)

        steps.append(
            ("visit", current, cost, path.copy())
        )

        if current == "Home":

            return steps, path, cost

        for next_node, route_cost in graph[current]:

            if next_node not in visited:

                new_cost = cost + route_cost

                new_path = path + [next_node]

                heapq.heappush(
                    queue,
                    (
                        new_cost,
                        next_node,
                        new_path
                    )
                )

                steps.append(
                    (
                        "add",
                        next_node,
                        new_cost,
                        new_path.copy()
                    )
                )

    return steps, None, None


# ==========================================================
# CREATE EXPLORATION
# ==========================================================

def start_ucs():

    global running
    global paused
    global exploration
    global explore_index
    global final_path
    global final_cost

    reset()

    exploration, final_path, final_cost = calculate_ucs()

    running = True
    paused = False
    explore_index = 0

    start_button.config(
        state="disabled"
    )

    pause_button.config(
        state="normal",
        text="Pause"
    )

    status.config(
        text="UCS is searching...",
        fg="#2563eb"
    )

    run_exploration()


# ==========================================================
# EXPLORE ROUTES
# ==========================================================

def run_exploration():

    global explore_index

    if not running:
        return

    if paused:

        root.after(
            200,
            run_exploration
        )

        return

    if explore_index >= len(exploration):

        show_final()

        return

    action, node, cost, path = exploration[explore_index]

    # ------------------------------------------
    # SHOW CURRENT PATH
    # ------------------------------------------

    if action == "visit":

        status.config(
            text=f"Checking {node} | Total Cost = ₹{cost}",
            fg="#2563eb"
        )

        route_label.config(
            text=" → ".join(path)
        )

        cost_label.config(
            text=f"Current Total: ₹{cost}"
        )

        # Highlight the route being checked
        reset_roads()

        for i in range(len(path) - 1):

            highlight_road(
                path[i],
                path[i + 1]
            )

        # Move car along this path
        move_car_on_path(
            path,
            0,
            lambda: continue_search()
        )

        return

    # ------------------------------------------
    # ADD TO PRIORITY QUEUE
    # ------------------------------------------

    if action == "add":

        status.config(
            text=f"Added {node} | Total Cost = ₹{cost}",
            fg="#7c3aed"
        )

        queue_label.config(
            text=f"Possible Path:\n{' → '.join(path)}\n\nCost: ₹{cost}"
        )

    explore_index += 1

    root.after(
        900,
        run_exploration
    )


# ==========================================================
# CONTINUE SEARCH
# ==========================================================

def continue_search():

    global explore_index

    explore_index += 1

    root.after(
        700,
        run_exploration
    )


# ==========================================================
# MOVE CAR
# ==========================================================

def move_car_on_path(path, index, callback):

    global car

    if paused:

        root.after(
            200,
            lambda: move_car_on_path(
                path,
                index,
                callback
            )
        )

        return

    if index >= len(path) - 1:

        callback()

        return

    start = path[index]
    end = path[index + 1]

    x1, y1 = pos[start]
    x2, y2 = pos[end]

    # Create car
    if car is None:

        car = canvas.create_oval(
            x1 - 14,
            y1 - 14,
            x1 + 14,
            y1 + 14,
            fill="#f59e0b",
            outline="#111827",
            width=2
        )

    move_steps = 25

    def animate(step):

        if paused:

            root.after(
                200,
                lambda: animate(step)
            )

            return

        if step > move_steps:

            move_car_on_path(
                path,
                index + 1,
                callback
            )

            return

        x = x1 + (x2 - x1) * step / move_steps
        y = y1 + (y2 - y1) * step / move_steps

        canvas.coords(
            car,
            x - 14,
            y - 14,
            x + 14,
            y + 14
        )

        root.after(
            30,
            lambda: animate(step + 1)
        )

    animate(0)


# ==========================================================
# SHOW FINAL ANSWER
# ==========================================================

def show_final():

    global running

    running = False

    reset_roads()

    if final_path:

        for i in range(len(final_path) - 1):

            highlight_road(
                final_path[i],
                final_path[i + 1],
                "#16a34a"
            )

        route_label.config(
            text=" → ".join(final_path)
        )

        cost_label.config(
            text=f"Lowest Total Cost: ₹{final_cost}"
        )

        status.config(
            text="GOAL FOUND! Lowest-Cost Path Selected.",
            fg="#16a34a"
        )

        queue_label.config(
            text="FINAL PATH\n\n"
                 + " → ".join(final_path)
                 + f"\n\nTotal = ₹{final_cost}"
        )

    start_button.config(
        state="normal"
    )

    pause_button.config(
        state="disabled"
    )


# ==========================================================
# PAUSE / RESUME
# ==========================================================

def pause_resume():

    global paused

    if not running:
        return

    paused = not paused

    if paused:

        pause_button.config(
            text="Resume"
        )

        status.config(
            text="UCS Paused",
            fg="#f59e0b"
        )

    else:

        pause_button.config(
            text="Pause"
        )

        status.config(
            text="UCS Resumed...",
            fg="#2563eb"
        )


# ==========================================================
# RESET
# ==========================================================

def reset():

    global running
    global paused
    global car

    running = False
    paused = False

    reset_roads()

    if car is not None:

        canvas.delete(car)
        car = None

    route_label.config(
        text="---"
    )

    cost_label.config(
        text="Current Total: ₹0"
    )

    queue_label.config(
        text="Waiting..."
    )

    status.config(
        text="Click Start UCS",
        fg="#374151"
    )

    start_button.config(
        state="normal"
    )

    pause_button.config(
        state="disabled",
        text="Pause"
    )


# ==========================================================
# INFORMATION PANEL
# ==========================================================

panel = tk.Frame(
    root,
    bg="white"
)

panel.pack()

status = tk.Label(
    panel,
    text="Click Start UCS",
    font=("Arial", 14, "bold"),
    bg="white"
)

status.grid(
    row=0,
    column=0,
    padx=20
)

route_label = tk.Label(
    panel,
    text="---",
    font=("Arial", 12, "bold"),
    bg="white"
)

route_label.grid(
    row=1,
    column=0,
    padx=20,
    pady=5
)

cost_label = tk.Label(
    panel,
    text="Current Total: ₹0",
    font=("Arial", 12, "bold"),
    bg="white"
)

cost_label.grid(
    row=2,
    column=0,
    padx=20
)

queue_label = tk.Label(
    panel,
    text="Waiting...",
    font=("Arial", 11),
    bg="white"
)

queue_label.grid(
    row=1,
    column=1,
    rowspan=2,
    padx=40
)

# ==========================================================
# BUTTONS
# ==========================================================

buttons = tk.Frame(
    root,
    bg="white"
)

buttons.pack(pady=10)

start_button = tk.Button(
    buttons,
    text="▶ Start UCS",
    command=start_ucs,
    width=15,
    font=("Arial", 11, "bold")
)

start_button.grid(
    row=0,
    column=0,
    padx=5
)

pause_button = tk.Button(
    buttons,
    text="⏸ Pause",
    command=pause_resume,
    width=15,
    font=("Arial", 11, "bold"),
    state="disabled"
)

pause_button.grid(
    row=0,
    column=1,
    padx=5
)

reset_button = tk.Button(
    buttons,
    text="↻ Reset",
    command=reset,
    width=15,
    font=("Arial", 11, "bold")
)

reset_button.grid(
    row=0,
    column=2,
    padx=5
)

# ==========================================================
# DRAW
# ==========================================================

draw_roads()
draw_nodes()

root.mainloop()
