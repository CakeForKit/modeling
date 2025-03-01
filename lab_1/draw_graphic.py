from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np



def draw_graphic(xvals, yvals):

    plt.plot(xvals, yvals, color='g')
    plt.xlabel('Ось х')  # Подпись для оси х
    plt.ylabel('Ось y')  # Подпись для оси y
    plt.title('График')  # Название
    plt.legend()
    plt.show()


# if __name__ == '__main__':
#     draw_graphic(FILE_DATA, N, printing=DEBUG)