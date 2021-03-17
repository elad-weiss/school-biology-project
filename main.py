from tkinter import *
import tkinter.ttk
import getpass
import json
import functionalities


class main_window:
    def __init__(self):
        # a variable that saves the current list that is on the screen
        self.curr_list = ""
        self.curr_frame = ""

        self.root = Tk()

        #sets app name, icon and size
        self.root.geometry("1000x600")
        self.root.title("Smart To Do")
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
            user_lists.append(Button(self.root, text=list_name, font="Helvetica 14", padx=15, borderwidth=0))

        #places each button from the user_lists list on the screen
        for i in range(len(user_lists)):
            y_pos = i/10+0.17
            user_lists[i].config(command=lambda name_index = user_lists[i].cget("text"): self.change_list(name_index))
            user_lists[i].place(relx=0.02, rely=y_pos)

        user_lists_len = (len(user_lists)+1)/10+0.01

        #a dividing line between the lists buttons and the add list button
        tkinter.ttk.Separator(self.root, orient=HORIZONTAL).place(relx=0.01, rely=user_lists_len+0.1, relwidth=0.15, relheight=1)

        #creats and places on the screen the "add list" button
        add_list_btn = Button(self.root, text="+ Add List", font="Helvetica 12 bold", padx=15, pady=15, borderwidth=0,
                              command=lambda: functionalities.add_list(self.root))
        add_list_btn.place(relx=0.02, rely=user_lists_len+0.12)

        #creats and places on the screen the "delete list" button
        delete_list_btn = Button(self.root, text="- Delete List", font="Helvetica 12 bold",
                                 padx=15, pady=15, borderwidth=0, command=lambda: functionalities.delete_list(self.root))
        delete_list_btn.place(relx=0.02, rely=user_lists_len+0.22)


        #separator between the main part of the app and the side bar
        main_separator = tkinter.ttk.Separator(self.root, orient=VERTICAL)
        main_separator.place(relx=0.2, rely=0, relwidth=0.2, relheight=1)

        #sets curr_list variable
        with open("lists.json") as f:
            lists = json.load(f)
            if self.curr_list == "": self.curr_list = next(iter(lists))
            else: self.curr_list = self.curr_list

        #displays the list title
        self.list_title = Label(self.root, text=self.curr_list, font="Helvetica 16 bold", padx=15, pady=30)
        self.list_title.place(relx=0.55, rely=0.03)

        #loads all the task bars on screen
        functionalities.load_list(self.curr_list, self.root, self.curr_frame)

        #an "add task" button
        add_task_btn = Button(self.root, text="+ Add Task", font="Helvetica 14", padx=15, pady=15, borderwidth=0.5,
                              command=lambda: functionalities.add_task(self.curr_list, self.root, self.curr_frame))
        add_task_btn.place(relx=0.55, rely=0.85)

        about_btn = Button(self.root, text="ABOUT", font="Helvetica 14", command=functionalities.show_about)
        about_btn.place(relx=0.90, rely=0.90)

        self.root.mainloop()

    # A function to change the current list
    def change_list(self, name):
        self.curr_list = name
        self.curr_frame = functionalities.load_list(name, self.root, self.curr_frame)
        self.list_title.config(text=self.curr_list)

if __name__ == '__main__':
    main_window()