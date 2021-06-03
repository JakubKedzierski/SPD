import collections
from ortools.sat.python import cp_model


def read_data_set(file):
    tasks, machines = [int(x) for x in next(file).split()] 
    time_matrix = [] 

    for i in range(0,tasks):
        time_matrix.append([int(x) for x in next(file).split()])

    return tasks, machines, time_matrix

def load_flowshop_problem(file_name):
    path=""
    file_name="./datasets/" + str(file_name)
    try:
        with open(path+file_name, "r") as file:

            return read_data_set(file)
                  
    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError

def flowshop_ortools(filename):
    tasks,machines,time_matrix = load_flowshop_problem(filename)
    model = cp_model.CpModel()
    task_type = collections.namedtuple('task_type', 'start end interval')

    all_tasks={}
    machine_to_intervals = collections.defaultdict(list)
    worst_possibly_cmax = sum(task for job in time_matrix for task in job)

    for job_id, job in enumerate(time_matrix):
        for task_id, task in enumerate(job):
            duration=task

            start_var = model.NewIntVar(0,worst_possibly_cmax,'start task: '+str(job_id)+' machine: '+str(task_id))
            end_var = model.NewIntVar(0,worst_possibly_cmax,'end task: '+str(job_id)+' machine: '+str(task_id))
            interval_var = model.NewIntervalVar(start_var, duration, end_var, 'interval'+str(job_id)+' machine: '+str(task_id))
            all_tasks[job_id, task_id] = task_type(start=start_var, end=end_var, interval=interval_var)
            machine_to_intervals[task_id].append(interval_var)
    
    for machine in range(0, machines):
        model.AddNoOverlap(machine_to_intervals[machine])  

    for job_id, job in enumerate(time_matrix):
        for task_id in range(0,machines-1):
            model.Add(all_tasks[job_id, task_id + 1].start >= all_tasks[job_id, task_id].end)

    #ograniczenie mające na celu,aby zadania na każdej kolejnej maszynie wykonywały się w tej samej kolejności co na pierwszej
    for job_id in range(0,tasks-1):
        for j in range(job_id+1,tasks):
            b= model.NewBoolVar('b'+str(job_id)+' '+str(j))
            model.Add(all_tasks[job_id, 0].start>all_tasks[j, 0].start).OnlyEnforceIf(b)
            model.Add(all_tasks[job_id, 0].start<all_tasks[j, 0].start).OnlyEnforceIf(b.Not())
            for machine_id in range(1,machines):
                model.Add(all_tasks[job_id, machine_id].start > all_tasks[j, machine_id].start).OnlyEnforceIf(b)
                model.Add(all_tasks[job_id, machine_id].start < all_tasks[j, machine_id].start).OnlyEnforceIf(b.Not())
    

    cmax_var = model.NewIntVar(0, worst_possibly_cmax, 'cmax')
    model.AddMaxEquality(cmax_var,
                         [all_tasks[job_id, machines - 1].end for job_id in range(0,tasks)])
    model.Minimize(cmax_var)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 120
    status=solver.Solve(model)

    if (status is not cp_model.OPTIMAL): # sprawdzamy status, aby określić czy solver znalazł rozwiązanie optymalne
        status_readable = "not optimal solution"
    else:
        status_readable = "optimum found!"
    

    pi_order=[]
    for task_number in range(0,tasks):
        pi_order.append((task_number+1,solver.Value(all_tasks[task_number, 0].start)))
    """
    for i in range(0,tasks):
        print("")
        for j in range(0,machines):
            print(str(solver.Value(all_tasks[i,j].end))+" ",end='')
            """
    pi_order.sort(key=lambda x:x[1])
    pi_order=[x[0] for x in pi_order]

    print(status_readable)
    print('Cmax: %i' % solver.ObjectiveValue())
    print(pi_order)


