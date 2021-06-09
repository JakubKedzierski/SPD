from ortools.linear_solver import pywraplp
from job_shop_ortools import *
from rpq_ortools import *
from witi_ortools import *
from flowshop_ortools import *

def rpq_ortools(file_path):
    test_instance = RPQ_Instance.load_from_file(file_path)
    cmax, pi_order = solve_rpq_with_solver(test_instance)
    print(f"Cmax: {cmax}\norder: {pi_order}\n")

def witi_ortools(file_path):
    test_instance = WiTi_Instance.load_from_file(file_path)
    objective, pi_order = solve_witi_with_solver(test_instance)
    print(f"f(s) (suma wazonych spoznien): {objective}\norder: {pi_order}\n")


def main():
    #job_shop_ortools('insa_set')
    #rpq_ortools('datasets/rpq2')
    #witi_ortools('datasets/witi_single_data')
    flowshop_ortools('data000.txt')




if __name__ == '__main__':
    main()