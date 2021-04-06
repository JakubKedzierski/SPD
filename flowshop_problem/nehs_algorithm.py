import numpy as np
from Cmatrix_operations import *


def find_critical_path(schedule, time_matrix):
    tasks=len(schedule)
    machines=len(time_matrix[0])
    Cmatrix = count_Cmatrix(schedule, time_matrix)
    critical_path=[]
    critical_path_list=[]
    critical_path.append((schedule[tasks-1], machines ))
    # idziemy od końca
    i = tasks-1 # zadanie do dodania na sciezce
    j = machines-1 # maszyna do dodania na sciezce
    correct=True
    while(True):
        if (j-1) < 0 and (i-1) <0 : # gdy przeszlimy po wszystkich maszynach to koniec
            break

        if i == 0: # gdy nie ma zadan to poruszamy sie po maszynie
            if Cmatrix[i][j-1] == (Cmatrix[i][j]-time_matrix[schedule[i]-1][j]):
                j = j-1
            else:
                correct = False
                break

        elif j == 0: # gdy nie ma maszyn to poruszamy sie po zadaniach
            if Cmatrix[i-1][j] == (Cmatrix[i][j]-time_matrix[schedule[i]-1][j]):
                i = i-1
            else:
                correct = False
                break

        elif Cmatrix[i][j-1] == Cmatrix[i-1][j]: # gdy czas zakonczenia na poprzedniej maszynie i zadaniu
            if Cmatrix[i-1][j] == (Cmatrix[i][j]-time_matrix[schedule[i]-1][j]): # oraz gdy na sciezce krytycznej
                critical_path_copy=critical_path.copy()
                critical_path_copy.append((schedule[i-1],j+1))
                critical_paths,found=find_next_critical_path(schedule, time_matrix,critical_path_copy,Cmatrix,i-1,j) # szukaj kolejnej ścieżki

                if found:
                    for k in range(0, len(critical_paths)):
                        critical_path_list.append(critical_paths[k])
                j = j-1
            else:
                correct = False
                break

        elif Cmatrix[i][j-1] == (Cmatrix[i][j]-time_matrix[schedule[i]-1][j]):
            j = j-1

        elif Cmatrix[i-1][j] == (Cmatrix[i][j]-time_matrix[schedule[i]-1][j]):
            i = i-1
        else:
            correct = False
            break

        critical_path.append((schedule[i], j+1)) # sciezka w formacie [ (zadanie, maszyna), (zadanie, maszyna) ... ]

    if correct:
        critical_path.reverse()
        critical_path_list.append(critical_path)

    return critical_path_list


def find_next_critical_path(schedule, time_matrix,critical_path,Cmatrix,i,j):
    critical_path_list=[]
    correct=True
    overall_correct=False

    while(True):
        if (j-1) < 0 and (i-1) <0 : # gdy przeszlimy po wszystkich maszynach to koniec
            break

        if i == 0: # gdy nie ma zadan to poruszamy sie po maszynie
            if Cmatrix[i][j-1]==(Cmatrix[i][j]-time_matrix[schedule[i]-1][j]):
                j = j-1
            else:
                correct = False
                break
        elif j == 0:
            if Cmatrix[i-1][j] == (Cmatrix[i][j]-time_matrix[schedule[i]-1][j]):
                i = i-1
            else:
                correct = False
                break
        elif Cmatrix[i][j-1] == Cmatrix[i-1][j]:
            if Cmatrix[i-1][j] == (Cmatrix[i][j]-time_matrix[schedule[i]-1][j]):
                critical_path_copy=critical_path.copy()
                critical_path_copy.append((schedule[i-1],j+1))
                critical_paths,found=find_next_critical_path(schedule, time_matrix,critical_path_copy,Cmatrix,i-1,j)

                if found == True:
                    overall_correct=True
                    for k in range(0,len(critical_paths)):
                        critical_path_list.append(critical_paths[k])
                j=j-1
            else:
                correct=False
                break
        elif Cmatrix[i][j-1] == (Cmatrix[i][j]-time_matrix[schedule[i]-1][j]):
            j=j-1
        elif Cmatrix[i-1][j] == (Cmatrix[i][j]-time_matrix[schedule[i]-1][j]):
            i=i-1
        else:
            correct=False
            break

        critical_path.append((schedule[i], j+1)) # sciezka w formacie [ (zadanie, maszyna), (zadanie, maszyna) ... ]

    if correct:
        critical_path.reverse()
        critical_path_list.append(critical_path)
        overall_correct = True
    
    return critical_path_list,overall_correct


def print_critical_path(critical_path):
    print("Critical path")
    for i in range(0,len(critical_path)):
        print("Krok",i,"Maszyna:",critical_path[i][1], "Zadanie:",critical_path[i][0])


def NEH_algorithm(tasks,machine,time_matrix):
    time_matrix=np.array(time_matrix)
    w2=np.sum(time_matrix,axis=1).tolist() # wyznaczenie priorytetów
    w=[i * (-1) for i in w2]
    sorted_order=np.argsort(w,kind='mergesort') + 1 # stabilne sortowanie
    schedule=[sorted_order[0]] # na poczatku na liscie jedno zadanie
    for i in range (1,tasks):
        best_in=0
        temp_schedule=schedule
        for j in range(0,i+1): # wstawianie zadania na n pozycjach
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

        schedule.insert(best_in,sorted_order[i]) # wstawiamy zadanie na najlepszej pozycji
    return schedule,Cmax


def find_longest_on_critical_path(schedule,time_matrix): # zadanie z najdluzsza operacja na sciezce

    critical = find_critical_path(schedule,time_matrix)
    times_on_critical_path=[]

    for path in critical:
        for i in range(0,len(path)):
            times_on_critical_path.append((path[i][0],time_matrix[path[i][0]-1][path[i][1]-1]))   # format (zadanie, czas zadania)

    longest = max(times_on_critical_path, key=lambda item:item[1])[0] # wyciagamy najdluzsze zadanie (ze wzgledu na tuple jest lambda)

    return longest


def find_task_with_biggest_sum_of_operation_on_cirtical_path(schedule,time_matrix):
    critical = find_critical_path(schedule,time_matrix)
    for j in range(0,len(critical)):
        times_on_critical_path=[0] * max(schedule)
        for i in range(0,len(critical[j])):
            times_on_critical_path[critical[j][i][0]-1]+=time_matrix[critical[j][i][0]-1][critical[j][i][1]-1]
        if j==0:
            max_time=max(times_on_critical_path)
            biggest = times_on_critical_path.index(max_time)+1
        else:
            if max(times_on_critical_path)>max_time:
                max_time=max(times_on_critical_path)
                biggest = times_on_critical_path.index(max_time)+1

    return biggest


def find_task_with_the_most_operations_on_critical_path(schedule,time_matrix):
    critical = find_critical_path(schedule,time_matrix)
    for j in range(0,len(critical)):
        tasks_on_critical_path=[]
        for i in range(0,len(critical[j])):
            tasks_on_critical_path.append(critical[j][i][0])
        if j==0:
            most=max(tasks_on_critical_path, key=tasks_on_critical_path.count)
            max_count=tasks_on_critical_path.count(most)
        else:
            current_most=max(tasks_on_critical_path, key=tasks_on_critical_path.count)
            if tasks_on_critical_path.count(current_most)>max_count:
                most=current_most
                max_count=tasks_on_critical_path.count(current_most)

    return most

def find_task_which_make_Cmax_biggest(schedule,time_matrix):
    best=0
    for i in range(0,len(schedule)):
        temp=schedule.pop(i)
        if i == 0:
            Cmax=count_cmax(schedule,time_matrix)
        else:
            Cmax_temp=count_cmax(schedule,time_matrix)
            if Cmax_temp<Cmax:
                Cmax=Cmax_temp
                best=i
        
        schedule.insert(i,temp)
    
    result=schedule[best]

    return result



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
        longest_task = find_longest_on_critical_path(schedule,time_matrix)
        if (longest_task==sorted_order[i]): # jesli to to samo zadanie co przed chwila wstawialismy to lecimy dalej
            continue
        best_in=schedule.index(longest_task)
        schedule.remove(longest_task)

        temp_schedule = schedule
        for j in range(0,i+1):
            temp_schedule.insert(j,longest_task)

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
        longest_task = find_task_with_biggest_sum_of_operation_on_cirtical_path(schedule,time_matrix)
        if (longest_task==sorted_order[i]):  #jeżeli odnaleziony element to ten, który był sprawdzany przejdź do następnej częsci pętli
            continue
        best_in=schedule.index(longest_task)
        schedule.remove(longest_task)

        temp_schedule = schedule
        for j in range(0,i+1):
            temp_schedule.insert(j,longest_task)

            Cmax_temp = count_cmax(temp_schedule,time_matrix)
            if Cmax_temp < Cmax:
                best_in = j
                Cmax = Cmax_temp

            temp_schedule.pop(j)

        schedule.insert(best_in,longest_task)

    return schedule,Cmax


def extend_neh_version_3(tasks,machine,time_matrix):
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
        most_task = find_task_with_the_most_operations_on_critical_path(schedule,time_matrix)
        if (most_task==sorted_order[i]):
            continue
        best_in=schedule.index(most_task)
        schedule.remove(most_task)

        temp_schedule = schedule
        for j in range(0,i+1):
            temp_schedule.insert(j,most_task)

            Cmax_temp = count_cmax(temp_schedule,time_matrix)
            if Cmax_temp < Cmax:
                best_in = j
                Cmax = Cmax_temp

            temp_schedule.pop(j)

        schedule.insert(best_in,most_task)

    return schedule,Cmax



def extend_neh_version_4(tasks,machine,time_matrix):
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
        longest_task = find_task_which_make_Cmax_biggest(schedule,time_matrix)
        if (longest_task==sorted_order[i]):
            continue
        best_in=schedule.index(longest_task)
        schedule.remove(longest_task)

        temp_schedule = schedule
        for j in range(0,i+1):
            temp_schedule.insert(j,longest_task)

            Cmax_temp = count_cmax(temp_schedule,time_matrix)
            if Cmax_temp < Cmax:
                best_in = j
                Cmax = Cmax_temp

            temp_schedule.pop(j)

        schedule.insert(best_in,longest_task)

    return schedule,Cmax
