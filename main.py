from tkinter import *
import tkinter.ttk
import getpass
import json
import functionalities

#a variable that saves the current list that is on the screen
curr_list = ""
curr_frame = ""

#A function to change the current list
def change_list(name):
    global curr_list
    global curr_frame
    print(f"change list name: {name}")
    curr_list = name
    print(f"change curr_list: {curr_list}")
    curr_frame = functionalities.load_list(name, root, curr_frame)
    list_title.config(text=curr_list)

root = Tk()

#sets app name, icon and size
root.geometry("1000x600")
root.title("Smart To Do")
#TODO: create and place app icon

#sets personal greeting message in top left corner
user_greeting_lbl = Label(text=f"Hello {getpass.getuser()}", font="Helvetica 15", padx=15, pady=30)
user_greeting_lbl.place(relx=0.02, rely=0.01)

#gets all the lists names
with open("lists.json") as f:
    lists = json.load(f)

#initiats a list that contains all lists names
user_lists = []

#append each name from the json file to the user_lists list as a button object
for list_name in lists:
    print(f"checkpoint A: {list_name}")
    user_lists.append(Button(root, text=list_name, font="Helvetica 14", padx=15, pady=20, borderwidth=0))

#places each button from the user_lists list on the screen
for i in range(len(user_lists)):
    y_pos = i/10+0.25
    print("list text:", user_lists[i].cget("text"))
    user_lists[i].config(command=lambda name_index = user_lists[i].cget("text"): change_list(name_index))
    user_lists[i].place(relx=0.02, rely=y_pos)

user_lists_len = (len(user_lists)+1)/10+0.1

#a dividing line between the lists buttons and the add list button
tkinter.ttk.Separator(root, orient=HORIZONTAL).place(relx=0.01, rely=user_lists_len+0.1, relwidth=0.15, relheight=1)

#creats and places on the screen the "add list" button
add_list_btn = Button(root, text="+ Add List", font="Helvetica 12 bold", padx=15, pady=30, borderwidth=0)
add_list_btn.place(relx=0.02, rely=user_lists_len+0.12)

#creats and places on the screen the "delete list" button
delete_list_btn = Button(root, text="- Delete List", font="Helvetica 12 bold",
                         padx=15, pady=20, borderwidth=0)
delete_list_btn.place(relx=0.02, rely=user_lists_len+0.22)


#separator between the main part of the app and the side bar
main_separator = tkinter.ttk.Separator(root, orient=VERTICAL)
main_separator.place(relx=0.2, rely=0, relwidth=0.2, relheight=1)

#sets curr_list variable
with open("lists.json") as f:
    lists = json.load(f)
    if curr_list == "": curr_list = next(iter(lists))
    else: curr_list = curr_list

#displays the list title
list_title = Label(root, text=curr_list, font="Helvetica 16 bold", padx=15, pady=30)
list_title.place(relx=0.55, rely=0.03)

#loads all the task bars on screen
functionalities.load_list(curr_list, root, curr_frame)

#an "add task" button
add_task_btn = Button(root, text="+ Add Task", font="Helvetica 14", padx=15, pady=15, borderwidth=0.5)
add_task_btn.place(relx=0.55, rely=0.85)

print("this is a git test")


root.mainloop()