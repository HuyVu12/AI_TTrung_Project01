import numpy as np

def calc_model(x, y):
    row, col = len(x[0]) + 1, len(x[0]) + 1
    nums = len(x)
    M = []
    for i in range(row):
        M.append([])
        for j in range(col):
            M[i].append(0)

    for i in range(row):
        for j in range(col):
            for k in range(nums):
                ti = 1
                tj = 1
                if i != row - 1: ti = x[k][i]
                if j != col - 1: tj = x[k][j]
                M[i][j] += ti * tj
    
    Y = []
    for i in range(row):
        Y.append(0)
    for k in range(nums):
        for i in range(row):
            ti = 1
            if i != row - 1: ti = x[k][i]
            Y[i] += ti * y[k]
    A = np.linalg.solve(M, Y)
    print(f'''Model: parameters {A}''')
    return A
def predict_model(model, *args):
    if len(model) != len(args)+1:
        print(f'Your model need {len(model)-1} parameters but get {len(args)}!')
        return 0
    id = 0
    p = 0
    for x in args:
        p += model[id] * x
        id += 1
    p += model[-1]
    return p