from interpolation.newton import polynom_newton
from interpolation.work_data import build_short_data_x_from_data
import matplotlib.pyplot as plt

import numpy as np


def read_data_kT(variant=1):
    data_tab = []
    with open('data/kT.txt') as file:
        line = file.readline()
        while line != '':
            line = line.split()
            if variant == 1:
                data_tab.append([int(line[1]), float(line[2])])
            else:
                data_tab.append([int(line[1]), float(line[3])])

            line = file.readline()

        return data_tab
    
data_kT = read_data_kT(variant=1)

def k(T, printing=False):
    n = 3
    x = T
    short_data = build_short_data_x_from_data(data_kT, x, n + 1)
    return polynom_newton(short_data, x, n, printing)

def draw_graphic_k():
    Tvals = np.arange(data_kT[0][0], data_kT[-1][0] + 1, 100)
    kvals = [k[t] for t in range(Tvals)]

    plt.plot(Tvals, kvals, color='g')
    plt.xlabel('Ось х')  # Подпись для оси х
    plt.ylabel('Ось y')  # Подпись для оси y
    plt.title('График')  # Название
    plt.legend()
    plt.show()


if __name__ == '__main__':
    
    # T = 7500
    # print(k(T))

    draw_graphic_k()