from igraph import *

def matrizMenorCaminho(g):
    i=0
    matriz=[]
    while i<len(g.degree()):
        j=0
        temp=[]
        while j<len(g.get_all_shortest_paths(i)):
            temp.append(len(g.get_all_shortest_paths(i)[j])-1)
            j+=1
        matriz.append(temp)
        i+=1
    return matriz

def eficienciaGlobal(g):
    return calculosEficiencia(matrizMenorCaminho(g), g)

def calculosEficiencia(matriz, g):
    i=0
    x=0.0
    while i<len(matriz):
        j=0
        while j<len(matriz[i]):
            if matriz[i][j]!=0 and i<=j:
                x+=1.0/matriz[i][j]
            j+=1
        i+=1
    return x/(g.vcount()*(g.vcount()-1))

def eficienciaVertice(g, n):
    gr = Graph()
    gr.add_vertices(g.vcount()-1)
    gr.add_edges(g.get_edgelist())
    gr.delete_vertices(n)
    return calculosEficiencia(matrizMenorCaminho(gr), g)


def eficienciaVerticeCom5(g, n):
    gr = Graph()
    gr.add_vertices(g.vcount()-1)
    gr.add_edges(g.get_edgelist())
    gr.delete_vertices(n)
    matriz = matrizMenorCaminho(gr)
    i=0
    while i<len(matriz):
        j=0
        while j<len(matriz[i]):
            if matriz[i][j]==0 and i!=j:
                matriz[i][j]=5
            j+=1
        i+=1
    return calculosEficiencia(matriz, g)

def vulnerabilidade(ef, efg):
    return (efg-ef)/efg
    

####### ler grafo do arquivo ########

def strtoint(x):
    lista = []
    for i in x:
        lista.append((int(i[0]), int(i[1])))
    return lista


arquivo = open('karate.txt','r')

valores = []

for linha in arquivo:
    x=linha.replace('\n', '').split(' ')
    valores.append((x[0], x[1]))

#####################################

g = Graph()
g.add_vertices(len(valores)-1)
g.add_edges(strtoint(valores))


print(summary(g))

print('\nNúmero de Vértices:')
print(len(g.degree()))

print('\nNumero de arestas:')
print(len(g.get_edgelist()))

print('\nDiâmetro:')
print(g.diameter())

print('\nLista de arestas:')
print(g.get_edgelist())

print('\nGraus: ')
print(g.degree())

print('\nMinimo Caminho Médio:')
print(g.average_path_length())

print('\nBetweenness: ')
print(g.betweenness())

print('\nMatriz de adjacência:')
print(g.get_adjacency())

print('\nEficiencia Global:')
print(eficienciaGlobal(g))

i=0
n=len(g.degree())
while i<n:
    print('\nVértice ' + str(i) +':')
    print('Eficiencia: '+ str(eficienciaVertice(g, i)))
    print('Vulnerabilidade: ' + str(vulnerabilidade(eficienciaVertice(g, i), eficienciaGlobal(g))))
    print('Eficiencia com 5: '+ str(eficienciaVerticeCom5(g, i)))
    print('Vulnerabilidade com 5: ' + str(vulnerabilidade(eficienciaVerticeCom5(g, i), eficienciaGlobal(g))))
    i+=1


