""" This file contains methods to code convolutional codes and decode them using Viterbi algorithm """

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
    min_num = 0
    max_num = 0
    min_ind = 0
    for i in range(len(cell)):
        if cell[i] > min_num:
            if i != 0:
                if cell[i] >= cell[i - 1] and cell[i] > max_num:
                    min_ind = i
                    max_num = cell[i]
                if cell[i - 1] > cell[i] > max_num:
                    min_ind = i - 1
                    max_num = cell[i - 1]
    return min_ind


def hamming_distance(str1, str2):
    """ Method return Hamming distance between two strings """
    distance = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            distance += 1
    return distance


def get_cell(input_arr, trellis):
    """ This method return trellis diagram """
    cell = np.array([[0] * 4 for i in range(len(input_arr) + 1)])
    cell[0][0] = 0
    b = len(cell)
    for i in range(len(cell)):
        for j in range(len(cell[i])):
            if j == 0 and i != 0:
                cell[i][j] = max(mann_whitney(input_arr[i - 1], trellis[0][0]) + cell[i - 1][0],
                                 mann_whitney(input_arr[i - 1], trellis[0][1]) + cell[i - 1][2])
            elif j == 1 and i != 0:
                cell[i][j] = max(mann_whitney(input_arr[i - 1], trellis[1][0]) + cell[i - 1][0],
                                 mann_whitney(input_arr[i - 1], trellis[1][1]) + + cell[i - 1][2])
            elif j == 2 and i > 1:
                cell[i][j] = max(mann_whitney(input_arr[i - 1], trellis[2][0]) + cell[i - 1][1],
                                 mann_whitney(input_arr[i - 1], trellis[2][1]) + + cell[i - 1][3])
            elif j == 3 and i > 1:
                cell[i][j] = max(mann_whitney(input_arr[i - 1], trellis[3][0]) + cell[i - 1][1],
                                 mann_whitney(input_arr[i - 1], trellis[3][1]) + + cell[i - 1][3])
    return cell


def st(input_str):
    """This method creates an input signal for channel"""
    input_arr = np.array(list(input_str), dtype=int)
    output_arr = np.zeros(len(input_str)*4)
    for i in range(len(input_arr)):
        output_arr[i*4 + input_arr[i]] = 1
    return output_arr


def rt(input_arr):
    """This method creates an output signal for channel"""
    output_arr = np.zeros(8)
    for i in range(len(input_arr)):
        r_com1 = np.random.normal(0, 1) + np.random.normal(0, 1)*1j
        r_com2 = np.random.normal(0, 1) + np.random.normal(0, 1)*1j
        r_poisson = np.random.poisson(0.1)
        r = input_arr[i]*r_com1 + (r_poisson*(10**0.5) + 0.1**0.5)*r_com2
        output_arr[i] = abs(r)
    return output_arr


def channel(input_arr):
    """This method imitate channel"""
    input_str = ''.join(list(map(str, map(chr, np.packbits(input_arr)))))
    input_arr = np.array(list(input_str.split(" ")))
    output_arr = np.array([np.zeros(8)]*len(input_arr))
    for i in range(len(input_arr)):
        a = st(input_arr[i])
        b = rt(a)
        output_arr[i] = b
    return output_arr


def mann_whitney(input_arr, input_str):
    """Realization of finding Mann-Whitney's criteria"""
    rank_arr = np.argsort(np.argsort(input_arr))
    if input_str == "11":
        crit = rank_arr[1] + rank_arr[5]
    elif input_str == "00":
        crit = rank_arr[0] + rank_arr[4]
    elif input_str == "10":
        crit = rank_arr[1] + rank_arr[4]
    elif input_str == "01":
        crit = rank_arr[0] + rank_arr[5]
    return crit


def decoder():
    """ Basic method which decode convolutional code using Viterbi algorithm """
    input_arr = channel(coder(np.unpackbits(np.uint8(list(b'11111')))))
    trellis = np.array([["00", "11"], ["11", "00"], ["10", "01"], ["01", "10"]])
    way = np.array([0 for i in range(len(input_arr) + 1)])
    cell = get_cell(input_arr, trellis)
    for i in range(len(cell)):
        way[i] = get_min_index(cell[i])
    output_str = ""
    for i in range(len(way)):
        if i != 0:
            if way[i] == 0 or way[i] == 2:
                output_str = output_str + "0"
            if way[i] == 1 or way[i] == 3:
                output_str = output_str + "1"
    #output_arr = np.unpackbits(np.uint8(list(output_str)))
    return output_str


#print(coder(np.unpackbits(np.uint8(list(b'11111')))))
print(decoder())
'''print(np.unpackbits(np.uint8(list(b'hello'))))
print(np.packbits(np.unpackbits(np.uint8(list(b'hello')))))
print(np.argsort([1, 0, 1])) 
print(channel(coder(np.unpackbits(np.uint8(list(b'11111'))))))
print(np.argsort([1.56, 0.54, 1.01, 0.22, 0.72, 0.48, 0.81, 2.35]))
print(np.argsort([3, 5, 1, 4, 6, 2, 0, 7]))'''

