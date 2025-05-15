import random
import sys
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


def generar_cromosoma(bits):
    cromosoma =[random.randint(0,1) for _ in range(bits)]
    cromosoma = ''.join(map(str, cromosoma))
    return cromosoma

def genera_poblacion_inicial(cant_cromo, bits):
    return [generar_cromosoma(bits) for i in range(cant_cromo)]

def calcula_obj(poblacion,coef):
    return[((int(cromosoma,2)/coef)**2) for cromosoma in poblacion]

def calcula_fitness(valores_objs, sumatoria):
   return [i/sumatoria for i in valores_objs]


def busca_maximo(poblacion, coef):
    max = 0
    ganador = 0

    for cromo in poblacion:
        val = int(cromo,2)
        if (((val/coef)**2) > max):
            ganador = cromo
            max = ((val/coef)**2)
    
    return ganador



def torneo(cromosomas, fit):    
    seleccionados = []
    tam = len(fit)
    for _ in range(tam):
        idA = random.randint(0,tam-1)
        idB = random.randint(0,tam-1)
        if (fit[idA] > fit[idB]): seleccionados.append(cromosomas[idA])
        else: seleccionados.append(cromosomas[idB])
    
    return seleccionados


def ruleta(cromosomas, fit,cant):
    seleccionados = []
    ruleta = [] 
    for i in range(len(fit)):
        val = max(int(fit[i]*100),1)
        for _ in range(val): ruleta.append(i)
    
    while(len(ruleta) < 100): ruleta.append(len(fit)-1)     
    
    for _ in range(cant):
        salida = random.randint(0,99)
        seleccionados.append(cromosomas[ruleta[salida]])
    
    return seleccionados


def ruleta_elite(cromosomas,fit):
    seleccionados = []
    tam = len(fit)
    elite = []
    for i in range(tam): elite.append([fit[i],i])
    elite.sort()
    idA = elite[tam-1][1]
    idB = elite[tam-2][1]
    seleccionados.append(cromosomas[idA])
    seleccionados.append(cromosomas[idB])
    seleccion_ruleta = ruleta(cromosomas,fit,8)
    return seleccionados + seleccion_ruleta


def cruza(seleccionados,prob_cross):
    descendencia = []
    for i in range(0, len(seleccionados) - 1,2):
        prob = random.random()
        if (prob <= prob_cross):
            corte = random.randint(0,29)
            padre1 = seleccionados[i]
            padre2 = seleccionados[i+1]
            
            hijo1 = padre1[:corte] + padre2[corte:]
            hijo2 = padre2[:corte] + padre1[corte:]

            assert(len(padre1) == len(padre2))
            assert(len(hijo1) == len(padre1))
            assert(len(hijo2) == len(padre2))
            
            descendencia.append(hijo1)
            descendencia.append(hijo2)
        else:
            descendencia.append(seleccionados[i])
            descendencia.append(seleccionados[i+1])
    return descendencia


def mutacion(hijos,prob_mut):
    hijos_nuevos = []
    for hijo in hijos:
        hijo_nuevo = ""
        prob = random.random()
        if (prob <= prob_mut):
            lim_inf = random.randint(0,29)
            lim_sup = random.randint(0,29)

            if (lim_inf > lim_sup): lim_inf, lim_sup = lim_sup, lim_inf            
            
            segmento_inv = hijo[lim_inf:lim_sup+1][::-1]
            hijo_nuevo = hijo[:lim_inf] + segmento_inv + hijo[lim_sup+1:] 
            
            hijos_nuevos.append(hijo_nuevo) 
        else: hijos_nuevos.append(hijo)          
    return hijos_nuevos


def hacer_grafica(maximos,minimos,promedios,cant_individuos,cant_corridas):
    numero_corrida = [i+1 for i in range(cant_corridas)]
    for i in range(cant_corridas):
        promedios[i] = promedios[i]/cant_individuos
    plt.plot(figsize=(25, 10))
    plt.plot(numero_corrida,maximos,linestyle='-',label='Valor Maximo')
    plt.title('Maximo por corrida')
    plt.xlabel('Numero Corrida')
    plt.ylabel('Valor Maximo')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    plt.plot(numero_corrida,minimos,linestyle='-',label='Valor Minimo')
    plt.title('Minimo por corrida')
    plt.xlabel('Numero Corrida')
    plt.ylabel('Valor Minimo')
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.plot(numero_corrida,promedios,linestyle='-',label='Valor Promedio')
    plt.title('Promedio por corrida')
    plt.xlabel('Numero Corrida')
    plt.ylabel('Valor Promedio')
    plt.legend()
    plt.tight_layout()
    plt.show()

def hacer_tabla(maximos,minimos,promedios,cant_individuos,cant_corridas):
    for i in range(cant_corridas):
        promedios[i] = promedios[i]/cant_individuos
    df = pd.DataFrame(list(zip(maximos,minimos,promedios)),columns=['Valor Maximo','Valor Minimo','Promedio'])
    wb = Workbook()
    ws = wb.active
    cont = 0
    for r in dataframe_to_rows(df, index=True, header=True):
        if (cont == 0):
            r[0] = "Generacion"
        if (cont >= 2):
            r[0] = r[0]+1
        print(r)
        ws.append(r)
        cont += 1
    for cell in ws['A'] + ws[1]:
        cell.style = 'Pandas'
    wb.save("pandas_openpyxl.xlsx")
    

def main():
    if (len(sys.argv) != 11 or sys.argv[1] != "-c" or sys.argv[3] != "-m" or sys.argv[5] != "-n" or sys.argv[7] != "-o" or sys.argv[9] != "-g"):
        print("Este programa se utiliza con python tp1.py -c <prob_cross> -m <prob_mut> -n <cant_individuos> -o <metodo_seleccion> -g <cant_generaciones>")
        sys.exit()
    prob_cross = float(sys.argv[2])
    prob_mut = float(sys.argv[4])
    cant_individuos = int(sys.argv[6])
    op = int(sys.argv[8])
    generaciones = int(sys.argv[10])
    coef = (2**30) - 1
    cant_bits = 30
    max_por_ciclo = []
    valormin_por_ciclo = []
    valormax_por_ciclo = []
    sumas_obj_por_ciclo = []

    poblacion = genera_poblacion_inicial(cant_individuos, cant_bits)
    
    for i in range(generaciones):
        print(f"Poblacion {i}: {poblacion}")
        print("========================================================================")
        valores_func_obj = calcula_obj(poblacion, coef)
        valormin_por_ciclo.append(min(valores_func_obj))
        valormax_por_ciclo.append(max(valores_func_obj))
        sumas_obj_por_ciclo.append(sum(valores_func_obj)) 
        max_por_ciclo.append(busca_maximo(poblacion, coef))
    
        sumatoria = sum(valores_func_obj)
        fitness = calcula_fitness(valores_func_obj, sumatoria)
        if (op == 0): seleccionados = ruleta(poblacion, fitness,10)
        elif (op == 1): seleccionados = torneo(poblacion,fitness)
        elif (op == 2): seleccionados = ruleta_elite(poblacion,fitness)
        else:
            print("El metodo de seleccion elegido no es valido")
            print("Opciones:")
            print("-0: Ruleta")
            print("-1: Torneo")
            print("-2: Ruleta + Elitismo")
            sys.exit()
        hijos = cruza(seleccionados,prob_cross)
        poblacion = mutacion(hijos,prob_mut)
    
    for i in range(20):
        print("========================================================================")
        print(f"Valor maximo en poblacion {i}: {valormax_por_ciclo[i]} con el cromosoma {max_por_ciclo[i]}") 
        print(f"Valor minimo en poblacion {i}: {valormin_por_ciclo[i]}")
        print(f"Promedio de poblacion {i}: {sumas_obj_por_ciclo[i]/cant_individuos}")
        print("========================================================================")
    hacer_tabla(valormax_por_ciclo,valormin_por_ciclo,sumas_obj_por_ciclo,cant_individuos,generaciones)
    hacer_grafica(valormax_por_ciclo,valormin_por_ciclo,sumas_obj_por_ciclo,cant_individuos,generaciones)
   

main()

