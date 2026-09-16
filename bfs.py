import tkinter as tk
from collections import deque

# ---------------- MAZE ----------------
# 0 = Path
# 1 = Wall

maze = [
    [0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0]
]

ROWS = len(maze)
COLS = len(maze[0])
CELL = 65

START = (0, 0)
GOAL = (6, 6)

# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("BFS Shortest Path Visualizer")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=COLS * CELL,
    height=ROWS * CELL
)
canvas.pack(padx=10, pady=10)

# ---------------- VARIABLES ----------------

queue = deque()
visited = set()
parent = {}

searching = False
paused = False
finished = False

# ---------------- DRAW MAZE ----------------


def draw_maze():

    canvas.delete("all")

    for r in range(ROWS):
        for c in range(COLS):

            x1 = c * CELL
            y1 = r * CELL
            x2 = x1 + CELL
            y2 = y1 + CELL

            if maze[r][c] == 1:
                color = "black"
            else:
                color = "white"

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="gray"
            )

    # START
    r, c = START

    canvas.create_rectangle(
        c * CELL,
        r * CELL,
        (c + 1) * CELL,
        (r + 1) * CELL,
        fill="green",
        outline="gray"
    )

    canvas.create_text(
        c * CELL + CELL / 2,
        r * CELL + CELL / 2,
        text="START",
        fill="white",
        font=("Arial", 9, "bold")
    )

    # GOAL
    r, c = GOAL

    canvas.create_rectangle(
        c * CELL,
        r * CELL,
        (c + 1) * CELL,
        (r + 1) * CELL,
        fill="red",
        outline="gray"
    )

    canvas.create_text(
        c * CELL + CELL / 2,
        r * CELL + CELL / 2,
        text="GOAL",
        fill="white",
        font=("Arial", 9, "bold")
    )


# ---------------- CHECK VALID CELL ----------------


def valid_cell(r, c):

    return (
        0 <= r < ROWS
        and 0 <= c < COLS
        and maze[r][c] == 0
    )


# ---------------- START BFS ----------------


def start_bfs():

    global queue, visited, parent
    global searching, paused, finished

    queue = deque()
    visited = set()
    parent = {}

    queue.append(START)
    visited.add(START)

    searching = True
    paused = False
    finished = False

    status.config(
        text="BFS is searching...",
        fg="blue"
    )

    pause_button.config(
        text="Pause",
        state="normal"
    )

    start_button.config(
        state="disabled"
    )

    bfs_step()


# ---------------- BFS STEP ----------------


def bfs_step():

    global searching

    if not searching:
        return

    # If paused, stop here.
    if paused:
        return

    # Queue empty
    if not queue:

        searching = False

        status.config(
            text="No path found!",
            fg="red"
        )

        start_button.config(
            state="normal"
        )

        return

    # Take first item from queue
    current = queue.popleft()

    r, c = current

    # Goal found
    if current == GOAL:

        searching = False

        show_shortest_path()

        return

    # Show current cell
    if current != START:

        canvas.create_rectangle(
            c * CELL + 8,
            r * CELL + 8,
            (c + 1) * CELL - 8,
            (r + 1) * CELL - 8,
            fill="lightblue",
            outline=""
        )

    # Directions:
    # Up, Down, Left, Right

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for dr, dc in directions:

        nr = r + dr
        nc = c + dc

        if valid_cell(nr, nc):

            next_cell = (nr, nc)

            if next_cell not in visited:

                visited.add(next_cell)

                parent[next_cell] = current

                queue.append(next_cell)

    root.after(300, bfs_step)


# ---------------- SHOW SHORTEST PATH ----------------


def show_shortest_path():

    global finished

    path = []

    current = GOAL

    while current != START:

        path.append(current)
        current = parent[current]

    path.append(START)

    path.reverse()

    animate_path(path, 0)


def animate_path(path, index):

    if index >= len(path):

        global finished
        finished = True

        status.config(
            text="Shortest Path Found!",
            fg="green"
        )

        start_button.config(
            state="normal"
        )

        pause_button.config(
            state="disabled"
        )

        return

    r, c = path[index]

    if (r, c) != START and (r, c) != GOAL:

        canvas.create_rectangle(
            c * CELL + 15,
            r * CELL + 15,
            (c + 1) * CELL - 15,
            (r + 1) * CELL - 15,
            fill="yellow",
            outline=""
        )

    root.after(
        250,
        lambda: animate_path(path, index + 1)
    )


# ---------------- PAUSE / RESUME ----------------


def toggle_pause():

    global paused

    if not searching:
        return

    if paused:

        paused = False

        pause_button.config(
            text="Pause"
        )

        status.config(
            text="BFS is searching...",
            fg="blue"
        )

        bfs_step()

    else:

        paused = True

        pause_button.config(
            text="Resume"
        )

        status.config(
            text="BFS Paused",
            fg="orange"
        )


# ---------------- RESET ----------------


def reset():

    global searching, paused, finished

    searching = False
    paused = False
    finished = False

    start_button.config(
        state="normal"
    )

    pause_button.config(
        text="Pause",
        state="disabled"
    )

    status.config(
        text="Click Start BFS",
        fg="black"
    )

    draw_maze()


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

start_button = tk.Button(
    button_frame,
    text="Start BFS",
    command=start_bfs,
    width=12,
    font=("Arial", 11, "bold")
)

start_button.grid(
    row=0,
    column=0,
    padx=5
)

pause_button = tk.Button(
    button_frame,
    text="Pause",
    command=toggle_pause,
    width=12,
    state="disabled",
    font=("Arial", 11, "bold")
)

pause_button.grid(
    row=0,
    column=1,
    padx=5
)

reset_button = tk.Button(
    button_frame,
    text="Reset",
    command=reset,
    width=12,
    font=("Arial", 11, "bold")
)

reset_button.grid(
    row=0,
    column=2,
    padx=5
)

status = tk.Label(
    root,
    text="Click Start BFS",
    font=("Arial", 12, "bold")
)

status.pack(pady=8)

# Initial maze
draw_maze()

root.mainloop()