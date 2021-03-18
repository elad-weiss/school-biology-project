import json
from tkinter import *
from tkinter import messagebox
import webbrowser
import main
import datetime
import sorter


class task_bar:
    def __init__(self, root, text, place, state, main_root):
        self.task_frame = LabelFrame(root, text="", padx=5, pady=5)
        var = IntVar()
        self.start_task_btn = Button(self.task_frame, text="start",
                                     command=lambda: start_task(place, self.start_task_btn))
        if state: self.start_task_btn.config(state=DISABLED)
        else: self.start_task_btn.config(state=NORMAL)
        self.start_task_btn.place(relx=0.85, rely=-0.1)
        self.task_status = Checkbutton(self.task_frame, text=text, variable=var,
                                       command=lambda: edit_task_status(var.get(), place, self.start_task_btn, main_root, root),
                                       padx=5)
        self.task_status.place(relx=0.01, rely=-0.1)
        Label(self.task_frame, text="").grid(column=0, row=0)
        self.task_frame.pack()

    def create_task_bar(self):
        return self.task_frame

    def get_status(self):
        return self.task_status

#a global variable that keeps track of the current sort
current_sort = "sort a"

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
            curr_task_bar = task_bar(main_frame, task[0], place, task[1], root)
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


def edit_task_status(var, place, start_btn, root, curr_frame):
    with open("lists.json") as f:
        data = json.load(f)
    if var == 0:
        data[place[0]][place[1]][1] = False
        start_btn.config(state=NORMAL)
        try:
            del data[place[0]][place[1]][5]
        except IndexError:
            pass
        with open("lists.json", "w") as wf:
            json.dump(data, wf, indent=2)
    elif var == 1:
        data[place[0]][place[1]][1] = True
        start_datetime = data[place[0]][place[1]][4].split(":")
        curr_datetime = get_time().split(":")
        offsets = ([2022, 12, 30, 24, 60, 60], [525960, 43830, 1440, 60, 1, 0])
        minutes_sum = 0
        time_task_took = []
        for i in range(len(start_datetime)):
            diff = int(curr_datetime[i]) - int(start_datetime[i])
            time_task_took.append(diff)
        for i in range(len(time_task_took), 0, -1):
            if time_task_took[i - 1] < 0:
                time_task_took[i - 1] = offsets[0][i - 1] + time_task_took[i - 1]
                time_task_took[i-2] -= 1
            minutes_sum += time_task_took[i - 1] * offsets[1][i - 1]
        with open("lists.json", "w") as f:
            data[place[0]][place[1]].append(minutes_sum)
            json.dump(data, f, indent=2)
        start_btn.config(state=DISABLED)
        score_sort(place[0], root, curr_frame)
    else: messagebox.showerror("system update", "An error has occurred")


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
    #list saving protocol: "list name": ["task name", state(bool), est_time, is_liked(bool)]
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
        elif len(task_name) > 30:
            window.destroy()
            messagebox.showerror("Error", "Task name is too long")
            return None
        elif len(task_name) <= 0:
            window.destroy()
            messagebox.showerror("Error", "Task name is invalid")
            return None
    except ValueError:
        window.destroy()
        messagebox.showerror("Error", "Invalid number entered in est. time")
        return None
    #step III: insert the new task to the converted json file
    task_to_add = [task_name, False, est_time]
    if is_liked == "Yes": task_to_add.append(True)
    elif is_liked == "No": task_to_add.append(False)
    task_to_add.append(get_time())
    data[list_name].append(task_to_add)
    #step IV: convert data back to json and save to the file
    with open("lists.json", "w") as f:
        json.dump(data, f, indent=2)
    #step V: sort the list and reload the list on the screen
    sort_list(list_name)
    load_list(list_name, root, curr_frame)
    window.destroy()


def delete_task(list_name, root, curr_frame):
    #get current list data
    with open("lists.json") as rf:
        data = json.load(rf)
        curr_list = data[list_name]
    user_tasks = []
    for task in range(len(curr_list)):
        user_tasks.append(curr_list[task][0])

    #set up gui
    delete_task_win = Toplevel()
    delete_task_win.title("delete task")
    #set up "choose list" label
    Label(delete_task_win, text="choose task to delete:  ").grid(row=0, column=0)
    #set up option menu with all current tasks and the variable that saves which task has been chosen
    task_to_del = StringVar()
    task_to_del.set(user_tasks[0])
    task_to_del_menu = OptionMenu(delete_task_win, task_to_del, *user_tasks)
    task_to_del_menu.grid(row=0, column=1)
    #set up delete task button
    del_task_btn = Button(delete_task_win, text="delete", font="Helvetica 12",
                          command=lambda: delete_task_from_db(delete_task_win, list_name, task_to_del.get(), root, curr_frame))
    del_task_btn.grid(row=1, column=1)


def delete_task_from_db(window, list_name, task_name, root, curr_frame):
    task_place = IntVar()
    with open("lists.json") as rf:
        data = json.load(rf)
        for task in range(len(data[list_name])):
            if data[list_name][task][0] == task_name: task_place.set(task)
    del data[list_name][task_place.get()]
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)
    load_list(list_name, root, curr_frame)
    window.destroy()


def add_list(root):
    #create and setup the creation window
    new_list_window = Toplevel()
    new_list_window.title("New List")
    new_list_window.geometry("200x60")

    #set up the gui
    #"name: " label
    Label(new_list_window, text="Name: ", font="Helvetica 14").grid(row=0, column=0)
    #text box input
    list_name_input = Entry(new_list_window)
    list_name_input.grid(row=0, column=1)
    #create button
    create_btn = Button(new_list_window, text="create",
                        command=lambda: save_new_list(list_name_input.get(), new_list_window, root))
    create_btn.grid(row=1, column=1)


def save_new_list(list_name, window, root):
    list_name = str(list_name)
    if len(list_name) >= 13:
        window.destroy()
        messagebox.showerror("Error", "List name is too long")
        return None
    elif len(list_name) <= 0:
        window.destroy()
        messagebox.showerror("Error", "List name is invalid")
        return None
    with open("lists.json") as rf:
        data = json.load(rf)
        if list_name in list(data.keys()):
            window.destroy()
            messagebox.showerror("Error", "List name already exists")
            return None
        elif len(list(data.keys())) >= 6:
            window.destroy()
            messagebox.showerror("Error", "You have too many lists")
            return None
        data.update({list_name: []})
        with open("lists.json", "w") as wf:
            json.dump(data, wf, indent=2)
    window.destroy()
    root.destroy()
    main.main_window()


def delete_list(root):
    #set up window
    delete_list_win = Toplevel()
    delete_list_win.title("delete list")
    delete_list_win.geometry("250x75")
    #choose list to delete label
    Label(delete_list_win, text="Choose list to delete:  ", font="Helvetica 12").grid(row=0, column=0)
    #the variable that contains the list to delete
    list_to_del = StringVar()
    #a list containing all the user lists
    with open("lists.json") as rf:
        data = json.load(rf)
    user_lists = [name for name in data.keys()]
    list_to_del.set(user_lists[0])
    #all lists dropdown menu
    list_to_del_menu = OptionMenu(delete_list_win, list_to_del, *user_lists)
    list_to_del_menu.grid(row=0, column=1)
    #delete btn
    delete_btn = Button(delete_list_win, text="delete", font="Helvetica 12",
                        command=lambda: delete_list_from_db(list_to_del.get(), delete_list_win, root))
    delete_btn.grid(row=1, column=1)

#deletes the list from the data base
def delete_list_from_db(list_name, window, root):
    with open("lists.json") as rf:
        data = json.load(rf)
    del data[list_name]
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)
    window.destroy()
    root.destroy()
    main.main_window()


def sort_list(list_name):
    with open("sorting_templates.json") as f:
        data = json.load(f)
    template = ""
    for sort_template in data:
        if not data[sort_template][0]:
            template = sort_template
            with open("sorting_templates.json", "w") as f:
                data[sort_template][0] = True
                json.dump(data, f, indent=2)
            break
    if template == "":
        best_score = ("sort a", data["sort a"][1])
        for sort in data:
            if data[sort][1] > best_score[1]: best_score = (sort, data[sort][1])
        template = best_score[0]
    global current_sort
    current_sort = template
    if template == "sort a": sorter.sort_a(list_name)
    elif template == "sort b": sorter.sort_b(list_name)
    elif template == "sort c": sorter.sort_c(list_name)
    elif template == "sort d": sorter.sort_d(list_name)
    elif template == "sort e": sorter.sort_e(list_name)
    elif template == "sort f": sorter.sort_f(list_name)
    elif template == "sort g": sorter.sort_g(list_name)
    elif template == "sort h": sorter.sort_h(list_name)
    elif template == "sort i": sorter.sort_i(list_name)
    elif template == "sort j": sorter.sort_j(list_name)
    messagebox.showinfo("system update", "Your list has been sorted")


def score_sort(list_name, root, curr_frame):
    finished_list = True
    with open("lists.json") as rf:
        data = json.load(rf)
        curr_list = data[list_name]
    for task in curr_list:
        if not task[1]:
            finished_list = False
            break
    if finished_list:
        #sum up time list took to finish and add to score
        global current_sort
        score = 0
        for task in curr_list:
            score += task[2] - task[5]
        with open("sorting_templates.json") as rf:
            data = json.load(rf)
            data[current_sort][1] += score
            with open("sorting_templates.json", "w") as wf:
                json.dump(data, wf, indent=2)
        sort_list(list_name)
        load_list(list_name, root, curr_frame)


def show_about():
    url = "https://docs.google.com/document/d/11XoErCZp7__bgPXNzKR_mUDm_TOHd2FSd5p2P30XewM/edit?usp=sharing"
    webbrowser.open(url, new=1)


def get_time():
    full_time = str(datetime.datetime.now())
    full_time = full_time.split()
    time = full_time[1].split(".")[0]
    time = time.split(":")
    for i in range(len(time)):
        if time[i][0] == "0":
            if time[i][1] == "0" and i != 0: time[i] = "60"
            elif time[i][1] == "0" and i == 0: time[i] = "24"
            else: time[i] = time[i][1]
    time = ":".join(time)
    date = full_time[0].split("-")
    for i in range(len(date)):
        if date[i][0] == "0": date[i] = date[i][1]
    date = ":".join(date)
    curr_time = date + ":" + time
    return curr_time


def start_task(place, start_btn):
    with open("lists.json") as rf:
        data = json.load(rf)
        data[place[0]][place[1]][4] = get_time()
        with open("lists.json", "w") as wf:
            json.dump(data, wf, indent=2)
    start_btn.config(state=DISABLED)