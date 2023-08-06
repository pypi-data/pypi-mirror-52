from gooey import Gooey
import argparse
import multiprocessing
import time
import numpy as np
from scipy.spatial import cKDTree


class testclass:
    def __init__(self):
        self.arr = np.ones((100, 100))
        self.box_coords_data = np.empty(shape=(2, 2))

        self.box_coords_data[0, 0] = 1
        self.box_coords_data[0, 1] = 1
        self.box_coords_data[1, 0] = 2
        self.box_coords_data[1, 1] = 2

        self.box_coord_kdtree = cKDTree(self.box_coords_data)

    def test(self, i):

        print("Sleep", i, self.arr[0, 1])
        time.sleep(10)
        print("Done", i)


@Gooey
def _main_():
    parent = argparse.ArgumentParser(description="My program")
    parent.add_argument("-g", "--global", help="A global variable")
    subparsers = parent.add_subparsers(help="")
    parser_child_a = subparsers.add_parser(
        "childa", help="childa help", parents=[parent], add_help=False
    )
    parser_child_a.add_argument("-a", help="a option")

    parser_child_b = subparsers.add_parser(
        "childb", help="childb help", parents=[parent], add_help=False
    )
    parser_child_b.add_argument("-b", help="b option")

    args = parent.parse_args()

    poolargs = []

    for i in range(10):
        poolargs.append((testclass(), i))

    pool = multiprocessing.Pool()
    pool.map(wrapper, poolargs)


def wrapper(arg):
    obj, i = arg
    obj.test(i)


if __name__ == "__main__":
    _main_()
