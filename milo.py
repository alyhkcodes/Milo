import tkinter as tk
import math
import random
import ctypes
import colorsys
import sys

# --- Snake settings ---
snake_length = 20
segment_char = "*"
follow_distance = 200
move_speed = 3
float_speed = 1.5
inertia = 0.95
segment_smooth = 0.2
color_blend_speed = 0.02
target_change_speed = 0.005

# --- Screen dimensions ---
user32 = ctypes.windll.user32
width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# --- Cursor position ---
def get_cursor_pos():
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return [pt.x, pt.y]

# --- HSV to hex ---
def hsv_to_hex(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

# --- Launch floating snake ---
def launch_snake():
    title_window.destroy()  # close popup
    
    snake_root = tk.Tk()
    snake_root.geometry(f"{width}x{height}+0+0")
    snake_root.overrideredirect(True)
    snake_root.attributes("-topmost", True)
    snake_root.attributes("-transparentcolor", "black")
    snake_root.config(bg="black")

    canvas = tk.Canvas(snake_root, width=width, height=height, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # --- Initialize snake segments ---
    snake_segments = []
    for _ in range(snake_length):
        seg = canvas.create_text(random.randint(0, width),
                                 random.randint(0, height),
                                 text=segment_char,
                                 fill="#00ff00",
                                 font=("Courier", 16, "bold"))
        snake_segments.append(seg)

    # --- Segment colors (current & target) ---
    segment_colors = []
    for _ in range(snake_length):
        h = random.uniform(0, 1)
        s = 0.4 + random.uniform(0, 0.2)
        v = 0.7 + random.uniform(0, 0.2)
        segment_colors.append({"current": [h, s, v], "target": [h, s, v]})

    # --- Head velocity ---
    head_velocity = [random.uniform(-float_speed, float_speed),
                     random.uniform(-float_speed, float_speed)]

    # --- Snake movement and color update ---
    def move_snake():
        nonlocal head_velocity
        cursor_pos = get_cursor_pos()

        # --- Update head ---
        head_x, head_y = canvas.coords(snake_segments[0])
        dx = cursor_pos[0] - head_x
        dy = cursor_pos[1] - head_y
        dist = math.hypot(dx, dy)

        if dist < follow_distance:
            head_velocity[0] += dx / dist * 0.2 * move_speed
            head_velocity[1] += dy / dist * 0.2 * move_speed
        else:
            head_velocity[0] += random.uniform(-0.05, 0.05)
            head_velocity[1] += random.uniform(-0.05, 0.05)

        head_velocity[0] *= inertia
        head_velocity[1] *= inertia

        head_x += head_velocity[0]
        head_y += head_velocity[1]

        head_x = max(0, min(width, head_x))
        head_y = max(0, min(height, head_y))

        canvas.coords(snake_segments[0], head_x, head_y)

        # --- Update body ---
        for i in range(1, snake_length):
            prev_x, prev_y = canvas.coords(snake_segments[i-1])
            cur_x, cur_y = canvas.coords(snake_segments[i])
            dx = prev_x - cur_x
            dy = prev_y - cur_y
            distance = math.hypot(dx, dy)
            if distance > 0:
                cur_x += dx * segment_smooth
                cur_y += dy * segment_smooth
                canvas.coords(snake_segments[i], cur_x, cur_y)

        # --- Update colors ---
        for i, seg in enumerate(snake_segments):
            cur_h, cur_s, cur_v = segment_colors[i]["current"]
            target_h, target_s, target_v = segment_colors[i]["target"]

            # Blend toward target
            cur_h += (target_h - cur_h) * color_blend_speed
            cur_s += (target_s - cur_s) * color_blend_speed
            cur_v += (target_v - cur_v) * color_blend_speed
            segment_colors[i]["current"] = [cur_h, cur_s, cur_v]

            # Occasionally pick new target color
            if random.random() < target_change_speed:
                new_h = random.uniform(0, 1)
                new_s = 0.4 + random.uniform(0, 0.2)
                new_v = 0.7 + random.uniform(0, 0.2)
                segment_colors[i]["target"] = [new_h, new_s, new_v]

            canvas.itemconfig(seg, fill=hsv_to_hex(cur_h, cur_s, cur_v))

        snake_root.after(20, move_snake)

    move_snake()
    snake_root.mainloop()

# --- First aesthetic popup for Milo ---
title_window = tk.Tk()
title_window.title("Milo")
title_window.geometry("400x200+600+350")
title_window.configure(bg="#f4f4f9")
title_window.attributes("-topmost", True)
title_window.resizable(False, False)
title_window.overrideredirect(True)

# Aesthetic font
try:
    aesthetic_font = ("Helvetica Neue", 16, "bold")
except:
    aesthetic_font = ("Helvetica", 16, "bold")

# Greeting label
label = tk.Label(title_window,
                 text="Hey there!\nMilo is ready to play with you 🐍",
                 font=aesthetic_font,
                 fg="#4a4a4a",
                 bg="#f4f4f9",
                 justify="center")
label.pack(expand=True)

# Play button
play_button = tk.Button(title_window,
                        text="Play 🐍",
                        font=("Helvetica Neue", 12, "bold"),
                        fg="#f4f4f9",
                        bg="#8ab6d6",
                        activebackground="#a1c4e6",
                        activeforeground="#f4f4f9",
                        relief="flat",
                        command=launch_snake)
play_button.pack(pady=5, ipadx=20, ipady=8)

# Quit button
quit_button = tk.Button(title_window,
                        text="Quit ❌",
                        font=("Helvetica Neue", 12, "bold"),
                        fg="#f4f4f9",
                        bg="#d68a8a",
                        activebackground="#e6a1a1",
                        activeforeground="#f4f4f9",
                        relief="flat",
                        command=lambda: (title_window.destroy(), sys.exit()))
quit_button.pack(pady=5, ipadx=20, ipady=8)

# Center window
screen_width = title_window.winfo_screenwidth()
screen_height = title_window.winfo_screenheight()
x = (screen_width // 2) - 200
y = (screen_height // 2) - 100
title_window.geometry(f"+{x}+{y}")

title_window.mainloop()