from igraph import *

#this function generate a Matriz with the shortest paths between the nodes
#the matrix that will be made help us to know a lot of indices, for example
#vulnerability, global efficiency, straightness centrality
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

#this function make some calculations to get a matrix and define the efficiency 
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

#this function generate another Graph equals the basic one to delete the node in
#question to make some calculations to discover how eficient is the node
#and what happens if it is not there
def eficienciaVertice(g, n):
    gr = Graph()
    gr.add_vertices(g.vcount()-1)
    gr.add_edges(g.get_edgelist())
    gr.delete_vertices(n)
    return calculosEficiencia(matrizMenorCaminho(gr), g)

#this function makes exactly what the previous one but where the nodes do not
#connect the value 0 is replaced by a value not possible. one more the number of
#nodes
def eficienciaVerticeComMax(g, n):
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
                matriz[i][j]=g.vcount()
            j+=1
        i+=1
    return calculosEficiencia(matriz, g)

#this function make the vulnerability calculation with the node efficiency and
#the global efficiency
def vulnerabilidade(ef, efg):
    return (efg-ef)/efg


###### read graph from a file #######

#now, to the program not to be static, this part of the code is to read from a
#file the edgelist. With this list we can generate a Graph.

def strtoint(x):
    lista = []
    for i in x:
        lista.append((int(i[0]), int(i[1])))
    return lista


arquivo = open('karate.txt','r')

valores = []
teste=[]

for linha in arquivo:
    x=linha.replace('\n', '').split(' ')
    teste.append(int(x[0]))
    teste.append(int(x[1]))
    valores.append((x[0], x[1]))

valor = (max(teste))

#####################################

#All the results will be writen in a file.
file = open("valores.txt", "w")

g = Graph()
g.add_vertices(valor)
print(len(valores))
g.add_edges(strtoint(valores))



s=''

s+=(str(summary(g)))

s+=('\nNumber of Nodes:'+str(len(g.degree())))

s+=('\nNumber of Edge:'+str(len(g.get_edgelist())))

s+=('\nDiameter:'+str(g.diameter()))

s+=('\nEdge List:'+str(g.get_edgelist()))

s+=('\nDegree: '+str(g.degree()))

s+=('\nAverage path lenght:'+str(g.average_path_length()))

s+=('\nBetweenness: '+str(g.betweenness()))

s+=('\nEdge Betweenness: '+str(g.edge_betweenness()))

s+=('\nAdjacency Matrix:\n'+str(g.get_adjacency()))

efg=eficienciaGlobal(g)
s+=('\Global Eficiency:'+str(efg))


i=0
n=len(g.degree())
while i<n:
    s+=('\n\nNode ' + str(i) +':')
    s+=('\nEficiencia: '+ str(eficienciaVertice(g, i)))
    s+=('\nVulnerabilidade: ' + str(vulnerabilidade(eficienciaVertice(g, i), efg)))
    s+=('\nEficiencia com 5: '+ str(eficienciaVerticeComMax(g, i)))
    s+=('\nVulnerabilidade com 5: ' + str(vulnerabilidade(eficienciaVerticeComMax(g, i), efg)))
    
    i+=1

print s

file.write(s)
file.close()
