def subtract_function(x, y, b, m=None):
    base = {'0':0,'1':1,'2':2,'3':3,
            '4':4,'5':5,'6':6,'7':7,
            '8':8,'9':9,'a':10,'b':11,
            'c':12,'d':13,'e':14,'f':15}
    X = str(x)
    Y = str(y)
    carry = 0
    dig = 0
    maxL = max(len(X), len(Y))
    X = X.zfill(maxL)
    Y = Y.zfill(maxL)
    X2 = list(X)
    Y2 = list(Y)

    # maka sure the modulo has the same length as x and y
    if m is not None:
        m = m.zfill(maxL)

    result = []

    if x == 0 and m is None:
        return -int(y)
    if y == 0 and m is None:
        return x
    if b == 10:
        if m is None:
            return str(int(x) - int(y))
        else:
            return (int(x) - int(y)) % int(m)
    if x == y:
        return '0'

    # deal with negative numbers
    if X[0] == '-' and Y[0] == '-':
        Y = Y.replace('-','')
        return add_function(Y,X,b,m)
    if X[0] == '-':
        Y = '-' + Y
        return add_function(X,Y,b,m)
    if Y[0] == '-':
        Y = Y.replace('-','')
        return add_function(X,Y,b,m)

    if x > y:
        # convert abcdef into integers
        for i in range(maxL):
            X2[i] = base.get(X2[i])
            Y2[i] = base.get(Y2[i])

        for i in range(1,maxL+1):
            if X2[-i] >= Y2[-i]:
                dig = X2[-i] - Y2[-i]

            if X2[-i] < Y2[-i]: #take a borrow
                X2[-i-1] -= 1
                X2[-i] += b
                dig = X2[-i] - Y2[-i]
            result.append(dig)

        for i in range(maxL):
            invMap = {v: k for k, v in base.items()}
            # remap the dictionary such that integers >= 10
            # are converted to alphabet
            result[i] = invMap.get(result[i])

        if X2 > Y2:
            answer = ''.join(result[::-1])

            if m is not None:
                answer = simple_division(answer, m, b)

            if answer[0] is "0": answer = answer[1:]
            return answer
        else:
            result = subtract_function(y,x,b,m)


    if x < y:
        return '-' + subtract_function(y,x,b,m)
