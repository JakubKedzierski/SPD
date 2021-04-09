import numpy as np
from Cmatrix_operations import *
from johnson_algorithm import *
import random

def tabu_search(tasks,machines,time_matrix):
    tabu_list_max_size = 15
    max_iter = 100
    neighbour_rand_number = 10

    # z randomowymi wartosciami na starcie dawalo czasy minimalnie lepsze od johnsona
    # ze swapem po kolei typu 1-2, 2-3, 3-4, 4-5 dawalo slabe wyniki, random znacznie lepiej

    #schedule = [i for i in range(1, tasks+1)]
    #random.shuffle(schedule)
    schedule,stuff = johnson_for_N_machines(tasks,machines,time_matrix)

    current_schedule = schedule
    best_schedule = schedule
    best_cmax = count_cmax(schedule,time_matrix)
    tabu_list = []
    tabu_list.append(current_schedule)
    counter = 0

    while counter < max_iter:
        counter += 1

        neighbourhood = []
        for i in range(0, neighbour_rand_number):
            schedule = current_schedule.copy()
            first = random.randint(0,len(schedule)-2)
            second = random.randint(0, len(schedule) - 1)
            if second == first:
                second += 1

            schedule[first], schedule[second] = schedule[second], schedule[first]

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

    return best_schedule,best_cmax