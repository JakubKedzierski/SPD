from Cmatrix_operations import *

def johnson_for_2_machines(tasks: int, time_matrix_copy):
    time_matrix = time_matrix_copy.copy()
    task_on_list = list(range(1, tasks + 1))
    listA = []
    listB = []
    time_matrix = np.array(time_matrix)

    while True:
        if not task_on_list:
            break

        index = np.unravel_index(time_matrix.argmin(), time_matrix.shape)
        time_matrix[index[0], 0] = np.iinfo(
            np.int32).max  # przypisanie maksymalnych wartosci do czasow zadan ktore 'wyciagnelismy' z listy
        time_matrix[index[0], 1] = np.iinfo(np.int32).max

        task_on_list.remove(index[0] + 1)
        if index[1] == 0:  # jesli pierwsza maszyna to:
            listA.append(index[0] + 1)
        else:
            listB.insert(0, index[0] + 1)

    schedule = listA + listB
    Cmax = count_cmax(schedule, time_matrix_copy)

    return schedule, Cmax;


def johnson_for_N_machines(tasks, machines, time_matrix):
    imaginary_times = np.zeros((tasks, 2))

    if machines % 2 == 0:
        half = int(machines / 2)  # polowa maszyn ktore wpadaja do jednej z wirtualnych maszyn
    else:
        half = int(machines / 2) + 1

    for i in range(0, tasks):
        for j in range(0, half):
            imaginary_times[i, 0] += time_matrix[i][j]
        if machines % 2 == 1:
            for k in range(half - 1, machines):
                imaginary_times[i, 1] += time_matrix[i][k]
        else:
            for k in range(half, machines):
                imaginary_times[i, 1] += time_matrix[i][k]

    schedule, virutal_c_max = johnson_for_2_machines(tasks, imaginary_times)
    Cmax = count_cmax(schedule, time_matrix)

    return schedule, Cmax