import matplotlib.pyplot as plt
from numpy.core.arrayprint import LongFloatFormat
import numpy as np
from scipy.optimize.minpack import curve_fit
from scipy import asarray as ar,exp
import ladrillos_fuerzas_v1 as lf

'''
SELECCIÓN DE DATOS
'''
while True: #Opción una o varias iteraciones
    input1 = input("Teclear 'IT' para una sola iteración o 'ITS' para varias iteraciones: ")
    if input1=="IT":
        datos = [lf.matrices]
        break
    elif input1=="ITS":
        import tm_y_fp as tm_fp
        datos = [tm_fp.tension_media_matriz, tm_fp.frecuencia_paso_matriz]
        break
    else:
        print("Error: introduzca una secuencia válida.")
'''
DATOS Y REPRESENTACIÓN 2D
'''
def gauss(x, a, b, c):
	return a*exp(-(x-b)**2/(2*c**2))

for d, count in zip(datos, range(len(datos))):
    fig = plt.figure(num=count+1, clear=True)
    if len(datos) > 1: #Títulos de la página de matplotlibs
        if count == 0:
            fig.canvas.set_window_title('Tension media')
        else:
            fig.canvas.set_window_title('Frecuencia de paso')

    for z in range(lf.Z):
        ax = fig.add_subplot(lf.Z, 1, z+1)
        inicio_lads = (lf.m-z)*int(lf.dx/2)+1
        fin_lads = (lf.m+z)*int(lf.dx/2)
        xdata = []
        ydata = []
        if z == 0:
            xdata = [lf.F1[1][0]]
            ydata = [1]
        for x in range (inicio_lads, fin_lads+1):
            xdata.append(x)
            y_sum = 0
            for y in range(lf.Y):
                y_sum += d[z][y][x-1]
            ydata.append(y_sum)

        xdata = np.asarray(xdata)
        ydata = np.asarray(ydata)
        ax.scatter(xdata, ydata)

        ax.set_xlim(0.9, lf.X+1.1)
        ax.set_ylim(-0.1, 1.75)
        ax.set_xticks(np.arange(0, lf.X+0.1, 1))
        ax.set_yticks(np.arange(0, 1.75, 0.5))

        if z != 0:
            ax.set_yticklabels([])  
            ax.set_xticklabels([])
        #if z > 3: #Ajuste gaussiano
        #    parameters, covariance = curve_fit(gauss, xdata, ydata)
        #    x_fit = np.linspace(0.9, lf.X+0.1, 100)
        #    y_fit = gauss(x_fit, parameters[0], parameters[1], parameters[2])
        #    ax.plot(x_fit, y_fit)

    fig.subplots_adjust(left=0.05, bottom=0.025, right=0.975, top=0.975, wspace=0.2, hspace=0.5)
plt.show()