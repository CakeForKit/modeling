from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np

EPS = 1e-7
accuracy = 5

class Euler:
    x_arr = [0]     # направо
    _x_arr = [0]    # налево
    y_arr = [0]     # направо
    _y_arr = [0]    # налево

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
        # print(f'self.y(ind) = {self.y(ind)}')
        return self.x(ind) + self.y(ind) * self.y(ind) * self.y(ind)

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
    

def Picar1(x):
    return (x ** 2) / 2

def Picar2(x):
    return (x ** 2) / 2 + (x ** 7) / 56



def Picar3(x):
    return ((x**(22))/(3863552) + 
            (3*x**(17))/(106624) + 
            (x**(12))/(896) + 
            (x**7)/(56) + 
            (x**2)/2)

def Picar4(x):
    return ((x**(67))/(3863981943017739124736)+
            (9*x**(62))/(98677964914244452352)+
            (1081*x**(57))/(73440052228804050944)+
            (76623*x**(52))/(53388985337387155456)+
            (310503*x**(47))/(3244062457475366912)+
            (1069*x**(42))/(224099368435712)+
            (790667*x**(37))/(4145838316060672)+
            (11871*x**(32))/(1883187970048)+
            (361*x**(27))/(2101772288)+
            (47*x**(22))/(11941888)+
            (33*x**(17))/(426496)+
            (x**(12))/(896)+
            (x**7)/(56)+
            (x**2)/2)
    

if __name__ == '__main__':
    st = 0
    end = 2
    h = 0.05
    lcnt = round((0 - st) / h)
    rcnt = round((end - 0) / h)
    print(f'cnt = {lcnt + rcnt}')

    euler = Euler(h)
    xvals = euler.get_x(lcnt, rcnt)
    eyvals = euler.get_y(lcnt, rcnt)

    p1yvals = [Picar1(xi) for xi in xvals]
    p2yvals = [Picar2(xi) for xi in xvals]
    p3yvals = [Picar3(xi) for xi in xvals]
    p4yvals = [Picar4(xi) for xi in xvals]


    tab = PrettyTable()
    tab.field_names = ['x', 'y Euler', 'y Picar1', 'y Picar2', 'y Picar3', 'y Picar4']
    for i in range(len(xvals)):
        row = [f'{xvals[i]:.{accuracy}f}', f'{eyvals[i]:.{accuracy}f}',
               f'{p1yvals[i]:.{accuracy}f}', f'{p2yvals[i]:.{accuracy}f}',
               f'{p3yvals[i]:.{accuracy}f}', f'{p4yvals[i]:.{accuracy}f}']
        tab.add_row(row)
    print(tab)


    plt.plot(xvals, eyvals, color='r', marker='.', label='Euler y(x)')
    plt.plot(xvals, p1yvals, color='g', marker=',', label='Picar1 y(x)')
    plt.plot(xvals, p2yvals, color='b', marker='o', label='Picar2 y(x)')
    plt.plot(xvals, p3yvals, color='c', marker='v', label='Picar3 y(x)')
    plt.plot(xvals, p4yvals, color='m', marker='>', label='Picar4 y(x)')
    plt.xlabel('Ось х')  # Подпись для оси х
    plt.ylabel('Ось y')  # Подпись для оси y
    plt.title('График')  # Название
    plt.legend()
    plt.show()


