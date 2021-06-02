from ortools.linear_solver import pywraplp
from job_shop_ortools import *
from rpq_ortools import *




def main():
    #job_shop_ortools('insa_set')

    test_instance = RPQ_Instance.load_from_file("datasets/rpq2")
    cmax, pi_order, status = solve_rpq_with_solver(test_instance)
    print(f"Cmax: {cmax}\norder: {pi_order}\n{status}")



if __name__ == '__main__':
    main()