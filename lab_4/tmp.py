def TridiagonalSolve(Mat, F):
    n = len(Mat)
    
    if any(len(row) != n for row in Mat):
        raise ValueError("Матрица должна быть квадратной")
    if len(F) != n:
        raise ValueError("Длина вектора F должна совпадать с размером матрицы")

    A = [0] * n
    B = [0] * n
    C = [0] * n
    
    for i in range(n):
        A[i] = Mat[i][i - 1] if i - 1 >= 0 else 0
        B[i] = Mat[i][i]
        C[i] = Mat[i][i + 1] if i + 1 < n else 0
    
    eps = [0] * (n - 1)
    eta = [0] * (n - 1)
    x = [0] * n
    
    eps[0] = -C[0] / B[0]
    eta[0] = F[0] / B[0]


    for i in range(1, n - 1):
        denominator = B[i] - A[i] * eps[i - 1]
        eps[i] = C[i] / denominator
        eta[i] = (F[i] + A[i] * eta[i - 1]) / denominator
                
    x[-1] = (F[-1] - A[-1] * eta[-1]) / (A[-1] * eps[-1] + B[-1])
    for i in range(n - 2, -1, -1):
        x[i] = eta[i] + eps[i] * x[i + 1]
    
    return x