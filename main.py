from tkinter import *
import tkinter.ttk
import getpass
import json

root = Tk()

#sets app name and icon
root.title("Smart To Do")
#TODO: create and place app icon

#sets personal greeting message in top left corner
user_greeting_lbl = Label(text=f"Hello {getpass.getuser()}", font="Helvetica 15", padx=15, pady=30)
user_greeting_lbl.grid(column=0, row=0)

#gets all the lists names
with open("lists.json") as f:
    lists = json.load(f)

#a spacing between the greeting and all the lists buttons
Label(root, text=" ", padx=15, pady=40).grid(column=0, row=1)

#initiats a list that contains all lists names
user_lists = []

#append each name from the json file to the user_lists list as a button object
for list_name in lists:
    user_lists.append(Button(root, text=list_name, font="Helvetica 14", padx=15, pady=20, borderwidth=0))

#places each button from the user_lists list on the screen
for i in range(len(user_lists)):
    user_lists[i].grid(column=0, row=i+2)

user_lists_len = len(user_lists)

#a dividing line between the lists buttons and the add list button
tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=user_lists_len+3,
                                                    columnspan=1, sticky="we", pady=10)

#creats and places on the screen the "add list" button
add_list_btn = Button(root, text="+ Add List", font="Helvetica 12 bold", padx=15, pady=30, borderwidth=0)
add_list_btn.grid(column=0, row=user_lists_len+4)

delete_list_btn = Button(root, text="- Delete List", font="Helvetica 12 bold",
                         padx=15, pady=20, borderwidth=0)
delete_list_btn.grid(column=0, row=user_lists_len+5)


root.mainloop()