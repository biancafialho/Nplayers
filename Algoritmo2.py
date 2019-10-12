from itertools import product
from itertools import combinations
import Recursive_Backtracking

##@file Algoritmo2.py
#@brief Algoritmo para encontrar um equilíbrio em jogos com n jogadores.
#
#@details
# Reproduz o Algoritmo 2 de Porter et al (2008) para encontrar ao menos um equilíbrio de Nash para jogos com n jogadores.
#
#@b Referência: Porter, R.; Nudelman, E.; Shoham, Y. Simple search methods for finding a Nash equilibrium. @a Games @a and @a Economic @a Behavior, 63, 642-662, 2008.
#@date 07/07/2018
#@author Thiago Augusto de Oliveira Silva e Bianca Fialho da Silva
#


#Acoes= [[0,1,2], [0,1,2,3], [0,1]] #Lista contendo as listas de ações de cada jogador.
listofActions = [[0, 1], [0, 1], [0, 1]]
listofSupport = [[1], [0], [0, 1]]
##@b tamanho_suportes_somatorio
#@brief Função auxiliar do Algoritmo 2 de Porter et al (2008), de acordo com o primeiro critério de ordenação.
#
#@details
# Primeiro Critério de Ordenação - realiza a soma dos tamanhos das listas de ações de cada jogador, contabilizando o tamanho do suporte.
# O somatório é definido como:
# @f$ \sum {i}{x_i}@f$
#@param suporte é uma lista com o tamanho do suporte de cada jogador.
#@retval Tamanho de cada suporte gerado através da soma do tamanho do suporte dos jogadores.

def tamanho_suportes_somatorio(suporte):

    soma=0
    for i in range(len(suporte)):
        soma = soma + suporte[i]

    return (soma)
##@b tamanho_max
#@brief Função auxiliar do Algoritmo 2 de Porter et al (2008), de acordo com o segundo critério de ordenação.
#
#@details
# Segundo Critério de Ordenação - caso haja igualdade entre o tamanho de suportes, realiza-se a diferença entre o tamanho das listas de ações de cada jogador
# dos respectivos suportes, retornado o maior valor.
# A difença é definida como:
# @f$ \max_{x_{i,j}} (x_i- x_j)@f$
#@param suporte é uma lista com o tamanho do suporte de cada jogador.
#@retval Maior valor entre a diferença dos tamanhos das listas de ações de cada suporte.

def tamanho_max(suporte):
    tam = len(suporte) - 1
    k=1
    lista_max = []
    for i in range(tam):
        for j in range(k,tam+1):
            sub = suporte[i]-suporte[j]
            lista_max.append(sub)
        k = k + 1
    valor_max = max(lista_max)
    return(valor_max)

##@b algoritmo2
#@brief Algoritmo 2 proposto por  Porter et al (2008) para encontrar um equilíbrio um jogo de n jogadores.
#
#@details
# Procura equilíbrio de Nash em um jogo de dois jogadores fazendo uma busca a partir de suporte contidos no conjunto de Ações de cada jogador.
# Inicialmente gera perfis de suporte (tamanho) os combina de forma a selecionar os menores suporte primeiro.
#@param Acoes lista de ações dos jogadores.

#@retval p (completar!)
def algoritmo2 (Acoes):
    tamanhos = [len(a) for a in Acoes] #Cria uma lista com os tamanhos de cada lista de suporte dos jogadores

    tamanhos_possíveis = [list(range(1,t+1)) for t in tamanhos] #Cria uma lista com todos os tamanhos de suporte possiveis para cada jogador
    #print(tamanhos_possíveis)
    tamanhos_suportes = [list(tup) for tup in product(*tamanhos_possíveis)] #Cria uma lista com todas as combinacoes possiveis para os tamanhos de suporte dos jogadores
    #print(tamanhos_suportes)
    x=[]
    for a in tamanhos_suportes:
        x.append([a, tamanho_suportes_somatorio(a), tamanho_max(a)])
        #print(x)
    y = sorted(x, key=lambda x: (x[1],x[2])) #Ordena a lista de tamanhos de suportes em ordem crescente, primeiro pelo critáerio do somatório e segundo pelo máximo valor
    z = [i[0] for i in y] #Cria uma lista com as listas de tamanhos de suporte ordenadas

    print("Z",z)

    S =[]

    for zid in z: #Gera todas as combinações possíveis de tamanhos de suporte de acordo com os tamanhos da lista ordenada
        S=[]
        print("zid", zid)
        D = []
        listaD=[]
        for i in range(len(zid)):
            Di =[list(tup) for tup in list(combinations(Acoes[i],zid[i]))]
            D.append(Di)
        print("DDD", D)
        res = Recursive_Backtracking.Recursive_Backtraking(S,D,1,Acoes)
        print("Algoritmo 2 - res",res)
        if res is not None:
            print("NASH - Support", res[1])
            print("NASH - zid",zid)
            return res[0]

    print("Fim do Algoritmo sem equilíbrio")
    return None



resf = algoritmo2(listofActions)
print("Final",resf)

