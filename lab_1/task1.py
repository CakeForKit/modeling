from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np
import math as m

'''
4xu'' + 2u' + u = 0
x0 = 0, u(x0) = u0 = 1, u'(x0) = u'0 =  -0.5 
'''
EPS = 1e-7
accuracy = 5


def Tailor(x):
    return 1 - x / 2 + x ** 2 / 24 - x ** 3 / 720


def task1():
    x0 = 0
    y0 = 1
    dy0 = -0.5

    def ddyi(xi, yi, dyi):
        if -2 * dyi - yi == 0 and xi == 0:
            return 1 / 12
        return (-2 * dyi - yi) / (4 * xi)

    def dyip1(xi, yi, dyi, h):
        return dyi + h * ddyi(xi, yi, dyi)

    def yip1(yi, dyi, h):
        return yi + h * dyi
    
    xvals = [x0]
    eyvals = [y0]
    edyvals = [dy0]
    tyvals = [Tailor(x0)]
    funcvals = [y0]
    ravals = [0]

    hcur = 1e-5
    xmax = 15
    while xvals[-1] < xmax:
    # while ravals[-1] < 1e-4:
        xi = xvals[-1] + hcur
        yi = yip1(eyvals[-1], edyvals[-1], hcur)
        dyi = dyip1(xvals[-1], eyvals[-1], edyvals[-1], hcur)

        xvals.append(xi)
        eyvals.append(yi)
        edyvals.append(dyi)
        tyvals.append(Tailor(xvals[-1]))
        ravals.append(abs(eyvals[-1] - tyvals[-1]) / tyvals[-1])
        funcvals.append(m.cos(m.sqrt(xvals[-1])))
    print(f'cnt = {len(xvals)}')

    # tab = PrettyTable()
    # tab.field_names = ['x', 'y Euler', 'y Tailor', 'relative accuracy']
    # for i in range(len(xvals)):
    #     row = [f'{xvals[i]:.{accuracy}f}', f'{eyvals[i]:.{accuracy}f}', 
    #             f'{tyvals[i]:.{accuracy}f}', f'{ravals[i]:.{accuracy}f}']
    #     tab.add_row(row)
    # print(tab)

    plt.plot(xvals, tyvals, color='r', label='Tailor y(x)')
    plt.plot(xvals, eyvals, color='b', label='Euler y(x)')
    plt.plot(xvals, funcvals, color='g', label='cos(sqrt(x))')
    # plt.plot(xvals, edyvals, color='g', label='Euler dy')
    # plt.plot(xvals, eddyvals, color='y', label='Euler ddy')
    plt.xlabel('Ось х')  # Подпись для оси х
    plt.ylabel('Ось y')  # Подпись для оси y
    plt.title('График')  # Название
    plt.legend()
    plt.show()


import sys

if __name__ == '__main__':
    task1()


    
