import numpy
import galois
import itertools


def DrawPoints(arr):
    b_res = [1] * len(arr)  # take arr
    a2 = galois.GF2(arr)  # take arr
    b2 = galois.GF2(b_res)
    solutions = []

    for numbers in itertools.product([0, 1], repeat=len(b_res)):
        tmp = galois.GF2(numbers)
        tmp2 = a2 @ tmp
        if tmp2.all() == b2.all():
            solutions.append(list(numbers))  # solution found there
    return solutions


def process(d: dict):
    n = len(d.keys())
    arr = []
    arr_index = 0
    for point in d.keys():
        arr.append([0] * n)
        arr[arr_index][point.index] = 1
        for i in range(len(d[point])):
            arr[arr_index][d[point][i].index] = 1
        arr_index += 1
    return DrawPoints(arr)
