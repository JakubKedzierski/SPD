import collections
from ortools.sat.python import cp_model

def load_job_shop_insa(file_name):
    path="./datasets/"

    try:
        with open(path + file_name, "r") as file:
            data_set = str(next(file).split())
            _, data_set_number = data_set.split('.')
            data_set_number, _ = data_set_number.split(':')
            data_set_number = int(data_set_number)
            tasks, machines, operations = [int(x) for x in next(file).split()]
            jobshop_matrix = []
            for task in range(0,tasks):
                row = next(file).split()
                operation_in_task = int(row[0])
                job_matrix = []
                for i in range(1,operation_in_task*2,2):
                    m = int(row[i])
                    p = int(row[i+1])
                    job_matrix.append([m, p])
                jobshop_matrix.append(job_matrix)

            return jobshop_matrix, tasks, machines
    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError

def job_shop_ortools():
    jobshop_matrix, tasks, machines = load_job_shop_insa('insa_set')

    model = cp_model.CpModel()
