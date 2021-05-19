""" This file contains methods to code convolutional codes and decode them using Viterbi algorithm """

import numpy as np


def coder(input_arr):
    """ Basic method which code convolutional code with R = 1/2 """
    input_arr = np.insert(input_arr, len(input_arr), [0, 0])
    shift_reg = np.array([0, 0])
    output_arr = np.array([], dtype=int)
    for i in range(len(input_arr)):
        shift_reg = np.insert(shift_reg, 0, input_arr[i])
        output_arr = np.append(output_arr, (shift_reg[0] + shift_reg[1] + shift_reg[2]) % 2)
        output_arr = np.append(output_arr, (shift_reg[0] + shift_reg[2]) % 2)
    return output_arr


def get_way(input_arr):
    """This method return the optimal trellis' way"""
    input_arr = np.flip(input_arr, 0)
    way = np. zeros(len(input_arr))
    next_i = 0
    next_j = 0
    for i in range(len(input_arr)):
        for j in range(len(input_arr[i])):
            if i == next_i and j == next_j:
                way[i] = j
                next_i = i + 1
                next_j = input_arr[i][j][1]
    way = np.delete(way, -1)
    return way


def get_cell(input_arr, trellis):
    """ This method return trellis diagram """
    cell = np.zeros((int(len(input_arr) / 8 + 1), 4, 2))
    for i in range(1, len(cell)):
        for j in range(len(cell[i])):
            if j < 2:
                if i < 3:
                    cell[i][j][0] = mann_whitney(input_arr[i - 1:i + 7], trellis[j][0:2]) + cell[i - 1][0][0]
                else:
                    term1 = mann_whitney(input_arr[i - 1:i + 7], trellis[j][0:2]) + cell[i - 1][0][0]
                    term2 = mann_whitney(input_arr[i - 1:i + 7], trellis[j][2:]) + cell[i - 1][2][0]
                    if term1 > term2:
                        cell[i][j][0] = term1
                    else:
                        cell[i][j][0] = term2
                        cell[i][j][1] = 2
            if j > 1 and i > 1:
                if i < 3:
                    cell[i][j][0] = mann_whitney(input_arr[i - 1:i + 7], trellis[j][0:2]) + cell[i - 1][1][0]
                    cell[i][j][1] = 1
                else:
                    term1 = mann_whitney(input_arr[i - 1:i + 7], trellis[j][0:2]) + cell[i - 1][1][0]
                    term2 = mann_whitney(input_arr[i - 1:i + 7], trellis[j][2:]) + cell[i - 1][3][0]
                    if term1 > term2:
                        cell[i][j][0] = term1
                        cell[i][j][1] = 1
                    else:
                        cell[i][j][0] = term2
                        cell[i][j][1] = 3
    return cell


def st(input_arr):
    """This method creates an input signal for channel"""
    output_arr = np.zeros(len(input_arr) * 4)
    for i in range(len(input_arr)):
        output_arr[i * 4 + input_arr[i]] = 1
    return output_arr


def rt(input_arr):
    """This method creates an output signal for channel"""
    output_arr = np.zeros(len(input_arr))
    for i in range(len(input_arr)):
        r_com1 = np.random.normal(0, 1) + np.random.normal(0, 1) * 1j
        r_com2 = np.random.normal(0, 1) + np.random.normal(0, 1) * 1j
        r_poisson = np.random.poisson(0.1)
        r = input_arr[i] * r_com1 + (r_poisson * (10 ** 0.5) + 0.1 ** 0.5) * r_com2
        output_arr[i] = abs(r)
    return output_arr


def channel(input_arr):
    """This method imitate channel"""
    output_arr = np.argsort(np.argsort(rt(st(input_arr))))
    return output_arr


def mann_whitney(input_arr, trellis):
    """Realization of finding Mann-Whitney's criteria"""
    r1 = input_arr[trellis[0]]
    r2 = input_arr[trellis[1] + 4]
    crit = r1 + r2
    return crit


def decoder(input_arr):
    """ Basic method which decode convolutional code using Viterbi algorithm """
    trellis = np.array([[0, 0, 1, 1], [1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 0]])
    cell = get_cell(input_arr, trellis)
    way = get_way(cell)
    output_arr = np.zeros(int(len(input_arr) / 8))
    for i in range(len(way)):
        if way[i] == 1 or way[i] == 3:
            output_arr[i] = 1
    output_arr = output_arr[2:]
    return output_arr


ch = channel(coder(np.array([1, 1, 1, 1, 1])))
print(f"Результат работы декодирования {decoder(ch)}")
