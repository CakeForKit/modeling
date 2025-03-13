
def break_point():
    x0, y0 = 0, 0

    def dyi(xi, yi):
        return xi + yi ** 3

    def yip1(xi, yi, h):
        return yi + h * dyi(xi, yi)

    def yip1_2h(xi, yi, h):
        yih = yip1(xi, yi, h)
        xih = xi + h
        return yip1(xih, yih, h)

    hcur = 1e-2
    rel_accuracy = 1e-4
    xvals = [x0, x0 + hcur]
    eyvals = [y0, yip1(x0, y0, hcur)]
    # eyh2vals = [y0, yip1(x0, y0, hcur)]

    # change = False
    # print(f'h = {hcur}')
    while eyvals[-1] != float('inf'): 
        try:
            yh = yip1(xvals[-1], eyvals[-1], hcur)
            yh2 = yip1_2h(xvals[-1], eyvals[-1], hcur / 2)
            while abs(yh - yh2) / yh2 >= rel_accuracy:
                # change = True
                hcur /= 2
                yh = yip1(xvals[-1], eyvals[-1], hcur)
                yh2 = yip1_2h(xvals[-1], eyvals[-1], hcur / 2)
            # if change:
            #     change = False
            #     print(f'h = {hcur}')
            eyvals.append(yh)
            xvals.append(xvals[-1] + hcur)
        except OverflowError:
            break

    print(f'xmax = {xvals[-1]}')
    print(f'h_last = {hcur}')

    # accuracy = 10
    # tab = PrettyTable()
    # tab.field_names = ['x', 'y Euler']
    # for i in range(len(xvals)):
    #     row = [f'{xvals[i]:.{accuracy}f}', f'{eyvals[i]:.{accuracy}f}']
    #     tab.add_row(row)
    # print(tab)

    
    plt.plot(xvals, eyvals, color='r', marker='.', label='Euler y(x)')
    plt.xlabel('Ось х')  # Подпись для оси х
    plt.ylabel('Ось y')  # Подпись для оси y
    plt.title('График')  # Название
    plt.legend()
    plt.show()
