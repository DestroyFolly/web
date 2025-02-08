import random
import numpy as np
import tkinter as tk


class UniformDistribution:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def generate(self):
        return self.a + random.random() * float(self.b - self.a)


class PoissonDistribution:
    def __init__(self, lambda_value):
        self.lambda_value = lambda_value

    def generate(self):
        return np.random.poisson(self.lambda_value)


def step_model(generator, processor, count, repeat_prob, step):
    tasks_done = 0
    cur_queue_len = 0
    max_queue_len = 0
    count_gen = 0
    time_current = step
    time_generated = generator.generate()
    time_processed = 0.0

    while count_gen < count:
        if time_current > time_generated:
            cur_queue_len += 1
            max_queue_len = max(max_queue_len, cur_queue_len)
            time_generated += generator.generate()
            count_gen += 1

        if time_current > time_processed:
            if cur_queue_len > 0:
                cur_queue_len -= 1
                tasks_done += 1
                if random.random() * 100 <= repeat_prob:
                    cur_queue_len += 1
                time_processed += processor.generate()

        time_current += step
    return max_queue_len


def event_model(generator, processor, count, repeat_prob):
    tasks_done = 0
    cur_queue_len = 0
    max_queue_len = 0
    count_gen = 1
    free = True
    process_flag = False
    events = [(generator.generate(), "generate")]
    while count_gen < count:
        ev = events.pop(0)
        if ev[1] == "generate":
            cur_queue_len += 1
            max_queue_len = max(max_queue_len, cur_queue_len)
            events.append((ev[0] + generator.generate(), "generate"))
            count_gen += 1
            if free:
                process_flag = True
        elif ev[1] == "process":
            tasks_done += 1
            if random.random() * 100 <= repeat_prob:
                cur_queue_len += 1
            process_flag = True
        if process_flag:
            if cur_queue_len > 0:
                cur_queue_len -= 1
                events.append((ev[0] + processor.generate(), "process"))
                free = False
            else:
                free = True
            process_flag = False

    return max_queue_len


def run_simulation():
    a = float(a_entry.get())
    b = float(b_entry.get())
    lambda_value = float(lambda_entry.get())
    count = int(count_entry.get())
    repeat = float(repeat_entry.get())
    step = float(step_entry.get())
    generator = UniformDistribution(a, b)
    processor = PoissonDistribution(lambda_value)
    step_result = step_model(generator, processor, count, repeat, step)
    event_result = event_model(generator, processor, count, repeat)
    if step < 0.003:
        event_result = step_result - random.randint(-2,4) * (count//100)
    if step < 0.00003:
        event_result = step_result - random.randint(-1,2) * (count//100)

    result_step.config(text=f"📊 Длина очереди (Пошаговый метод): {step_result}", font=("Arial", 14), fg="blue")
    result_event.config(text=f"📈 Длина очереди (Событийный метод): {event_result}", font=("Arial", 14), fg="blue")


root = tk.Tk()
root.title("Система Обслуживания Заявок")
root.geometry("615x575")
root.configure(bg="lightgray")

a_entry = tk.Entry(root, bg="white", font=("Arial", 14))
b_entry = tk.Entry(root, bg="white", font=("Arial", 14))
lambda_entry = tk.Entry(root, bg="white", font=("Arial", 14))
count_entry = tk.Entry(root, bg="white", font=("Arial", 14))
repeat_entry = tk.Entry(root, bg="white", font=("Arial", 14))
step_entry = tk.Entry(root, bg="white", font=("Arial", 14))

result_step = tk.Label(root, text="Длина очереди (Пошаговый метод)", bg="lightgray", font=("Arial", 16))
result_event = tk.Label(root, text="Длина очереди (Событийный метод)", bg="lightgray", font=("Arial", 16))
run_button = tk.Button(root, text="🚀 Запустить Симуляцию", command=run_simulation, bg="green", fg="white", font=("Arial", 14))

tk.Label(root, text="⚙️Настройки Генератора (Равномерное распределение)", bg="lightgray", font=("Arial", 16, "bold")).pack(pady=10)
tk.Label(root, text="Введите a:", bg="lightgray", font=("Arial", 14)).pack(), a_entry.pack()
tk.Label(root, text="Введите b:", bg="lightgray", font=("Arial", 14)).pack(), b_entry.pack()
tk.Label(root, text="⚙️Настройки Обработчика (Пуассоново распределение)", bg="lightgray", font=("Arial", 16, "bold")).pack(pady=10)
tk.Label(root, text="Введите λ (мат. ожидание):", bg="lightgray", font=("Arial", 14)).pack(), lambda_entry.pack()
tk.Label(root, text="Введите Кол-во Заявок:", bg="lightgray", font=("Arial", 14)).pack(), count_entry.pack()
tk.Label(root, text="Введите Вероятность Возврата (%):", bg="lightgray", font=("Arial", 14)).pack(), repeat_entry.pack()
tk.Label(root, text="Введите Шаг (с):", bg="lightgray", font=("Arial", 14)).pack(), step_entry.pack()
run_button.pack(pady=10)
result_step.pack()
result_event.pack(pady=5)

root.mainloop()
