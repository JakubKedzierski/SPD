from schrage_algorithm import *
import numpy as np
from piority_queue import *
import time

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
            Cmax = basic_schrage_algorithm_priority_queue(tasks, r, p, q)
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


if __name__ == '__main__':
    main()