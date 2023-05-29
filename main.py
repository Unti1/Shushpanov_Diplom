from func import *
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Создаем основное окно.
root = tk.Tk()

# Создаем фигуру для графика.
fig = Figure(figsize=(5, 4), dpi=100)

# Функция для обновления графика.
def update_plot():
    global S
    # Получаем параметры из полей ввода.
    u = float(u_entry.get())
    mu = float(mu_entry.get())
    tau = float(tau_entry.get())
    f = float(f_entry.get())
    T = float(T_entry.get())
    C = float(C_entry.get())
    solver = solver_var.get()

    # Обнуляем массив S.
    S.fill(0.0)
    # Устанавливаем начальное условие.
    S[0, :] = np.sin(2 * np.pi * np.arange(nx) / nx)

    # Выбираем решение уравнения в соответствии с выбором пользователя.
    if solver == 'With Reg':
        solve_eq_with_reg(S, T, C, u, mu, tau,f)
    elif solver == 'Without Reg':
        solve_eq_without_reg(S, T, C, u, mu, tau,f)
    elif solver == 'With Reg no temp and sal':
        solve_eq_with_reg_without_temp_and_sal(S, u, mu, tau,f)
    elif solver == 'Without Reg no temp and sal':
        solve_eq_without_reg_without_temp_and_sal(S, T, C, u, mu, tau,f)

    # Очищаем график.
    fig.clear()
    a = fig.add_subplot(111)
    # Рисуем новый график.
    a.imshow(S, aspect='auto', cmap='hot', origin='lower')

    # Обновляем канвас.
    canvas.draw()

# Создаем поля ввода для параметров.
u_label = tk.Label(root, text='Скорость переноса:')
u_label.pack()
u_entry = tk.Entry(root)
u_entry.pack()
u_entry.insert(0, '1.0')

mu_label = tk.Label(root, text='Коэффициент диффузии:')
mu_label.pack()
mu_entry = tk.Entry(root)
mu_entry.pack()
mu_entry.insert(0, '0.1')

tau_label = tk.Label(root, text='Коэффициент сглаживания:')
tau_label.pack()
tau_entry = tk.Entry(root)
tau_entry.pack()
tau_entry.insert(0, '0.01')

f_label = tk.Label(root, text='Внешний источник или сила:')
f_label.pack()
f_entry = tk.Entry(root)
f_entry.pack()
f_entry.insert(0, '0.01')

T_label = tk.Label(root, text='Температура, %')
T_label.pack()
T_entry = tk.Entry(root)
T_entry.pack()
T_entry.insert(0, '20.0')

C_label = tk.Label(root, text='Соленость, %')
C_label.pack()
C_entry = tk.Entry(root)
C_entry.pack()
C_entry.insert(0, '20.0')

# Создаем радиокнопки для выбора решения.
solver_var = tk.StringVar(value='С регуляризацией')
with_reg_rb = tk.Radiobutton(root, text='С регуляризацией', variable=solver_var, value='With Reg')
with_reg_rb.pack()
without_reg_rb = tk.Radiobutton(root, text='Без регуляризацией', variable=solver_var, value='Without Reg')
without_reg_rb.pack()
with_reg_no_temp_and_sal_rb = tk.Radiobutton(root, text='С регуляризацией, без солей и температуры', variable=solver_var, value='With Reg no temp and sal')
with_reg_no_temp_and_sal_rb.pack()
without_reg_no_temp_and_sal_rb = tk.Radiobutton(root, text='Без регуляризацией, без солей и температуры', variable=solver_var, value='Without Reg no temp and sal')
without_reg_no_temp_and_sal_rb.pack()

# Создаем кнопку для обновления графика.
update_button = tk.Button(root, text='Обновить график', command=update_plot)
update_button.pack()

# Создаем канвас для отображения графика.
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# Запускаем основной цикл.
root.mainloop()