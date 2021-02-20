from tkinter import *
import tkinter.ttk
import getpass
import json

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
    user_lists.append(Button(root, text=list_name, font="Helvetica 14", padx=15, pady=20, borderwidth=0))

#places each button from the user_lists list on the screen
for i in range(len(user_lists)):
    y_pos = i/10+0.25
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


root.mainloop()