from itertools import permutations
from itertools import combinations
import numpy.random as rd
from math import sqrt
from scipy.stats import norm

def todasComb(tamMax,Perf):
#define todas as possíveis combinações de estratégias
#entrada: lista de Performances, tamMax -> número máximo de produtos
#retorna todas as possíveis combinações de performances para os produtos da empresa até o tamanho tamMax de produtos

	subPerf =[]
	for i in range(1,tamMax+1):
		for p in combinations(Perf,i):
			plist = list(p)
			subPerf.append(plist)
	return subPerf

def RecGeraPort(Perf,Preco,Custo):
#define subfunção recursiva para definir portfólio da empresa (lista de performances e preços)
#entrada: lista de Performances, lista de preços
#retorna todas as possíveis combinações de portfólios para uma empresa
	if len(Preco)>0:
		if len(Perf) == 1:
			lista = [[(Perf[0],y,Custo[0])] for y in Preco]
		else:
			lista = []
			for i in Preco:
				novoPreco = Preco[Preco.index(i)+1:]
				novaPerf = Perf[1:]
				novoCusto = Custo[1:]
				sublista = RecGeraPort(novaPerf,novoPreco,novoCusto)
				tupla = [(Perf[0],i,Custo[0])]
				for s in sublista:
					lista.append(tupla+s)
		return lista
	else:
		return []

def GeraPort(listPerf,Preco,listCusto):
#define o portfólio da empresa (lista de performances e preços)
#entrada: lista de Performances, lista de preços
#retorna todas as possíveis combinações de portfólios para uma empresa
	Portfolio=[]
	for l in range(len(listPerf)):
		subPort = RecGeraPort(listPerf[l],Preco,listCusto[l])
		for s in subPort:
			Portfolio.append(s)
	return Portfolio
