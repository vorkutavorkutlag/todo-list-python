import tkinter as tk
import tkinter.font
from sys import argv
from variable_functions import *


def initialize_root(root):
    root.geometry("+1650+55")
    root.resizable(False, False)
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.configure(bg=transparent_color)
    root.wm_attributes("-transparentcolor", transparent_color)


def main():
    # region initialization
    root: tk.Tk = tkinter.Tk()
    initialize_root(root)
    canvas = tk.Canvas(root, width=1920, height=1080, bg=transparent_color, highlightthickness=0)
    canvas.configure(highlightthickness=0, borderwidth=0)
    canvas.pack()

    """Handle sys arguments"""
    try:
        if argv[1] == "setfont":
            if validate_font(font_name := argv[2]):
                # Valid argument, valid font
                set_font(font_name=font_name)
            else:
                # Valid argument, invalid font
                raise FileNotFoundError("Entered font not found on system.")
    except IndexError:
        # Means no (valid) argument was passed, ignore
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

    # endregion

    def on_click(event):
        input_text.place(x=150, y=150, anchor="center")
        input_text.focus_set()

    def add_new_task(event=None):
        global next_y_position
        task_text = input_text.get("1.0", "end-1c").strip()

        if task_text:
            # Add the clickable box with the exclamation mark
            box_id = canvas.create_text(45, next_y_position+10, text="【❗】", font=small_font, fill="orange", anchor="w")

            # Add the task text itself
            task_text_id = canvas.create_text(75, next_y_position, text=task_text, font=small_font, fill=text_color,
                                              width=200, anchor="nw")

            # Bind the click event to the box
            canvas.tag_bind(box_id, "<Button-1>", lambda _: complete_task(box_id, task_text_id))

            # Initialize hover effects for the task text
            current_color_index_map[task_text_id] = 0
            hovering_map[task_text_id] = False
            canvas.tag_bind(task_text_id, "<Enter>", lambda _, task_id=task_text_id: on_enter(task_id))
            canvas.tag_bind(task_text_id, "<Leave>", lambda _, task_id=task_text_id: on_leave(task_id))

            next_y_position += int(canvas.bbox(task_text_id)[3] - canvas.bbox(task_text_id)[1]) + 20

        # Clear the input and hide the text entry
        input_text.delete("1.0", "end")
        input_text.place_forget()

    def complete_task(box_id, task_text_id):
        global next_y_position
        # Change the task text color to green
        canvas.itemconfig(task_text_id, fill="green")

        # Start flashing the box and then hide it
        flash_widget(box_id, times=6, on_complete=lambda: canvas.delete(box_id))

        # Start flashing the task text after the box disappears
        root.after(800, lambda: flash_widget(task_text_id, times=6, on_complete=lambda: canvas.delete(task_text_id)))
        next_y_position -= int(canvas.bbox(task_text_id)[3] - canvas.bbox(task_text_id)[1]) + 20

    def flash_widget(widget_id, times, on_complete=None):
        def toggle_visibility(count):
            if count > 0:
                # Toggle widget visibility by changing its color
                current_color = canvas.itemcget(widget_id, "fill")
                canvas.itemconfig(widget_id, fill="black" if current_color != "black" else "orange")
                root.after(100, lambda: toggle_visibility(count - 1))
            else:
                # Final callback after flashing completes
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

    mainline_textid = canvas.create_text(150, 100, text=mainlinetxt, font=bold_font, fill=text_color)
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

    root.mainloop()


if __name__ == "__main__":
    next_y_position = 140
    transparent_color = "white"
    current_color_index_map = {}
    hovering_map = {}
    main()
