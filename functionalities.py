import json
from tkinter import *

class task_bar:
    def __init__(self, root, text):
        #TODO: finish function and return the frame(task_frame) before packing into "root"
        self.main_frame = Frame(root, padx=5, pady=5)
        self.task_frame = LabelFrame(self.main_frame, text="", padx=5, pady=5)
        self.task = Label(self.task_frame, text=text)
        self.task.pack()
        self.task_frame.pack()

    def create_task_bar(self):
        return self.main_frame


def load_list(name, root):
    with open("lists.json") as f:
        lists = json.load(f)
        list_content = lists[name]
        task_bars = []
        for task in list_content:
            curr_task_bar = task_bar(root, task)
            task_bars.append(curr_task_bar.create_task_bar())
        for task in range(len(task_bars)):
            y_pos = task / 10 + 0.25
            task_bars[task].place(relx=0.25, rely=y_pos, relwidth=0.5)