"""
Autor skryptu: Teodor Niżyński
"""
from dataclasses import dataclass

@dataclass
class RPQ_Task:
    def __init__(self, task_number, r, p, q):
        self.id: int = task_number
        self.r: int = r
        self.p: int = p
        self.q: int = q

    def __repr__(self):
        return "[{0},{1},{2},{3}]".format(self.id, self.r, self.p, self.q)

    def __str__(self):
        return "task: {0}, r: {1}, p: {2}, q: {3}".format(self.id, self.r, self.p, self.q)

class RPQ_Instance:

    tasks: list # lista wszystkich zadań, będą po kolei dla wygody
    tasks_number: int # liczba wszystkich zadań

    @staticmethod
    def load_from_file(file_path: str):
        instance = RPQ_Instance()
        try:
            with open(file_path, "r") as file:
                instance.tasks_number, columns = [int(x) for x in next(file).split()]
                instance.tasks = []

                for i in range(0, instance.tasks_number):
                    row = next(file).split()
                    r = (int(row[0]))
                    p = (int(row[1]))
                    q = (int(row[2]))
                    task = RPQ_Task(i, r, p, q)
                    instance.tasks.append(task)

        except FileNotFoundError:
            print("File not found.")
            raise FileNotFoundError

        return instance

    def print_instance(self):
        print(self.tasks)
        print('Tasks:', self.tasks_number)

    def get_r(self, task_number):
        return self.tasks[task_number].r

    def get_p(self, task_number):
        return self.tasks[task_number].p

    def get_q(self, task_number):
        return self.tasks[task_number].q



def solve_rpq_with_solver(instance: RPQ_Instance):
    from ortools.sat.python import cp_model

    model = cp_model.CpModel() # inicjalizacja modelu - przechowa nasze zmienne oraz ograniczenia naszego problemu

    # Model będzie operować na zmiennych całkowitoliczbowych - jakie zmienne? Czas rozpoczęcia, czas zakończenia, cmax...
    # Potrzebujemy określić zakres tych zmiennych - najmniej 0, bo nasz problem nie może mieć negatywnych czasów rozpoczęcia, zakończenia czy cmax.
    # Co z maksymalną wartością? Spróbujmy policzyć najbardziej pesymistyczny scenariusz (możliwie złą kolejność):
    # Dla tej złej kolejności zaczniemy od zadania, które ma największe r, później pozostałe zadania i na koniec zadanie o największym q
    # Gdybyśmy nie znali problemu, moglibyśmy po prostu dodać wszystkie czasy, byłby to gorszy zakres, więcej roboty dla solvera.

    max_r = 0
    max_q = 0
    sum_p = 0
    for task_number in range(instance.tasks_number): # iterujemy po wszystkich zadaniach:
        sum_p = sum_p + instance.get_p(task_number)
        max_r = max(max_r, instance.get_r(task_number))
        max_q = max(max_q, instance.get_q(task_number))

    variable_max_value = 1 + max_r + sum_p + max_q # dla pewności o jeden za dużo
    variable_min_value = 0 # nic nie jest ujemne w naszym wypadku

    # Zaraz będziemy inicjalizować zmienne wewnątrz modelu, aby łatwo się do nich odwoływać - tworzymy na razie puste listy:
    model_start_vars = [] # tutaj będą czasy rozpoczęć zadań
    model_ends_vars = [] # tutaj będą czasy zakończeń zadań
    model_interval_vars = [] # tutaj będą przechowywane zmienne odpowiedzialne za zmienne interwałowe

    # teraz inicjalizacja zmiennych wewnątrz modelu:
    # zaczniemy od pojedynczej zmiennej, która będzie przechowywać cmax - proszę zauważyć, że jest to zmienna tworzona
    # wewnątrz modelu i nie jest to typowy int - próba sprawdzenia, czy jest to pythonowy typ int zwróci fałsz:
    # aby stworzyć tą zmienną musimy podać zakres oraz nazwę zmiennej
    # print("type of cmax:", type(cmax_optimalization_objective), isinstance(cmax_optimalization_objective, int))
    cmax_optimalization_objective = model.NewIntVar(variable_min_value, variable_max_value, 'cmax_makespan')

    # więcej zmiennych: dla czasu rozpoczęcia, zakończenia i interwałów, ale dla każdego zdania więc korzystamy z pętli
    for task_number in range(instance.tasks_number):
        suffix = f"t:{task_number}" # do zmiennych należy dodawać nazwę - u nas będzie to po prostu numer zadania
        start_var = model.NewIntVar(variable_min_value, variable_max_value, 'start_' + suffix) # zmienna wewnątrz solvera odpowiedzialna za czas rozpoczęcia
        end_var = model.NewIntVar(variable_min_value, variable_max_value, 'end_' + suffix) # zmienna wewnątrz solvera odpowiedzialna za czas zakończenia
        # zmienna interwałowa "łączy" czas rozpoczęcia oraz czas zakonczenia - dodatkowo nasz wykonania zdania trwa dokładnie p:
        interval_var = model.NewIntervalVar(start_var, instance.get_p(task_number), end_var, 'interval_' + suffix) # zmienna interwałowa wewnątrz solvera odpowiedzialna za nie nakładanie się zadań

        # dodawanie zmiennych na listy pomocnicze:
        model_start_vars.append(start_var)
        model_ends_vars.append(end_var)
        model_interval_vars.append(interval_var)

    # Pora na dodanie ograniczeń - zacznimy od najtrudniejszego: nasze zadania nie mogą się na siebie "nakładać na siebie",
    # czyli jedyna maszyna w problemie RPQ może pracować na raz tylko nad jednym zadaniem.
    # W ramach CP jest to ograniczenie łatwe do dodania:
    model.AddNoOverlap(model_interval_vars)
    # Gdybyśmy mieli więcej maszyn to musielibyśmy trochę bardziej pokombinować, ale ponieważ w RPQ jest jedna maszyna to
    # dodajemy wszystkie interwały. W wypadku wielomaszynowym tylko interwały z tej samej maszyny nie mogły się nakładać.

    # Pora teraz na ograniczenie związane z czasem rozpoczęcia - tutaj sytuacja jest jasna: start zadania jest możliwy dopiero po upływie czasu rozpoczęcia (r)
    for task_number in range(instance.tasks_number):
        model.Add(model_start_vars[task_number] >= instance.get_r(task_number)) # dodajemy do modelu ograniczenie w postaci nierówność

    # Zostało nam ograniczenie związane z czasem dostarczenia...
    # My zawrzemy je w ramach obliczenia cmaxa - proszę zwrócić uwagę, że cmax to największy czas dostarczenia ze wszystkich zadań
    # łatwo to przedstawić jako odpowiednią nierówność - cmax musi być większy/równy od czasu dostarczenia dla każdego zadania
    for task_number in range(instance.tasks_number):
        model.Add(cmax_optimalization_objective >= model_ends_vars[task_number] + instance.get_q(task_number))

    # Pora dodać do modelu informacje czego właściwie szukamy - chcemy zminimalizować cmax więc:
    model.Minimize(cmax_optimalization_objective)

    # Inicjalizujemy solver, który spróbuje znaleźć rozwiązanie w ramach naszego modelu:
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300.0 # dodatkowo ograniczmy czas wykonywania obliczeń do maksymalnie 5 min

    # Wszystkie ograniczenia dodane! pora odpalić solver!
    status = solver.Solve(model) # solver zwróci status, ale jako typ wyliczeniowy, więc troche nieczytelnie dla nas

    if (status is not cp_model.OPTIMAL): # sprawdzamy status, aby określić czy solver znalazł rozwiązanie optymalne
        status_readable = "not optimal solution :( -- nie wiem dlaczego, wyniki sa optymalne a solver mówi że nie"
    else:
        status_readable = "optimum found!"

    # Oprócz cmaxa przydałoby się odczytać kolejność wykonywania zadań - dla RPQ będzie to łatwe.
    # Wystarczy, że sprawdzimy czasy rozpoczęć (lub zakończeń) dla poszczególnych zadań:
    # Tworzymy listę z parami: (numer zadania, czas rozpoczęcia), sortujemy po tej drugiej wartości.
    pi_order = []
    for task_number in range(instance.tasks_number):
        pi_order.append((task_number, solver.Value(model_start_vars[task_number])))
    pi_order.sort(key=lambda x: x[1])
    pi_order = [x[0] for x in pi_order] # modyfikujemy naszą listę, aby przechowywać tylko numer zadań, bez czasów rozpoczęć

    return solver.ObjectiveValue(), pi_order, status_readable # zwracamy cmax, kolejność wykonywania zadań oraz informacje czy znaleźliśmy optimum



