from decimal import Decimal, getcontext
import math

# Установка точности вычислений
getcontext().prec = 100

def read_data_kT(variant=1):
    data_tab = []
    with open('data/kT.txt') as file:
        for line in file:
            if line.strip():
                parts = line.split()
                T = Decimal(parts[1])
                k_val = Decimal(parts[2] if variant == 1 else parts[3])
                data_tab.append((T, k_val))
    return data_tab

def linear_interpolation(x, x_values, y_values):
    """Ручная реализация линейной интерполяции с Decimal"""
    for i in range(len(x_values)-1):
        if x_values[i] <= x <= x_values[i+1]:
            return y_values[i] + (y_values[i+1] - y_values[i]) * (x - x_values[i]) / (x_values[i+1] - x_values[i])
    # Экстраполяция если x за границами
    if x < x_values[0]:
        return y_values[0]
    return y_values[-1]

def getkFunc(variantkT):
    data_kT = read_data_kT(variantkT)
    log_T = [d[0].ln() for d in data_kT]
    log_k = [d[1].ln() for d in data_kT]
    
    def k(T):
        T_dec = Decimal(str(T))
        x = T_dec.ln()
        interp_log_k = linear_interpolation(x, log_T, log_k)
        return interp_log_k.exp()
    
    return k

# Методы Рунге-Кутта с Decimal
def RungeKutta2Step(duFunc, dFFunc, ri, ui, Fi, h, alpha):
    h = Decimal(str(h))
    alpha = Decimal(str(alpha))
    ri = Decimal(str(ri))
    ui = Decimal(str(ui))
    Fi = Decimal(str(Fi))
    
    k1 = duFunc(ri, ui, Fi)
    q1 = dFFunc(ri, ui, Fi)

    h_2a = h / (Decimal('2') * alpha)
    k2 = duFunc(ri + h_2a, ui + h_2a * k1, Fi + h_2a * q1)
    q2 = dFFunc(ri + h_2a, ui + h_2a * k1, Fi + h_2a * q1)

    yip1 = ui + h * ((Decimal('1') - alpha) * k1 + alpha * k2)
    zip1 = Fi + h * ((Decimal('1') - alpha) * q1 + alpha * q2)
    
    return yip1, zip1

def RungeKutta2(duFunc, dFFunc, r0, y0, z0, h, rTarget, alpha=1):
    r0 = Decimal(str(r0))
    y0 = Decimal(str(y0))
    z0 = Decimal(str(z0))
    h = Decimal(str(h))
    rTarget = Decimal(str(rTarget))
    
    rvals = [r0]
    yvals = [y0]
    Fvals = [z0]
    
    while rvals[-1] < rTarget:
        ri = rvals[-1] + h
        yi, Fi = RungeKutta2Step(duFunc, dFFunc, rvals[-1], yvals[-1], Fvals[-1], h, alpha)
        rvals.append(ri)
        yvals.append(yi)
        Fvals.append(Fi)
    
    return rvals, yvals, Fvals

def RungeKutta4Step(duFunc, dFFunc, ri, ui, Fi, h):
    h = Decimal(str(h))
    ri = Decimal(str(ri))
    ui = Decimal(str(ui))
    Fi = Decimal(str(Fi))
    
    k1 = duFunc(ri, ui, Fi)
    q1 = dFFunc(ri, ui, Fi)
    
    h2 = h / Decimal('2')
    k2 = duFunc(ri + h2, ui + h2 * k1, Fi + h2 * q1)
    q2 = dFFunc(ri + h2, ui + h2 * k1, Fi + h2 * q1)
    
    k3 = duFunc(ri + h2, ui + h2 * k2, Fi + h2 * q2)
    q3 = dFFunc(ri + h2, ui + h2 * k2, Fi + h2 * q2)
    
    k4 = duFunc(ri + h, ui + h * k3, Fi + h * q3)
    q4 = dFFunc(ri + h, ui + h * k3, Fi + h * q3)
    
    yip1 = ui + (h/Decimal('6')) * (k1 + Decimal('2')*k2 + Decimal('2')*k3 + k4)
    zip1 = Fi + (h/Decimal('6')) * (q1 + Decimal('2')*q2 + Decimal('2')*q3 + q4)
    
    # if yip1 < 0:
    #     print(f"RK4step: yip1={float(yip1)}, k1={float(k1)} k2={float(k2)} k3={float(k3)} k4={float(k4)}, ri={float(ri)}, ui={float(ui)}, Fi={float(Fi)}")
    
    return yip1, zip1

def RungeKutta4(duFunc, dFFunc, r0, y0, z0, h, rTarget):
    r0 = Decimal(str(r0))
    y0 = Decimal(str(y0))
    z0 = Decimal(str(z0))
    h = Decimal(str(h))
    rTarget = Decimal(str(rTarget))
    
    rvals = [r0]
    yvals = [y0]
    Fvals = [z0]
    
    while rvals[-1] < rTarget:
        ri = rvals[-1] + h
        yi, Fi = RungeKutta4Step(duFunc, dFFunc, rvals[-1], yvals[-1], Fvals[-1], h)
        rvals.append(ri)
        yvals.append(yi)
        Fvals.append(Fi)
    
    return rvals, yvals, Fvals

# Константы и вспомогательные функции
c = Decimal('3') * Decimal('1e10')
R = Decimal('0.35')

def T_r(r):
    r = Decimal(str(r))
    Tw = Decimal('2000')
    To = Decimal('1e4')
    p = Decimal('4')
    return (Tw - To) * ((r / R) ** p) + To

def up_r(r):
    r = Decimal(str(r))
    const1 = Decimal('3.084E-4')
    const2 = Decimal('4.799E4')
    T = T_r(r)
    denominator = (const2 / T).exp() - Decimal('1')
    return const1 / denominator

k = getkFunc(variantkT=2)

r0 = Decimal('0')
def get_y0(khi):
    khi = Decimal(str(khi))
    return khi * up_r(r0)
z0 = Decimal('0')
rTarget = R

def du(ri, ui, Fi):
    ri = Decimal(str(ri))
    ui = Decimal(str(ui))
    Fi = Decimal(str(Fi))
    k_val = k(T_r(ri))
    return -Decimal('3') * k_val * Fi / c

def dF(ri, ui, Fi):
    ri = Decimal(str(ri))
    ui = Decimal(str(ui))
    Fi = Decimal(str(Fi))
    k_val = k(T_r(ri))
    up = up_r(ri)
    
    if ri == Decimal('0') and Fi == Decimal('0'):
        return Decimal('0.5') * k_val * (up - ui)
    return -Fi / ri + c * k_val * (up - ui)

# Метод стрельбы и половинного деления
def solutionShooting(khi, RungeKuttaFunc, h_start):
    khi = Decimal(str(khi))
    h = Decimal(str(h_start))
    y0 = get_y0(khi)
    
    res_h = RungeKuttaFunc(du, dF, r0, y0, z0, h, rTarget)
    yR_h = res_h[1][-1]
    
    res_h2 = RungeKuttaFunc(du, dF, r0, y0, z0, h/Decimal('2'), rTarget)
    yR_h2 = res_h2[1][-1]
    
    while abs(yR_h - yR_h2) / yR_h2 >= Decimal('1e-2'):
        print(f"khi = {khi}, h = {h}, yR_h = {yR_h}, yR_h2 = {yR_h2}, acc = {abs(yR_h - yR_h2) / yR_h2}")
        h /= Decimal('2')
        res_h, yR_h = res_h2, yR_h2
        res_h2 = RungeKuttaFunc(du, dF, r0, y0, z0, h/Decimal('2'), rTarget)
        yR_h2 = res_h2[1][-1]
    
    return (res_h[1][-1], res_h[2][-1]), h

def equationTarget(uR, FR):
    uR = Decimal(str(uR))
    FR = Decimal(str(FR))
    return FR - Decimal('0.39') * c * uR

def HalfDivMethod(RungeKuttaFunc, h_start):
    h = Decimal(str(h_start))
    khi_l, khi_r = Decimal('0.1'), Decimal('1')
    
    res_l, h = solutionShooting(khi_l, RungeKuttaFunc, h)
    res_r, h = solutionShooting(khi_r, RungeKuttaFunc, h)

    while abs(khi_r - khi_l) / khi_l >= Decimal('1e-2'):
        khi_mid = (khi_l + khi_r) / Decimal('2')
        res_mid, h = solutionShooting(khi_mid, RungeKuttaFunc, h)
        
        if equationTarget(*res_mid) * equationTarget(*res_l) < Decimal('0'):
            khi_r = khi_mid
        else:
            khi_l = khi_mid
            res_l = res_mid
    
    return khi_mid, h

# Запуск расчета
h_st = Decimal('0.01')
khi_solution, h_solution = HalfDivMethod(RungeKutta4, h_st)
print(f"Решение: χ = {khi_solution}, h = {h_solution}")



import plotly.express as px
import pandas as pd

RungeKutta = RungeKutta4
y0 = get_y0(khi_solution)
print(f"khi = {khi_solution}, h = {h_solution}")
rvals, yvals, Fvals = RungeKutta(du, dF, r0, y0, z0, h_solution, rTarget)
upvals = [up_r(ri) for ri in rvals]

df1 = pd.DataFrame({"r": rvals, "f": yvals, "label": ["u(r)"] * len(rvals) })
df2 = pd.DataFrame({"r": rvals, "f": Fvals, "label": ["F(r)"] * len(rvals)})
df3 = pd.DataFrame({"r": rvals, "f": upvals, "label": ["up(r)"] * len(rvals)})

df = pd.concat([df1, df3])
fig2 = px.line(df, x="r", y="f", color="label", title="", markers = True)
fig2.show()

fig1 = px.line(df2, x="r", y="f", color="label", title="", markers = True)
fig1.show()