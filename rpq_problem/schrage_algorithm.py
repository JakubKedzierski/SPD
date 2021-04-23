import random
import numpy as np
from piority_queue import *

def basic_schrage_algorithm(tasks, r, p, q):

    i = 0
    schedule = np.zeros(tasks)
    ready_list = []
    not_ready_list = [task for task in range(1, tasks+1)]
    not_ready_list = np.array((not_ready_list, r, p, q))
    not_ready_list = np.transpose(not_ready_list)
    t = np.min(not_ready_list[:, 1])
    Cmax = 0
    while not len(ready_list) == 0 or not len(not_ready_list) == 0:
        while not len(not_ready_list) == 0 and np.min(not_ready_list[:, 1]) <= t:
            j = np.argmin(not_ready_list[:, 1])
            if len(ready_list) > 0:
                ready_list = np.vstack((ready_list, not_ready_list[j,:]))
            else:
                ready_list = np.zeros((1, 4))
                ready_list[0, 0] = not_ready_list[j,0]
                ready_list[0, 1] = not_ready_list[j,1]
                ready_list[0, 2] = not_ready_list[j,2]
                ready_list[0, 3] = not_ready_list[j,3]

            not_ready_list = np.delete(not_ready_list, j, axis= 0)

        if len(ready_list) == 0:
            t = np.min(not_ready_list[:, 1])
        else:
            j = np.argmax(ready_list[:, 3])
            task = ready_list[j, 0]
            p_j = ready_list[j, 2]
            q_j = ready_list[j, 3]
            ready_list = np.delete(ready_list, j, axis=0)
            schedule[i] = task
            i = i+1
            t = t+p_j
            Cmax = max(Cmax, t +q_j)

    return schedule,Cmax


def pmtn_schrage_algorithm(tasks, r, p, q):

    ready_list = []
    #q_0=np.iinfo(np.int32).max
    not_ready_list = [task for task in range(1, tasks+1)]
    not_ready_list = np.array((not_ready_list, r, p, q))
    not_ready_list = np.transpose(not_ready_list)
    t = 0
    l = 0
    Cmax = 0
    #print(not_ready_list)
    while not len(ready_list) == 0 or not len(not_ready_list) == 0:
        while not len(not_ready_list) == 0 and np.min(not_ready_list[:, 1]) <= t:
            j = np.argmin(not_ready_list[:, 1])
            if len(ready_list) > 0:
                ready_list = np.vstack((ready_list, not_ready_list[j,:]))
            else:
                ready_list = np.zeros((1, 4), dtype=int)
                ready_list[0, 0] = not_ready_list[j,0]
                ready_list[0, 1] = not_ready_list[j,1]
                ready_list[0, 2] = not_ready_list[j,2]
                ready_list[0, 3] = not_ready_list[j,3]

            q_j=not_ready_list[j,3]
            r_j=not_ready_list[j,1]
            not_ready_list = np.delete(not_ready_list, j, axis= 0)
            if l!=0:
                if q_j>q[l]:
                    p_l=t-r_j
                    t=r_j
                    if p[l]>0:
                        ready_list = np.vstack((ready_list, [l+1,r[l],p_l,q[l]]))
        if len(ready_list) == 0:
            t = np.min(not_ready_list[:, 1])
        else:
            j = np.argmax(ready_list[:, 3])
            p_j = ready_list[j, 2]
            q_j = ready_list[j, 3]
            l=ready_list[j,0]-1
            ready_list = np.delete(ready_list, j, axis=0)
            t=t+p_j
            Cmax = max(Cmax, t +q_j)
    return Cmax


def pmtn_schrage_algorithm_priority_queue(tasks, r, p, q):

    ready_queue=PriorityQueue(True)
    not_ready_queue=PriorityQueue(False)
    for i in range(0,tasks):
        not_ready_queue.insert(Node(r[i],p[i],q[i]))
    t = 0
    Cmax = 0
    node2=Node(0,0,np.iinfo(np.int32).max)
    #print(not_ready_list)
    while not ready_queue.isEmpty() or not not_ready_queue.isEmpty():
        while not not_ready_queue.isEmpty() and not_ready_queue.queue[0].r <= t:
            node=not_ready_queue.pop()
            ready_queue.insert(node)
            if node.q>node2.q:
                node2.p=t-node.r
                t=node.r
                if node2.p>0:
                    ready_queue.insert(node2)
        if ready_queue.isEmpty():
            t = not_ready_queue.queue[0].r
        else:
            node2=ready_queue.pop()
            t=t+node2.p
            Cmax = max(Cmax, t + node2.q)
    return Cmax