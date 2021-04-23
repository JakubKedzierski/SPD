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
    file_name="./datasets/" + "data008.txt"

    try:
        with open(path + file_name, "r") as file:
            tasks, r, p, q = read_data_set(file)
            schedule,Cmax = basic_schrage_algorithm(tasks, r, p, q)
            print(Cmax)
            start=time.time()
            Cmax2=pmtn_schrage_algorithm(tasks,r,p,q)
            end=time.time()
            print(end-start)
            print(Cmax2)
            start=time.time()
            Cmax3=pmtn_schrage_algorithm_priority_queue(tasks,r,p,q)
            end=time.time()
            print(end-start)
            print(Cmax3)


    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError


if __name__ == '__main__':
    main()