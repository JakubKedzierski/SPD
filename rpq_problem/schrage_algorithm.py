import random
import numpy as np

def basic_schrage_algorithm(tasks, r, p, q):

    i = 0
    schedule = np.zeros(tasks)
    ready_list = []
    not_ready_list = [task for task in range(1, tasks+1)]
    not_ready_list = np.array((not_ready_list, r, p, q))
    not_ready_list = np.transpose(not_ready_list)
    t = np.min(not_ready_list[:, 1])

    while not len(ready_list) == 0 or not len(not_ready_list) == 0:
        while not len(not_ready_list) == 0 and min(r) <= t:
            j = np.argmin(not_ready_list[:, 1])
            if len(ready_list) > 0:
                ready_list = np.vstack((ready_list, not_ready_list[j,:]))
            else:
                ready_list = not_ready_list[j,:]

            not_ready_list = np.delete(not_ready_list, j, axis= 0)

        if len(ready_list) == 0:
            t = np.min(not_ready_list[:, 1])
        else:
            j = np.argmax(ready_list[:, 3])   # tu blad
            ready_list = np.delete(ready_list, j, axis=0)
            schedule[i] = j
            i = i+1
            #t = t+j

    print(schedule)