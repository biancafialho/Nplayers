from itertools import product
from scipy.optimize import least_squares
import numpy as np
import Gerador_Nplayers as ger


##@file funcoes.py
#@brief Implementação do Feasibility Problem para encontrar o melhor suporte em jogos de n jogadores.
#
#@details
# Reproduz o Feasibility Problem de Porter et al (2008) para encontrar o melhor suporte em jogos de n jogadores através do
# método de Mínimos quadrados.
#@b Referência: Porter, R.; Nudelman, E.; Shoham, Y. Simple search methods for finding a Nash equilibrium. @a Games @a and @a Economic @a Behavior, 63, 642-662, 2008.
#@date 07/07/2018
#@author Thiago Augusto de Oliveira Silva e Bianca Fialho da Silva
#
##@b arrayToListOfList
#@brief Verifica a existência de ações condicionalmente dominadas para um jogador dado um suporte do oponente de acordo com a Definição 2
#de Porter et al (2008).
#
#@details
# Definição 2 (Porter et al (2008)) - Uma ação @f$ a_i \in S @f$ é dita condicionalmente dominada dado um conjunto de ações @f$ A^{'}_{-i} @f$
# se a seguinte condição é satisfeita:
# @f$ \exists a^{'}_i \in S, \forall a_{-i} \in A^{'}_{-i}: u_i(a_i,a_{-i}) <u_i(a^{'}_i,a_{-i}) @f$
#@param listofActions
#@param my_array
#@param payoff matriz de payoff indexada como payoff[id_açao_jogador1][id_acao_jogador2][id_jogador]
#@param idj variavel boleana que recebe zero quando as acoes do jogador 1 e 1 quando as acoes do jogador 2
#@retval Lista de listas .

'''''
utilidade = [[[[0.42, 0.37], [0.34, 0.60]], [[0.40, 0.34], [0.24, 0.42]]],
             [[[0.24, 0.23], [0.40, 0.18]], [[0.26, 0.40], [0.18, 0.24]]],
             [[[0.34, 0.40], [0.26, 0.22]], [[0.34, 0.26], [0.60, 0.34]]]]
'''''

def arrayToListOfList(listofActions,my_array):
    k=0
    LOL = []
    tamanholistofActions= len(listofActions)
#    for u in range(tamanholistofActions):
#        if (listofActions[u]==[]):
#            tamanholistofActions = tamanholistofActions-1
    inotvaz = 0
    k=0
    for i in range(tamanholistofActions):
        if (listofActions[i]!=[]):
            LOL.append([])

            for j in range(len(listofActions[i])):
                LOL[inotvaz].append(my_array[k])
                k = k+1
            inotvaz = inotvaz+1

    return LOL

def splitVar(x, listofSupport, listNotSupport,nPlayers,nActions,nActionsSup,nActionsNotSup):
    listaP = x[0:nActionsSup]
    listaV = x[nActionsSup: (nActionsSup + nPlayers)]
    listaF = x[nActionsSup+nPlayers:(nActionsSup+nPlayers+nActionsNotSup)]

    listaP = arrayToListOfList(listofSupport, listaP)
    listaF = arrayToListOfList(listNotSupport, listaF)


    return [listaP,listaV,listaF]

def gera_utilidade2(jogador,acao, listaAopp,lista_par, Acoes):
    #lista_par =[lista_perf,media,desv,VendasTotais,Orc,Gamma]
    densPerf = ger.densidade(lista_par[0],lista_par[1],lista_par[2],lista_par[3])
    n = len(listaAopp)
    port = []
    for j in range(n):
        if j == jogador:
            port.append(Acoes[jogador][acao])
        else:
            if j < jogador:
                port.append(Acoes[j][listaAopp[j]])
            else:
                port.append(Acoes[j][listaAopp[j-1]])

    payoff = ger.calc_Payoff(port,lista_par[0],densPerf,lista_par[2],lista_par[3])
    return payoff[jogador]

'''''
def gera_utilidade(jogador,acao, listaAopp, Utilidade): #retorna o payoff do jogador fixo a partir das ações dos demais jogadores

    n = len(Utilidade)
    payoff= Utilidade[jogador]
    for i in range(n):
        if i == jogador:
            payoff = payoff[acao]
        else:
            if i < jogador:
                payoff = payoff[listaAopp[i]]
            else:
                payoff = payoff[listaAopp[i-1]]

    return payoff
'''''

def probabilidade_acao(ListaP, jogador,acoes_oponentes, ListaSup):
    mult_prob = 1
    ListaP2 = ListaP[0:jogador] + ListaP[(jogador+1):len(ListaP)] #Listas de probabilidades dos oponentes

    for e in range(len(ListaP2)):
            mult_prob = mult_prob * ListaP2[e][ListaSup[e].index(acoes_oponentes[e])]/100

    return mult_prob


def somatorio_c10(ListaSup, jogador,acao_jogador, ListaP, lista_par, Acoes):
    soma = 0
    ListaSup2 = ListaSup[0:jogador]+ListaSup[(jogador+1):len(ListaSup)] #Lista de Suporte de ações dos oponentes
    combSuport =[list(tup) for tup in product(*ListaSup2)] #Lista de combinações entre as ações dos oponentes
    #for e in combSuport:
    soma=soma+probabilidade_acao(ListaP, jogador,e,ListaSup2)*gera_utilidade2(jogador,acao_jogador,combSuport,lista_par, Acoes)

    return soma


def c11(jogador, acao_jogador, ListaSup, ListaP, ListaV, lista_par, Acoes):

    result_sub = ListaV[jogador] - somatorio_c10(ListaSup, jogador, acao_jogador, ListaP, lista_par, Acoes)

    return result_sub


def c1(numero_jogadores, ListaSup, ListaP, ListaV, lista_par, Acoes):

    arrayC1 = []
    for i in range(numero_jogadores):
        for a in ListaSup[i]:
            arrayC1.append(c11(i, a, ListaSup, ListaP, ListaV,lista_par, Acoes))

    return arrayC1

def c21(ListaP, jogador):
    e = jogador
    soma_prob = 0
    for a in range(len(ListaP[e])):
        soma_prob = soma_prob + ListaP[e][a]
    return soma_prob

def c2(ListaP):
    arrayC2 = []
    for j in range(len(ListaP)):
        c21v = c21(ListaP, j)
        sub = 100 - c21v
        arrayC2.append(sub)

    return arrayC2


def c3(ListaP,ListaV,Folgas, ListaSup, ListaNotSup, lista_par, Acoes):
    arrayC3 = []
    jfolga =0
    for j in range(len(ListaP)):
        if (ListaNotSup[j]!= []):
           for a in range(len(ListaNotSup[j])):
                print("ListaSup", ListaSup)
                print("ListaNotSup", ListaNotSup)
                result_sub = ListaV[j] - Folgas[jfolga][a] - somatorio_c10(ListaSup, j, ListaNotSup[j][a], ListaP, lista_par, Acoes)
                arrayC3.append(result_sub)
           jfolga = jfolga + 1
    return arrayC3

jogadores = [0, 1, 2]

acoes =[[0, 1], [0, 1], [0, 1]]


prob_acao = [[0.25, 0.75], [0.40, 0.60], [0.80, 0.20]]

def fun_FeasibilityProblem(x0,arg1,arg2,arg3,arg4,arg5):
    # assume que a lista de ações e a lista de suporte possuem o mesmo número de listas (= nplayers)
    nPlayers = arg1
    listofActions = arg2
    listofSupport = arg3
    Acoes_det = arg4
    lista_par = arg5
    nActions = 0
    nActionsSup = 0
    nActionsNotSup = 0
    listNotSupport = []

    for i in range(nPlayers):
        nActions = nActions + len(listofActions[i])
        nActionsSup = nActionsSup + len(listofSupport[i])
        listNotSupport.append(list(set(listofActions[i]) - set(listofSupport[i])))
    nActionsNotSup = nActions - nActionsSup


    [listaP,listaV,listaF] = splitVar(x0, listofSupport, listNotSupport,nPlayers,nActions,nActionsSup,nActionsNotSup)
    r1 = c1(nPlayers, listofSupport, listaP, listaV, lista_par, Acoes_det)

    r2 =c2(listaP)

    r3 = c3(listaP,listaV,listaF, listofSupport, listNotSupport, lista_par, Acoes_det)

    return np.array(r1+r2+r3)

def FeasibilityProblem1(listofActions,listofSupport,Acoes_det,lista_par):

    n = len(listofActions)
    x0 = []
    lb = []
    ub = []
    for i in range(n):
        for j in range(len(listofSupport[i])):
            x0.append(0.0)
            lb.append(0.0)
            ub.append(100.0)
    listNotSupport = []
    for i in range(n):
        listNotSupport.append(list(set(listofActions[i]) - set(listofSupport[i])))
        x0.append(0.0)
        lb.append(-np.inf)
        ub.append(np.inf)
    for i in range(n):
        for j in range(len(listNotSupport[i])):
            x0.append(0.0)
            lb.append(0.0)
            ub.append(np.inf)

    res_1 = least_squares(fun_FeasibilityProblem, x0, args=[n, listofActions, listofSupport,Acoes_det,lista_par], bounds=(lb, ub), verbose=2,ftol=1e-15,xtol=1e-32,gtol=1e-20)
    success = (res_1.cost <=1e-05)and(res_1.cost>=-1e-05)
    print("success:",success)
    print("opt:",res_1.cost)
    return [list(res_1.x),success]


