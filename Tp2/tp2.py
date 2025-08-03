def exhaustivo(objetos,maximo):
    conjuntos = []
    for i in range(0,(1<<len(objetos))):
        flag = True
        actual = 0
        suma = 0
        for j in range(0,len(objetos)):
            if ((i&(1<<j))>0):
                if (actual+objetos[j][0]<=maximo):
                    actual = actual + objetos[j][0]
                    suma = suma + objetos[j][1]
                else:
                    flag = False
        if (flag):
            s = format(i,'b')
            s = s.zfill(len(objetos))
            conjuntos.append([suma,s[::-1]])
    conjuntos = sorted(conjuntos)
    tam = len(conjuntos)-1
    i = tam
    print("Resultado Exhaustivo")
    print(f"Los mejores conjuntos tienen valor {conjuntos[tam][0]} y son: ")
    while(i>=0 and conjuntos[i][0] == conjuntos[tam][0]):
        print(conjuntos[i][1])
        i = i-1


def greedy(objetos,maximo):
    aportes = []
    idx = 0
    for obj in objetos:
        aportes.append([obj[1]/obj[0],obj[1],obj[0],idx])
        idx = idx + 1
    aportes = sorted(aportes,reverse=True)
    peso = 0
    suma = 0
    conjunto = 0
    for obj in aportes:
        if (obj[2]+peso <= maximo):
            peso = peso + obj[2]
            suma = suma + obj[1]
            conjunto = conjunto + (1<<obj[3])
    s = format(conjunto,'b')
    s = s[::-1]
    print(f"Resultado Greedy -> Conjunto: {s} con suma {suma}")
        
    

if __name__ == "__main__":
    objetos = [[150,20],[325,40],[600,50],[805,36],[430,25],[1200,64],[770,54],[60,18],[930,46],[353,28]]
    exhaustivo(objetos,4200)
    greedy(objetos,4200)
    objetos = [[1800,72],[600,36],[1200,60]]
    exhaustivo(objetos,3000)
    greedy(objetos,3000)
