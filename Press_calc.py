import math  # Пакет математики
import os  # Пакет для работы с операционной системой

# ОБЪЯВЛЯЕМ РАБОЧУЮ ДИРЕКТОРИЮ
dir = "/home/igor/lammps/src/"  # Задаем абсолютный путь к файлу
os.chdir(dir)  # объявили директорию

# ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ:
epsilon = 0.0103  # [eV] -- энергия связи, умножить на epsilon, чтобы получить размерную величину энергии [eV]
sigma = 3.4  # [A] -- длина связи, умножнить на sigma, чтобы получить размерную величину длины [A]
Pscale = 419.819865662528  # умножить на Pscale, чтобы получить размерную величину давления в [бар]
Tscale = 119.52653665398  # умножить на Tscale, чтобы получить размерную величину температуры в [K]
Rhoscale = 1.6877919550173  # умножить на Rhoscale, чтобы получить размерную величину плотности в [г/см^3]
k_B = 1.38 * 10 ** (-23)  # Постоянная Больцмана [дж/К]
pi = math.pi  # Пи
e = math.e  # Постоянная e

T = 110  # Температура для расчета давления по уравнению Гилгена [k]
rho = 1.25  # [g/cm^3] Плотность жидкости для расчета давления по уравнению Вассермана
T_c = 150.687  # Крит температура [K]
p_c = 4.863  # Крит давление [MPa]
rho_c = 0.9  # [g/cm^3]
r_c = 4  # БЕЗРАЗМЕРНОЕ ЗНАЧЕНИЕ РАДИУСА ОБРЕЗАНИЯ ДЕЙСТВИЯ ПЛД
tau = (1 - T / T_c)


i, k, sum_pressL1, sum_pressG, sum_pressL2, sys_ave_press = 0, 0, 0, 0, 0, 0
sum_pressL1_NkT, sum_pressG_NkT, sum_pressL2_NkT, sys_ave_press_NkT = 0, 0, 0, 0
avepress_L1, avepress_G, avepress_L2 = 0, 0, 0

################################ НАЧАЛО БЛОКА ОПИСАНИЯ ФУНКЦИЙ #########################################
# СОЗДАЕМ ВЫХОДНЫЕ ФАЙЛЫ
def create_output(*args):  # объявляем функцию, *args -- позволяет задать любое кол-во аргументов функции

    with open(args[0], "w") as f:  # Создаем пустой файл для выходных данных и записываем 4 столбца.
        f.write('Chunk_num Ncount v_pp Chunk_press \n')  # v_pp -- давление на один атом в чанке
    f.close()

    with open(args[1], "w") as p:  # Создаем dat для gnuplot
        p.write('Chunk_num Chunk_press_NkT Chunk_press \n')
    p.close()

def pressure(file):  # функция, которая обрабатывает выходной файл по строчкам
    i, k, sum_pressL1, sum_pressG, sum_pressL2, sys_ave_press = 0, 0, 0, 0, 0, 0
    sum_pressL1_NkT, sum_pressG_NkT, sum_pressL2_NkT, sys_ave_press_NkT = 0, 0, 0, 0
    avepress_L1, avepress_G, avepress_L2 = 0, 0, 0
    l = 2  # Кол-во нижних и верхних чанков, которые не рассматриваем при расчете давления.
    chunk_volume = 1 * 10 ** (-26)
    with open(file, 'r+') as z:  # Открываем выходной файл lammps
        new_string = z.readline()
        while new_string:  # Читаем по строчке до тех пор, пока не получим пустую строчку, тогда false и выход из цикла
            new_string = z.readline()
            try:
                if new_string[0] == '#':  # Пропускаем комментарии
                    pass
                else:
                    new_string = new_string.split(' ')  # Превращаем строчку в список
                    len_new_string = len(new_string)  # Определяем длину списка

                    if len_new_string == 3:
                        i, sum_pressL1, sum_pressG, sum_pressL2 = 0, 0, 0, 0
                        with open(dir + "Press_py.dat", "a") as a:
                            new_string = new_string[0] + ' ' + new_string[1] + ' ' + new_string[2] + '\n'
                            a.write(new_string)

                        with open(dir + "Press_prof_py.dat", "a") as a:
                            new_string = new_string[0] + ' ' + new_string[1] + ' ' + new_string[2] + '\n'
                            a.write(new_string)

                    if len_new_string == 9:
                        press_atom = float(new_string[-2].replace('\n', ''))  # среднее давление на один атом в чанке
                        Ncount = float(new_string[-3])  # среднее кол-во частиц в чанке
                        temp = float(new_string[-1])  # температура в чанке с учетом гидродин ск-ти
                        press_chunk = str(press_atom * Ncount)  # среднее давление в чанке с учетом вириала
                        press_chunk += '\n'  # добавляем символ переноса строки
                        chunk_number = new_string[2]
                        press_chunk_NkT = (Ncount * k_B * temp / chunk_volume) * 10 ** (
                            -5)  # Давление по формуле NkT/V в [бар]
                        # print(press_chunk_NkT, Ncount,temp)
                        i += 1
                        if l < i <= 20:
                            sum_pressL1 += float(press_chunk.replace('\n', ''))
                            sum_pressL1_NkT += press_chunk_NkT
                        elif 20 < i <= 79:
                            sum_pressG += float(press_chunk.replace('\n', ''))
                            sum_pressG_NkT += press_chunk_NkT
                        elif 80 < i <= 100 - l:
                            sum_pressL2 += float(press_chunk.replace('\n', ''))
                            sum_pressL2_NkT += press_chunk_NkT

                        if i == 100:
                            sum_pressL1 = sum_pressL1 / (20 - l)
                            sum_pressG = sum_pressG / (60)
                            sum_pressL2 = sum_pressL2 / (20 - l)
                            avepress = (sum_pressL1 + sum_pressL2 + sum_pressG) / 3
                            sum_pressL1_NkT = sum_pressL1_NkT / (20 - l)
                            sum_pressG_NkT = sum_pressG_NkT / (60)
                            sum_pressL2_NkT = sum_pressL2_NkT / (20 - l)
                            avepress_NkT = (sum_pressL1_NkT + sum_pressL2_NkT + sum_pressG_NkT) / 3
                            k += 1
                            if k > 2:  # Первые шаги включают минимизацию, поэтому не рассматриваем их при расчете давления
                                sys_ave_press += avepress  # Суммируем давление всей системы на каждом шаге
                                sys_ave_press_NkT += avepress_NkT  # Суммируем давление всей системы на каждом шаге
                                avepress_L1 += sum_pressL1
                                avepress_G += sum_pressG
                                avepress_L2 += sum_pressL2
                            steps = 'steps: ' + str(k) + '\n'
                            print('{}NkT/v - W: sum_pressL1 = {} sum_pressG = {} sum_pressL2 = {} avepress = {}'.format(
                                steps,
                                sum_pressL1,
                                sum_pressG,
                                sum_pressL2,
                                avepress))
                            print('NkT: sum_pressL1 = {} sum_pressG = {} sum_pressL2 {} avepress = {}'.format(
                                sum_pressL1_NkT,
                                sum_pressG_NkT,
                                sum_pressL2_NkT,
                                avepress_NkT))
                            i, sum_pressL1, sum_pressG, sum_pressL2 = 0, 0, 0, 0
                            sum_pressL1_NkT, sum_pressG_NkT, sum_pressL2_NkT = 0, 0, 0

                        with open(dir + "Press_py.dat", "a") as f:
                            new_string = '{} {} {} {}'.format(chunk_number, Ncount, press_atom, press_chunk)
                            f.write(new_string)

                        with open(dir + "Press_prof_py.dat",
                                  "a") as p:  # пишем файл для gnuplot: № чанка и давление в нем
                            new_string = '{} {} {}'.format(chunk_number, press_chunk_NkT, press_chunk)
                            p.write(new_string)
            except IndexError:
                pass

        z.close()



################################ КОНЕЦ БЛОКА ОПИСАНИЯ ФУНКЦИЙ ###########################################

# НАЧАЛО ПРОГРАММЫ:
create_output("Press_py.dat", "Press_prof_py.dat")  # Создаем выходные файлы
pressure("pp.dat")  # Открываем выходной файл из lammps, считаем давление.


