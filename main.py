import tkinter as tk
import keyboard
from sys import argv

from variable_functions import *

# Global offset variables
offsetx = 0
offsety = 0

def initialize_root(root):
    root.geometry("+1650+55")
    root.resizable(False, False)
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.configure(bg=transparent_color)
    root.wm_attributes("-transparentcolor", transparent_color)

def main():
    root: tk.Tk = tk.Tk()
    init_config()
    initialize_root(root)
    canvas = tk.Canvas(root, width=1920, height=1080, bg=transparent_color, highlightthickness=0)
    canvas.configure(highlightthickness=0, borderwidth=0)
    canvas.pack()

    """Handle sys arguments"""
    try:
        if argv[1] == "setfont":
            if validate_font(font_name := argv[2]):
                set_font(font_name=font_name)
            else:
                raise FileNotFoundError("Entered font not found on system.")
    except IndexError:
        pass

    """Decide font"""
    try:
        bold_font: tk.font.Font = tk.font.Font(family=get_font(), size=20, weight="bold")
        font: tk.font.Font = tk.font.Font(family=get_font(), size=20, weight="normal")
        small_font: tk.font.Font = tk.font.Font(family=get_font(), size=15, weight="normal")
    except KeyError:
        bold_font: tk.font.Font = tk.font.Font(family=tk.font.families()[-1], size=20, weight="normal")
        font: tk.font.Font = tk.font.Font(family=tk.font.families()[-1], size=20, weight="normal")
        small_font: tk.font.Font = tk.font.Font(family=tk.font.families()[-1], size=15, weight="normal")

    text_color = "DarkGoldenrod1"
    mainlinetxt = "───➕───"

    def on_click(event):
        input_text.place(x=150 + offsetx, y=150 + offsety, anchor="center")
        input_text.focus_set()

    def add_new_task(event=None, task=None):
        global next_y_position

        if not task:
            task_text = input_text.get("1.0", "end-1c").strip()
            save_task(task_text) if task_text else ()
        else:
            task_text = task

        if task_text:
            # Add the clickable box with the exclamation mark
            box_id = canvas.create_text(50 + offsetx, next_y_position + 15 + offsety, text="【!】 ", font=small_font, fill="orange", anchor="w")
            current_color_index_map[box_id] = 0
            canvas.tag_bind(box_id, "<Enter>", lambda _: on_enter(box_id))
            canvas.tag_bind(box_id, "<Leave>", lambda _: on_leave(box_id))

            # Add the task text itself
            task_text_id = canvas.create_text(75 + offsetx, next_y_position + offsety, text=task_text, font=small_font, fill=text_color,
                                              width=200, anchor="nw")

            # Store both box and text in the tasks list as a tuple
            tasks.append((box_id, task_text_id))

            # Bind the click event to the box
            canvas.tag_bind(box_id, "<Button-1>", lambda _: complete_task(box_id, task_text_id))

            # Initialize hover effects for the task text
            current_color_index_map[task_text_id] = 0
            hovering_map[task_text_id] = False
            canvas.tag_bind(task_text_id, "<Enter>", lambda _, task_id=task_text_id: on_enter(task_id))
            canvas.tag_bind(task_text_id, "<Leave>", lambda _, task_id=task_text_id: on_leave(task_id))

            # Move the y position for the next task
            next_y_position += int(canvas.bbox(task_text_id)[3] - canvas.bbox(task_text_id)[1]) + 20

        input_text.delete("1.0", "end")
        input_text.place_forget()

    def complete_task(box_id, task_text_id):
        x1, y1, x2, y2 = canvas.bbox(task_text_id)

        # Create a green semi-transparent rectangle behind the task text and button
        background_rect_id = canvas.create_rectangle(
            x1 - 10, y1 - 5, x2 + 10, y2 + 5,
            fill="green",
            stipple="gray25",  # Creates a semi-transparent effect with a stipple pattern
            outline=""  # No border
        )

        # Bring text and button to the front so they are on top of the rectangle
        canvas.tag_raise(task_text_id)
        canvas.tag_raise(box_id)

        # Start flashing the box, text, and backgrounda
        flash_widget(box_id, times=6, on_complete=lambda: canvas.delete(box_id))
        flash_widget(task_text_id, times=6, on_complete=lambda: canvas.delete(task_text_id))
        flash_widget(background_rect_id, times=6, on_complete=lambda: canvas.delete(background_rect_id))

        # Remove the task from JSON after the flashing is complete
        task_text = canvas.itemcget(task_text_id, "text")
        remove_config_task(task_text)

        # Adjust remaining tasks after this one is removed
        root.after(1000, lambda: remove_task(box_id, task_text_id))
        update_task_positions()

    def remove_task(box_id, task_text_id):
        # Remove the completed task from the canvas and the tasks list
        canvas.delete(task_text_id)
        for task in tasks:
            if task[0] == box_id:
                tasks.remove(task)
                break

        # Update positions of remaining tasks
        update_task_positions()

    def update_task_positions():
        global next_y_position
        next_y_position = 140  # Reset starting y-position
        for box_id, task_text_id in tasks:
            canvas.coords(box_id, 50 + offsetx, next_y_position + 15 + offsety)
            canvas.coords(task_text_id, 75 + offsetx, next_y_position + offsety)
            next_y_position += int(canvas.bbox(task_text_id)[3] - canvas.bbox(task_text_id)[1]) + 20

    def flash_widget(widget_id, times, on_complete=None):
        def toggle_visibility(count):
            if count > 0:
                # Toggle widget visibility by changing its color
                current_color = canvas.itemcget(widget_id, "fill")
                canvas.itemconfig(widget_id, fill="green" if current_color != "green" else "lawn green")
                root.after(100, lambda: toggle_visibility(count - 1))
            else:
                if on_complete:
                    on_complete()

        toggle_visibility(times)

    def on_enter(text_id):
        hovering_map[text_id] = True
        cycle_colors(text_id)

    def on_leave(text_id):
        hovering_map[text_id] = False
        canvas.itemconfig(text_id, fill=text_color)

    def cycle_colors(text_id):
        if hovering_map[text_id]:
            canvas.itemconfig(text_id, fill=f"goldenrod{current_color_index_map[text_id] + 1}")
            current_color_index_map[text_id] = (current_color_index_map[text_id] + 1) % 4
            root.after(100, lambda: cycle_colors(text_id))

    # Define shortcuts


    def toggle_visibility():
        if root.attributes("-alpha") == 1.0:
            root.attributes("-alpha", 0.0)
        else:
            root.attributes("-alpha", 1.0)

    canvas.focus_force()
    # Following works only if app is focused
    # root.bind("<Control-Shift-L><N>", lambda _: on_click(None))
    # root.bind("<Control-Shift-L><H>", lambda _: toggle_visibility())
    # root.bind("<Control-Shift-L><C>", lambda _: complete_task(*tasks[0]) if tasks else None)
    # root.bind("<Control-Shift-L><K>", lambda _: root.destroy())

    keyboard.add_hotkey('ctrl + shift + l + k', root.destroy, args=())
    keyboard.add_hotkey('ctrl + shift + l + h', toggle_visibility, args=())
    keyboard.add_hotkey('ctrl + shift + l + c', complete_task, args=(tasks[0] if tasks else None))
    keyboard.add_hotkey('ctrl + shift + l + n', on_click, args=())

    mainline_textid = canvas.create_text(150 + offsetx, 100 + offsety, text=mainlinetxt, font=bold_font, fill=text_color)
    current_color_index_map[mainline_textid] = 0
    hovering_map[mainline_textid] = False

    canvas.tag_bind(mainline_textid, "<Enter>", lambda _: on_enter(mainline_textid))
    canvas.tag_bind(mainline_textid, "<Leave>", lambda _: on_leave(mainline_textid))
    canvas.tag_bind(mainline_textid, "<Button-1>", on_click)

    input_text = tk.Text(root, width=20, height=2, wrap="word", font=small_font, fg=text_color, bg=transparent_color,
                         bd=1,
                         highlightthickness=0, insertbackground="orange2")
    input_text.bind("<Return>", add_new_task)
    input_text.bind("<FocusOut>", lambda event: input_text.focus_set())

    task_list = get_tasks()
    for task in task_list:
        add_new_task(event=None, task=task)
    root.mainloop()


if __name__ == "__main__":
    next_y_position = 140
    transparent_color = "white"
    current_color_index_map = {}
    hovering_map = {}
    tasks = []  # List to hold tasks as tuples of (box_id, task_text_id)
    main()
