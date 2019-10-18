# -*- coding: utf-8 -*-
from itertools import permutations
from itertools import combinations
import numpy.random as rd
from math import sqrt
from scipy.stats import norm


def todasComb(tamMax, Perf):
    # define todas as possíveis combinações de estratégias
    # entrada: lista de Performances, tamMax -> número máximo de produtos
    # retorna todas as possíveis combinações de performances para os produtos da empresa até o tamanho tamMax de produtos

    subPerf = []
    for i in range(1, tamMax + 1):
        for p in combinations(Perf, i):
            plist = list(p)
            subPerf.append(plist)
    return subPerf


def RecGeraPort(Perf, Preco, Custo):
    # define subfunção recursiva para definir portfólio da empresa (lista de performances e preços)
    # entrada: lista de Performances, lista de preços
    # retorna todas as possíveis combinações de portfólios para uma empresa
    if len(Preco) > 0:
        if len(Perf) == 1:
            lista = [[(Perf[0], y, Custo[0])] for y in Preco]
        else:
            lista = []
            for i in Preco:
                novoPreco = Preco[Preco.index(i) + 1:]
                novaPerf = Perf[1:]
                novoCusto = Custo[1:]
                sublista = RecGeraPort(novaPerf, novoPreco, novoCusto)
                tupla = [(Perf[0], i, Custo[0])]
                for s in sublista:
                    lista.append(tupla + s)
        return lista
    else:
        return []


def GeraPort(listPerf, Preco, listCusto):
    # define o portfólio da empresa (lista de performances e preços)
    # entrada: lista de Performances, lista de preços
    # retorna todas as possíveis combinações de portfólios para uma empresa
    Portfolio = []
    for l in range(len(listPerf)):
        subPort = RecGeraPort(listPerf[l], Preco, listCusto[l])
        for s in subPort:
            Portfolio.append(s)
    return Portfolio


def distProdPerf(prodPerf, perf):
    # dado a performance de um produto (k), calcula a distância para um ponto de performance (v) do consumidor
    # entrada: vetor de performances do produto, vetor de preferências de performances do cliente
    # retorna d(k,v)
    dtotal = 0
    for i in range(len(prodPerf)):
        d = max(0, perf[i] - prodPerf[i])
        dtotal = dtotal + d ** 2
    return sqrt(dtotal)


def nivelAdq(prodPerf, perf):
    # dado a performance de um produto (k), calcula o nível de adequação um ponto de performance (v) do consumidor
    # entrada: vetor de performances do produto, vetor de preferências de performances do cliente
    # retorna na(k,v)
    return 1 / (distProdPerf(prodPerf, perf) + 1)


def calcFatias(perf, listaProd, Orc, gamma):
    # Calcula o A(k,v)(p_k) e retorna uma lista com este valor para todos os produtos
    # entrada: listaprodutos no formato [[produtos da empresa 1,produtos da empresa 1, todos os produtos] para todas as possibilidades], vetor de preferências de performances do cliente
    # entrada nova: Orc - orçamento do consumidor, gamma -  parâmetro
    # retorna A(k,v)(p_k)
    ########## ESSA FUNÇÃO DEVE SER ALTERADA
    na = [nivelAdq([i[0]], [perf]) for i in listaProd]
    listaCB = [na[i] + gamma * (Orc - j[1]) for i, j in enumerate(listaProd)]  # alterado
    fatia = [i / sum(listaCB) for i in listaCB]
    return fatia


def calcVendas(listaPerf, densPerf, listaProd, Orc, gamma):
    # Calcula o Delta_k(p_k) e retorna uma lista com este valor para todos os produtos
    # NÃO hÁ NECESSIDADE DE ALTERAR
    fatias = [calcFatias(p, listaProd, Orc, gamma) for p in listaPerf]
    vendas = []
    for prod in range(len(listaProd)):
        venda = 0
        for p in range(len(listaPerf)):
            venda = venda + fatias[p][prod] * densPerf[p]
        vendas.append(venda)
    return vendas


def calcFat(precos, vendas):
    # Calcula o Gamma(p) e retorna um valor do faturamento total
    # NÃO hÁ NECESSIDADE DE ALTERAR
    fat = 0
    for p in range(len(precos)):
        fat = fat + precos[p] * vendas[p]
    return fat


def calcCusto(custos, vendas):
    # Calcula o a segunda parte da expressão (7 - Li(p)) e retorna o valor
    # deveremos entrar com uma lista de custos de cada produto
    custo = 0
    for p in range(len(custos)):
        custo = custo + custos[p] * (vendas[p] ** 2)
    return custo


def calcLuc(precos, vendas, custos):
    # Calcula o Li(p) e retorna uma lista com este valor para todos os produtos
    custo = calcCusto(custos, vendas)
    fat = calcFat(precos, vendas)
    lucro = fat - custo
    return lucro


def Payoff(Estrat, listaperf, dens, Orc, gamma):
    # Calcula o o payoff para cada empresa e retorna uma lista de payoffs para cada ação
    # já alterada
    pay = []
    for s in Estrat:
        p1 = s[0]
        p2 = s[1]
        lp = s[2]
        vendas = calcVendas(listaperf, dens, lp, Orc, gamma)
        vp1 = vendas[0:len(p1)]
        vp2 = vendas[len(p1):]
        pp1 = [ip1[1] for ip1 in p1]
        pp2 = [ip2[1] for ip2 in p2]
        cp1 = [ip1[2] for ip1 in p1]
        cp2 = [ip2[2] for ip2 in p2]
        f1 = calcLuc(pp1, vp1, cp1)
        f2 = calcLuc(pp2, vp2, cp2)
        pay.append((f1, f2))
    return pay


def densidade(perfs, media, desv, total):
    mx = max(perfs)
    mn = min(perfs)
    step = (mx - mn) / (len(perfs) - 1)
    ant = 0
    dens = []
    for i in range(len(perfs)):
        if i == len(perfs) - 1:
            cdf = 1
        else:
            ls = perfs[i] + step / 2
            ls = (ls - media) / desv
            cdf = norm.cdf(ls)
        d = cdf - ant
        dens.append(d * total)
        ant = cdf
    return dens


def define_acoes(lista_jogadores, lista_par_custo, lista_perf, lista_preco):
    Portfolio = []
    subperf = todasComb(3, lista_perf)
    for j in range(len(lista_jogadores)):
        custo_jog = [round(
            float((lista_par_custo[j][0] + i / lista_par_custo[j][1]) * lista_par_custo[j][2] + lista_par_custo[j][3]) /
            lista_par_custo[j][4], 3) for i in range(len(lista_perf))]
        subcusto = todasComb(3, custo_jog)
        Portfolio.append(GeraPort(subperf, lista_preco, subcusto))
    return Portfolio


def calc_Payoff(lista_port, listaperf, dens, Orc, gamma):
    # Calcula o o payoff para cada empresa e retorna uma lista de payoffs para cada ação
    # já alterada
    pay = []
    lp = []
    for j in lista_port:
        lp = lp + j

    print
    "lp: {}".format(lp)
    vendas = calcVendas(listaperf, dens, lp, Orc, gamma)
    print("vendas: {}".format(vendas))
    tamanho = [len(j) for j in lista_port]
    print ("tamanho: {}".format(tamanho))
    vp = []
    inicio = 0
    for j in range(len(lista_port)):
        fim = inicio + tamanho[j]
        vj = vendas[inicio:fim]
        inicio = fim
        print("vj: {}".format(vj))
        pj = [ip[1] for ip in lista_port[j]]
        print("pj: {}".format(pj))
        cpj = [ip[2] for ip in lista_port[j]]
        print("cpj: {}".format(cpj))
        fj = calcLuc(pj, vj, cpj)
        print("fj: {}".format(fj))
        pay.append(fj)

    return pay



def fun_main():
    Orc = 120
    gamma = 0.025
    media = 4.0
    desv = 1.0

    portIVECO = [(4.0, 90, custoIv1), (5.5, 105, custoIv2)]  # com custos
    portMB = [(3.5, 90, custoMb1), (4.0, 95, custoMb2), (5.0, 100, custoMb3)]  # com custos
    Sit = [portIVECO, portMB, portIVECO + portMB]

    Portfolio = GeraPort(subPerf, Precos, [[0.0 for i in range(len(subPerf[j]))] for j in range(len(subPerf))])

    densPerf = densidade(Performances, media, desv, 2316)
    vendasSit = calcVendas(Performances, densPerf, Sit[2], Orc, gamma)

    calc_Payoff(port, Performances, densPerf, Orc, gamma)



if __name__ == '__main__':
    fun_main()

