import IRSDS
import Feasibility_Program


def Recursive_Backtraking(S, D, i, listofActions, Acoes_det, lista_par):
    n = len(D)
    #print("RB D", D)
    #print("RB len(D)", len(D))
    #print("print 0 RB S", S)

    if i > n:
        #print("i>n!!")
        #S_action = [l[0] for l in S]
        res = Feasibility_Program.FeasibilityProblem1(listofActions, S, Acoes_det, lista_par)
        if res[1]:
            return [res[0], S]
        else:
            #print("resultado NONE")
            return None
    else:
        newD = []
        Di = D[i - 1]
        for s in Di:
            S2 = [s1 for s1 in S]
            #print("print1 RB for S2", S2)

            #print("RB for i", i)
            #print("RB for s", s)
            #print("RB for S", S)
            #print("RB for S2", S2)
            S2.append(s)
            #print("print 2 RB for S2", S2)
            Di.remove(s)
            newS = [[si] for si in S2]
            newD = D[i:n]

            #print("newS", newS)
            #print("RB newD", newD)
            #print("RB len(newD)", len(newD))
            newD2 = newS + newD
            Dr = IRSDS.IRSDS(newD2, listofActions, Acoes_det, lista_par)

            #print("RB Dr", Dr)
            if (Dr is not None):
                #print("Dr is not none")
                #print("RB len(Dr)", len(Dr))
                resp = Recursive_Backtraking(S2, Dr, i + 1, listofActions, Acoes_det, lista_par)
                if (resp is not None):
                    #print("resp", resp)
                    return resp

    return None




