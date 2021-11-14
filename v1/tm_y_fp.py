import ladrillos_fuerzas_v1 as lf
import numpy as np
import time
start_time = time.time()

'''
TENSION MEDIA Y FRECUENCIA DE PASO (Nota: El programa tarda en ejecutarse ~3min por cada 100 iteraciones con m=7 dx=4 dy=8)
'''
iteraciones = 101
count = 0
frecuencia_paso_matriz = np.zeros((lf.Z, lf.Y, lf.X))
tension_media_matriz = np.zeros((lf.Z, lf.Y, lf.X))

for i in range(iteraciones):
    #TENSION MEDIA
    tension_media_matriz += lf.matrices
    #FRECUENCIA DE PASO
    for z in range(lf.Z):
        for y in range(lf.Y):
            for x in range(lf.X):
                if lf.matrices[z][y][x] != 0:
                    frecuencia_paso_matriz[z][y][x] += 1

    lf.main()
    count += 1
    print(count)

for z in range(lf.Z): #Se divide cada valor entre el número de iteraciones
    for y in range(lf.Y):
        for x in range(lf.X):
            tension_media_matriz[z][y][x] = tension_media_matriz[z][y][x]/iteraciones
            frecuencia_paso_matriz[z][y][x] = frecuencia_paso_matriz[z][y][x]/iteraciones

'''
SUMA DE LAS TENSIONES POR HILADA
'''
suma_tensiones = []
for z in tension_media_matriz:
    count = 0
    for y in z:
        for x in y:
            count +=x
    suma_tensiones.append(count)

'''
SUMA DE LAS FRECUENCIAS POR HILADA
'''
suma_frecuencias = []
for z in frecuencia_paso_matriz:
    count = 0
    for y in z:
        for x in y:
            count +=x
    suma_frecuencias.append(count)

'''
SALIDA EN FORMATO TXT
'''
tm = open('tension_media.txt', 'w') #Se crea un archivo tension_media.txt, si existe el archivo se sobrescribe.
fp = open('frecuencia_paso.txt', 'w') #Se crea un archivo frecuencia_paso.txt, si existe el archivo se sobrescribe.
for z in range(lf.Z):
    for j in range(lf.Y):
        list_tm = []
        list_fp = []
        for x in range(lf.X):
            if round(tension_media_matriz[z][j][x], 2) == 0:
                list_tm.append('0'+3*' ') #nº de espacios = nº de cifras decimales +1
            else:
                list_tm.append('{0:.2f}'.format(tension_media_matriz[z][j][x])) #Se trunca a 2 cifras decimales
            if round(frecuencia_paso_matriz[z][j][x], 2) == 0:
                list_fp.append('0'+3*' ') #nº de espacios = nº de cifras decimales +1
            else:
                list_fp.append('{0:.2f}'.format(frecuencia_paso_matriz[z][j][x])) #Se trunca a 2 cifras decimales
        string_tm = ' '.join(list_tm)
        string_fp = ' '.join(list_fp)
        tm.write(string_tm)
        tm.write('\n')
        fp.write(string_fp)
        fp.write('\n')
    tm.write('\n')
    tm.write('\n')
    fp.write('\n')
    fp.write('\n')
tm.close()
fp.close()

print("Suma de las tensiones de cada hilada: " + str(suma_tensiones))
print()
print("Suma de las frecuencias de cada hilada: " + str(suma_frecuencias))
print()
print("Tiempo de ejecución: %.2f segundos" % (time.time()-start_time))
print()