import os
import math


os.chdir("/home/igor/Рабочий стол/Верификация профиля давления/")
outputfile = 'Output.txt'
file1 = 'Сравнение с экспериментом газ.txt'
#file2 = 'Pressure_Rc=3_NOTshifted.txt'
#file3 = 'Pressure_Rc=7_NOTshifted.txt'

Pscale = 419.819865662528  # умножить на Pscale, чтобы получить размерную величину давления в [бар]
Tscale = 119.52653665398  # умножить на Tscale, чтобы получить размерную величину температуры в [K]
Rhoscale = 1.6877919550173  # умножить на Rhoscale, чтобы получить размерную величину плотности в [г/см^3]
Npoint = 10

with open(outputfile, 'w') as n:
    n.close()


def save_val(file, is_first):
    new_text = str()
    file_rho = list()
    file_p_MD = list()
    file_p_MD_full = list()
    with open(file, 'r') as f:
        new_string = f.readline()
        while new_string:
            new_string = f.readline()

            if 'rho = ' in new_string:
                new_list = new_string.split()
                file_rho.append(new_list[6])

            if 'P_MD_full =' in new_string:
                new_list = new_string.split()
                file_p_MD_full.append(new_list[-2])

    if is_first == True:
        with open(outputfile, 'a') as n:
            for i in range(Npoint):
                n.writelines('{} {} \n'.format(file_rho[i], file_p_MD_full[i]))
    else:
        with open(outputfile, 'r+') as n:
            for i in range(Npoint):
                old_string = n.readline()
                old_string = old_string.replace('\n', '')
                new_string = old_string + '{} \n'.format(file_p_MD_full[i])
                new_text += new_string
        with open(outputfile, 'w') as n:
            n.write(new_text)

def set_label(file):
    lines = 0
    for line in open(file):
        lines += 1

    with open(file, 'r') as r:
        new_string = r.readline()
        while new_string:
            new_list = new_string.split()
            for i in range(1,len(new_list)):
                print('set label "{}" at {},{}\n'.format(new_list[i],new_list[0],new_list[i] ))
            new_string = r.readline()

def p_LRC(rho, r_c):
    rho = float(rho)/Rhoscale
    P_LRC = (32 / 9) * math.pi * rho ** 2 * (r_c ** -9) - (16 / 3) * math.pi * rho ** 2 * (r_c ** -3)

    return P_LRC


def pressure_correction(file):
    with open(file, 'r') as f:
        rho = list()
        pressPmdRc25 = list()
        pressPmdRc30 = list()
        pressPmdRc25full = list()
        pressPmdRc30full = list()
        experiment = list()
        new_string = f.readline()
        while new_string:
            if 'rho =' in new_string:
                new_list = new_string.split()
                rho.append(new_list[-2])

            if 'experiment: p =' in new_string:
                new_list = new_string.split()
                experiment.append(new_list[-2])

            if 'R_c = 1.08' in new_string:
                new_list = new_string.split()
                pressPmdRc25.append(float(new_list[-6]))

            if 'R_c = 2.16' in new_string:
                new_list = new_string.split()
                pressPmdRc30.append(float(new_list[-6]))

            new_string = f.readline()
        print(rho)
        print(pressPmdRc25)
        for i in range(0,Npoint):
            P_lrc = p_LRC(rho[i],3)
            pressPmdRc25full.append((pressPmdRc25[i]+P_lrc*Pscale))
            print(pressPmdRc25[i], P_lrc*Pscale)

        for i in range(0,Npoint):
            P_lrc = p_LRC(rho[i],7)
            pressPmdRc30full.append((pressPmdRc30[i] + P_lrc*Pscale))


        with open(outputfile, 'r+') as f:
            for i in range(Npoint):
                f.write('{} {} {} {}\n'.format(rho[i], experiment[i], round(pressPmdRc25full[i], 4),
                                               round(pressPmdRc30full[i],4)))


pressure_correction(file1)
#save_val(file1, True)
#save_val(file2, False)
#save_val(file3, False)
#add_analitical_data(file1)
#set_label(outputfile)

