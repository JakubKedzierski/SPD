from schrage_algorithm import *
import numpy as np

def read_data_set(file):
    tasks, columns = [int(x) for x in next(file).split()]

    r = np.zeros(tasks)
    p = np.zeros(tasks)
    q = np.zeros(tasks)

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
            tasks, r, p, q = read_data_set(file)
            schedule,Cmax = basic_schrage_algorithm(tasks, r, p, q)
            print(Cmax)

    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError


if __name__ == '__main__':
    main()