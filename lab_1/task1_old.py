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

class Euler:
    x_arr = [0]     # направо
    _x_arr = [0]    # налево
    y_arr = [1]     # направо
    _y_arr = [1]    # налево
    dy_arr = [-0.5] # направо
    _dy_arr = [-0.5] # налево

    def __init__(self, h):
        self.h = h

    def x(self, ind):
        if ind >= 0:
            while len(self.x_arr) <= ind:
                self.x_arr.append(self.x(ind - 1) + self.h)
            return self.x_arr[ind]
        else:
            while len(self._x_arr) <= -ind:
                self._x_arr.append(self.x(ind + 1) - self.h)
            return self._x_arr[-ind]

    def y(self, ind):
        if ind >= 0:
            while len(self.y_arr) <= ind:
                self.y_arr.append(self.y(ind - 1) + self.h * self.dy(ind - 1))
            return self.y_arr[ind]
        else:
            while len(self._y_arr) <= -ind:
                self._y_arr.append(self.y(ind + 1) - self.h * self.dy(ind + 1))
            return self._y_arr[-ind]

    def dy(self, ind):
        if ind >= 0:
            while len(self.dy_arr) <= ind:
                self.dy_arr.append(self.dy(ind - 1) + self.h * self.ddy(ind - 1))
            return self.dy_arr[ind]
        else:
            while len(self._dy_arr) <= -ind:
                self._dy_arr.append(self.dy(ind + 1) - self.h * self.ddy(ind + 1))
            return self._dy_arr[-ind]

    def ddy(self, ind):
        if (abs(-2 * self.dy(ind) - self.y(ind)) < EPS and 
            abs(4 * self.x(ind)) < EPS):
            return 1 / 12   # правило Лапиталя, посчитано на листе
        if self.x(ind) == 0:
            print(ind, self._x_arr)
        return (-2 * self.dy(ind) - self.y(ind)) / (4 * self.x(ind))

    def get_x(self, left_cnt, right_cnt):
        x = [self.x_arr[0] + self.h * i for i in range(-left_cnt, right_cnt + 1)]
        return x

    def get_y(self, left_cnt, right_cnt):
        ry = [self.y(i) for i in range(right_cnt + 1)]
        ly = [self.y(-i) for i in range(1, left_cnt + 1)]
        ly.reverse()
        return ly + ry
    
    def get_dy(self, left_cnt, right_cnt):
        ry = [self.dy(i) for i in range(right_cnt + 1)]
        ly = [self.dy(-i) for i in range(1, left_cnt + 1)]
        ly.reverse()
        return ly + ry
    
    def get_ddy(self, left_cnt, right_cnt):
        _ddy_arr = []
        ddy_arr = []
        for i in range(right_cnt + 1):
            ddy_arr.append(self.ddy(i))
        
        for i in range(1, left_cnt + 1):
            _ddy_arr.append(self.ddy(-i))
        
        return list(reversed(_ddy_arr)) + ddy_arr



def Tailor(x):
    return 1 - x / 2 + x ** 2 / 24 - x ** 3 / 720


if __name__ == '__main__':
    print_tab = False
    st = -5
    end = 5
    h = 1e-1
    cnt = round((end - st) / h)
    print(f'cnt = {cnt * 2 + 1}')
    
    euler = Euler(h)
    xvals = euler.get_x(cnt, cnt)
    tyvals = [Tailor(xi) for xi in xvals]
    eyvals = euler.get_y(cnt, cnt)
    edyvals = euler.get_dy(cnt, cnt)
    eddyvals = euler.get_ddy(cnt, cnt)
    if print_tab:
        print('Euler')
        tab = PrettyTable()
        tab.field_names = ['x', 'y', 'dy', 'ddy']
        for i in range(len(xvals)):
            row = [f'{xvals[i]:.{accuracy}f}', f'{eyvals[i]:.{accuracy}f}', 
                    f'{edyvals[i]:.{accuracy}f}', f'{eddyvals[i]:.{accuracy}f}']
            tab.add_row(row)
        print(tab)

        print(Tailor)
        tab = PrettyTable()
        tab.field_names = ['x', 'y']
        for i in range(len(xvals)):
            row = [f'{xvals[i]:.{accuracy}f}', f'{tyvals[i]:.{accuracy}f}']
            tab.add_row(row)
        print(tab)

    tab = PrettyTable()
    tab.field_names = ['x', 'y Euler', 'y Tailor', 'diff']
    for i in range(len(xvals)):
        row = [f'{xvals[i]:.{accuracy}f}', f'{eyvals[i]:.{accuracy}f}', 
                f'{tyvals[i]:.{accuracy}f}', f'{eyvals[i] - tyvals[i]:.{accuracy}f}']
        tab.add_row(row)
    print(tab)

    plt.plot(xvals, tyvals, color='r', label='Tailor y(x)')
    plt.plot(xvals, eyvals, color='b', label='Euler y(x)')
    # plt.plot(xvals, edyvals, color='g', label='Euler dy')
    # plt.plot(xvals, eddyvals, color='y', label='Euler ddy')
    plt.xlabel('Ось х')  # Подпись для оси х
    plt.ylabel('Ось y')  # Подпись для оси y
    plt.title('График')  # Название
    plt.legend()
    plt.show()
    


    
