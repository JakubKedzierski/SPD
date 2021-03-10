import sys


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



def main():
    path=""
    file_name="data.txt"
    number_of_datasets_to_read=1

    try:
        with open(path+file_name, "r") as file:
            for i in range(0,number_of_datasets_to_read):
                tasks,machines,time_matrix,Cmax,schedule=read_data_set(file)
                
                print(tasks,machines,"\n",time_matrix,"\n",Cmax,"\n",schedule)
            

    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError



if __name__ == '__main__':
    main()