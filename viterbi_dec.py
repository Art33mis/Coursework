""" This file contains methods to code convolutional codes and decode them using Viterbi algorithm """

import math
import numpy as np


def coder(input_arr):
    """ Basic method which code convolutional code with R = 1/2 """
    input_str = ''.join(list(map(str, map(chr, np.packbits(input_arr)))))
    output_str = ""
    shift_reg = "00"
    for i in range(len(input_str)):
        shift_reg = input_str[i] + shift_reg
        output1 = (int(shift_reg[0]) + int(shift_reg[1]) + int(shift_reg[2])) % 2
        output2 = (int(shift_reg[0]) + int(shift_reg[2])) % 2
        output_str = output_str + str(output1) + str(output2) + " "
    output_list = list(map(str, map(ord, output_str[:-1])))
    output_arr = np.unpackbits(np.uint8(output_list))
    return output_arr


def get_min_index(cell):
    """ This method return index of the smallest value in array """
    min_num = math.inf
    min_ind = 0
    for i in range(len(cell)):
        if cell[i] < min_num:
            if i != 0:
                if cell[i] <= cell[i - 1]:
                    min_ind = i
                else:
                    min_ind = i - 1
    return min_ind


def hamming_distance(str1, str2):
    """ Method return Hamming distance between to strings """
    distance = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            distance += 1
    return distance


def get_cell(input_list, trellis):
    """ This method return trellis diagram """
    cell = np.array([[math.inf] * 4 for i in range(len(input_list) + 1)])
    cell[0][0] = 0
    for i in range(len(cell)):
        for j in range(len(cell)):
            if j == 0 and i != 0:
                cell[i][j] = min(hamming_distance(input_list[i - 1], trellis[0][0]) + cell[i - 1][0],
                                 hamming_distance(input_list[i - 1], trellis[0][1]) + cell[i - 1][2])
            elif j == 1 and i != 0:
                cell[i][j] = min(hamming_distance(input_list[i - 1], trellis[1][0]) + cell[i - 1][0],
                                 hamming_distance(input_list[i - 1], trellis[1][1]) + + cell[i - 1][2])
            elif j == 2 and i > 1:
                cell[i][j] = min(hamming_distance(input_list[i - 1], trellis[2][0]) + cell[i - 1][1],
                                 hamming_distance(input_list[i - 1], trellis[2][1]) + + cell[i - 1][3])
            elif j == 3 and i > 1:
                cell[i][j] = min(hamming_distance(input_list[i - 1], trellis[3][0]) + cell[i - 1][1],
                                 hamming_distance(input_list[i - 1], trellis[3][1]) + + cell[i - 1][3])
    return cell


def st(input_str):
    """This method creates an input signal for channel"""
    input_arr = np.array(list(input_str), dtype=int)
    output_arr = np.array([], dtype=int)
    for i in range(len(input_arr)):
        if input_arr[i] == 1:
            output_arr = np.concatenate([output_arr, [0, 1, 0, 0]])
        if input_arr[i] == 0:
            output_arr = np.concatenate([output_arr, [1, 0, 0, 0]])
    return output_arr


def rt(input_arr):
    """This method creates an output signal for channel"""
    output_arr = np.array([], dtype=int)
    for i in range(len(input_arr)):
        r_com1 = np.random.randint(100) + np.random.randint(100)*1j
        r_com2 = np.random.randint(100) + np.random.randint(100)*1j
        r_poisson = np.random.poisson(10)
        r = input_arr[i]*r_com1 + (r_poisson*(10**0.5) + 0.1**0.5)*r_com2
        output_arr = np.append(output_arr,  int(r.real))
    return output_arr


def m_w(input_str):
    return []



def decoder(input_arr):
    """ Basic method which decode convolutional code using Viterbi algorithm """
    input_str = ''.join(list(map(str, map(chr, np.packbits(input_arr)))))
    input_list = input_str.split(" ")
    trellis = np.array([["00", "11"], ["11", "00"], ["10", "01"], ["01", "10"]])
    way = np.array([0 for i in range(len(input_list) + 1)])
    cell = get_cell(input_list, trellis)
    for i in range(len(cell)):
        way[i] = get_min_index(cell[i])
    output_str = ""
    for i in range(len(way)):
        if i != 0:
            if way[i] == 0 or way[i] == 2:
                output_str = output_str + "0"
            if way[i] == 1 or way[i] == 3:
                output_str = output_str + "1"
    output_arr = np.unpackbits(np.uint8(list(output_str)))
    return output_arr


''' print(coder(np.unpackbits(np.uint8(list(b'11111')))))
print(decoder(coder(np.unpackbits(np.uint8(list(b'11111'))))))
print(np.unpackbits(np.uint8(list(b'hello'))))
print(np.packbits(np.unpackbits(np.uint8(list(b'hello')))))
print(np.argsort([1, 0, 1])) '''
print(st("11"))
print(rt(st("11")))


