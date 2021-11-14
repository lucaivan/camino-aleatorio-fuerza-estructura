import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import ladrillos_fuerzas_v1 as lf

'''
SELECCIÓN DE DATOS
'''
unica_pagina = True
while True: #Opción una o varias iteraciones
    input1 = input("Teclear 'IT' para una sola iteración o 'ITS' para varias iteraciones: ")
    if input1=="IT":
        datos = lf.matrices
        break
    elif input1=="ITS":
        import tm_y_fp as tm_fp
        datos_tm = tm_fp.tension_media_matriz
        datos_fp = tm_fp.frecuencia_paso_matriz
        unica_pagina = False
        break
    else:
        print("Error: introduzca una secuencia válida.")
input2 = input("Teclear 'S' para superficie, 'W' para wireframe: ")
def op(ax, X, Y, Z): #Opción superficie o wireframe
    global input2
    while True:
        if input2 == 'S':
            ax.plot_surface(X, Y, Z)
            return
        elif input2 == 'W':
            ax.plot_wireframe(X, Y, Z)
            return
        else:
            input2 = input("Teclear 'S' para superficie, 'W' para wireframe: ")
            print("Error: introduzca una secuencia válida")
'''
GRÁFICAS 3D
'''
#MATRICES X,Y
X = np.array([[i for i in range(1,lf.X+1)]]*lf.Y)
temp_y = []
for y in range(1,lf.Y+1):
    temp = [y]*lf.X
    temp_y.append(temp)
Y = np.array(temp_y)
#MATRIZ Z
if unica_pagina: #Una iteración
    fig = plt.figure(num=1, figsize = [10, 30], clear=True)
    for z in range(lf.Z):
        ax = fig.add_subplot(lf.Z, 1, z+1, projection='3d')
        Z = datos[z]
        op(ax, X, Y, Z)

        ax.set_zlim(0,1)
        ax.view_init(elev=50, azim=-75)
        ax.grid(False)  
        ax.axis('off')
    fig.tight_layout()
    plt.show()
else: #Varias iteraciones
    fig_tm = plt.figure(num=1, figsize = [10, 30], clear=True)
    fig_tm.canvas.set_window_title('Tension media') 
    fig_fp = plt.figure(num=2, figsize = [10, 30], clear=True)
    fig_fp.canvas.set_window_title('Frecuencia de paso') 
    for z in range(lf.Z):
        ax_tm = fig_tm.add_subplot(lf.Z, 1, z+1, projection='3d')
        ax_fp = fig_fp.add_subplot(lf.Z, 1, z+1, projection='3d')
        Z_tm = datos_tm[z]
        Z_fp = datos_fp[z]
        op(ax_tm, X, Y, Z_tm)
        op(ax_fp, X, Y, Z_fp)

        ax_tm.set_zlim(0,1)
        ax_tm.view_init(elev=50, azim=-75)
        ax_tm.grid(False)  
        ax_tm.axis('off')

        ax_fp.set_zlim(0,1)
        ax_fp.view_init(elev=50, azim=-75)
        ax_fp.grid(False)  
        ax_fp.axis('off')
    fig_tm.tight_layout()
    fig_fp.tight_layout()
    plt.show()

#AVISO: En la gráfica el eje Y esta invertido con respecto a la matriz. Por ejemplo en x hilada, un 0.10
#en la esquina superior izquierda de la matriz sería representado en la gráfica en la esquina inferior izquierda.


