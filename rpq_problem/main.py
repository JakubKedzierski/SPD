def read_data_set(file):
    tasks, columns = [int(x) for x in next(file).split()]

    r = []
    p = []
    q = []

    for i in range(0, tasks):
        row = next(file).split()
        r.append(int(row[0]))
        p.append(int(row[1]))
        q.append(int(row[2]))

    return tasks, r, p, q


def main():
    path=""
    file_name="./datasets/" + "in50.txt"
    number_of_datasets_to_read= 1

    try:
        with open(path + file_name, "r") as file:
            tasks, r, p, q = read_data_set(file)

    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError


if __name__ == '__main__':
    main()