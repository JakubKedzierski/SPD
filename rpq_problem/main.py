from schrage_algorithm import *
import numpy as np
from piority_queue import *
import time
import random
from heap import *

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
    path=""
    file_name="./datasets/" + "in50.txt"

    try:
        with open(path + file_name, "r") as file:

            tasks, r, p, q = read_data_set(file)
            not_ready_list = [task for task in range(1, tasks + 1)]
            not_ready_list = np.array((not_ready_list, r, p, q))
            not_ready_list = np.transpose(not_ready_list)

            # tworzenie heap max, pop zwraca max q
            heap = MaxHeap()
            heap.tab = not_ready_list
            heap.heap_size = tasks
            heap.build_heap_max_q_in_node(heap.heap_size)
            ####

            # tworzenie heap min, pop zwraca min r, dodawanie elementów normalnie poprzez insert
            heap2 = MinHeap()
            ####

            while(heap.heap_size >0):
                row = heap.pop_max()
                heap2.insert_min_heap(row)

            while (heap2.heap_size > 0):
                print(heap2.pop_min())




            """
            start = time.time()
            schedule,Cmax = basic_schrage_algorithm(tasks, r, p, q)
            end = time.time()
            print("basic schrage")
            print(Cmax)
            print(end - start)

            start = time.time()
            schedule, Cmax = basic_schrage_algorithm_priority_queue(tasks, r, p, q)
            end = time.time()
            print("basic schrage priority")
            print(Cmax)
            print(end - start)
            
            start=time.time()
            Cmax=pmtn_schrage_algorithm(tasks,r,p,q)
            end=time.time()
            print("pmtn schrage")
            print(Cmax)
            print(end-start)

            start=time.time()
            Cmax=pmtn_schrage_algorithm_priority_queue(tasks,r,p,q)
            end=time.time()
            print("pmtn schrage priority")
            print(Cmax)
            print(end-start)
            """

    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError


def testing_main():
    sets = [50,100,150,200,250,300,400,500,1000,2000]
    repeat = 5

    for numb in sets:
        time_b = 0
        cmax_b = 0

        time_p = 0
        cmax_p = 0

        time_bp = 0
        cmax_bp = 0

        time_pp = 0
        cmax_pp = 0

        for i in range(0, repeat):
   
            r = np.zeros(numb, dtype=int)
            p = np.zeros(numb, dtype=int)
            q = np.zeros(numb, dtype=int)
            for j in range(0,numb):
                r[j] = random.randint(10, 100)
                p[j] = random.randint(5, 100)
                q[j] = random.randint(10, 100)

            start = time.time()
            schedule, Cmax = (0,0)
            schedule, Cmax = basic_schrage_algorithm(numb, r, p, q)
            end = time.time()
            time_b = time_b + (end - start)
            cmax_b = cmax_b + Cmax

            start = time.time()
            schedule,Cmax = basic_schrage_algorithm_priority_queue(numb, r, p, q)
            end = time.time()
            time_bp = time_bp + (end - start)
            cmax_bp = cmax_bp + Cmax
            start = time.time()
            Cmax = pmtn_schrage_algorithm(numb, r, p, q)
            end = time.time()
            time_p = time_p + (end - start)
            cmax_p = cmax_p + Cmax

            Cmax = pmtn_schrage_algorithm_priority_queue(numb, r, p, q)
            end = time.time()
            time_pp = time_pp + (end - start)
            cmax_pp = cmax_pp + Cmax


        time_b = time_b/repeat
        cmax_b = cmax_b/repeat

        time_p = time_p/repeat
        cmax_p = cmax_p/repeat

        time_bp = time_bp/repeat
        cmax_bp = cmax_bp/repeat

        time_pp = time_pp/repeat
        cmax_pp = cmax_pp/repeat

        print(numb,cmax_b,time_b)
        print(numb,cmax_bp,time_bp)
        print(numb, cmax_p, time_p)
        print(numb, cmax_pp, time_pp)



if __name__ == '__main__':
    main()