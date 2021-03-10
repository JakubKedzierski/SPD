
def read_data_set(file):
    file.readline()
    tasks, machines = [int(x) for x in next(file).split()] 
    time_matrix = [] 
    
    for i in range(0,tasks):
        time_matrix.append([int(x) for x in next(file).split()])
        
    file.readline()
    file.readline()
    Cmax = int(file.readline())
    schedule= [int(x) for x in next(file).split()] 
    file.readline()

    return tasks,machines,time_matrix,Cmax,schedule

def draw_gantt(schedule,time_matrix):
    pass



def total_review(tasks,machines,time_matrix):
    pass
    # return schedule, Cmax


def johnson_for_2_machines(tasks,machines,time_matrix):
    pass
    # return schedule, Cmax


def johnson_for_N_machines(tasks,machines,time_matrix):
    pass
    # return schedule, Cmax



def main():
    path=""
    file_name="data.txt"
    number_of_datasets_to_read=1   # liczba setów, jakie mają zostac odczytane z pliku - mozemy na poczatku pracowac na tym pierwszym poczatkowym

    try:
        with open(path+file_name, "r") as file:
            for i in range(0,number_of_datasets_to_read):
                tasks,machines,time_matrix,Cmax,schedule=read_data_set(file)

                """
                Cmax i schedule - sa to wyniki z danego datasetu, mozemy je uzyc gdzies pozniej do testowania danych
                na przyklad w taki sposób:
                """

                """
                 our_schedule, our_Cmax = johnson_for_2_machines
                 if (our_schedule == schedule and our_Cmax = Cmax) good_result_count++
                """
                
                # print(tasks,machines,"\n",time_matrix,"\n",Cmax,"\n",schedule)
            

    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError



if __name__ == '__main__':
    main()