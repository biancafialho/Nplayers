import Feasibility_Program as fp
from itertools import product

def VerificaDominacao(i,a,al,listofUnion,fun_payoff,utilidade):
    soma = 0
    ListaSup2 = listofUnion[0:i]+listofUnion[(i+1):len(listofUnion)] #Lista de Suporte de ações dos oponentes
    combSuport =[list(tup) for tup in product(*ListaSup2)] #Lista de combinações entre as ações dos oponentes
    dominada = True
    for e in combSuport:
        print("combSuport", combSuport)
        print("List Aopp:",e)
        payoff1 = fun_payoff(i,a,e,utilidade)
        print("Payoff1:",payoff1 )
        payoff2 = fun_payoff(i,al,e,utilidade)
        print("Payoff2:", payoff2)
        if (payoff1>= payoff2):
            print("IF-VerificaDominacao")
            dominada = False
            break

    return dominada


def RetiraDominadosCondicionalmente(j,D):

    for di in D:
        if j in di:
            D.remove(di)
    return D


def IRSDS(D,A):
    print("IRSDS - D:", D)
    changed = None

    listUnion = []
    for i in range(len(D)):
        print("Jogador :",i)
        uniond = set()
        print("D[i]:",D[i])
        for d in D[i]:
            uniond = set(uniond).union(d)
        listUnion.append(list(uniond))
    print("listUnion",listUnion)

    changed = True
    while changed:
        changed = False
        for i in range(len(D)):
            print("############### Jogador :", i)
            print("List of Union i :", listUnion[i])

            for a in listUnion[i]:
                print("a:", a)
                Alal = [a2 for a2 in A[i] if a2!=a]
                print("Alal:",Alal)
                for al in Alal:
                    f = VerificaDominacao(i, a, al, listUnion, fp.gera_utilidade, fp.utilidade)
                    print("FFFFFFFFFF",f)
                    if(f):
                        print("D[i]:", D[i])
                        D[i]= RetiraDominadosCondicionalmente(a, D[i])
                        print("D[i]:", D[i])
                        changed = True
                        print("CHANGED")
                        listUnion[i].remove(a)
                        if len(D[i]) ==0:
                            return None

    return D



