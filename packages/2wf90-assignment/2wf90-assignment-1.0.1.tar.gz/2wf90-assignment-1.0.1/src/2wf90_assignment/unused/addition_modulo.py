def add_function(x, y, b, m=None):
    base = {'0':0,'1':1,'2':2,'3':3,
        '4':4,'5':5,'6':6,'7':7,
        '8':8,'9':9,'a':10,'b':11,
        'c':12,'d':13,'e':14,'f':15}
    X = str(x)
    Y = str(y)
    carry = 0
    result = ''

    if x == '0' and m is None:
        return y

    if y == '0' and m is None:
        return x

    if y == '0' and x == '0':
        return '0'

    if b == 10:
        if m is None:
            return str(int(x)+int(y))
        else:
            return (int(x) + int(y)) % int(m)

    if X[0] == '-' and Y[0] == '-': #both inputs are minus, take -sign out and do normal addition
        count = 1
        X = X.replace('-','')
        Y = Y.replace('-','')
        return add_function(X,Y,b)

    if X[0] == '-':
        X = X.replace('-','')
        return subtract_function(Y,X,b)

    if Y[0] == '-':
        Y = Y.replace('-','')
        return subtract_function(X,Y,b)

    if b >= 2 and b <= 16:
        result = []
        maxL = max(len(X), len(Y))
        X = X.zfill(maxL)
        Y = Y.zfill(maxL)
        X2 = list(X)
        Y2 = list(Y)

        # maka sure the modulo has the same length as x and y
        if m is not None:
            m = m.zfill(maxL)

        # convert abcdef into integers
        for i in range(maxL):
            X2[i] = base.get(X2[i])
            Y2[i] = base.get(Y2[i])

        # primary school method of addition
        for i in range(1,maxL+1):
            dig = X2[-i] + Y2[-i] + carry
            if dig >= b:
                carry = 1
                dig %= b
            else:
                carry = 0
            result.append(dig)

        if carry == 1:
            result.append(str(carry))

        # remap the dictionary such that integers >= 10
        # are converted to alphabet
        for i in range(maxL):
            invMap = {v: k for k, v in base.items()}
            result[i] = invMap.get(result[i])

        answer = ''.join(result[::-1])

        # if m, divide by m and keep remainder as answer
        if m is not None:
            answer = simple_division(answer, m, b)[1]
        if answer[0] is "0": answer = answer[1:]
        return answer
