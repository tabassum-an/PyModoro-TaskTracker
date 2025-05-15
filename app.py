from tkinter import *
import math
import threading
from playsound import playsound
from datetime import datetime

# CONSTANTS
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#5F8B4C"
CREAM = "#f7ede0"
DARK_BG = "#2e2e2e"
DARK_FG = "#e0e0e0"
DARK_ENTRY = "#3c3c3c"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

reps = 0
timer = None
paused = False
current_count = 0
current_task = ""
dark_mode = False

# SOUND PLAY
def play_sound():
    def _play():
        try:
            playsound("mixkit-software-interface-start.wav")
        except Exception as e:
            print("Sound error:", e)
    threading.Thread(target=_play, daemon=True).start()

# TASK HISTORY
def log_task(task):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_text.config(state=NORMAL)
    history_text.insert(END, f"{timestamp} - Completed: {task}\n")
    history_text.see(END)
    history_text.config(state=DISABLED)

# TIMER RESET
def reset_timer():
    global timer, reps, paused, current_count, current_task
    if timer is not None:
        window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    task_display.config(text="")
    task_entry.delete(0, END)
    reps = 0
    paused = False
    current_count = 0
    current_task = ""
    start_button.config(text="Start")

# TIMER MECHANISM
def start_timer():
    global reps, current_task
    reps += 1

    if reps % 2 != 0:
        current_task = task_entry.get()
        task_display.config(text=f"Task: {current_task}")

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)

# COUNTDOWN
def count_down(count):
    global timer, current_count, paused
    paused = False
    current_count = count
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        play_sound()
        if reps % 2 == 0 and current_task.strip():
            log_task(current_task)
        start_timer()
        marks = "✔" * (math.floor(reps / 2))
        check_marks.config(text=marks)
        start_button.config(text="Start")

# PAUSE TIMER
def pause_timer():
    global paused, timer
    if not paused:
        if timer is not None:
            window.after_cancel(timer)
        paused = True
        start_button.config(text="Resume")
    else:
        paused = False
        start_button.config(text="Pause")
        count_down(current_count)

# DARK MODE
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg = DARK_BG if dark_mode else CREAM
    fg = DARK_FG if dark_mode else GREEN
    entry_bg = DARK_ENTRY if dark_mode else "white"

    window.config(bg=bg)
    title_label.config(bg=bg, fg=fg)
    task_label.config(bg=bg, fg=fg)
    task_display.config(bg=bg, fg=fg)
    task_entry.config(bg=entry_bg, fg=fg, insertbackground=fg)
    canvas.config(bg=bg)
    check_marks.config(bg=bg, fg=fg)
    history_label.config(bg=bg, fg=fg)
    history_text.config(bg=entry_bg, fg=fg, insertbackground=fg)

# UI SETUP
window = Tk()
window.title("Pomodoro")
window.geometry("800x700")
window.config(padx=30, pady=20, bg=CREAM)

title_label = Label(text="Timer", fg=GREEN, bg=CREAM, font=(FONT_NAME, 40))
title_label.grid(column=1, row=0, pady=10)

# TASK ENTRY
task_label = Label(text="Enter Task:", fg=GREEN, bg=CREAM, font=(FONT_NAME, 12, "bold"))
task_label.grid(column=0, row=1, sticky=E)

task_entry = Entry(width=30)
task_entry.grid(column=1, row=1, columnspan=1)

task_display = Label(text="", fg=GREEN, bg=CREAM, font=(FONT_NAME, 12))
task_display.grid(column=1, row=2, columnspan=1)

# Canvas (Image and Timer)
canvas = Canvas(width=400, height=300, bg=CREAM, highlightthickness=0)
try:
    tomato_img = PhotoImage(file="cute_tomato.png").subsample(2, 2)  # Shrink image to fit better
    #tomato_img = PhotoImage(file="tomato.png").subsample(2, 3)
    #tomato_img = PhotoImage(file="pomodoro.png").subsample(2, 2)
    canvas.create_image(200, 150, image=tomato_img)
except:
    canvas.create_text(200, 150, text="(Image not found)", fill="red", font=(FONT_NAME, 20))
timer_text = canvas.create_text(200, 205, text="00 : 00", fill="white", font=(FONT_NAME, 24, "bold"))
canvas.grid(column=1, row=3, pady=10)

# Buttons
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=4, pady=1)

pause_button = Button(text="Pause/Resume", highlightthickness=0, command=pause_timer)
pause_button.grid(column=1, row=4)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=4)

dark_button = Button(text="Toggle Dark Mode", highlightthickness=0, command=toggle_dark_mode)
dark_button.grid(column=3, row=1, padx=5)

# Checkmarks
check_marks = Label(fg=GREEN, bg=CREAM)
check_marks.grid(column=1, row=5)

# Task History Label and Scrollable Text
history_label = Label(text="Task History", fg=GREEN, bg=CREAM, font=(FONT_NAME, 12, "bold"))
history_label.grid(column=1, row=6, pady=(10, 5))

history_frame = Frame(window)
history_frame.grid(column=1, row=7, columnspan=2)

scrollbar = Scrollbar(history_frame)
scrollbar.pack(side=RIGHT, fill=Y)

history_text = Text(history_frame, height=5, width=65, font=(FONT_NAME, 10),
                    yscrollcommand=scrollbar.set, wrap=WORD)
history_text.pack(side=LEFT)
history_text.config(state=DISABLED)
scrollbar.config(command=history_text.yview)

window.mainloop()
