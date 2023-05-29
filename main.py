import numpy as np
import matplotlib.pyplot as plt

# Параметры симуляции.
u = 1.0   # Скорость переноса.
mu = 0.1  # Коэффициент диффузии.
tau = 0.01  # Коэффициент сглаживания.
f = 0.01  # Внешний источник или сила.

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

# Вычисляем температурный и солевой члены роста планктонных популяций.
def compute_growth_terms(T, C, m):
    temperature_term = -alpha * m * ((T - Topt) / Topt) ** 2
    salinity_term = -beta * m * ((C - Copt) / Copt) ** 2
    return temperature_term, salinity_term

# Шаги по времени.
for n in range(nt - 2):  # Уменьшаем диапазон на 1, чтобы избежать выхода за границы массива.
    for i in range(1, nx - 1):
        # Расчет членов уравнения.
        advection_term = u * (S[n, i + 1] - S[n, i - 1]) / (2 * dx)
        diffusion_term = mu * (S[n, i + 1] - 2 * S[n, i] + S[n, i - 1]) / dx ** 2
        temperature_term, salinity_term = compute_growth_terms(T, C, 1)
        growth_term = np.exp(temperature_term) * np.exp(salinity_term) * S[n, i]
        regularizer_term = tau / dt ** 2 + u / dx + mu / dx ** 2

        # Обновление S[n + 1, i] с учетом всех членов.
        S[n + 1, i] = (S[n, i] + dt * (advection_term - diffusion_term + growth_term)) / (1 + dt * regularizer_term)

# График решения.
plt.figure(figsize=(10, 6))
plt.imshow(S, aspect='auto', cmap='hot', origin='lower')
plt.colorbar(label='Концентрация')
plt.xlabel('X')
plt.ylabel('Время')
plt.title('Пространственно-временная эволюция концентрации')
plt.show()
