import math


def get_min_num(a, b):
    if a >= b:
        return b
    if a < b:
        return a


def get_min_index(cell):
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
    distance = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            distance += 1
    return distance


def get_cell(input_list, trellis):
    cell = [[math.inf] * 4 for i in range(len(input_list) + 1)]
    cell[0][0] = 0
    for i in range(len(cell)):
        for j in range(4):
            if j == 0 and i != 0:
                cell[i][j] = get_min_num(hamming_distance(input_list[i - 1], trellis[0][0]) + cell[i - 1][0],
                                         hamming_distance(input_list[i - 1], trellis[0][1]) + cell[i - 1][2])
            elif j == 1 and i != 0:
                cell[i][j] = get_min_num(hamming_distance(input_list[i - 1], trellis[1][0]) + cell[i - 1][0],
                                         hamming_distance(input_list[i - 1], trellis[1][1]) + + cell[i - 1][2])
            elif j == 2 and i > 1:
                cell[i][j] = get_min_num(hamming_distance(input_list[i - 1], trellis[2][0]) + cell[i - 1][1],
                                         hamming_distance(input_list[i - 1], trellis[2][1]) + + cell[i - 1][3])
            elif j == 3 and i > 1:
                cell[i][j] = get_min_num(hamming_distance(input_list[i - 1], trellis[3][0]) + cell[i - 1][1],
                                         hamming_distance(input_list[i - 1], trellis[3][1]) + + cell[i - 1][3])
    return cell


def decoder(input_str):
    input_list = input_str.split(" ")
    trellis = [["00", "11"], ["11", "00"], ["01", "10"], ["10", "01"]]
    way = [0 for i in range(len(input_list) + 1)]
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
    return output_str


print(decoder("11 10 01 11 01"))
