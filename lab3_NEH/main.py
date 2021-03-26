import plotly.express as px
import pandas as pd
import numpy as np


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

def count_cmax(schedule, time_matrix):
    tasks=len(schedule)
    machines=len(time_matrix[0])
    Cmatrix=[[0 for x in range(machines)] for y in range(tasks)] #macierz czasow zakonczen poszczegolnych zadan na danej maszynie
    for i in range(0,tasks):
        for j in range(0,machines):
            if i==0:
                if j==0:
                    Cmatrix[i][j]=time_matrix[schedule[i]-1][j]
                else:
                    Cmatrix[i][j]=(Cmatrix[i][j-1]+time_matrix[schedule[i]-1][j])
            else:
                if j==0:
                    Cmatrix[i][j]=Cmatrix[i-1][j]+time_matrix[schedule[i]-1][j]
                else:
                    Cmatrix[i][j]=max(Cmatrix[i-1][j],Cmatrix[i][j-1])+time_matrix[schedule[i]-1][j]

    #print(schedule,Cmatrix[tasks-1][machines-1])                
    return Cmatrix[tasks-1][machines-1]

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
        if index[1] == 0: # jesli pierwsza maszyna to:
            listA.append(index[0]+1)
        else:
            listB.insert(0,index[0]+1)
        
    
    schedule = listA+listB
    Cmax=count_cmax(schedule,time_matrix_copy)

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
    

    schedule,virutal_c_max = johnson_for_2_machines(tasks,imaginary_times)
    Cmax = count_cmax(schedule,time_matrix)
    
    return schedule,Cmax

    
def NEH_algorithm(tasks,machine,time_matrix):
    time_matrix=np.array(time_matrix)
    w2=np.sum(time_matrix,axis=1).tolist()
    w=[i * (-1) for i in w2]
    sorted_order=np.argsort(w,kind='mergesort') + 1
    schedule=[sorted_order[0]]
    for i in range (1,tasks):
        best_in=0
        temp_schedule=schedule
        for j in range(0,i+1): 
            temp_schedule.insert(j,sorted_order[i])
            #print(temp_schedule)
            if j==0:
                Cmax=count_cmax(temp_schedule,time_matrix)
            else:
                Cmax_temp=count_cmax(temp_schedule,time_matrix)
                if (Cmax_temp<Cmax):
                    best_in=j
                    Cmax=Cmax_temp
            temp_schedule.pop(j)
        schedule.insert(best_in,sorted_order[i])
    return schedule,Cmax




def main():
    path=""
    file_name="./datasets/" + "data072.txt"
    number_of_datasets_to_read=1  # liczba setów, jakie mają zostac odczytane z pliku - mozemy na poczatku pracowac na tym pierwszym poczatkowym

    try:
        with open(path+file_name, "r") as file:
            for i in range(0,number_of_datasets_to_read):
                
                tasks,machines,time_matrix=read_data_set(file)  

                               
                
                schedule_from_func,Cmax=NEH_algorithm(tasks,machines,time_matrix)
                print(Cmax)
                print(schedule_from_func)
                #draw_gantt(schedule_from_func,time_matrix)
                
                

    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError


if __name__ == '__main__':
    main()