import msvcrt as m
from colorama import Fore, Style, init

init(convert=True)


class LoadSudokuBoard:
    def __init__(self, file_name='sudoku.txt'):
        self.file_name = file_name
        self.board = self.load_data_from_text_file()

    def load_data_from_text_file(self):
        try:
            f = open(self.file_name, 'r')
        except:
            print('Unable to open ' + self.file_name + ' file!\nFile was renamed, moved or deleted!')
            return None

        board = f.read().split('\n')

        try:
            value = 1 / int(self.check_user_input_correctness(board))
        except:
            print('Given sudoku field is incorrect!\nWrong size and/or forbidden character!')
            return None

        f.close()

        return [[int(el) for el in row] for row in board]

    @staticmethod
    def check_user_input_correctness(board):
        valid_characters = [str(number) for number in range(10)]
        if len(board) == 9:
            for i in range(len(board)):
                if len(board[i]) != 9:
                    return False
                for j in range(len(board[i])):
                    if board[i][j] not in valid_characters:
                        return False
        else:
            return False

        return True

    def get_user_board(self):
        return self.board


class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.old_board = [[el for el in row] for row in self.board]
        self.possible_numbers_in_the_field_list = None

    @staticmethod
    def internal_square_index_position(index_table):
        for i in range(len(index_table)):
            if index_table[i] < 3:
                index_table[i] = 0
            elif index_table[i] < 6:
                index_table[i] = 3
            else:
                index_table[i] = 6

        return index_table

    def possible_numbers_in_the_field(self):
        possible_numbers_in_the_field_list = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]:
                    continue
                used_numbers = []
                used_numbers.append(self.board[i])

                row = []
                for k in range(len(self.board)):
                    row.append(self.board[k][j])
                used_numbers.append(row)

                internal_square_begin_index = (self.internal_square_index_position([i, j]))
                for k in range(3):
                    used_numbers.append(self.board[internal_square_begin_index[0] + k][internal_square_begin_index[1]:internal_square_begin_index[1] + 3])

                used_numbers = [el for row in used_numbers for el in row]
                possible_numbers_in_the_field_list.append([number for number in [1, 2, 3, 4, 5, 6, 7, 8, 9] if number not in used_numbers])

        return possible_numbers_in_the_field_list

    def locate_field_with_only_one_possibility(self):
        for i in range(len(self.possible_numbers_in_the_field_list)):
            if len(self.possible_numbers_in_the_field_list[i]) == 1:
                return i

        return -1

    def change_number_on_the_board(self, number, empty_field_index):
        counter = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    counter += 1
                if counter == empty_field_index + 1:
                    self.board[i][j] = number
                    return

    def check_if_board_is_possible_to_solve(self):
        for i in range(len(self.possible_numbers_in_the_field_list)):
            if not len(self.possible_numbers_in_the_field_list[i]):
                return False

        return True

    def locate_the_field_with_the_lowest_amount_of_possibilities(self):
        minimum_index, minimum = 0, 10
        for i in range(len(self.possible_numbers_in_the_field_list)):
            if len(self.possible_numbers_in_the_field_list[i]) < minimum:
                minimum = len(self.possible_numbers_in_the_field_list[i])
                minimum_index = i

        return minimum_index

    def main(self):
        loop_status = True
        array_backup, assumption_index_backup, assumption_backup = [], [], []

        while loop_status:
            self.possible_numbers_in_the_field_list = self.possible_numbers_in_the_field()
            loop_status = bool(len(self.possible_numbers_in_the_field_list))
            if loop_status:
                if self.check_if_board_is_possible_to_solve():
                    if self.locate_field_with_only_one_possibility() >= 0:
                        min_index = self.locate_field_with_only_one_possibility()
                        self.change_number_on_the_board(self.possible_numbers_in_the_field_list[min_index][0], min_index)
                    else:
                        array_backup.append([[el for el in row] for row in self.board])
                        assumption_index_backup.append(self.locate_the_field_with_the_lowest_amount_of_possibilities())
                        assumption_backup.append(self.possible_numbers_in_the_field_list[self.locate_the_field_with_the_lowest_amount_of_possibilities()])
                        self.change_number_on_the_board(assumption_backup[-1][0], assumption_index_backup[-1])
                else:
                    del assumption_backup[-1][0]
                    if len(assumption_backup[-1]):
                        self.board = array_backup[-1]
                        self.change_number_on_the_board(assumption_backup[-1][0], assumption_index_backup[-1])
                    else:
                        loop_status2 = True
                        while loop_status2:
                            del assumption_backup[-1]
                            del assumption_backup[-1][0]
                            del assumption_index_backup[-1]
                            del array_backup[-1]
                            loop_status2 = not (bool(len(assumption_backup[-1])))

                        self.board = array_backup[-1]
                        self.change_number_on_the_board(assumption_backup[-1][0], assumption_index_backup[-1])

        return self.format_output()

    def format_output(self):
        line = f'{Style.BRIGHT}'
        line += '-------------------------'
        for i in range(len(self.board)):
            if i % 3 == 0:
                print(line)
            string = f'{Style.BRIGHT}'
            for j in range(len(self.board[0])):
                if not j:
                    string += '| '
                if not self.old_board[i][j]:
                    string += str(f'{Fore.BLUE}' + str(self.board[i][j]) + f'{Fore.RESET}')
                else:
                    string += str(f'{Fore.WHITE}' + str(self.board[i][j]) + f'{Fore.RESET}')
                if (j + 1) % 3 == 0:
                    string += ' | '
                else:
                    string += ' '
            print(string)
        print(line)

    def run(self):
        if self.board is not None:
            return self.main()
        else:
            print('Invalid board')


SudokuSolver(LoadSudokuBoard().get_user_board()).run()
m.getch()
