import math

Pscale = 419.819865662528  # умножить на Pscale, чтобы получить размерную величину давления в [бар]
Tscale = 119.52653665398  # умножить на Tscale, чтобы получить размерную величину температуры в [K]
Rhoscale = 1.6877919550173  # умножить на Rhoscale, чтобы получить размерную величину плотности в [г/см^3]

def calc_pressure(rho_r, T_r):
    T = round((T_r*Tscale), 6)
    rho = round((rho_r*Rhoscale), 6)
    print("rho* = {}, rho = {} [g/cm^3], T* = {}, T = {} [K]".format(rho_r, rho, T_r, T))
    gamma = 3
    x = (
    -0.044480725, 7.2738221, -14.343368000000002, 3.8397096, -2.0057745, 1.9084472, -5.7441787, 25.110073, -4523.2787,
    0.008932716200000001, 9.816335800000001, -61.434571999999996, 14.161454, 43.353840999999996, 1107.8327, -35.429519,
    10.591298, 497.70046, -353.38542, 4503.6093, 7.7805296, 13567.114, -8.5818023, 16646.578, -14.092234000000001,
    19386.911, 38.585868, 3380.0371, -185.67754, 8487.4693, 97.508689, -14.48306
    )

    P_r = (rho_r * T_r + rho_r ** 2 * (x[0] * T_r + x[1] * T_r ** (1 / 2) + x[2] + x[3] * T_r ** (-1) + x[4] * T_r ** (-2)) +
           rho_r ** 3 * (x[5] * T_r + x[6] + x[7] * T_r ** (-1) + x[8] * T_r ** (-2)) +
           rho_r ** 4 * (x[9] * T_r + x[10] + x[11] * T_r ** (-1)) +
           rho_r ** 5 * (x[12]) +
           rho_r ** 6 * (x[13] * T_r ** (-1) + x[14] * T_r ** (-2)) +
           rho_r ** 7 * (x[15] * T_r ** (-1)) +
           rho_r ** 8 * (x[16] * T_r ** (-1) + x[17] * T_r ** (-2)) +
           rho_r ** 9 * (x[18] * T_r ** (-2)) +
           rho_r ** 3 * (x[19] * T_r ** (-2) + x[20] * T_r ** (-3)) * math.exp(-gamma * rho_r ** 2) +
           rho_r ** 5 * (x[21] * T_r ** (-2) + x[22] * T_r ** (-4)) * math.exp(-gamma * rho_r ** 2) +
           rho_r ** 7 * (x[23] * T_r ** (-2) + x[24] * T_r ** (-3)) * math.exp(-gamma * rho_r ** 2) +
           rho_r ** 9 * (x[25] * T_r ** (-2) + x[26] * T_r ** (-4)) * math.exp(-gamma * rho_r ** 2) +
           rho_r ** 11 * (x[27] * T_r ** (-2) + x[28] * T_r ** (-3)) * math.exp(-gamma * rho_r ** 2) +
           rho_r ** 13 * (x[29] * T_r ** (-2) + x[30] * T_r ** (-3) + x[31] * T_r ** (-4)) * math.exp(
                -gamma * rho_r ** 2)
           )
    P_r = round(P_r, 3)
    P_Nicloas = round((P_r * Pscale), 3)

    P_Liq_by_Vasserman = ((-456.6 + 4.157 * T + 4274 * (10 ** 2) * (T ** -2) - 360553 * (10 ** 4) * (T ** -4)) *
                          (rho ** 2) - (733.5 - 2.67 * T) * (rho ** 4) + 287 * (rho ** 6))
    P_Liq_by_Vasserman = round(P_Liq_by_Vasserman, 3)
    P_Liq_by_Vasserman_r = round((P_Liq_by_Vasserman / Pscale), 3)
    print("Давление по ур-ию Николаса: P* = {}; P = {} [бар]".format(P_r, P_Nicloas))
    print("Давление по ур-ию Вассермана: P* = {}; P = {} [бар]".format(P_Liq_by_Vasserman_r, P_Liq_by_Vasserman))
    print("\n")


Temp = 0.6
Rho = 0.9
while Rho < 1.2:
    calc_pressure(Rho, Temp)
    Rho = round((Rho + 0.025), 3)

SetT = 110
SetRho = 1
TinReduced = round((SetT / Tscale), 6)
RhoinReduced = round((SetRho / Rhoscale), 6)
print("Температура размерном виде Т = {} [K] - Температура в безрамзерном виде T* = {}".format(SetT, TinReduced))
print("Температура размерном виде Rho = {} [g/cm^3] - Температура в безрамзерном виде Rho* = {}".format(SetRho, RhoinReduced))

calc_pressure(RhoinReduced, Temp)






