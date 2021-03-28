import numpy as np
from Cmatrix_operations import *


def find_critical_path(schedule, time_matrix):
    tasks=len(schedule)
    machines=len(time_matrix[0])
    Cmatrix = count_Cmatrix(schedule, time_matrix)
    critical_path=[]
    critical_path.append((schedule[tasks-1], machines ))
    # idziemy od końca
    i=tasks-1
    j=machines-1

    while(True):
        if (j-1) < 0 and (i-1) <0 : # gdy przeszlimy po wszystkich maszynach to koniec
            break

        if (i - 1) < 0: # gdy nie ma zadan to poruszamy sie po maszynie
            j = j - 1
        elif (j-1) < 0: # gdy nie ma maszyn to poruszamy sie po zadaniach
            i = i - 1
        else:
            if Cmatrix[i][j-1] >= Cmatrix[i-1][j]: #porownujemy ktora operacja decyduje o wyborze sciezki
                j = j - 1
            else:
                i = i - 1

        critical_path.append((schedule[i], j+1)) # sciezka w formacie [ (zadanie, maszyna), (zadanie, maszyna) ... ]

    critical_path.reverse()

    return critical_path


def print_critical_path(critical_path):
    print("Critical path")
    for i in range(0,len(critical_path)):
        print("Krok",i,"Maszyna:",critical_path[i][1], "Zadanie:",critical_path[i][0])


def NEH_algorithm(tasks,machine,time_matrix):
    time_matrix=np.array(time_matrix)
    w2=np.sum(time_matrix,axis=1).tolist()
    w=[i * (-1) for i in w2]
    sorted_order=np.argsort(w,kind='mergesort') + 1
    schedule=[sorted_order[0]]
    for i in range (1,tasks):
        best_in=0
        temp_schedule=schedule
        for j in range(0,i+1):
            temp_schedule.insert(j,sorted_order[i])
            #print(temp_schedule)
            if j==0:
                Cmax=count_cmax(temp_schedule,time_matrix)
            else:
                Cmax_temp=count_cmax(temp_schedule,time_matrix)
                if (Cmax_temp<Cmax):
                    best_in=j
                    Cmax=Cmax_temp
            temp_schedule.pop(j)

        schedule.insert(best_in,sorted_order[i])
    return schedule,Cmax


def find_longest_on_critical_path(schedule,time_matrix):

    critical = find_critical_path(schedule,time_matrix)
    times_on_critical_path=[]

    for path in critical:
        times_on_critical_path.append((path[0],time_matrix[path[0]-1][path[1]-1]))   # format (zadanie, czas zadania)

    longest = max(times_on_critical_path, key=lambda item:item[1])[0] # wyciagamy najdluzsze zadanie (ze wzgledu na tuple jest lambda)

    return longest


def find_task_with_biggest_sum_of_operation_on_cirtical_path(schedule,time_matrix):
    critical = find_critical_path(schedule,time_matrix)
    task, machine = zip(*critical)
    biggest = max(task, key=task.count)
    return biggest


def extend_neh_version_1(tasks,machine,time_matrix):
    time_matrix=np.array(time_matrix)
    w2=np.sum(time_matrix,axis=1).tolist()
    w=[i * (-1) for i in w2]
    sorted_order=np.argsort(w,kind='mergesort') + 1
    schedule=[sorted_order[0]]

    for i in range (1,tasks):
        best_in=0
        temp_schedule=schedule

        for j in range(0,i+1):
            temp_schedule.insert(j,sorted_order[i])

            if j == 0:
                Cmax = count_cmax(temp_schedule,time_matrix)
            else:
                Cmax_temp = count_cmax(temp_schedule,time_matrix)
                if Cmax_temp < Cmax:
                    best_in = j
                    Cmax = Cmax_temp

            temp_schedule.pop(j)

        schedule.insert(best_in,sorted_order[i])

        """
        Zaczynamy krok 5
        """
        longest_task = find_longest_on_critical_path(temp_schedule,time_matrix)
        schedule.remove(longest_task)

        temp_schedule = schedule
        for j in range(0,i+1):
            temp_schedule.insert(j,longest_task)

            if j == 0:
                Cmax = count_cmax(temp_schedule,time_matrix)
            else:
                Cmax_temp = count_cmax(temp_schedule,time_matrix)
                if Cmax_temp < Cmax:
                    best_in = j
                    Cmax = Cmax_temp

            temp_schedule.pop(j)

        schedule.insert(best_in,longest_task)

    return schedule,Cmax

def extend_neh_version_2(tasks,machine,time_matrix):
    time_matrix=np.array(time_matrix)
    w2=np.sum(time_matrix,axis=1).tolist()
    w=[i * (-1) for i in w2]
    sorted_order=np.argsort(w,kind='mergesort') + 1
    schedule=[sorted_order[0]]

    for i in range (1,tasks):
        best_in=0
        temp_schedule=schedule

        for j in range(0,i+1):
            temp_schedule.insert(j,sorted_order[i])

            if j == 0:
                Cmax = count_cmax(temp_schedule,time_matrix)
            else:
                Cmax_temp = count_cmax(temp_schedule,time_matrix)
                if Cmax_temp < Cmax:
                    best_in = j
                    Cmax = Cmax_temp

            temp_schedule.pop(j)

        schedule.insert(best_in,sorted_order[i])

        """
        Zaczynamy krok 5
        """
        longest_task = find_task_with_biggest_sum_of_operation_on_cirtical_path(temp_schedule,time_matrix)
        schedule.remove(longest_task)

        temp_schedule = schedule
        for j in range(0,i+1):
            temp_schedule.insert(j,longest_task)

            if j == 0:
                Cmax = count_cmax(temp_schedule,time_matrix)
            else:
                Cmax_temp = count_cmax(temp_schedule,time_matrix)
                if Cmax_temp < Cmax:
                    best_in = j
                    Cmax = Cmax_temp

            temp_schedule.pop(j)

        schedule.insert(best_in,longest_task)

    return schedule,Cmax

