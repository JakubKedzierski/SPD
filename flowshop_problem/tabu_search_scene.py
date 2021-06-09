import numpy as np
from Cmatrix_operations import *
from johnson_algorithm import *
from nehs_algorithm import *
import random
import time

def generate_modyfied_random_neighbourhood(current_schedule, tabu_list_schedule, tabu_list_movements): #kazde zadanie jest wymieniane z losowym innym

    neighbourhood = []
    neighbourhood_movements = []

    for i in range(0, len(current_schedule)-1):
        first = i

        is_on_banned_list = False
        while True:
            first = random.randint(0, len(current_schedule) - 2)
            second = random.randint(0, len(current_schedule) - 1)
            if second == first:
                second += 1

            schedule = current_schedule.copy()
            schedule[first], schedule[second] = schedule[second], schedule[first]
            is_on_banned_list = False

            for j in range(0, len(tabu_list_schedule)):
                if schedule == tabu_list_schedule[j]:
                    is_on_banned_list = True
                    break


            for banned_move in tabu_list_movements:
                if first == banned_move[0] and second == banned_move[1]:
                    is_on_banned_list = True
                    break

            if not is_on_banned_list:
                break

        neighbourhood.append(schedule)
        neighbourhood_movements.append((first, second))

    return neighbourhood, neighbourhood_movements

def tabu_search_scene(tasks,machines,time_matrix):
    tabu_list_max_size = 30
    max_iter = 400

    schedule, stuff = johnson_for_N_machines(tasks,machines,time_matrix)

    current_schedule = schedule
    best_schedule = schedule
    best_cmax = count_cmax(schedule, time_matrix)
    tabu_list = []
    tabu_list_movements = []
    counter = 0

    start = time.time()
    end = time.time()
    elapsed = end - start
    while elapsed < 60:

    #while counter < max_iter:
        counter += 1
        #neighbourhood = generate_modyfied_random_neighbourhood_insert(current_schedule, tabu_list)
        neighbourhood, neighbourhood_movements = generate_modyfied_random_neighbourhood(current_schedule, tabu_list, tabu_list_movements)
        if len(neighbourhood) == 0:
            continue

        neighbour_best_cmax = count_cmax(neighbourhood[0], time_matrix)
        best_neighbour = neighbourhood[0]
        index_best_neighbour = 0

        for i in range(1,len(neighbourhood)):
            schedule = neighbourhood[i]
            cmax = count_cmax(schedule,time_matrix)

            if cmax < neighbour_best_cmax:
                neighbour_best_cmax = cmax
                best_neighbour = schedule
                index_best_neighbour = i

        current_schedule = best_neighbour

        if len(tabu_list) > tabu_list_max_size:
            tabu_list.pop(0)

        if len(tabu_list_movements) > tabu_list_max_size:
            tabu_list_movements.pop(0)

        tabu_list.append(current_schedule)
        tabu_list_movements.append(neighbourhood_movements[index_best_neighbour])

        if neighbour_best_cmax < best_cmax:
            best_cmax = neighbour_best_cmax
            best_schedule = best_neighbour
            in_row_number = 0

        end = time.time()
        elapsed = end - start


    return best_schedule, best_cmax

