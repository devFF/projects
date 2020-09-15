# Код для обработки выходного файла pp.dat алгоритма Parallel_plates1/Parallel_plates2
dir = "/home/igor/lammps/src/"  # Задаем абсолютный путь к файлу


# Обязательно проверять объем чанка!


def pressure(new_string):  # функция, которая обрабатывает выходной файл по строчкам
    global sum_pressL2, sum_pressL1, sum_pressG, i, k, l, k_B, chunk_volume, sum_pressL1_NkT, sum_pressG_NkT, \
        sum_pressL2_NkT, sys_ave_press, sys_ave_press_NkT, avepress_L1, avepress_G, avepress_L2
    # print(i)
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
            press_chunk_NkT = (Ncount * k_B * temp / chunk_volume) * 10 ** (-5)  # Давление по формуле NkT/V в [бар]
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
                print('{}NkT/v - W: sum_pressL1 = {} sum_pressG = {} sum_pressL2 = {} avepress = {}'.format(steps,
                                                                                                            sum_pressL1,
                                                                                                            sum_pressG,
                                                                                                            sum_pressL2,
                                                                                                            avepress))
                print('NkT: sum_pressL1 = {} sum_pressG = {} sum_pressL2 {} avepress = {}'.format(sum_pressL1_NkT,
                                                                                                  sum_pressG_NkT,
                                                                                                  sum_pressL2_NkT,
                                                                                                  avepress_NkT))
                i, sum_pressL1, sum_pressG, sum_pressL2 = 0, 0, 0, 0
                sum_pressL1_NkT, sum_pressG_NkT, sum_pressL2_NkT = 0, 0, 0

            with open(dir + "Press_py.dat", "a") as f:
                new_string = '{} {} {} {}'.format(chunk_number, Ncount, press_atom, press_chunk)
                f.write(new_string)

            with open(dir + "Press_prof_py.dat", "a") as p:  # пишем файл для gnuplot: № чанка и давление в нем
                new_string = '{} {} {}'.format(chunk_number, press_chunk_NkT, press_chunk)
                p.write(new_string)


# ОБЪЯВЛЯЫЕМ ПОСТОЯННЫЕ И ПЕРЕМЕННЫЕ
epsilon = 0.0103  # [eV] -- энергия связи
sigma = 3.4  # [A] -- длина связи
Pscale = 419.819865662528  # умножить на Pscale, чтобы получить размерную величину давления в [бар]
Tscale = 119.52653665398  # умножить на Tscale, чтобы получить размерную величину температуры в [K]
Rhoscale = 1.6877919550173  # умножить на Rhoscale, чтобы получить размерную величину плотности в [г/см^3]
k_B = 1.38 * 10 ** (-23)  # Постоянная больцмана [дж/К]
chunk_volume = 4.7 * 10 ** (-26)  # Объем чанка в [м^3]
e = 2.7182818  # Постоянная e
T = 110  # Температура для расчета давления по уравнению Гилгена [k]
rho = 1.25  # [g/cm^3] Плотность жидкости для расчета давления по уравнению Вассермана
T_c = 150.687  # Крит температура [K]
p_c = 4.863  # Крит давление [MPa]
rho_c = 0.9  # [g/cm^3]
r_c = 4 # БЕЗРАЗМЕРНОЕ ЗНАЧЕНИЕ РАДИУСА ОБРЕЗАНИЯ ДЕЙСТВИЯ ПЛД
tau = (1 - T / T_c)
N_1, N_2, N_3, N_4 = -5.940978, 1.355389, -0.4649761, -1.539904  # Для газа
N_L1, N_L2, N_L3, N_L4, N_L5 = 1.867389, -0.6486635, -1.843047, 2.949138, -1.104305 # Коэффициенты для жидкости

i, k, sum_pressL1, sum_pressG, sum_pressL2, sys_ave_press = 0, 0, 0, 0, 0, 0
sum_pressL1_NkT, sum_pressG_NkT, sum_pressL2_NkT, sys_ave_press_NkT = 0, 0, 0, 0
avepress_L1, avepress_G, avepress_L2 = 0, 0, 0
l = 2  # Количество обрезаемых чанков по краям, чтобы не учитывать термостатированный слой

with open(dir + "Press_py.dat", "w") as f:  # Создаем файл, в который сохраняем обоаботанные данные
    f.write('Chunk_num Ncount v_pp Chunk_press \n')
    f.close()

with open(dir + "Press_prof_py.dat", "w") as p:  # Создаем dat для gnuplot
    p.write('Chunk_num Chunk_press_NkT Chunk_press \n')
    p.close()

with open(dir + "pp.dat", 'r+') as f:
    new_string = f.readline()
    while new_string:  # Читаем по строчке до тех пор, пока не получим пустую строчку, тогда false и выход из цикла
        new_string = f.readline()
        try:
            pressure(new_string)
        except IndexError:
            pass
    sys_ave_press = sys_ave_press / (
                k - 2)  # Определяем среднее давление всей системы (-2 это не учитанные первые 2 шага)
    sys_ave_press_NkT = sys_ave_press_NkT / (k - 2)  # Определяем среднее давление всей системы
    avepress_L1 = avepress_L1 / (k - 2)
    avepress_G = avepress_G / (k - 2)
    avepress_L2 = avepress_L2 / (k - 2)
    # P_vap_liq_equilibrium = (e ** 4.6334 - 4.5397 / (T/T_c) - 0.22715/ ((T/T_c) ** 2) + 0.13114 * (T/T_c) ** 5.7406)*p_c
    P_Gas_by_Gilgen = (e ** ((T_c / T) * (N_1 * tau + N_2 * tau ** 1.5 + N_3 * tau ** 2 + N_4 * tau ** 4.5))) * p_c
    Rho_Liq_by_Gilgen = (e ** (N_L1 * tau ** 0.35 + N_L2 * tau ** (3 / 6) + N_L3 * tau ** (14 / 6) + N_L4 * tau ** (
                15 / 6) + N_L5 * tau ** (17 / 6))) * rho_c
    P_Liq_by_Vasserman = ((-456.6 + 4.157 * T + 4274 * (10 ** 2) * (T ** -2) - 360553 * (10 ** 4) * (T ** -4)) *
                          (rho ** 2) - (733.5 - 2.67 * T) * (rho ** 4) + 287 * (rho ** 6))
    mol_gram = 34.36 * (39.948 / 1000)  # Перевод плотности из [моль/литр] -> [гр/см^3]

    P_LRC = (32 / 9) * 3.14 * rho_c ** 2 * (r_c ** -9) - (16 / 3) * 3.14 * rho_c ** 2 * (r_c ** -3)  # дальнодействующая поправка к давлению
    P_full = sys_ave_press + P_LRC*Pscale

    print('mol_gram = {} [г/см^3]'.format(mol_gram))
    print("Плотность жидкости по уравнению Гилгена = {} [g/cm^3]".format(Rho_Liq_by_Gilgen))
    print("Давление в газе по уравнению Гилгена = {} [МПа] = {} [бар]".format(P_Gas_by_Gilgen, P_Gas_by_Gilgen * 10))
    print("Давление в жидкости по уравнению Вассермана = {} [бар]".format(P_Liq_by_Vasserman))  # Работает при плотности
    # от 0.869 г/см^3 до 1.450 г/см^3
    # print("Жидкость-пар равновесное давление = {} [Мпа] (уравнение Вилсака)".format(P_vap_liq_equilibrium))
    print('sys_ave_press = {} [бар], sys_ave_press_NkT = {} [бар]'.format(sys_ave_press, sys_ave_press_NkT))
    print('Среднее давлеие в L1: {} [бар], Среднее давление в G: {} [бар], '
          'Среднее давление в L2: {} [бар]'.format(avepress_L1, avepress_G, avepress_L2))
    print('Среднее давление в системе sys_ave_press с учетом дальнодействующей поправки P = {} [bars]'.format(P_full))
