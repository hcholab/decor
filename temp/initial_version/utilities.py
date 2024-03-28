import random

gl = 1


def printt(str, level):
    if level <= gl:
        print(str)


def getAllTermsFromFunc(f, d, maxVal=20):
    gg = 0
    while 1:
        gg += 1
        # print(gg)

        # TODO: we need to think about the sampling interval here
        x1 = random.random() * maxVal - maxVal / 2
        x2 = random.random() * maxVal - maxVal / 2

        # try:
        tp = f(x1 + x2)
        tm = f(x1 - x2)
        t1 = f(x1)
        t2 = f(x2)
        break
        # except OverflowError:
        #     print("Math range error: Result exceeds representable range.")

    # return getAllTerms(d, [tp, tm, t1, t2, math.sqrt(t1*t2), 1], ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "sqrt(f(x)*f(y))", "1"], "1")
    # return getAllTerms(d, [tp, tm, t1, t2, 1], ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"], "1")
    # allTermsP = getAllTerms(d, [tp, t1, t2, 1], ["f(x+y)", "f(x)", "f(y)", "1"], "1")
    allTermsM = getAllTerms(
        d, [tp, tm, t1, t2, 1], ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"], "1"
    )
    # allTermsM = getAllTerms(d, [tp, tm, t1, t2, 1], ["f(x+y)", "f(x-y)", "f(x)", "1"], "1")
    # return (allTermsP[0]+allTermsM[0],allTermsP[1]+allTermsM[1])
    return allTermsM
    # return getAllTerms(d, [tp, t1, t2, 1], ["f(x+y)", "f(x)", "f(y)", "1"], "1")


def getAllTermNames(d):
    return getAllTermsFromFunc(lambda x: x, d)[1]


def containsTerm(t, ct):
    return ct in t


def getAllTerms(d, var_list, name_list, o):
    # g: the concatenation function used below. Typically it's the concat method above.
    # d: the max degree of each term
    # l: the list of variables
    # n: the list of variable names
    # o: name of 1

    def sconcato(o):
        def sconcat(v):
            return lambda y: y if v == o else v + "*" + y

        return sconcat

    def concat(v):
        return lambda y: v * y

    if d == 1:
        return (var_list, name_list)
    else:
        if len(var_list) == 0:
            return (var_list, name_list)
        else:
            v = var_list[len(var_list) - 1]
            vname = name_list[len(name_list) - 1]
            out1 = list(map(concat(v), getAllTerms(d - 1, var_list, name_list, o)[0]))
            out1names = list(
                map(sconcato(o)(vname), getAllTerms(d - 1, var_list, name_list, o)[1])
            )
            out2 = []
            out2names = []
            lt = var_list[:]
            lt.pop()
            nt = name_list[:]
            nt.pop()
            (out3, out3names) = getAllTerms(d, lt, nt, o)

            return (out1 + out2 + out3, out1names + out2names + out3names)
