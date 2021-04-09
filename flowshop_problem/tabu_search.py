import numpy as np
from Cmatrix_operations import *
import random

def tabu_search(tasks,machine,time_matrix):
    tabu_list_max_size = 20
    schedule = [i for i in range(1, tasks+1)]
    random.shuffle(schedule)

    current_schedule = schedule
    best_schedule = schedule
    best_cmax = count_cmax(schedule,time_matrix)
    tabu_list = []
    tabu_list.append(current_schedule)
    counter = 0
    max_iter = 200

    while counter < max_iter:
        counter += 1

        neighbourhood = []
        for i in range(0,len(current_schedule)-1):
            schedule = current_schedule.copy()
            schedule[i], schedule[i+1] = schedule[i+1], schedule[i]

            is_on_banned_list = False
            for j in range(0,len(tabu_list)):
                if schedule == tabu_list[j]:
                    is_on_banned_list = True
                    break

            if not is_on_banned_list:
                neighbourhood.append(schedule)

        neighbour_best_cmax = count_cmax(neighbourhood[0], time_matrix)
        best_neighbour = neighbourhood[0]
        for schedule in neighbourhood[1:]:
            cmax = count_cmax(schedule,time_matrix)

            if cmax < neighbour_best_cmax:
                neighbour_best_cmax = cmax
                best_neighbour = schedule

        current_schedule = best_neighbour

        if len(tabu_list) > tabu_list_max_size:
            tabu_list.pop()

        tabu_list.append(current_schedule)

        if neighbour_best_cmax < best_cmax:
            best_cmax = neighbour_best_cmax
            best_schedule = best_neighbour

    return schedule,best_cmax