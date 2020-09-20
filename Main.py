import msvcrt as m
from colorama import Fore, Style, init

init(convert=True)


def check_field(array):
    test = True
    valid_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if (len(array) == 9):
        for i in range(len(array)):
            for j in range(len(array[i])):
                if (len(array[i]) != 9):
                    test = False
                if (array[i][j] not in valid_characters):
                    test = False
            if (test == False):
                break
    else:
        test = False

    return test


def data_load(string):
    try:
        f = open(string, 'r')
    except:
        print('Unable to open sudoku.txt file!')
        print('File was renamed, moved or deleted!')
        m.getch()
    content = f.read().split('\n')
    try:
        value = 1 / int(check_field(content))
    except:
        print('Given sudoku field is incorrect!')
        print('Wrong size and/or forbidden character!')
        m.getch()
    array = []
    for i in range(len(content)):
        row = []
        for j in range(len(content[0])):
            row.append(int(content[i][j]))
        array.append(row)
    f.close()

    return array


def internal_square_index_position(index_table):
    for i in range(len(index_table)):
        if (index_table[i] < 3):
            index_table[i] = 0
            continue
        if (index_table[i] < 6):
            index_table[i] = 3
            continue
        index_table[i] = 6

    return index_table


def flat_nested_list(array):
    row = []
    for i in range(len(array)):
        for j in range(len(array[i])):
            row.append(array[i][j])

    return row


def match_array(array):
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    match = []
    for i in range(len(numbers)):
        if (numbers[i] not in array):
            match.append(numbers[i])

    return match


def possible_numbers(array):
    possible_array = []
    for i in range(len(array)):
        for j in range(len(array[0])):
            if (array[i][j] != 0):
                continue
            used_numbers = []
            
            used_numbers.append(array[i])
            
            row = []
            for k in range(len(array)):
                row.append(array[k][j])
            used_numbers.append(row)
            
            internal_square_begin_index=(internal_square_index_position([i, j]))
            for k in range(3):
                used_numbers.append(array[internal_square_begin_index[0] + k][
                                    internal_square_begin_index[1]:internal_square_begin_index[1] + 3])

            used_numbers = flat_nested_list(used_numbers)
            possible_array.append(match_array(used_numbers))

    return possible_array


def check_length(array):
    check = -1
    for i in range(len(array)):
        if (len(array[i]) == 1):
            check = i
            break

    return check


def change_number(array, number, position):
    counter = 0
    flag = True
    for i in range(len(array)):
        if (not (flag)):
            break
        for j in range(len(array[0])):
            if (array[i][j] == 0):
                counter += 1
            if (counter == position + 1):
                array[i][j] = number
                flag = False
                break

    return array


def check_possible_array(array):
    result = True
    for i in range(len(array)):
        if (len(array[i]) == 0):
            result = False
            break

    return result


def min_len_possible_array_index(array):
    minimum_index = 0
    minimum = 10
    for i in range(len(array)):
        if (len(array[i]) < minimum):
            minimum = len(array[i])
            minimum_index = i

    return minimum_index


def add_to_array(array):
    new_array = []
    for i in range(len(array)):
        row = []
        for j in range(len(array[0])):
            row.append(array[i][j])
        new_array.append(row)

    return list(new_array)


def main(array):
    old_array = add_to_array(array)
    loopstatus = True
    array_backup = []
    assumption_index_backup = []
    assumption_backup = []

    while loopstatus:
        try:
            possible_array = possible_numbers(array)
            loopstatus = bool(len(possible_array))
            if (loopstatus):
                if (check_possible_array(possible_array)):
                    if (check_length(possible_array) >= 0):
                        array = change_number(array, possible_array[check_length(possible_array)][0],
                                              check_length(possible_array))
                    else:
                        array_backup.append(add_to_array(array))
                        assumption_index_backup.append(min_len_possible_array_index(possible_array))
                        assumption_backup.append(possible_array[min_len_possible_array_index(possible_array)])
                        array = change_number(array, assumption_backup[-1][0], assumption_index_backup[-1])
                else:
                    del assumption_backup[-1][0]
                    if (len(assumption_backup[-1])):
                        array = array_backup[-1]
                        array = change_number(array, assumption_backup[-1][0], assumption_index_backup[-1])
                    else:
                        loopstatus2 = True
                        while loopstatus2:
                            del assumption_backup[-1]
                            del assumption_backup[-1][0]
                            del assumption_index_backup[-1]
                            del array_backup[-1]
                            loopstatus2 = not (bool(len(assumption_backup[-1])))

                        array = array_backup[-1]
                        array = change_number(array, assumption_backup[-1][0], assumption_index_backup[-1])
        except:
            print('Fixed points in sudoku field are incorrect!')
            m.getch()

    return (array, old_array)


def format_output(arrays):
    array = arrays[0]
    old_array = arrays[1]
    line = f'{Style.BRIGHT}'
    line += '-------------------------'
    for i in range(len(array)):
        if (i % 3 == 0):
            print(line)
        string = f'{Style.BRIGHT}'
        for j in range(len(array[0])):
            if (j == 0):
                string += '| '
            if (old_array[i][j] == 0):
                string += str(f'{Fore.BLUE}' + str(array[i][j]) + f'{Fore.RESET}')
            else:
                string += str(f'{Fore.WHITE}' + str(array[i][j]) + f'{Fore.RESET}')
            if ((j + 1) % 3 == 0):
                string += ' | '
            else:
                string += ' '
        print(string)
    print(line)


# Start program
def run():
    return format_output(main(data_load('sudoku.txt')))


run()
m.getch()
