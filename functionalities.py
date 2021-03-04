import json
from tkinter import *
from tkinter import messagebox
import webbrowser


class task_bar:
    def __init__(self, root, text, place):
        # TODO: finish function and return the frame(task_frame) before packing into "root"
        self.task_frame = LabelFrame(root, text="", padx=5, pady=5)
        var = IntVar()
        self.task_status = Checkbutton(self.task_frame, text=text, variable=var,
                                       command=lambda: edit_task_status(var.get(), place))
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
        place = (name, 0)
        for task in list_content:
            curr_task_bar = task_bar(main_frame, task[0], place)
            task_bars.append(curr_task_bar.create_task_bar())
            task_status = curr_task_bar.get_status()
            if task[1]:
                task_status.select()
            else:
                task_status.deselect()
            place = (name, place[1] + 1)
        for task in range(len(task_bars)):
            y_pos = task / 10 + 0.25
            task_bars[task].place(relx=0.33, rely=y_pos, relwidth=0.5)
        main_frame.place(relx=0.25, rely=0.2, relheight=0.65, relwidth=0.6)
        return main_frame


def edit_task_status(var, place):
    with open("lists.json") as f:
        data = json.load(f)
        if var == 0: data[place[0]][place[1]][1] = False
        elif var == 1: data[place[0]][place[1]][1] = True
        else: print("An error has happened")
    with open("lists.json", "w") as f:
        json.dump(data, f, indent=2)


def add_task(name, root, curr_frame):
    #creating a new window and setting a title
    new_task = Toplevel()
    new_task.title("New Task")

    # a title inside the window
    Label(new_task, text="NEW TASK", font="Helvetica 13 bold").grid(row=0, column=0)

    #a label before the input that gets the new task's name
    Label(new_task, text="Task name: ", font="Helvetica 12").grid(row=1, column=0)
    #creating and placing the input box
    task_name_input = Entry(new_task)
    task_name_input.grid(row=1, column=1)

    #a label before the estimated time the task will take
    Label(new_task, text="Est. time: ", font="Helvetica 12").grid(row=2, column=0)
    #creating and placing the input box
    time_input = Entry(new_task)
    time_input.grid(row=2, column=1)
    #a label denoting the units in which the time is measured
    Label(new_task, text=" minutes", font="Helvetica 12").grid(row=2, column=2)

    #a variable containing a "Yes" or "No" strong if the user likes the task
    liked = StringVar()
    liked.set("Yes")
    #a label before the check if the user likes the task
    Label(new_task, text="I like this task: ", font="Helvetica 12").grid(row=3, column=0)
    #a dropdown menu for a yes or now option(default is "yes")
    liked_task = OptionMenu(new_task, liked, "Yes", "No")
    liked_task.grid(row=3, column=1)

    #a button that add the task to the json file
    create_btn = Button(new_task, text="CREATE",
                        command=lambda: save_new_task(new_task, name, task_name_input.get(), time_input.get(), liked.get(), root, curr_frame))
    create_btn.grid(row=4, column=2)


def save_new_task(window, list_name, task_name, est_time, is_liked, root, curr_frame):
    #step I: get the data from the json file and convert to python
    with open("lists.json") as f:
        data = json.load(f)
    #step II: checks if all the inputs are valid(list does not contain more then 7 task and est time is a number and task name ins not too long)
    try:
        est_time = int(est_time)
        if len(data[list_name]) >= 7:
            window.destroy()
            messagebox.showerror("Error", "List is full")
            return None
        if len(task_name) > 30:
            window.destroy()
            messagebox.showerror("Error", "Task name is too long")
            return None
        if len(task_name) <= 0:
            window.destroy()
            messagebox.showerror("Error", "Task name is invalid")
    except ValueError:
        window.destroy()
        messagebox.showerror("Error", "Invalid number entered in est. time")
        return None
    #step III: insert the new task to the converted json file
    task_to_add = [task_name, False, est_time]
    if is_liked == "Yes": task_to_add.append(True)
    elif is_liked == "No": task_to_add.append(False)
    data[list_name].append(task_to_add)
    #step IV: convert data back to json and save to the file
    with open("lists.json", "w") as f:
        json.dump(data, f, indent=2)
    #step V: sort the list and reload the list on the screen
    sort_list()
    load_list(list_name, root, curr_frame)
    window.destroy()



def sort_list():
    pass


def show_about():
    url = "https://github.com/elad-weiss/school-biology-project/blob/master/README.md"
    webbrowser.open(url, new=1)