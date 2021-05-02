from schrage_algorithm import *
import numpy as np
from piority_queue import *
import time
import random

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
    file_name="./datasets/" + "in200.txt"

    try:
        with open(path + file_name, "r") as file:

            start = time.time()
            tasks, r, p, q = read_data_set(file)
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


    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError


def testing_main():
    sets = [200,300,400,500,600,700]
    repeat = 5

    for numb in sets:
        time_b = 0
        cmax_b = 0

        time_p = 0
        cmax_p = 0

        for i in range(0, repeat):
            r = np.zeros(numb, dtype=int)
            p = np.zeros(numb, dtype=int)
            q = np.zeros(numb, dtype=int)
            for j in range(0,numb):
                r[j] = random.randint(10, 1500)
                p[j] = random.randint(5, 100)
                q[j] = random.randint(10, 1500)

            start = time.time()
            schedule, Cmax = (0,0)
            schedule, Cmax = basic_schrage_algorithm(numb, r, p, q)
            end = time.time()
            time_b = time_b + (end - start)
            cmax_b = cmax_b + Cmax

            start = time.time()
            Cmax = pmtn_schrage_algorithm(numb, r, p, q)
            end = time.time()
            time_p = time_p + (end - start)
            cmax_p = cmax_p + Cmax

        time_b = time_b/repeat
        cmax_b = cmax_b/repeat

        time_p = time_p/repeat
        cmax_p = cmax_p/repeat

        print(numb,cmax_b,time_b)
        print(numb, cmax_p, time_p)



if __name__ == '__main__':
    testing_main()