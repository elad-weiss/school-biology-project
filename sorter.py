import json

#this file contains all the sorting functions
#the functions are based on the bubble sort algorithm

#sorts tasks from shortest to longest
def sort_a(list_name):
    with open("lists.json") as rf:
        data = json.load(rf)
    for i in range(len(data[list_name])-1, 0, -1):
        for t in range(i):
            if data[list_name][t][2] > data[list_name][t+1][2]:
                temp = data[list_name][t]
                data[list_name][t] = data[list_name][t+1]
                data[list_name][t+1] = temp
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)

#sorts tasks from longest to shortest
def sort_b(list_name):
    with open("lists.json") as rf:
        data = json.load(rf)
    for i in range(len(data[list_name]) - 1, 0, -1):
        for t in range(i):
            if data[list_name][t][2] < data[list_name][t + 1][2]:
                temp = data[list_name][t]
                data[list_name][t] = data[list_name][t + 1]
                data[list_name][t + 1] = temp
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)

#sorts one short task on long task
def sort_c(list_name):
    sort_a(list_name)
    with open("lists.json") as rf:
        data = json.load(rf)
    curr_list = data[list_name]
    sorted_list = []
    for i in range(len(curr_list)-1):
        if i % 2 == 0: sorted_list.append(curr_list[int(i/2)])
        else: sorted_list.append(curr_list[len(curr_list)-int(i/2)-1])
    data[list_name] = sorted_list
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)

#sorts all the liked tasks to be first and all the disliked task last
def sort_d(list_name):
    with open("lists.json") as rf:
        data = json.load(rf)
    for i in range(len(data[list_name]) - 1, 0, -1):
        for t in range(i):
            if data[list_name][t][3] < data[list_name][t + 1][3]:
                temp = data[list_name][t]
                data[list_name][t] = data[list_name][t + 1]
                data[list_name][t + 1] = temp
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)

#sorts all the disliked tasks to be first and all the liked task last
def sort_e(list_name):
    with open("lists.json") as rf:
        data = json.load(rf)
    for i in range(len(data[list_name]) - 1, 0, -1):
        for t in range(i):
            if data[list_name][t][3] > data[list_name][t + 1][3]:
                temp = data[list_name][t]
                data[list_name][t] = data[list_name][t + 1]
                data[list_name][t + 1] = temp
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)

#sorts one liked task one disliked task
def sort_f(list_name):
    sort_d(list_name)
    with open("lists.json") as rf:
        data = json.load(rf)
    curr_list = data[list_name]
    sorted_list = []
    for i in range(len(curr_list)):
        if i % 2 == 0: sorted_list.append(curr_list[int(i/2)])
        else: sorted_list.append(curr_list[len(curr_list)-int(i/2)-1])
    data[list_name] = sorted_list
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)

#sorts liked first and disliked last when in each sublist(liked and disliked) its shorted from shortest to longest
def sort_g(list_name):
    sort_d(list_name)
    with open("lists.json") as rf:
        data = json.load(rf)
    base_list = data[list_name]
    for i in range(len(base_list)):
        if not base_list[i][3]:
            base_list = [base_list[0:i], base_list[i:len(base_list)]]
            break
    for curr_list in base_list:
        for i in range(len(curr_list)-1):
            for j in range(0, len(curr_list)-i-1):
                if curr_list[j][2] > curr_list[j + 1][2]:
                    curr_list[j], curr_list[j + 1] = curr_list[j + 1], curr_list[j]
    base_list = base_list[0] + base_list[1]
    data[list_name] = base_list
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)

#sorts liked first and disliked last when in each sublist(liked and disliked) its shorted from longest to shortest
def sort_h(list_name):
    sort_d(list_name)
    with open("lists.json") as rf:
        data = json.load(rf)
    base_list = data[list_name]
    for i in range(len(base_list)):
        if not base_list[i][3]:
            base_list = [base_list[0:i], base_list[i:len(base_list)]]
            break
    for curr_list in base_list:
        for i in range(len(curr_list) - 1):
            for j in range(0, len(curr_list) - i - 1):
                if curr_list[j][2] < curr_list[j + 1][2]:
                    curr_list[j], curr_list[j + 1] = curr_list[j + 1], curr_list[j]
    base_list = base_list[0] + base_list[1]
    data[list_name] = base_list
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)

#sorts disliked first and liked last when in each sublist(liked and disliked) its shorted from shortest to longest
def sort_i(list_name):
    sort_e(list_name)
    with open("lists.json") as rf:
        data = json.load(rf)
    base_list = data[list_name]
    for i in range(len(base_list)):
        if base_list[i][3]:
            base_list = [base_list[0:i], base_list[i:len(base_list)]]
            break
    for curr_list in base_list:
        for i in range(len(curr_list) - 1):
            for j in range(0, len(curr_list) - i - 1):
                if curr_list[j][2] > curr_list[j + 1][2]:
                    curr_list[j], curr_list[j + 1] = curr_list[j + 1], curr_list[j]
    base_list = base_list[0] + base_list[1]
    data[list_name] = base_list
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)

#sorts disliked first and liked last when in each sublist(liked and disliked) its shorted from longest to shortest
def sort_j(list_name):
    sort_e(list_name)
    with open("lists.json") as rf:
        data = json.load(rf)
    base_list = data[list_name]
    for i in range(len(base_list)):
        if base_list[i][3]:
            base_list = [base_list[0:i], base_list[i:len(base_list)]]
            break
    for curr_list in base_list:
        for i in range(len(curr_list) - 1):
            for j in range(0, len(curr_list) - i - 1):
                if curr_list[j][2] < curr_list[j + 1][2]:
                    curr_list[j], curr_list[j + 1] = curr_list[j + 1], curr_list[j]
    base_list = base_list[0] + base_list[1]
    data[list_name] = base_list
    with open("lists.json", "w") as wf:
        json.dump(data, wf, indent=2)