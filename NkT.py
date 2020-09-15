import os
os.chdir("/home/igor/Рабочий стол/Верификация профиля давления/20k частиц")

V = 1015200 * (10 ** -30)
k_B = 1.38 * 10 ** (-23)
T = 100
N = 21423
P = (N * k_B * T / V) * (10 ** -5)
print(P)

n_val_list = list()
with open('Output.txt', 'r') as o:
    n_string = o.readline()
    while n_string:
        n_list = n_string.split()
        if len(n_list) > 2:
            n_val_list.append(n_list[-1])
        n_string = o.readline()
    o.close()

print(n_val_list)


n_val_list1 = list()
with open('Pressure_Rc=3_NOTshifted.txt', 'r') as f:
    n_string = f.readline()
    while n_string:
        if 'P_MD =' in n_string:
            new_list = n_string.split()
            n_val_list1.append(new_list[-2])
        n_string = f.readline()
    f.close()
print(n_val_list1)

rho = 1.33
for i in range(0,8):
    virial = round(float(n_val_list1[i]) - float(n_val_list[i]),4)
    print(rho, n_val_list[i], virial, n_val_list1[i])
    rho = round(rho + 0.01,2)
#123