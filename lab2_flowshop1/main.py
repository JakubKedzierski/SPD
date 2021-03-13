import plotly.express as px
import pandas as pd
import numpy as np

def read_file_with_lots_of_datasets(file):
    file.readline()
    
    tasks, machines, time_matrix = read_data_set(file)

    file.readline()
    file.readline()
    Cmax = int(file.readline())
    schedule= [int(x) for x in next(file).split()] 
    file.readline()

    return tasks,machines,time_matrix,Cmax,schedule


def read_data_set(file):
    tasks, machines = [int(x) for x in next(file).split()] 
    time_matrix = [] 

    for i in range(0,tasks):
        time_matrix.append([int(x) for x in next(file).split()])

    return tasks, machines, time_matrix


def draw_gantt(schedule,time_matrix):
    if len(time_matrix) != len(schedule):
        raise ValueError('Invalid sequnce number')
    tasksnr=len(time_matrix)
    machinesnr=len(time_matrix[0])
    m='Machine nr '
    task='Task nr '
    Cmatrix=[[0 for x in range(machinesnr)] for y in range(tasksnr)] #macierz czasow zakonczen poszczegolnych zadan na danej maszynie
    for i in range(0,tasksnr):
        for j in range(0,machinesnr):
            if i==0:
                if j==0:
                    Cmatrix[i][j]=time_matrix[schedule[i]-1][j]
                    df = pd.DataFrame([dict(Machine=m+str(j+1), Start=0, Finish=Cmatrix[i][j], Task=task+str(schedule[i]))])
                else:
                    Cmatrix[i][j]=(Cmatrix[i][j-1]+time_matrix[schedule[i]-1][j])
                    df=df.append(pd.DataFrame([dict(Machine=m+str(j+1), Start=Cmatrix[i][j-1], Finish=Cmatrix[i][j], Task=task+str(schedule[i]))]))
            else:
                if j==0:
                    Cmatrix[i][j]=Cmatrix[i-1][j]+time_matrix[schedule[i]-1][j]
                    df=df.append(pd.DataFrame([dict(Machine=m+str(j+1), Start=Cmatrix[i-1][j], Finish=Cmatrix[i][j], Task=task+str(schedule[i]))]))
                else:
                    Cmatrix[i][j]=max(Cmatrix[i-1][j],Cmatrix[i][j-1])+time_matrix[schedule[i]-1][j]
                    df=df.append(pd.DataFrame([dict(Machine=m+str(j+1), Start=max(Cmatrix[i-1][j],Cmatrix[i][j-1]), Finish=Cmatrix[i][j], Task=task+str(schedule[i]))]))
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Machine", color="Task")
    fig.update_yaxes(autorange="reversed")
    fig.layout.xaxis.type = 'linear'
    for i in range(0,tasksnr):
        fig.data[i].x = time_matrix[schedule[i]-1]
    fig.show()

    pass



def total_review(tasks,machines,time_matrix):
    pass
    # return schedule, Cmax


def johnson_for_2_machines(tasks:int,time_matrix_copy):
    time_matrix = time_matrix_copy.copy()
    task_on_list=list(range(1,tasks+1))
    listA=[]
    listB=[]
    time_matrix=np.array(time_matrix)
    

    while True:
        if not task_on_list:
            break

        index=np.unravel_index(time_matrix.argmin(), time_matrix.shape)
        time_matrix[index[0],0] = np.iinfo(np.int64).max   # przypisanie maksymalnych wartosci do czasow zadan ktore 'wyciagnelismy' z listy
        time_matrix[index[0],1] = np.iinfo(np.int64).max
        
        task_on_list.remove(index[0]+1)
        if index[1] == 0:
            listA.append(index[0]+1)
        else:
            listB.insert(0,index[0]+1)
        
    
    schedule = listA+listB
    
    
    Cmax=0  # max czas wykonania wszystkich operacji
    machine_tasks_ends=[] # tablica czasow zakonczenia kolejnych zadan na pierwszej maszynie

    for i in range(0,tasks):
        if i==0:
            machine_tasks_ends.append(time_matrix_copy[schedule[i]-1][0])
            Cmax=time_matrix_copy[schedule[i]-1][0]
        else:
            machine_tasks_ends.append(machine_tasks_ends[i-1]+time_matrix_copy[schedule[i]-1][0])
            if machine_tasks_ends[i] > ( Cmax + time_matrix_copy[schedule[i-1]-1][1] ):
                Cmax = machine_tasks_ends[i]
            else:
                Cmax = Cmax + time_matrix_copy[schedule[i-1]-1][1]

    Cmax =  Cmax + time_matrix_copy[schedule[-1]-1][1]  
    #na koniec musimy dodac jeszcze czas potrzebny na wykonanie ostatniego zadania z harmonogramu na 2 maszynie

    return schedule,Cmax;


def johnson_for_N_machines(tasks,machines,time_matrix):
    imaginary_times =  np.zeros((tasks,2))
    
    if machines%2 == 0:
        half=int(machines/2)  # polowa maszyn ktore wpadaja do jednej z wirtualnych maszyn
    else:
        half=int(machines/2)+1
   
    for i in range(0,tasks):
        for j in range(0,half):
            imaginary_times[i,0]+=time_matrix[i][j]
        for k in range(half-1,machines):
            imaginary_times[i,1]+=time_matrix[i][k]
    

    schedule,Cmax = johnson_for_2_machines(tasks,imaginary_times)
    
    return schedule
    # do zrobienia jeszcze liczenie Cmax




def main():
    path=""
    file_name="./datasets/" + "data.txt"
    number_of_datasets_to_read=5  # liczba setów, jakie mają zostac odczytane z pliku - mozemy na poczatku pracowac na tym pierwszym poczatkowym

    try:
        with open(path+file_name, "r") as file:
            for i in range(0,number_of_datasets_to_read):

                tasks,machines,time_matrix,Cmax,schedule=read_file_with_lots_of_datasets(file)     
                
                #tasks,machines,time_matrix=read_data_set(file)     
                
                schedule_from_func=johnson_for_N_machines(tasks,machines,time_matrix)
                
                if schedule_from_func != schedule:
                    print("Błąd",schedule_from_func,schedule)
                
                """
                schedule=johnson_for_N_machines(tasks,machines,time_matrix)
                draw_gantt(schedule,time_matrix)
                """

    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError


if __name__ == '__main__':
    main()
