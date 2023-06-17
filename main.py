from func import *
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Создаем основное окно.
root = tk.Tk()

# Создаем фигуру для графика.
fig = Figure(figsize=(5,4), dpi=500)

# Функция для обновления графика.
def update_plot(*args):
    global S
    # Получаем параметры из полей ввода.
    u = float(u_slider.get())
    mu = float(mu_slider.get())
    tau = float(tau_slider.get())
    f = float(f_slider.get())
    T = float(T_slider.get())
    C = float(C_slider.get())
    mortality_rate = float(mortality_slider.get())
    solver = solver_var.get()

    # Обнуляем массив S.
    S.fill(0.0)
    # Устанавливаем начальное условие.
    S[0, :] = np.sin(2 * np.pi * np.arange(nx) / nx)

    # Выбираем решение уравнения в соответствии с выбором пользователя.
    if solver == 'With Reg':
        solve_eq_with_reg(S, T, C, u, mu, tau,f,mortality_rate = mortality_rate)
    elif solver == 'Without Reg':
        solve_eq_without_reg(S, T, C, u, mu, tau,f)
    elif solver == 'With Reg no temp and sal':
        solve_eq_with_reg_without_temp_and_sal(S, u, mu, tau,f)
    elif solver == 'Without Reg no temp and sal':
        solve_eq_without_reg_without_temp_and_sal(S, T, C, u, mu, tau,f)

    # Очищаем и рисуем новый график
    fig.clear()
    ax = fig.add_subplot(111)
    ax.imshow(S, aspect='auto', cmap='hot', origin='lower', vmin=0)
    ax.set_xlabel('X')
    ax.set_ylabel('Время')
    cbar = plt.colorbar(ax.imshow(S, aspect='auto', cmap='hot', origin='lower',vmin=0))
    cbar.set_label('Концентрация')
    canvas.draw_idle()

# Создаем слайдеры для параметров.
u_label = tk.Label(root, text='Скорость переноса:')
u_label.pack()
u_slider = tk.Scale(root, from_=0.01, to=10, resolution=0.01, orient=tk.HORIZONTAL, command=update_plot)
u_slider.set(1.0)
u_slider.pack()

mu_label = tk.Label(root, text='Коэффициент диффузии:')
mu_label.pack()
mu_slider = tk.Scale(root, from_=0.01, to=1, resolution=0.01, orient=tk.HORIZONTAL, command=update_plot)
mu_slider.set(0.1)
mu_slider.pack()

tau_label = tk.Label(root, text='Коэффициент сглаживания:')
tau_label.pack()
tau_slider = tk.Scale(root, from_=0.01, to=1, resolution=0.001, orient=tk.HORIZONTAL, command=update_plot)
tau_slider.set(0.01)
tau_slider.pack()

f_label = tk.Label(root, text='Внешний источник или сила:')
f_label.pack()
f_slider = tk.Scale(root, from_=0.01, to=1, resolution=0.001, orient=tk.HORIZONTAL, command=update_plot)
f_slider.set(0.01)
f_slider.pack()

T_label = tk.Label(root, text='Температура, %')
T_label.pack()
T_slider = tk.Scale(root, from_=0, to=100, resolution=1, orient=tk.HORIZONTAL, command=update_plot)
T_slider.set(20.0)
T_slider.pack()

C_label = tk.Label(root, text='Соленость, %')
C_label.pack()
C_slider = tk.Scale(root, from_=0, to=100, resolution=1, orient=tk.HORIZONTAL, command=update_plot)
C_slider.set(20.0)
C_slider.pack()

mortality_label = tk.Label(root, text='Смертность:')
mortality_label.pack()
mortality_slider = tk.Scale(root, from_=0.01, to=1, resolution=0.01, orient=tk.HORIZONTAL, command=update_plot)
mortality_slider.set(1.0)
mortality_slider.pack()

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
canvas.get_tk_widget().configure(width=700, height=500)

# Запускаем основной цикл.
root.mainloop()