import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator

with open(sys.argv[1]) as in_file:
    file = in_file.readlines()

useCPU = []  # Утилизация ЦПУ
runqSz = []  # Очередь
timer = []  # Время

flagRunq = False

for line in file:
    str1 = line.split()
    if "all" in str1 and 'Average:' not in str1 and len(str1) == 11:
        timer.append(str(str1[0][:-3]))
        useCPU.append(100 - float(str1[10]))

    if flagRunq is True and 'Average:' not in str1:  # Обрабатываю данные колонки с очередью
        if line == '\n':
            flagRunq = False
        else:
            runqSz.append(int(str1[1]))
    if "runq-sz" in line:  # Нашел строку с очередью
        flagRunq = True

plt.style.use('seaborn')  # Стиль
figure = plt.figure(num='Утилизация CPU', figsize=(12, 8))
ax1 = figure.add_subplot(1, 1, 1)
ax1.plot(timer, useCPU)  # принимает массив таймер на ось Х, принимает массив useCPU на ось У
ax1.set_ylim([0, max(useCPU) + int(max(useCPU) * 0.2)])
ax1.set_xlim([0, max(timer)])
ax1.set_ylabel('Утилизация CPU, %', )
ax1.set_xlabel('Вермя проведения теста ч:мм', loc='right')
plt.xticks(rotation=45)

# Дополнительная ось у
ax2 = ax1.twinx()
ax2.plot(timer, runqSz, color='g')
ax2.set_ylim([0, max(runqSz)])
ax2.set_yticks([i for i in range(0, max(runqSz) + 2)])
ax2.set_ylabel('Длина очереди, шт.')

ax2.xaxis.set_major_locator(LinearLocator(20))  # Кол-во меток на оси х

# Легенда
data = {'Утилизация CPU': useCPU,
        'Длина очереди': runqSz}
df = pd.DataFrame(data)
plt.plot(timer, df)
plt.legend(data, bbox_to_anchor=(0.6, -0.08), ncol=2)

plt.title(r'Утилизация CPU', fontsize=16, y=1.08)  # доббавляем заголовок к графику "График функции y=x^2
plt.show()
