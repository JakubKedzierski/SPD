from schrage_algorithm import *
import sys
import copy

class Carlier:
    def __init__(self):
        self.UB=sys.maxsize
        self.best_schedule=[]

    # licze Cmatrixa zeby przy liczeniu b skorzystac sobie i wybrac to ostatnie zadanie na sciezce
    def count_c_maxtrix(self,tasks,schedule,r,p,q):
        t = 0
        Cmatrix = [None] * tasks
        Smatrix = [None] * tasks
        for i in range(0,tasks):
            S = max(t, r[schedule[i]-1])
            Smatrix[i] = S
            t = S + p[schedule[i]-1]
            Cmatrix[i] = t + q[schedule[i]-1]

        return Cmatrix,Smatrix

    def find_b_for_carlier(self,Cmatrix,schedule):
        Cmatrix.reverse()
        index = Cmatrix.index(max(Cmatrix))
        b = schedule[len(Cmatrix) - index - 1]
        Cmatrix.reverse()
        return b
        # tu trzeba zwracac ostatnie wystapienie, a nie ma w pythonie rindex
        # ta konstrukcja pozwala na zwrocenie ostatniego wystapienia


    def find_a_for_carlier(self,Cmax,r,p,q,schedule,b):
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
                return task


    def find_c_for_carlier(self,schedule,a,b,q):
        index_a_in_schedule = schedule.index(a)
        index_b_in_schedule = schedule.index(b)

        j=index_b_in_schedule-1
        while (j>=index_a_in_schedule):
            if (q[schedule[j]-1]<q[b-1]):
                return schedule[j]
            j=j-1
        return None
        """
        sublist_to_check = schedule[index_a_in_schedule:index_b_in_schedule+1]

        q_b = q[b - 1]
        c_proposition = []
        for task in sublist_to_check:
            if q[task-1] < q_b:
                c_proposition.append(task)
        if len(c_proposition) == 0:
            return None
        else:
            return c_proposition[-1]
        """

    def get_new_r_q_p_from_k_set(self,k_set,r,p,q):
        min_r = r[k_set[0] - 1]
        min_q = q[k_set[0] - 1]
        sum_p_j = 0

        for task in k_set:
            if r[task - 1] < min_r:
                min_r = r[task - 1]

            if q[task - 1] < min_q:
                min_q = q[task - 1]

            sum_p_j = sum_p_j + p[task - 1]

        return min_r,min_q,sum_p_j

    def carlier_alogrithm(self,tasks,r,p,q):
        schedule,U = basic_schrage_algorithm2(tasks,r,p,q)

        if U<self.UB:
            self.UB = U
            self.best_schedule = schedule

        Cmatrix, Smatrix = self.count_c_maxtrix(tasks,schedule,r,p,q)

        b = self.find_b_for_carlier(Cmatrix,schedule)

        a = self.find_a_for_carlier(U,r,p,q,schedule,b)

        c = self.find_c_for_carlier(schedule,a,b,q)


        if c is None:
            return self.UB
    #else:
    #    print(r[a - 1], r[b - 1], r[c - 1])

        index_c_in_schedule = schedule.index(c)
        index_b_in_schedule = schedule.index(b)
        k_set = schedule[index_c_in_schedule+1:index_b_in_schedule+1]

        r_k, q_k, p_k = self.get_new_r_q_p_from_k_set(k_set, r, p, q)

        r_old = r[c - 1].copy()
        r[c - 1] = max(r[c - 1], (r_k+p_k))

        LB = pmtn_schrage_algorithm2(tasks,r,p,q)

        H_k = r_k + q_k + p_k

        k_set_with_c = schedule[index_c_in_schedule:index_b_in_schedule + 1]
        r_k_with_c, q_k_with_c, p_k_with_c = self.get_new_r_q_p_from_k_set(k_set_with_c, r, p, q)
        H_k_with_c = r_k_with_c + q_k_with_c + p_k_with_c

        LB = max(H_k, H_k_with_c, LB)

        if LB < self.UB:
            self.carlier_alogrithm(tasks,r,p,q)

        r[c - 1] = r_old.copy()
        q_old = q[c - 1].copy()
        q[c - 1] = max(q[c - 1], (q_k + p_k))

        LB = pmtn_schrage_algorithm2(tasks,r,p,q)

        k_set_with_c = schedule[index_c_in_schedule:index_b_in_schedule + 1]
        r_k_with_c, q_k_with_c, p_k_with_c = self.get_new_r_q_p_from_k_set(k_set_with_c, r, p, q)
        H_k_with_c = r_k_with_c + q_k_with_c + p_k_with_c
        LB = max(H_k, H_k_with_c, LB)

        if LB < self.UB:
            self.carlier_alogrithm(tasks,r,p,q)

        q[c - 1] = q_old

        return self.UB