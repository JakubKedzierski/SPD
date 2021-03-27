import numpy as np
import plotly.express as px
import pandas as pd


def count_cmax(schedule, time_matrix):
    tasks=len(schedule)
    machines=len(time_matrix[0])
    Cmatrix = count_Cmatrix(schedule, time_matrix)

    #print(schedule,Cmatrix[tasks-1][machines-1])
    return Cmatrix[tasks-1][machines-1]


def count_Cmatrix(schedule, time_matrix):
    tasks=len(schedule)
    machines=len(time_matrix[0])
    Cmatrix=np.zeros((tasks,machines))
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
    return Cmatrix


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