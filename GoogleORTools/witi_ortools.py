from dataclasses import dataclass

@dataclass
class WiTi_Task:
    def __init__(self, task_number, p, w, t):
        self.id: int = task_number
        self.p: int = p
        self.t: int = t
        self.w: int = w

    def __repr__(self):
        return "[i:{0},p:{1},w:{2},t:{3}]".format(self.id, self.p, self.w, self.t)


class WiTi_Instance:

    tasks: list
    tasks_number: int

    @staticmethod
    def load_from_file(file_path: str):
        instance = WiTi_Instance()
        try:
            with open(file_path, "r") as file:
                next(file)
                row = next(file).split()
                instance.tasks_number = int(row[0])
                instance.tasks = []

                for i in range(0, instance.tasks_number):
                    row = next(file).split()
                    p = (int(row[0]))
                    w = (int(row[1]))
                    t = (int(row[2]))
                    task = WiTi_Task(i, p, w, t)
                    instance.tasks.append(task)

        except FileNotFoundError:
            print("File not found.")
            raise FileNotFoundError

        return instance

    def print_instance(self):
        print(self.tasks)
        print('Tasks:', self.tasks_number)

    def get_p(self, task_number):
        return self.tasks[task_number].p

    def get_w(self, task_number):
        return self.tasks[task_number].w

    def get_t(self, task_number):
        return self.tasks[task_number].t

def solve_witi_with_solver(instance: WiTi_Instance):
    from ortools.sat.python import cp_model
    model = cp_model.CpModel()




    objective = 0
    pi_order = []
    status = ''

    return objective, pi_order, status

