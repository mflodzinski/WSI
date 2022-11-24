import numpy as np

def fillOddOrder(magicSquare, n):
    i = 0
    j = n//2
    num = 1
    while num <= n*n:
        if i < 0 and j >= n: 
            i += 2
            j -= 1 
        if j >= n: 
            j = 0 
        if i < 0: 
            i = n - 1
        if magicSquare[i][j] != 0:
            i += 2 
            j -= 1 
            continue 
        else:
            magicSquare[i][j] = num
            num += 1
        i -= 1 
        j += 1
        
def fillDoublyEvenOrder(magicSquare, n):
    for i in range(n):
        for j in range(n):
            magicSquare[i][j] = (n*i) + j + 1
    for i in range(n//4):
        for j in range(n//4):
            magicSquare[i][j] = (n*n + 1) - magicSquare[i][j] 
    for i in range(n//4):
        for j in range(3*(n//4), n):
            magicSquare[i][j] = (n*n + 1) - magicSquare[i][j] 
    for i in range(3*(n//4), n):
        for j in range(n//4):
            magicSquare[i][j] = (n*n+1) - magicSquare[i][j] 
    for i in range(3*(n//4), n):
        for j in range(3*(n//4), n):
            magicSquare[i][j] = (n*n + 1) - magicSquare[i][j] 
    for i in range(n//4, 3*(n//4)):
        for j in range(n//4, 3*(n//4)):
            magicSquare[i][j] = (n*n + 1) - magicSquare[i][j] 
            
def fillSinglyEvenOrder(magicSquare, n):
    fillQuarterOfSinglyEvenOrder(magicSquare, 0, n/2, 0, n/2, 1, (n/2)*(n/2))
    fillQuarterOfSinglyEvenOrder(magicSquare, n/2, n, n/2, n, (n/2)*(n/2) + 1, n*n/2)
    fillQuarterOfSinglyEvenOrder(magicSquare, 0, n/2, n/2, n, n*n/2 + 1, 3*(n/2)*(n/2))
    fillQuarterOfSinglyEvenOrder(magicSquare, n/2, n, 0, n/2, 3*(n/2)*(n/2) + 1, n*n)

    shiftCol = int((n/2 - 1)/2)
    for i in range(n//2):
        for j in range(shiftCol):
            if i == n//4:
                exchangeCell(i, j + shiftCol, magicSquare)
            else: 
                exchangeCell(i, j, magicSquare)
    for i in range(n//2):
        for j in range(n - 1, n - shiftCol, -1):
            exchangeCell(i, j, magicSquare)

def fillQuarterOfSinglyEvenOrder(magicSquare, firstRow, lastRow, firstCol, lastCol, num, lastNum):
    i = firstRow 
    j = (lastCol + firstCol)//2

    while num <= lastNum: 
        if i < firstRow and j >= lastCol: 
            i += 2 
            j -= 1
        if j >= lastCol: 
            j = firstCol 
        if i < firstRow: 
            i = lastRow - 1 
        i = int(i)
        j = int(j)
        if magicSquare[i][j] != 0: 
            i += 2 
            j -= 1 
            continue 
        else:
            magicSquare[i][j] = int(num)
            num += 1
        i -= 1 
        j += 1 

def exchangeCell(i, j, matrix):
    r = len(matrix)//2 + i
    matrix[i][j], matrix[r][j] = matrix[r][j], matrix[i][j]

def fillMatrix(n):
    # Edge cases:
    if n == 1: 
        return [[1]]
    if n == 2: 
        return None

    magicSquare = [[0 for i in range(n)] for i in range(n)]
    # Fill the magicSquare depends on its type:
    # Odd order:
    if n % 2 == 1:
        fillOddOrder(magicSquare, n)
    # Singly-even order:
    elif n % 4 == 2:
        fillSinglyEvenOrder(magicSquare, n)
    # Doubly-even order:
    else:
        fillDoublyEvenOrder(magicSquare, n)
    
    return magicSquare

def heurestic_matrix(n):
    matrix = np.full((n, n), 2)
    np.fill_diagonal(matrix, 3)
    np.fill_diagonal(np.fliplr(matrix), 3)
    if (n%2 == 1):
        center = n//2
        matrix[center][center] = 4
    return matrix.tolist()