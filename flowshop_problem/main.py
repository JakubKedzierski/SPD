from Cmatrix_operations import *
from nehs_algorithm import *
from johnson_algorithm import *
import pandas as pd
import numpy as np
from itertools import permutations


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
    if tasks!=len(time_matrix):
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



def main():
    path=""
    file_name="./datasets/" + "data011.txt"
    number_of_datasets_to_read=1

    try:
        with open(path+file_name, "r") as file:
            for i in range(0,number_of_datasets_to_read):

                tasks,machines,time_matrix=read_data_set(file)     

                
                schedule_from_func,Cmax=extend_neh_version_1(tasks,machines,time_matrix)
                print(schedule_from_func,Cmax)
                schedule_from_func,Cmax=extend_neh_version_2(tasks,machines,time_matrix)
                print(schedule_from_func,Cmax)
                schedule_from_func,Cmax=extend_neh_version_3(tasks,machines,time_matrix)
                print(schedule_from_func,Cmax)
                schedule_from_func,Cmax=extend_neh_version_4(tasks,machines,time_matrix)
                print(schedule_from_func,Cmax)
                schedule_from_func,Cmax=NEH_algorithm(tasks,machines,time_matrix)
                print(schedule_from_func,Cmax)

                
                #schedule_from_func,Cmax=total_review(tasks,machines,time_matrix)
                #print(schedule_from_func,Cmax)


                #draw_gantt(schedule_from_func,time_matrix)

    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError


if __name__ == '__main__':
    main()



