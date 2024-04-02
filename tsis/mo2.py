from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
# Параметры модели
lambda_val = 0.5
mu_val = 1
T = 10

# Уравнение для W(n)
def dW_dt(W, t):
    n = len(W)
    dW = [0]*n
    for i in range(1, n-1):
        dW[i] = lambda_val*(i-1)*(W[i-1]+1/mu_val) - lambda_val*W[i] - mu_val*W[i] + mu_val*W[i+1]
    dW[0] = lambda_val*(W[0]+1/mu_val) - lambda_val*W[0] - mu_val*W[0] + mu_val*W[1]
    dW[n-1] = lambda_val*(n-2)*(W[n-2]+1/mu_val) - lambda_val*W[n-1] - mu_val*W[n-1]
    return dW

# Уравнение для Q(n)
def dQ_dt(Q, t):
    n = len(Q)
    W = odeint(dW_dt, [0]*n, t)[:, -1]
    dQ = [0]*n
    for i in range(1, n-1):
        dQ[i] = lambda_val*(i-1)*(Q[i-1]+(W[i-1]>T)) - lambda_val*Q[i] - mu_val*Q[i] + mu_val*Q[i+1]
    dQ[0] = lambda_val*(Q[0]+(W[0]>T)) - lambda_val*Q[0] - mu_val*Q[0] + mu_val*Q[1]
    dQ[n-1] = lambda_val*(n-2)*(Q[n-2]+(W[n-2]>T)) - lambda_val*Q[n-1] - mu_val*Q[n-1]
    return dQ

# Начальные условия
n = 5
W0 = [0]*n
Q0 = [0]*n
t = np.linspace(0, 10, 101)

# Решение уравнений
W = odeint(dW_dt, W0, t)
Q = odeint(dQ_dt, Q0, t)

# Визуализация результатов
plt.plot(t, W[:, 2], label='W(2)')
plt.plot(t, Q[:, 2], label='Q(2)')
plt.legend()
plt.show()