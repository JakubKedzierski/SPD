from schrage_algorithm import *
import sys
import copy


def count_c_maxtrix(tasks, schedule, r, p, q):
    t = 0
    Cmatrix = [None] * tasks
    Smatrix = [None] * tasks
    for i in range(0, tasks):
        S = max(t, r[schedule[i] - 1])
        Smatrix[i] = S
        t = S + p[schedule[i] - 1]
        Cmatrix[i] = t + q[schedule[i] - 1]

    return Cmatrix, Smatrix

def count_c_max(tasks, schedule, r, p, q):
    Cmatrix, S = count_c_maxtrix(tasks, schedule, r, p, q)
    return max(Cmatrix)

class Carlier:
    def __init__(self):
        self.UB=sys.maxsize
        self.best_schedule=[]

    # licze Cmatrixa zeby przy liczeniu b skorzystac sobie i wybrac to ostatnie zadanie na sciezce
    

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
        #print(U)

        if U<self.UB:
            self.UB = U
            self.best_schedule = schedule

        Cmatrix, Smatrix = count_c_maxtrix(tasks,schedule,r,p,q)

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


    def carlier_alogrithm_heap(self,tasks,r,p,q):
        schedule,U = basic_schrage_algorithm_heap(tasks,r,p,q)
        #print(U)
        #print(schedule)

        if U<self.UB:
            self.UB = U
            self.best_schedule = schedule

        Cmatrix, Smatrix = count_c_maxtrix(tasks,schedule,r,p,q)

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

        LB = pmtn_schrage_algorithm_heap(tasks,r,p,q)

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

        LB = pmtn_schrage_algorithm_heap(tasks,r,p,q)

        k_set_with_c = schedule[index_c_in_schedule:index_b_in_schedule + 1]
        r_k_with_c, q_k_with_c, p_k_with_c = self.get_new_r_q_p_from_k_set(k_set_with_c, r, p, q)
        H_k_with_c = r_k_with_c + q_k_with_c + p_k_with_c
        LB = max(H_k, H_k_with_c, LB)

        if LB < self.UB:
            self.carlier_alogrithm(tasks,r,p,q)

        q[c - 1] = q_old

        return self.UB


    def carlier_alogrithm2(self,tasks,r,p,q):
        schedule,U = basic_schrage_algorithm2(tasks,r,p,q)
        equality_list=[]
        check_equlity_list=False

        if U<self.UB:
            self.UB = U
            self.best_schedule = schedule
        while True:
            #print(U)
            Cmatrix, Smatrix = count_c_maxtrix(tasks, schedule, r, p, q)

            b = self.find_b_for_carlier(Cmatrix,schedule)
            

            a = self.find_a_for_carlier(U,r,p,q,schedule,b)
 
            c = self.find_c_for_carlier(schedule,a,b,q)

            if c is None or check_equlity_list==True:
                
                if len(equality_list)<=0:
                    break
                else:
                    temp=equality_list.pop(0)
                    r=temp[0]
                    p=temp[1]
                    q=temp[2]
                    U=temp[3]
                    schedule=temp[4]
                    continue
                
    #else:
    #    print(r[a - 1], r[b - 1], r[c - 1])

            index_c_in_schedule = schedule.index(c)
            index_b_in_schedule = schedule.index(b)
            k_set = schedule[index_c_in_schedule+1:index_b_in_schedule+1]

            r_k, q_k, p_k = self.get_new_r_q_p_from_k_set(k_set, r, p, q)

            r_old = r[c - 1].copy()
            r[c - 1] = max(r[c - 1], (r_k+p_k))

            LB1 = pmtn_schrage_algorithm2(tasks,r,p,q)

            H_k = r_k + q_k + p_k

            k_set_with_c = schedule[index_c_in_schedule:index_b_in_schedule + 1]
            r_k_with_c, q_k_with_c, p_k_with_c = self.get_new_r_q_p_from_k_set(k_set_with_c, r, p, q)
            H_k_with_c = r_k_with_c + q_k_with_c + p_k_with_c

            LB1 = max(H_k, H_k_with_c, LB1)
            U1=-1
            if LB1 < self.UB:
                schedule1,U1=basic_schrage_algorithm2(tasks,r,p,q)

            r[c - 1] = r_old.copy()
            q_old = q[c - 1].copy()
            q[c - 1] = max(q[c - 1], (q_k + p_k))

            LB2 = pmtn_schrage_algorithm2(tasks,r,p,q)

            k_set_with_c = schedule[index_c_in_schedule:index_b_in_schedule + 1]
            r_k_with_c, q_k_with_c, p_k_with_c = self.get_new_r_q_p_from_k_set(k_set_with_c, r, p, q)
            H_k_with_c = r_k_with_c + q_k_with_c + p_k_with_c
            LB2 = max(H_k, H_k_with_c, LB2)
            U2=-1
            if LB2 < self.UB:
                schedule2,U2=basic_schrage_algorithm2(tasks,r,p,q)
            if U1 ==-1 and U2==-1:
                q[c - 1] = q_old
                check_equlity_list=True
            elif U1==-1 and U2!=-1:
                schedule=schedule2
                U=U2
                if U2<self.UB:
                    self.UB = U2
                    self.best_schedule = schedule2
            elif U2==-1 and U1!=-1:
                schedule=schedule1
                U=U1
                q[c - 1] = q_old
                r[c - 1] = max(r[c - 1], (r_k+p_k))
                if U1<self.UB:
                    self.UB = U1
                    self.best_schedule = schedule1
            elif U1<U2:
                schedule=schedule1
                U=U1
                q[c - 1] = q_old
                r[c - 1] = max(r[c - 1], (r_k+p_k))
                if U1<self.UB:
                    self.UB = U1
                    self.best_schedule = schedule1
            elif U1==U2:
                q[c - 1] = q_old
                r[c - 1] = max(r[c - 1], (r_k+p_k))
                equality_list.append([r.copy(),p.copy(),q.copy(),U1,schedule1])
                r[c - 1] = r_old.copy()
                q[c - 1] = max(q[c - 1], (q_k + p_k))
                schedule=schedule2
                U=U2
                if U2<self.UB:
                    self.UB = U2
                    self.best_schedule = schedule2
                
            else:
                schedule=schedule2
                U=U2
                if U2<self.UB:
                    self.UB = U2
                    self.best_schedule = schedule2
            #print("U1: "+str(U1))
            #print("U2: "+str(U2))



        return self.UB



    def carlier_alogrithm3(self,tasks,r,p,q):
        schedule,U = basic_schrage_algorithm2(tasks,r,p,q)
        carlier_list=[]
        #carlier_list2=[]
        max_iter=9 #jest to ograniczenie maksymalnej głębokości w celu osiągniecia rozsądnych czasów

        if U<self.UB:
            self.UB = U
            self.best_schedule = schedule
        iter=0
        while True:
            #print(U)
            #Usuwając warunek na liczbe iteracji mamy prawdziwą implementacja przeszukiwania greed
            if (pmtn_schrage_algorithm2(tasks,r,p,q)!=U) and (iter<=max_iter):
                Cmatrix, Smatrix = count_c_maxtrix(tasks, schedule, r, p, q)

                b = self.find_b_for_carlier(Cmatrix,schedule)
                #print("b:"+str(b))
                a = self.find_a_for_carlier(U,r,p,q,schedule,b)
                #print("a:"+str(a))
                c = self.find_c_for_carlier(schedule,a,b,q)
                #print("c:"+str(c))
                #print(c)
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
                #print(r[c-1])

                LB1 = pmtn_schrage_algorithm2(tasks,r,p,q)

                H_k = r_k + q_k + p_k

                k_set_with_c = schedule[index_c_in_schedule:index_b_in_schedule + 1]
                r_k_with_c, q_k_with_c, p_k_with_c = self.get_new_r_q_p_from_k_set(k_set_with_c, r, p, q)
                H_k_with_c = r_k_with_c + q_k_with_c + p_k_with_c
                place=0
                if LB1<self.UB:
                    LB1 = max(H_k, H_k_with_c, LB1)
                    if LB1 < self.UB:
                    #schedule1,U1=basic_schrage_algorithm2(tasks,r,p,q)
                # if (U1==LB1):
                    #  self.UB = U1
                    #  self.best_schedule = schedule1
                    # return self.UB
                        carlier_list.insert(place,[r.copy(),p.copy(),q.copy(),LB1,iter+1])
                        place=place+1
                    #print(carlier_list)

                r[c - 1] = r_old.copy()
                q_old = q[c - 1].copy()
                q[c - 1] = max(q[c - 1], (q_k + p_k))

                LB2 = pmtn_schrage_algorithm2(tasks,r,p,q)

                k_set_with_c = schedule[index_c_in_schedule:index_b_in_schedule + 1]
                r_k_with_c, q_k_with_c, p_k_with_c = self.get_new_r_q_p_from_k_set(k_set_with_c, r, p, q)
                H_k_with_c = r_k_with_c + q_k_with_c + p_k_with_c
                if LB2<self.UB:
                    LB2 = max(H_k, H_k_with_c, LB2)
                    if LB2 < self.UB:
                #schedule2,U2=basic_schrage_algorithm2(tasks,r,p,q)
                #if (U2==LB2):
                   # self.UB = U2
                   # self.best_schedule = schedule2
                   # return self.UB
                        carlier_list.insert(place,[r.copy(),p.copy(),q.copy(),LB2,iter+1])
            if len(carlier_list)>0:
                temp=[]
                for i in carlier_list:
                    temp.append(i[3])
                temp=carlier_list.pop(temp.index(min(temp)))
                r=temp[0]
                p=temp[1]
                q=temp[2]
                iter=temp[4]
                schedule,U=basic_schrage_algorithm2(tasks,r,p,q)
                #print(temp[3])
                if U<self.UB:
                    self.UB = U
                    self.best_schedule = schedule
                if self.UB==temp[3]:
                    return self.UB
                #print(U)
            else:
                return self.UB


    def carlier_alogrithm3_heap(self,tasks,r,p,q):
        schedule,U = basic_schrage_algorithm_heap(tasks,r,p,q)
        carlier_list=[]
        #carlier_list2=[]
        max_iter=9 #jest to ograniczenie maksymalnej głębokości w celu osiągniecia rozsądnych czasów

        if U<self.UB:
            self.UB = U
            self.best_schedule = schedule
        iter=0
        while True:
            #print(U)
            #Usuwając warunek na liczbe iteracji mamy prawdziwą implementacja przeszukiwania greed
            if (pmtn_schrage_algorithm_heap(tasks,r,p,q)!=U) and (iter<=max_iter):
                Cmatrix, Smatrix = count_c_maxtrix(tasks, schedule, r, p, q)

                b = self.find_b_for_carlier(Cmatrix,schedule)
                #print("b:"+str(b))
                a = self.find_a_for_carlier(U,r,p,q,schedule,b)
                #print("a:"+str(a))
                c = self.find_c_for_carlier(schedule,a,b,q)
                #print("c:"+str(c))
                #print(c)
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
                #print(r[c-1])

                LB1 = pmtn_schrage_algorithm_heap(tasks,r,p,q)

                H_k = r_k + q_k + p_k

                k_set_with_c = schedule[index_c_in_schedule:index_b_in_schedule + 1]
                r_k_with_c, q_k_with_c, p_k_with_c = self.get_new_r_q_p_from_k_set(k_set_with_c, r, p, q)
                H_k_with_c = r_k_with_c + q_k_with_c + p_k_with_c
                place=0
                if LB1<self.UB:
                    LB1 = max(H_k, H_k_with_c, LB1)
                    if LB1 < self.UB:
                    #schedule1,U1=basic_schrage_algorithm2(tasks,r,p,q)
                # if (U1==LB1):
                    #  self.UB = U1
                    #  self.best_schedule = schedule1
                    # return self.UB
                        carlier_list.insert(place,[r.copy(),p.copy(),q.copy(),LB1,iter+1])
                        place=place+1
                    #print(carlier_list)

                r[c - 1] = r_old.copy()
                q_old = q[c - 1].copy()
                q[c - 1] = max(q[c - 1], (q_k + p_k))

                LB2 = pmtn_schrage_algorithm_heap(tasks,r,p,q)

                k_set_with_c = schedule[index_c_in_schedule:index_b_in_schedule + 1]
                r_k_with_c, q_k_with_c, p_k_with_c = self.get_new_r_q_p_from_k_set(k_set_with_c, r, p, q)
                H_k_with_c = r_k_with_c + q_k_with_c + p_k_with_c
                if LB2<self.UB:
                    LB2 = max(H_k, H_k_with_c, LB2)
                    if LB2 < self.UB:
                #schedule2,U2=basic_schrage_algorithm2(tasks,r,p,q)
                #if (U2==LB2):
                   # self.UB = U2
                   # self.best_schedule = schedule2
                   # return self.UB
                        carlier_list.insert(place,[r.copy(),p.copy(),q.copy(),LB2,iter+1])
            if len(carlier_list)>0:
                temp=[]
                for i in carlier_list:
                    temp.append(i[3])
                temp=carlier_list.pop(temp.index(min(temp)))
                r=temp[0]
                p=temp[1]
                q=temp[2]
                iter=temp[4]
                schedule,U=basic_schrage_algorithm_heap(tasks,r,p,q)
                #print(temp[3])
                if U<self.UB:
                    self.UB = U
                    self.best_schedule = schedule
                if self.UB==temp[3]:
                    return self.UB
                #print(U)
            else:
                return self.UB


