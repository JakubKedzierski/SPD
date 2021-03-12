import sys
import unittest
from lab2_flowshop1.main import *


class TestPNGFileParser(unittest.TestCase):

    def test_if_data_is_read_properly_from_known_file(self):
         with open("data.txt", "r") as file:
            tasks,machines,time_matrix,Cmax,schedule=read_data_set(file)
            self.assertEqual(4,tasks)
            self.assertEqual(3,machines)
            self.assertEqual(32,Cmax)
            known_list=[1, 4, 3, 2]
            self.assertListEqual(known_list,schedule)


if __name__ == '__main__':
   unittest.main()
