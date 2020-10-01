import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
def potential(r):
    eps = 0.0104 # [eV]
    sigma = 3.4  # [A]
    u = 4 * eps * ((sigma/r)**12 - (sigma/r)**6)
    return u

with open('LD_data.txt', 'w') as f:
    f.close()

r = 3.3
radius = list()
u = list()
with open('LD_data.txt', 'a') as f:
    for i in range(0, 660):
        radius.append(r)
        u.append(potential(r))
        f.write("{} {}\n".format(r, potential(r)))
        r += 0.05
xaxis = list()
yaxis = list()
for i in range(0,21):
    xaxis.append(i)
    yaxis.append(0)

fig, ax = plt.subplots(figsize=(8,6))
ax.set_title('Потенциал Леннард-Джонса', fontsize=16)
ax.set_xlabel('Радиус, [A]', fontsize=14)
ax.set_ylabel('Потенциальная энергия, [eV]', fontsize=14)
ax.axis([0,20,-0.011,0.01])  # [xstart, xend, ystart, yend]  # диапазон значений осей
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))  # интервал деления по оси х
ax.grid()
ax.plot(radius,u, color='red')
ax.plot(xaxis, yaxis, color = 'black')
plt.annotate('$1\sigma$', xy=(3.4,0),xytext=(3.7,0.002), fontsize=14, arrowprops=dict(facecolor='blue'))
plt.annotate('$R_c=2.5\sigma$', xy=(8.5,0),xytext=(7,0.002), fontsize=14, arrowprops=dict(facecolor='blue'))
plt.annotate('$R_c=3\sigma$', xy=(10.2,0),xytext=(10.4,0.0035), fontsize=14, arrowprops=dict(facecolor='blue'))
plt.show()

"""
plt.title('Потенциал Леннард-Джонса')
plt.xlabel('Радиус, [A]')
plt.ylabel('Потенциальная энергия, [eV]')
plt.grid('both')  # сетка
plt.axis([0,20,-0.011,0.01])  # [xstart, xend, ystart, yend]
plt.plot(radius,u)
plt.show()"""



