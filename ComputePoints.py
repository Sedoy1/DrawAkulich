import galois
import itertools
import random
from Top import *


def create_matrix(N, K):
    matrix = []
    for i in range(N):
        matrix.append([0] * N)
    edges = 0

    for i in range(N):
        for j in range(N):
            if i < j and edges <= K * N:
                matrix[i][j] = random.randint(0, 1)
                edges += matrix[i][j]
            elif i > j:
                matrix[i][j] = matrix[j][i]
            elif i == j:
                matrix[i][j] = 1
    return matrix


def generate_random_graph() -> dict:
    N = random.randint(4, 7)
    K = random.randint(1, 2)

    if N < 200 and K * N < N * (N - 1) / 2:
        matrix = create_matrix(N, K)


    elif int(1.2 * N) < 200 and 0.8 * K * N < N * (N - 1) / 2:
        N = int(1.2 * N)
        K = int(0.8 * K)
        matrix = create_matrix(N, K)

    else:
        matrix = []
        for i in range(N):
            matrix.append([])
            for j in range(N):
                if i == j:
                    matrix[i].append(1)
                else:
                    matrix[i].append(0)

    pos = [[random.randint(100, 1200), random.randint(100, 790)] for _ in range(N)]

    G = dict()
    tops = list()
    for i in range(N):
        top = Top(i, pos[i][0], pos[i][1])
        tops.append(top)

    for i in range(N):
        G[tops[i]] = []
        for j in range(N):
            if matrix[i][j] and i != j:
                G[tops[i]].append(tops[j])
    return G, solve(matrix)


def solve(arr):
    b_res = [1] * len(arr)  # take arr
    a2 = galois.GF2(arr)  # take arr
    b2 = galois.GF2(b_res)
    solutions = []
    for numbers in itertools.product([0, 1], repeat=len(b_res)):
        tmp = galois.GF2(numbers)
        tmp2 = a2 @ tmp
        if tmp2.all() == b2.all():
            solutions.append(list(numbers))

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
    return solve(arr)
