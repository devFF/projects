import os


os.chdir("/home/igor/Рабочий стол/Верификация профиля давления/20k частиц")
outputfile = 'Output.txt'
file1 = 'Pressure_Rc=6_NOTshifted.txt'
file2 = 'Pressure_Rc=7_NOTshifted.txt'


Npoint = 8

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

            if 'P_MD =' in new_string:
                new_list = new_string.split()
                file_p_MD.append(new_list[-2])

            if 'P_MD_full =' in new_string:
                new_list = new_string.split()
                file_p_MD_full.append(new_list[-2])
    if is_first == True:
        with open(outputfile, 'a') as n:
            for i in range(Npoint):
                n.writelines('{} {} {} \n'.format(file_rho[i], file_p_MD_full[i], file_p_MD[i]))
    else:
        with open(outputfile, 'r+') as n:
            for i in range(Npoint):
                old_string = n.readline()
                old_string = old_string.replace('\n', '')
                new_string = old_string + '{} {} \n'.format(file_p_MD_full[i], file_p_MD[i])
                new_text += new_string
        with open(outputfile, 'w') as n:
            n.write(new_text)

def add_analitical_data(file):
    new_text = str()
    file_Jonson = list()
    file_Vasserman = list()
    with open(file, 'r') as f:
        new_string = f.readline()
        while new_string:
            new_string = f.readline()

            if 'ур. Джонсона:' in new_string:
                new_list = new_string.split()
                file_Jonson.append(new_list[-2])

            if 'ур. Вассермана:' in new_string:
                new_list = new_string.split()
                file_Vasserman.append(new_list[-2])
        with open(outputfile, 'r+') as n:
            for i in range(Npoint):
                old_string = n.readline()
                old_string = old_string.replace('\n', '')
                new_string = old_string + '{} {} \n'.format(file_Jonson[i], file_Vasserman[i])
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


save_val(file1, True)
save_val(file2, False)
add_analitical_data(file1)
#set_label(outputfile)

