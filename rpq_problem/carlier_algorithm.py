from schrage_algorithm import *
import sys

# licze Cmatrixa zeby przy liczeniu b skorzystac sobie i wybrac to ostatnie zadanie na sciezce
def count_c_maxtrix(tasks,schedule,r,p,q):
    t = 0
    Cmatrix = [None] * tasks
    for i in range(0,tasks):
        S = max(t, r[schedule[i]-1])
        t = S + p[schedule[i]-1]
        Cmatrix[i] = t + q[schedule[i]-1]

    return Cmatrix

def find_b_for_carlier(Cmatrix,schedule):
    Cmatrix.reverse()
    index = Cmatrix.index(max(Cmatrix))
    return schedule[len(Cmatrix) - index - 1]
    # tu trzeba zwracac ostatnie wystapienie, a nie ma w pythonie rindex
    # ta konstrukcja pozwala na zwrocenie ostatniego wystapienia

def find_a_for_carlier(Cmax,r,p,q,schedule,b):
    q_b = q[b-1]
    index_b_in_schedule = schedule.index(b)
    tasks_to_check = schedule[0:index_b_in_schedule+1] # zadania do sprawdzenia to tylko te ktore sa przed b

    a_proposition = []
    for task in tasks_to_check: # lecimy po zadaniach do sprawdzenia
        index_task_in_tasks_to_check = tasks_to_check.index(task)
        sublist_of_task_to_check = tasks_to_check[index_task_in_tasks_to_check:] # wyjmujemy subliste z listy do sprawdzenia od obecnego zadania w petli do b
        sum = r[task-1]

        for subtask in sublist_of_task_to_check:
            sum = sum +p[subtask-1]

        sum =  sum + q_b

        if sum == Cmax:
            a_proposition.append(task)  # dodaje do proponowanych poniewaz na koniec trzeba zrobic min ze zbioru

    return min(a_proposition)

def find_c_for_carlier(schedule,a,b,q):
    pass


def carlier_alogrithm(tasks,r,p,q):
    schedule,U = basic_schrage_algorithm2(tasks,r,p,q)
    best_schedule = []
    UB = sys.maxsize
    if U<UB:
        UB = U
        best_schedule = schedule

    #schedule = [1,2,3,4,5,6] do debuggowania

    Cmatrix = count_c_maxtrix(tasks,schedule,r,p,q)
    b = find_b_for_carlier(Cmatrix,schedule)

    #a = find_a_for_carlier(21, r, p, q, schedule, b) do debuggowania 21 Cmax z schedula 1 2 3 4 5 6
    a = find_a_for_carlier(U,r,p,q,schedule,b)

    c = find_c_for_carlier(schedule,a,b,q)
