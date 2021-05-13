from schrage_algorithm import *
import numpy as np
from piority_queue import *
import time
import random
from heap import *
from carlier_algorithm import *
import sys

def read_data_set(file):
    tasks, columns = [int(x) for x in next(file).split()]

    r = np.zeros(tasks, dtype=int)
    p = np.zeros(tasks, dtype=int)
    q = np.zeros(tasks, dtype=int)

    for i in range(0, tasks):
        row = next(file).split()
        r[i] = (int(row[0]))
        p[i] = (int(row[1]))
        q[i] = (int(row[2]))
    
    return tasks, r, p, q


def compute_testing_set(file):
    sets, repeats = [int(x) for x in next(file).split()]
    for i in range(0,sets):
        tasks, columns = [int(x) for x in next(file).split()]

        r = np.zeros(tasks, dtype=int)
        p = np.zeros(tasks, dtype=int)
        q = np.zeros(tasks, dtype=int)

        for i in range(0, tasks):
            row = next(file).split()
            r[i] = (int(row[0]))
            p[i] = (int(row[1]))
            q[i] = (int(row[2]))

    return tasks, r, p, q


def main():
    sys.setrecursionlimit(4500)
    # wywala RecursionError: maximum recursion depth exceeded in comparison, mozna probowac to obchodzic przez ten limit
    # ale wtedy wywala segm fault :(

    path=""
    file_name="./datasets/" + "rpq6"

    try:
        with open(path + file_name, "r") as file:

            tasks, r, p, q = read_data_set(file)
            schedule = carlier_alogrithm(tasks,r,p,q)
            Cmatrix,Smatrix = count_c_maxtrix(tasks,schedule,r,p,q)

            print("Cmax", max(Cmatrix) )
            print("Schedule", schedule)
            
            
    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError


def testing_main():
    sets = [8000,10000]
    repeat = 2

    for numb in sets:
        time_b = 0
        cmax_b = 0

        time_p = 0
        cmax_p = 0

        time_bp = 0
        cmax_bp = 0

        time_pp = 0
        cmax_pp = 0

        time_b2 = 0
        cmax_b2 = 0

        time_p2 = 0
        cmax_p2 = 0

        time_ph = 0
        cmax_ph = 0

        time_bh = 0
        cmax_bh = 0

        for i in range(0, repeat):
   
            r = np.zeros(numb, dtype=int)
            p = np.zeros(numb, dtype=int)
            q = np.zeros(numb, dtype=int)
            for j in range(0,numb):
                r[j] = random.randint(10, 100)
                p[j] = random.randint(5, 100)
                q[j] = random.randint(10, 100)

            """
            start = time.time()
            schedule, Cmax = (0,0)
            schedule, Cmax = basic_schrage_algorithm(numb, r, p, q)
            end = time.time()
            time_b = time_b + (end - start)
            cmax_b = cmax_b + Cmax
            
            start = time.time()
            schedule,Cmax = basic_schrage_algorithm2(numb, r, p, q)
            end = time.time()
            time_b2 = time_b2 + (end - start)
            cmax_b2 = cmax_b2 + Cmax
            
            start = time.time()
            schedule,Cmax = basic_schrage_algorithm_priority_queue(numb, r, p, q)
            end = time.time()
            time_bp = time_bp + (end - start)
            cmax_bp = cmax_bp + Cmax
            """
            start = time.time()
            schedule,Cmax = basic_schrage_algorithm_heap(numb, r, p, q)
            end = time.time()
            time_bh = time_bh + (end - start)
            cmax_bh = cmax_bh + Cmax
            
            """
            start = time.time()
            Cmax = pmtn_schrage_algorithm(numb, r, p, q)
            end = time.time()
            time_p = time_p + (end - start)
            cmax_p = cmax_p + Cmax
           
            start = time.time()
            Cmax = pmtn_schrage_algorithm2(numb, r, p, q)
            end = time.time()
            time_p2 = time_p2 + (end - start)
            cmax_p2 = cmax_p2 + Cmax
            
            start = time.time()
            Cmax = pmtn_schrage_algorithm_priority_queue(numb, r, p, q)
            end = time.time()
            time_pp = time_pp + (end - start)
            cmax_pp = cmax_pp + Cmax
            
            start = time.time()
            Cmax = pmtn_schrage_algorithm_heap(numb, r, p, q)
            end = time.time()
            time_ph = time_ph + (end - start)
            cmax_ph = cmax_ph + Cmax
            """


        time_b = time_b/repeat
        cmax_b = cmax_b/repeat

        time_p = time_p/repeat
        cmax_p = cmax_p/repeat

        time_bp = time_bp/repeat
        cmax_bp = cmax_bp/repeat

        time_p2 = time_p2/repeat
        cmax_p2 = cmax_p2/repeat

        time_b2 = time_b2/repeat
        cmax_b2 = cmax_b2/repeat

        time_pp = time_pp/repeat
        cmax_pp = cmax_pp/repeat

        time_ph = time_ph/repeat
        cmax_ph = cmax_ph/repeat

        time_bh = time_bh/repeat
        cmax_bh = cmax_bh/repeat

        #print("Pierwotny basic:")
        #print(numb,time_b)
        #print("Priority basic:")
        #print(numb,time_bp)
        #print("Podstawowa lista basic:")
        #print(numb,time_b2)
        #print("Heap basic:")
        print(numb,time_bh)


        #print("Pierwotny pmtn:")
        #print(numb, cmax_p, time_p)
        #print("Priority pmtn:")
        #print(numb, cmax_pp, time_pp)
        #print("Podstawowa lista pmtn:")
        #print(numb, time_p2)
        #print("Heap pmtn:")
        #print(numb, time_ph)




if __name__ == '__main__':
    main()