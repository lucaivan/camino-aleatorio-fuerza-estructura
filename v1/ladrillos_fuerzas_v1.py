import numpy as np 
from random import choice
from itertools import combinations
import math
import time

start_time = time.time()

'''
DATOS DE PARTIDA
'''
dx, dy = 8, 16 #Discretización de los ladrillos (x,y)
m = 7 #Número de hiladas. (Si se quiere se puede poner otro número de hiladas)
F1 = [1, [int(m*dx/2),4]] #Fuerza inicial
L1 = {int(m*dx/2)} #Punto medio del ladrillo inicial X

'''
MATRIZ DE RESULTADOS
'''
Z, Y, X = m+1,dy, dx*m
'''
APLICAR VALORES A LA MATRIZ DE RESULTADOS
'''
def aplicar_valores(resultados, indice_matriz):
    for s in resultados:
        matrices[indice_matriz][s[1][1]-1][s[1][0]-1] = s[0]

'''
REACCIÓN QUE PRODUCE UNA FUERZA EN UN LADRILLO
'''
def reacciones (med_x, N, P):
    Apoyos_x = [i for i in range(int(med_x-(dx/2-1)),int(med_x+dx/2+1))]
    Apoyos_y = [i for i in range(1, dy+1)]
    Apoyos = [(x,y) for x in Apoyos_x for y in Apoyos_y] #Posibles puntos de apoyo
    Comb_Apoyos = list(combinations(Apoyos, 3))
    
    for i in range(0, len(Comb_Apoyos)):
        Ps = choice(Comb_Apoyos) #Se escoge un trio de posiciones al azar
        Sol = EcuacionesEq(Ps, N, P)
        if ExistenTracciones(Sol):#Se excluyen las tracciones
            Comb_Apoyos.remove(Ps)
        else:
            break
        if ExistenTracciones(Sol) and i == len(Comb_Apoyos)-1:
            return None
    return [[Sol[i], list(Ps[i])] for i in range(3)]
'''
ECUACIONES DE EQUILIBRIO
'''
def EcuacionesEq(Ps, N, P):
    eq_x = [(i[0]-0.5)-(P[0]-0.5) for i in Ps] #Se resta 0.5 para calcular los puntos medios y no el cuadrado entero
    eq_y = [(i[1]-0.5)-(P[1]-0.5) for i in Ps]
    a = np.array([ [1,1,1], eq_x, eq_y ])
    b = np.array ([N, 0, 0])
    try:
        t = np.linalg.solve(a,b)
    except np.linalg.linalg.LinAlgError: #Aquí se han excluido el trio de posiciones que tienen infinitas soluciones. Es decir las alineadas en linea vertical o horizontal
        t = [0,0,0]                    
    t2 = [int(i*10**10)/10**10 for i in t] #Se excluyen las que tienen un valor muy cercano a 0 (son producto de un error de precisión y no factibles realmente, salvo que m sea muy grande)
    return t2

'''
COMPROBAR SI EXISTEN TRACCIONES
'''
def ExistenTracciones(sol):
    if sol[0] <= 0  or sol[1] <= 0  or sol[2] <= 0:
        return True
    else:
        return False

'''
RESULTANTE DE FUERZAS EN UN MISMO LADRILLO
'''
def resultante(fuerzas):
    N_resultante = 0
    P_resultante = [0,0]
    eq_x = []
    eq_y = []
    for i in fuerzas:
        N_resultante += i[0]
        eq_x.append(i[0]*(i[1][0]-0.5))
        eq_y.append(i[0]*(i[1][1]-0.5))
    P_resultante[0] = math.ceil(sum(eq_x)/N_resultante)
    P_resultante[1] = math.ceil(sum(eq_y)/N_resultante)

    return [N_resultante, P_resultante]

'''
DISTINGUE EN QUE LADRILLO ESTAN LAS REACCIONES
'''
def divisor(med_x, reacciones):
    reacs = []
    for r in reacciones:
        if  r[1][0] <= med_x +dx/2 and r[1][0] >= med_x-(dx/2-1):
            reacs.append(r)
    return reacs

'''
RECURSIÓN A TRAVÉS DE LA PIRÁMIDE
'''
def iteracion_hiladas(hilada_lad, hilada_reac, h):
    global m
    global hilada_lad_total
    global hilada_reac_total
    if h <= m:
        hilada_lad_next = set()
        hilada_reac_next = []
        stop = False
        for i in hilada_lad:
            reacs_aplicadas = divisor(i, hilada_reac) #Distingue las reacciones que se aplican sobre el ladrillo
            if reacs_aplicadas:
                f_aplicada = resultante(reacs_aplicadas) #Calcula la resultante de esas reacciones
                if f_aplicada[1][0] == i + dx/2 or f_aplicada[1][0] == i-(dx/2-1) or f_aplicada[1][1] == dy or f_aplicada[1][1]==1:
                    #Se excluyen las fuerzas aplicadas que están en los bordes (ya que no tienen solución) y se ahorra tiempo de ejecución
                    reacs_lad = None
                else:
                    reacs_lad = reacciones(i, f_aplicada[0], f_aplicada[1]) #Calcula las reacciones de esa resultante
                if reacs_lad == None:
                    stop = True
                    break
                [hilada_reac_next.append(i) for i in reacs_lad]
                hilada_lad_next.add(int(i-dx/2))
                hilada_lad_next.add(int(i+dx/2)) #Calcula la posición media de los ladrillos que tiene debajo
        if stop:#Retrocede una hilada
            h -= 1
            hilada_lad_total = hilada_lad_total[:-1]
            hilada_reac_total = hilada_reac_total[:-1]
            iteracion_hiladas(hilada_lad_total[h-1], hilada_reac_total[h-1], h) 
        else:#Avanza una hilada
            h += 1
            hilada_lad_total.append(hilada_lad_next)
            hilada_reac_total.append(hilada_reac_next)
            iteracion_hiladas(hilada_lad_next, hilada_reac_next, h)
    
'''
MAIN
'''
def main():
    global matrices; global hilada_lad_total; global hilada_reac_total
    matrices = np.zeros((Z, Y, X)); hilada_lad_total = [L1]; hilada_reac_total = [[F1]] #Valores iniciales
    iteracion_hiladas(hilada_lad_total[0], hilada_reac_total[0], 1) #Iteración por la pirámide
    for h_reac, h in zip(hilada_reac_total, range(m+1)): #Aplicar valores a la matriz de resultados
        aplicar_valores(h_reac, h)

main()
'''
VERIFICACIÓN SUMA DE LAS TENSIONES POR HILADA
'''
suma_tensiones = []
for z in matrices:
    count = 0
    for y in z:
        for x in y:
            count +=x
    suma_tensiones.append(count)

'''
SALIDA EN FORMATO TXT
'''
fh = open('resultados.txt', 'w') #Se crea un archivo resultados.txt, si existe el archivo se sobrescribe.
for i in range(len(matrices)):
    for j in range(Y):
        listK = []
        for k in range(X):
            if round(matrices[i][j][k], 2) == 0:
                listK.append('0'+3*' ') #nº de espacios = nº de cifras decimales +1
            else:
                listK.append('{0:.2f}'.format(matrices[i][j][k])) #Se trunca a 2 cifras decimales
        stringK = ' '.join(listK)
        fh.write(stringK)
        fh.write('\n')
    fh.write('\n')
    fh.write('\n')
fh.close()

print("Comprobación suma de tensiones por hilada: " + str(suma_tensiones))
print("Tiempo de ejecución: %.2f segundos" % (time.time() - start_time))
    

