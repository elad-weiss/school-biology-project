import json
from tkinter import *


class task_bar:
    def __init__(self, root, text):
        # TODO: finish function and return the frame(task_frame) before packing into "root"
        self.task_frame = LabelFrame(root, text="", padx=5, pady=5)
        var = IntVar()
        self.task_status = Checkbutton(self.task_frame, text=text, variable=var)
        self.task_status.grid(row=0, column=0)
        self.task_frame.pack()

    def create_task_bar(self):
        return self.task_frame

    def get_status(self):
        return self.task_status


def load_list(name, root, curr_frame):
    if curr_frame != "":
        curr_frame.destroy()
    main_frame = Frame(root, padx=5, pady=5)
    with open("lists.json") as f:
        lists = json.load(f)
        list_content = lists[name]
        task_bars = []
        for task in list_content:
            curr_task_bar = task_bar(main_frame, task[0])
            task_bars.append(curr_task_bar.create_task_bar())
            task_status = curr_task_bar.get_status()
            if task[1]:
                task_status.select()
            else:
                task_status.deselect()
        for task in range(len(task_bars)):
            y_pos = task / 10 + 0.25
            task_bars[task].place(relx=0.33, rely=y_pos, relwidth=0.5)
        main_frame.place(relx=0.25, rely=0.2, relheight=0.65, relwidth=0.6)
        return main_frame
