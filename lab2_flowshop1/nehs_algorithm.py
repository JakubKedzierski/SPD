import numpy as np
from Cmatrix_operations import *


def find_critical_path(schedule, time_matrix):
    tasks=len(time_matrix)
    machines=len(time_matrix[0])
    Cmatrix = count_Cmatrix(schedule, time_matrix)
    critical_path=[]
    critical_path.append((1, 1))
    i=0
    j=0


    while(True):
        if (j+1) >= machines:
            break

        if (i + 1) >= tasks:
            j = j + 1
        else:
            if Cmatrix[i][j+1] >= Cmatrix[i+1][j]:
                j = j + 1
            else:
                i = i + 1

        critical_path.append((i+1, j+1))




    print(critical_path)




    # machines in order
    return critical_path
