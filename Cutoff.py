import math
#rho = 0.9
#r_c = 2.5
Pscale = 419.819865662528
"""U_tail = (8/3) * 3.14 * rho * ((1/3) * (1/r_c)**9 - (1/r_c)**3)
P_tail = (16/3) * 3.14 * (rho**2) * ((2/3) * (1/r_c)**9 - (1/r_c)**3)
P_LRC = (32/9) * 3.14 * rho ** 2 * (r_c ** -9) - (16/3) * 3.14 * rho ** 2 * (r_c ** -3)
print("Энергия парных взимодейсвтий, которую не учитываем из-за обрезанного потенциала U*_tail = {} = {} [eV] \n"
      "Давление за пределами r_c P*_tail = {} = {} [bars] \n"
      "Поправка к давлению P*_LRC = {} = {} [bars]".format(U_tail, U_tail/0.0104, P_tail, P_tail*Pscale,
                                                           P_LRC, P_LRC * Pscale))"""
def p_LRC(rho, r_c):
    P_LRC = (32 / 9) * math.pi * rho ** 2 * (r_c ** -9) - (16 / 3) * math.pi * rho ** 2 * (r_c ** -3)
    print("P_LRC = {} При r_c = {} и rho = {}".format(round(P_LRC*Pscale,4), r_c, rho))

rho = (0.006, 0.711, 0.7702, 0.8295)
r_c = (2.5, 3, 5, 7, 9)

for i in range(0,4):
    for j in range(0,5):
        p_LRC(rho[i], r_c[j])
