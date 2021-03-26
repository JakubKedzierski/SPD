import numpy as np
from Cmatrix_operations import *


def find_critical_path(schedule, time_matrix):
    tasks=len(time_matrix)
    machines=len(time_matrix[0])
    Cmatrix = count_Cmatrix(schedule, time_matrix)
    critical_path=[]
    critical_path.append((tasks, machines ))
    i=tasks-1
    j=machines-1

    while(True):
        if (j-1) < 0 and (i-1) <0 : # gdy przeszlimy po wszystkich maszynach to koniec
            break

        if (i - 1) < 0:
            j = j - 1
        elif (j-1) < 0:
            i = i - 1
        else:
            if Cmatrix[i][j-1] >= Cmatrix[i-1][j]: #porownujemy ktora operacja decyduje o wyborze sciezki
                j = j - 1
            else:
                i = i - 1

        critical_path.append((i+1, j+1)) # sciezka w formacie [ (zadanie, maszyna), (zadanie, maszyna) ... ]

    print_critical_path(critical_path)
    return critical_path

def print_critical_path(critical_path):
    print("Critical path")
    for i in range(0,len(critical_path)):
        print("Krok",i,"Maszyna:",critical_path[i][1], "Zadanie:",critical_path[i][0])
