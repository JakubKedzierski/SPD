from Cmatrix_operations import *
from nehs_algorithm import *
from johnson_algorithm import *
from tabu_search import *
import pandas as pd
import numpy as np
from itertools import permutations
import time


def read_file_with_lots_of_datasets(file):
    file.readline()
    
    tasks, machines, time_matrix = read_data_set(file)

    file.readline()
    file.readline()
    Cmax = int(file.readline())
    schedule= [int(x) for x in next(file).split()] 
    file.readline()

    return tasks,machines,time_matrix,Cmax,schedule


def read_data_set(file):
    tasks, machines = [int(x) for x in next(file).split()] 
    time_matrix = [] 

    for i in range(0,tasks):
        time_matrix.append([int(x) for x in next(file).split()])

    return tasks, machines, time_matrix



def total_review(tasks,machines,time_matrix):
    if tasks != len(time_matrix):
        raise ValueError('Invalid tasks number')
    if machines!=len(time_matrix[0]):
        raise ValueError('Invalid machines number')
    schedules=list(permutations(range(1,tasks+1)))
    Cmax=0
    schedule_index=0
    for k in range(0,len(schedules)):
        Cmax_func=count_cmax(schedules[k],time_matrix)
        if k==0:
            Cmax=Cmax_func
            schedule_index=k
        if Cmax>Cmax_func:
            Cmax=Cmax_func
            schedule_index=k
    return schedules[schedule_index],Cmax

def find_critical_path_v2(schedule, time_matrix):
    tasks=len(schedule)
    machines=len(time_matrix[0])
    Cmatrix = count_Cmatrix(schedule, time_matrix)
    critical_path=[]
    critical_path.append((schedule[tasks-1], machines ))
    # idziemy od końca
    i=tasks-1
    j=machines-1
    paths = 1
    while(True):
        if (j-1) < 0 and (i-1) <0 : # gdy przeszlimy po wszystkich maszynach to koniec
            break

        if (i - 1) < 0: # gdy nie ma zadan to poruszamy sie po maszynie
            j = j - 1
        elif (j-1) < 0: # gdy nie ma maszyn to poruszamy sie po zadaniach
            i = i - 1
        else:
            if Cmatrix[i][j-1] > Cmatrix[i-1][j]: #porownujemy ktora operacja decyduje o wyborze sciezki
                j = j - 1
            elif Cmatrix[i][j-1] == Cmatrix[i-1][j]:
                i = i - 1
                
            elif Cmatrix[i][j-1] < Cmatrix[i-1][j]:
                i = i - 1

        critical_path.append((schedule[i], j+1)) # sciezka w formacie [ (zadanie, maszyna), (zadanie, maszyna) ... ]

    critical_path.reverse()

    return critical_path

def main():
    path=""
    file_name="./datasets/" + "data4.txt"
    number_of_datasets_to_read= 1

    try:
        with open(path + file_name, "r") as file:
            for i in range(0, number_of_datasets_to_read):
                tasks, machines, time_matrix = read_data_set(file)

                start = time.time()
                schedule_from_func, Cmax = tabu_search(tasks, machines, time_matrix)
                end = time.time()
                elapsed = end - start
                print(schedule_from_func)
                print("Cmax: ",Cmax)
                print("Time: ",elapsed)

                start = time.time()
                schedule_from_func, Cmax = NEH_algorithm(tasks, machines, time_matrix)
                end = time.time()
                elapsed = end - start
                print(schedule_from_func)
                print("Cmax: ",Cmax)
                print("Time: ",elapsed)

                start = time.time()
                schedule_from_func, Cmax = extend_neh_version_2(tasks, machines, time_matrix)
                end = time.time()
                elapsed = end - start
                print(schedule_from_func)
                print("Cmax: ",Cmax)
                print("Time: ",elapsed)


    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError




if __name__ == '__main__':
    main()




