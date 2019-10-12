import IRSDS
import Feasibility_Program

def Recursive_Backtraking(S,D,i,listofActions):
    n = len(D)
    print("RB D", D)

    if i > n:
        print("i>n!!")
        res = Feasibility_Program.FeasibilityProblem1(listofActions, S)
        print("resultado",res)
        if res[1]:
            return [res[0],S]
        else:
            print("resultado NONE")
            return None
    else:
        newD =[]
        Di = D[i-1]
        for s in Di:
            S.append(s)
            Di.remove(s)
            newD = [[si] for si in S ]

            for j in range(i, len(D)):
                newD.append(D[j])
            print("lista S", S)
            D = IRSDS.IRSDS(newD,listofActions)
            if (D is not None):
                resp = Recursive_Backtraking(S, D, i+1, listofActions)
                if (resp is not None):
                    print("resp",resp)
                    return resp

    return None




