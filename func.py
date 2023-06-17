import numpy as np
import matplotlib.pyplot as plt

# # Параметры симуляции.
# u = 1.0   # Скорость переноса.
# mu = 0.01  # Коэффициент диффузии.
# tau = 0.01  # Коэффициент сглаживания.
# f = 0.01  # Внешний источник или сила.

# Параметры, связанные с планктоном.
alpha = 0.5  # Параметр влияния температуры.
beta = 0.5   # Параметр влияния солености.
Topt = 25.0  # Оптимальная температура.
Copt = 30.0  # Оптимальная соленость.

# Текущие условия.
T = 20.0  # Текущая температура.
C = 20.0  # Текущая соленость.

# Параметры сетки.
nx = 100  # Количество точек сетки по оси x.
nt = 100  # Количество временных шагов.
dx = 1.0  # Шаг сетки по x.
dt = 0.01  # Размер временного шага.

# Инициализируем массив для хранения концентрации S.
S = np.zeros((nt, nx))

# Устанавливаем начальное условие.
S[0, :] = np.sin(2 * np.pi * np.arange(nx) / nx)
S[1, :] = np.sin(2 * np.pi * np.arange(nx) / nx) # добавляем начальное условие для S[1, :]

# Вычисляем температурный и солевой члены роста планктонных популяций. С УЧЕТОМ СМЕРТНОСТИ СРАЗУ
def compute_growth_terms(T, C, m, mortality_rate):
    temperature_term = -alpha * m * ((T - Topt) / Topt) ** 2
    salinity_term = -beta * m * ((C - Copt) / Copt) ** 2
    return temperature_term - mortality_rate, salinity_term - mortality_rate

# Решение уравнения с регуляризатором
def compute_next_step_reg(S, n, i, T, C, m, u = 1.0 , mu = 0.01, tau = 0.01, f = 0.01, mortality_rate = 0.1):
    advection_term = u * (S[n, i + 1] - S[n, i]) / (2 * dx)
    diffusion_term = mu * (S[n, i + 1] - 2 * S[n, i] + S[n, i - 1]) / dx ** 2
    temperature_term, salinity_term = compute_growth_terms(T, C, m, mortality_rate)
    growth_term = np.exp(temperature_term) * np.exp(salinity_term) * S[n, i]
    regularizer_term = (S[n, i] - S[n-1, i]) / dt + tau * (S[n, i] - 2 * S[n-1, i] + S[n-2, i]) / dt ** 2

    # Обновление S[n + 1, i] с учетом всех членов.
    S[n + 1, i] = (S[n, i] + dt * (advection_term - diffusion_term + growth_term + regularizer_term)) / (1 + dt)

# Решение уравнения с регуляризатором
def solve_eq_with_reg(S, T, C, u = 1.0, mu = 0.01, tau = 0.01, f = 0.01, mortality_rate = 0.1):
    for n in range(2, nt - 1):
        for i in range(1, nx - 1):
            compute_next_step_reg(S, n, i, T, C, 1, u = u , mu = mu, tau = tau, f = f, mortality_rate = mortality_rate)


# Решение уравнения без регуляризатора
def compute_next_step_no_reg(S, n, i, T, C, m, u = 1.0 , mu = 0.01, tau = 0.01, f = 0.01, mortality_rate = 0.1):
    advection_term = u * (S[n, i + 1] - S[n, i]) / (2 * dx)
    diffusion_term = mu * (S[n, i + 1] - 2 * S[n, i] + S[n, i - 1]) / dx ** 2
    temperature_term, salinity_term = compute_growth_terms(T, C, m, mortality_rate = mortality_rate)
    growth_term = np.exp(temperature_term) * np.exp(salinity_term) * S[n, i]

    # Обновление S[n + 1, i] с учетом всех членов.
    S[n + 1, i] = (S[n, i] + dt * (advection_term - diffusion_term + growth_term)) / (1 + dt)

# Решение уравнения без регуляризатора
def solve_eq_without_reg(S, T, C, u = 1.0 , mu = 0.01, tau = 0.01, f = 0.01, mortality_rate = 0.1):
    for n in range(nt - 2):
        for i in range(1, nx - 1):
            compute_next_step_no_reg(S, n, i, T, C, 1, u = u , mu = mu, tau = tau, f = f, mortality_rate = mortality_rate)

# Решение уравнения с регуляризатором без учета солености и температуры
def compute_next_step_reg_without_temp_and_sal(S, n, i, u = 1.0 , mu = 0.01, tau = 0.01, f = 0.01, mortality_rate = 0.1):
    advection_term = u * (S[n, i + 1] - S[n, i]) / (2 * dx)
    diffusion_term = mu * (S[n, i + 1] - 2 * S[n, i] + S[n, i - 1]) / dx ** 2
    regularizer_term = tau * (S[n, i] - 2 * S[n-1, i] + S[n-2, i]) / dt ** 2

    # Обновление S[n + 1, i] с учетом всех членов.
    S[n + 1, i] = (S[n, i] + dt * (advection_term - diffusion_term - mortality_rate + regularizer_term)) / (1 + dt)

def solve_eq_with_reg_without_temp_and_sal(S, u = 1.0 , mu = 0.01, tau = 0.01, f = 0.01, mortality_rate = 0.1):
    for n in range(2, nt - 1):
        for i in range(1, nx - 1):
            compute_next_step_reg_without_temp_and_sal(S, n, i, u = u , mu = mu, tau = tau, f = f, mortality_rate = mortality_rate)

# Решение уравнения без регуляризатора без учета солености и температуры
def compute_next_step_no_reg_without_temp_and_sal(S, n, i, u = 1.0 , mu = 0.01, tau = 0.01, f = 0.01, mortality_rate = 0.1):
    advection_term = u * (S[n, i + 1] - S[n, i]) / (2 * dx)
    diffusion_term = mu * (S[n, i + 1] - 2 * S[n, i] + S[n, i - 1]) / dx ** 2

    # Обновление S[n + 1, i] с учетом всех членов.
    S[n + 1, i] = (S[n, i] + dt * (advection_term - diffusion_term - mortality_rate)) / (1 + dt)

def solve_eq_without_reg_without_temp_and_sal(S, n, i,u = 1.0 , mu = 0.01, tau = 0.01, f = 0.01, mortality_rate = 0.1):
    for n in range(nt - 2):
        for i in range(1, nx - 1):
            compute_next_step_no_reg_without_temp_and_sal(S, n, i, u = u , mu = mu, tau = tau, f = f, mortality_rate = mortality_rate)