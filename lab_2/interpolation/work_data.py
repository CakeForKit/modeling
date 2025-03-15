DEBUG = False


def find_start_end_ind_x(filename, x, size, debug=DEBUG):
    with open(filename) as f:
        f.readline() # считываем шапку
        # print(f.readline())
        min_diff = abs(x - float(f.readline().split()[0]))
        ind = i = 0

        elem = f.readline()
        while elem != '':
            elem = float(elem.split()[0])
            i += 1
            if abs(x - elem) < min_diff:
                ind = i
                min_diff = abs(x - elem)
            elem = f.readline()

    before = size // 2
    after = size - before - 1
    # print(f'before = {before}, after = {after}, ind = {ind}')
    if ind >= before and i - ind >= after:
        st_ind = ind - before
        end_ind = ind + after
    elif ind <= after:
        st_ind, end_ind = 0, size - 1
    else:
        st_ind, end_ind = i - size + 1, i

    if debug:
        print(f'find_start_end_ind:\t x = {x}, (st, end) = ({st_ind, end_ind})')

    return st_ind, end_ind


# предполагается что строк в таблице >= n + 1
# return data = [[x, y, y', y''], ...]
def read_short_data(filename, x, n):
    st, end = find_start_end_ind_x(filename, x, n + 1, debug=False)
    data = list()
    with open(filename) as f:
        f.readline() # считываем шапку
        i = 0

        elem = f.readline()
        while elem != '' and i <= end:
            if st <= i <= end:
                data.append(list(map(float, elem.split())))

            elem = f.readline()
            i += 1
    return data


def find_start_end_root(filename, size, debug=False):
    with open(filename) as f:
        f.readline() # считываем шапку
        elem1 = float(f.readline().split()[1])
        ind = i = 0

        str = f.readline()
        while str != '':
            elem2 = float(str.split()[1])
            i += 1
            if elem1 * elem2 <= 0:
                ind = i
            elem1 = elem2
            str = f.readline()

    before = size // 2
    after = size - before - 1
    # print(f'before = {before}, after = {after}, ind = {ind}')
    if ind >= before and i - ind >= after:
        st_ind = ind - before
        end_ind = ind + after
    elif ind <= after:
        st_ind, end_ind = 0, size - 1
    else:
        st_ind, end_ind = i - size + 1, i

    if debug:
        print(f'find_start_end_root:\t (st, end) = ({st_ind, end_ind})')

    return st_ind, end_ind


# предполагается что строк в таблице >= n + 1
# и в таблице есть корень
def read_data_search_root(filename, n):
    st, end = find_start_end_root(filename, n + 1, debug=False)
    data = list()
    with open(filename) as f:
        f.readline()  # считываем шапку
        i = 0

        elem = f.readline()
        while elem != '' and i <= end:
            if st <= i <= end:
                data.append(list(map(float, elem.split())))

            elem = f.readline()
            i += 1
    return data


def read_data_f_g(file_f, file_g):
    f_data, g_data = list(), list()
    with open(file_f) as f:
        f.readline()  # считываем шапку
        line = f.readline()
        while line != '':
            f_data.append(list(map(float, line.split())))
            line = f.readline()

    with open(file_g) as f:
        f.readline()  # считываем шапку
        line = f.readline()
        while line != '':
            g_data.append(list(map(float, line.split())))
            line = f.readline()

    return f_data, g_data


def build_short_data_x_from_data(data, x, size, debug=DEBUG):
    min_diff = abs(x - float(data[0][0]))
    ind = i = 0
    while i + 1 < len(data):
        i += 1
        diff = abs(x - data[i][0])
        if diff < min_diff:
            ind = i
            min_diff = diff
    before = size // 2
    after = size - before - 1
    if ind >= before and i - ind >= after:
        st_ind = ind - before
        end_ind = ind + after
    elif ind <= after:
        st_ind, end_ind = 0, size - 1
    else:
        st_ind, end_ind = i - size + 1, i

    return data[st_ind:end_ind + 1]


def build_short_data_root_from_data(data, size, debug=False):
    elem1 = data[0][1]
    ind = i = 0
    while i + 1 < len(data):
        i += 1
        elem2 = data[i][1]
        if elem1 * elem2 <= 0:
            ind = i
        elem1 = elem2

    before = size // 2
    after = size - before - 1
    # print(f'before = {before}, after = {after}, ind = {ind}')
    if ind >= before and i - ind >= after:
        st_ind = ind - before
        end_ind = ind + after
    elif ind <= after:
        st_ind, end_ind = 0, size - 1
    else:
        st_ind, end_ind = i - size + 1, i

    return data[st_ind:end_ind + 1]


def read_data(filename):
    data = list()
    with open(filename) as f:
        f.readline()
        line = f.readline()
        while line != '':
            data.append(list(map(float, line.split()))[:2])
            line = f.readline()
    return data