import numpy as np
from Cmatrix_operations import *
from johnson_algorithm import *
from nehs_algorithm import *
import random
import time

def generate_random_neighbourhood(current_schedule, tabu_list): # zadana liczba wymian
    neighbour_rand_number = 30

    neighbourhood = []
    for i in range(0, neighbour_rand_number):
        schedule = current_schedule.copy()
        first = random.randint(0, len(schedule) - 2)
        second = random.randint(0, len(schedule) - 1)
        if second == first:
            second += 1

        schedule[first], schedule[second] = schedule[second], schedule[first]

        is_on_banned_list = False
        for j in range(0, len(tabu_list)):
            if schedule == tabu_list[j]:
                is_on_banned_list = True
                break

        if not is_on_banned_list:
            neighbourhood.append(schedule)

    return neighbourhood

def generate_modyfied_random_neighbourhood(current_schedule, tabu_list): #kazde zadanie jest wymieniane z losowym innym

    neighbourhood = []
    for i in range(0, len(current_schedule)-1):
        schedule = current_schedule.copy()
        first = i
        second = random.randint(0, len(schedule) - 1)
        if second == first:
            second += 1

        schedule[first], schedule[second] = schedule[second], schedule[first]

        is_on_banned_list = False
        for j in range(0, len(tabu_list)):
            if schedule == tabu_list[j]:
                is_on_banned_list = True
                break


        if not is_on_banned_list:
            neighbourhood.append(schedule)

    return neighbourhood


def generate_modyfied_random_neighbourhood_insert(current_schedule, tabu_list): #kazde zadanie jest wstawiane w losowe miejsce

    neighbourhood = []
    for i in range(0, len(current_schedule)):
        schedule = current_schedule.copy()
        first = schedule.pop(i)
        second = random.randint(0, len(schedule) - 1)
        while (second==i):
            second = random.randint(0, len(schedule) - 1)

        schedule.insert(second,first)

        is_on_banned_list = False
        for j in range(0, len(tabu_list)):
            if schedule == tabu_list[j]:
                is_on_banned_list = True
                break


        if not is_on_banned_list:
            neighbourhood.append(schedule)

    return neighbourhood



def generate_all_neighbourhood_insert(schedule):
    neighbourhood=[]
    for i in range(0,len(schedule)):
        temp_schedule=schedule.copy()
        current=temp_schedule.pop(i)
        for j in range(0,len(schedule)):
            if j!=i and j!=i-1:
                temp_schedule.insert(j,current)
                neighbourhood.append(temp_schedule.copy())
                temp_schedule.pop(j)
    
    return neighbourhood


def generate_all_neighbourhood_swap(schedule):
    neighbourhood=[]
    for i in range(0,len(schedule)):
        temp_schedule=schedule.copy()
        for j in range(i+1,len(schedule)):
            temp_schedule[i],temp_schedule[j]=temp_schedule[j],temp_schedule[i]
            neighbourhood.append(temp_schedule.copy())
            temp_schedule[i],temp_schedule[j]=temp_schedule[j],temp_schedule[i]
    
    return neighbourhood


def tabu_search_with_all_neighbours(tasks,machines,time_matrix):
    tabu_list_max_size = 15
    max_iter = 30
    schedule, stuff = johnson_for_N_machines(tasks,machines,time_matrix)

    current_schedule = schedule
    best_schedule = schedule
    best_cmax = count_cmax(schedule, time_matrix)
    tabu_list = []
    tabu_list.append(current_schedule)

    for i in range(0,max_iter):
        neighbourhood=generate_all_neighbourhood_insert(current_schedule)
        #neighbourhood=generate_all_neighbourhood_swap(current_schedule)
        current_best_Cmax=count_cmax(neighbourhood[0],time_matrix)
        current_best_schedule=neighbourhood[0]
        for j in range(1,len(neighbourhood)):
            is_on_tabu_list=False
            for k in tabu_list:
                if neighbourhood[j]==k:
                    is_on_tabu_list=True
                    break
            if (is_on_tabu_list==False):
                current_cmax=count_cmax(neighbourhood[j],time_matrix)
                if (current_cmax<current_best_Cmax):
                    current_best_Cmax=current_cmax
                    current_best_schedule=neighbourhood[j]
        
        current_schedule=current_best_schedule
        tabu_list.append(current_schedule)
        if (len(tabu_list)>tabu_list_max_size):
            tabu_list.pop(0)
        if (current_best_Cmax<best_cmax):
            best_cmax=current_best_Cmax
            best_schedule=current_schedule
    
    return best_schedule, best_cmax




def tabu_search(tasks,machines,time_matrix):
    tabu_list_max_size = 15
    max_iter = 30

    #schedule = [i for i in range(1, tasks+1)]
    #random.shuffle(schedule)

    schedule, stuff = johnson_for_N_machines(tasks,machines,time_matrix)

    current_schedule = schedule
    best_schedule = schedule
    best_cmax = count_cmax(schedule, time_matrix)
    tabu_list = []
    tabu_list.append(current_schedule)
    counter = 0

    """
    in_row_number = 0
    in_row = False
    while not in_row:
    """

    #start = time.time()
    #end = time.time()
    #elapsed = end - start
    #while elapsed < 10:


    while counter < max_iter:
        counter += 1

        #neighbourhood = generate_modyfied_random_neighbourhood_insert(current_schedule, tabu_list)
        neighbourhood = generate_modyfied_random_neighbourhood(current_schedule, tabu_list)
        if len(neighbourhood)==0:
            continue
        neighbour_best_cmax = count_cmax(neighbourhood[0], time_matrix)
        best_neighbour = neighbourhood[0]

        for schedule in neighbourhood[1:]:
            cmax = count_cmax(schedule,time_matrix)

            if cmax < neighbour_best_cmax:
                neighbour_best_cmax = cmax
                best_neighbour = schedule

        current_schedule = best_neighbour

        if len(tabu_list) > tabu_list_max_size:
            tabu_list.pop(0)

        tabu_list.append(current_schedule)

        if neighbour_best_cmax < best_cmax:
            best_cmax = neighbour_best_cmax
            best_schedule = best_neighbour
            in_row_number = 0

        """
        else:
            in_row_number = in_row_number + 1

        if in_row_number > 50:
            in_row = True
        """

        #end = time.time()
        #elapsed = end - start

    return best_schedule, best_cmax



def generate_all_neighbourhood_swap_with_break(schedule,best_cmax,time_matrix,tabu_list):
    found=False
    current_best_schedule=schedule.copy()
    current_best_Cmax=np.iinfo(np.int32).max
    for i in range(0,len(schedule)):
        temp_schedule=schedule.copy()
        for j in range(i+1,len(schedule)):
            temp_schedule[i],temp_schedule[j]=temp_schedule[j],temp_schedule[i]
            is_on_tabu_list=False
            for k in tabu_list:
                if (temp_schedule == k):
                    is_on_tabu_list=True
                    break
            if (is_on_tabu_list==True):
                continue
            current_Cmax=count_cmax(temp_schedule,time_matrix)
            if current_Cmax<current_best_Cmax:
                current_best_schedule=temp_schedule.copy()
                current_best_Cmax=current_Cmax
                if (current_best_Cmax<best_cmax):
                    found=True
                    return current_best_Cmax, current_best_schedule,found
            temp_schedule[i],temp_schedule[j]=temp_schedule[j],temp_schedule[i]
    
    return current_best_Cmax,current_best_schedule,found



def tabu_search_FIN(tasks,machines,time_matrix):
    tabu_list_max_size = 15
    max_iter = 50
    schedule, stuff = johnson_for_N_machines(tasks,machines,time_matrix)

    current_schedule = schedule
    best_schedule = schedule
    best_cmax = count_cmax(schedule, time_matrix)
    tabu_list = []
    tabu_list.append(current_schedule)

    for i in range(0,max_iter):
        current_best_Cmax,current_best_schedule,found=generate_all_neighbourhood_swap_with_break(current_schedule,best_cmax,time_matrix,tabu_list)
        if current_best_schedule==current_schedule: #wszyscy sasiedzi byli na liscie tabu
            break
        if (found==True):
            best_cmax=current_best_Cmax
            best_schedule=current_best_schedule
        current_schedule=current_best_schedule
        tabu_list.append(current_schedule)
        if (len(tabu_list)>tabu_list_max_size):
            tabu_list.pop(0)

    
    return best_schedule, best_cmax

