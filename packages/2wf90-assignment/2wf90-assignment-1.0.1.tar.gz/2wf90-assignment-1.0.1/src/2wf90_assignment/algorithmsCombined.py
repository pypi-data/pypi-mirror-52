# All algorithms combined
def addition(inputX, positiveX, inputY, positiveY, b, countAdd = 0, countMult = 0):
    lenX = len(inputX)
    lenY = len(inputY)
    inputXY = inputX, inputY
    maxLen = max(map(len, inputXY))

    # add digits
    for digits in inputXY:
        while len(digits) <= maxLen:
            digits.insert(0, 0)

    if (positiveX == False) and (positiveY == False):
        # set positive indicator
        positiveOutput = False
        # run addition
        [output, countAdd, countMult] = addition(inputX, True, inputY, True, b, countAdd, countMult)[1:4]

    elif (positiveX == True) and (positiveY == False):
        # run subtraction
        [positiveOutput, output, countAdd, countMult] = subtraction(inputX, True, inputY, True, b, countAdd, countMult)

    elif (positiveX == False) and (positiveY == True):
        # run subtraction
        [positiveOutput, output, countAdd, countMult] = subtraction(inputY, True, inputX, True, b, countAdd, countMult)

    elif (positiveX == True) and (positiveY == True):
        # set positive indicator
        positiveOutput = True

        # sum the digits from listX with listY according to index in each list
        sumXY = [sum(x) for x in zip(*inputXY)]
        output = sumXY.copy()
        for i in range(1, len(output)):
            rem, carry = 0, 0
            if output[-i] >= b:
                carry = output[-i] // b
                output[-i] = output[-i] % b
                output[-(i+1)] += carry
                countAdd += 1

    i = 0
    while i < (len(output) - 1):
        if (output[i] == 0):
            output.pop(0)
            continue
        break

    return [positiveOutput, output, countAdd, countMult]


def subtraction(inputX, positiveX, inputY, positiveY, b, countAdd = 0, countMult = 0):
    lenX = len(inputX)
    lenY = len(inputY)
    inputXY = inputX, inputY
    maxLen = max(map(len, inputXY))

    # add digits
    for digits in inputXY:
        while len(digits) < maxLen:
            digits.insert(0, 0)

    if (positiveX == False) and (positiveY == False):
        # run addition
        [positiveOutput, output, countAdd, countMult] = subtraction(inputY, True, inputX, True, b, countAdd, countMult)

    elif (positiveX == True) and (positiveY == False):
        # run subtraction
        [positiveOutput, output, countAdd, countMult] = addition(inputX, True, inputY, True, b, countAdd, countMult)

    elif (positiveX == False) and (positiveY == True):
        # run subtraction
        [positiveOutput, output, countAdd, countMult] = addition(inputX, False, inputY, False, b, countAdd, countMult)

    elif (positiveX == True) and (positiveY == True):
        # check which number is bigger
        for i in range(maxLen):
            if (inputX[i] > inputY[i]):
                positiveOutput = True
            elif (inputX[i] < inputY[i]):
                inputTemp= inputX.copy()
                inputX = inputY.copy()
                inputY = inputTemp.copy()
                inputXY = inputX, inputY
                positiveOutput = False
            elif (inputX[i] == inputY[i]):
                if (i == maxLen - 1):
                    return [True, [0], countAdd, countMult]
                continue
            break

        # sum the digits from listX with listY according to index in each list
        diffXY = [0] * maxLen
        for i in range(maxLen):
            diffXY[i] = inputX[i] - inputY[i]
            countAdd += 1
        output = diffXY.copy()

        for i in range(1, len(output)):
            rem = 0
            if output[-i] < 0:
                output[-(i+1)] -= 1
                rem = output[-i] + b
                output[-i] = rem
                countAdd += 2

    i = 0
    while i < (len(output) - 1):
        if (output[i] == 0):
            output.pop(0)
            continue
        break

    return [positiveOutput, output, countAdd, countMult]


def multiplication(inputX, positiveX, inputY, positiveY, b, countAdd = 0, countMult = 0):
    inputXY = inputX, inputY
    maxLen = max(map(len, inputXY))
    minLen = min(map(len, inputXY))
    positiveOutput = not(positiveX ^ positiveY)

    for digits in inputXY:
        while len(digits) < maxLen:
            digits.insert(0, 0)

    n = len(inputX)
    output = [0]*2*n

    for i in range(0, n):
        digit2 = inputY[-(i+1)]
        for j in range(0, n):
            digit1 = inputX[-(j+1)]
            outputNumber = digit1 * digit2
            output[-(1+i+j)] += outputNumber
            countAdd += 1
            countMult += 1

    for i in range(1, len(output)+1):
        if output[-i] >= b:
            carry = output[-i] // b
            output[-i] = output[-i] % b
            output[-(i+1)] += carry
            countAdd += 1

    i = 0
    while i < (len(output) - 1):
        if (output[i] == 0):
            output.pop(0)
            continue
        break

    return [positiveOutput, output, countAdd, countMult]


def karatsuba(inputX, positiveX, inputY, positiveY, b, countAdd = 0, countMult = 0):
    positiveOutput = not (positiveX ^ positiveY)

    i = 0;
    while i < (len(inputX)-1):
        if (inputX[i] == 0):
            inputX.pop(0)
            continue
        break

    i = 0;
    while i < (len(inputY)-1):
        if (inputY[i] == 0):
            inputY.pop(0)
            continue
        break

    if (len(inputX) <= 1 or len(inputY) <= 1):
        [positive, output, countAdd, countMult] = multiplication(inputX, positiveX, inputY, positiveY, b, countAdd, countMult)
        return [positive, output, countAdd, countMult]

    inputXY = inputX, inputY
    maxLen = max(len(inputX), len(inputY))

    for digits in inputXY:
        while len(digits) < maxLen:
            digits.insert(0, 0)

    if (len(inputX) % 2 == 1):
        inputX.insert(0, 0)

    if (len(inputY) % 2 == 1):
        inputY.insert(0, 0)

    n = max(len(inputX), len(inputY)) // 2

    # define x_hi, x_lo, y_hi and y_lo
    x_hi = inputX[:n]
    x_lo = inputX[n:]
    y_hi = inputY[:n]
    y_lo = inputY[n:]

    # calculate all multiplications with recursion
    [xy_hi, countAdd, countMult] = karatsuba(x_hi, True, y_hi, True, b, countAdd, countMult)[1:4]
    [xy_lo, countAdd, countMult] = karatsuba(x_lo, True, y_lo, True, b, countAdd, countMult)[1:4]
    [sumX, countAdd, countMult] = addition(x_hi, True, x_lo, True, b, countAdd, countMult)[1:4]
    [sumY, countAdd, countMult] = addition(y_hi, True, y_lo, True, b, countAdd, countMult)[1:4]
    [sumXY, countAdd, countMult] = karatsuba(sumX, True, sumY, True, b, countAdd, countMult)[1:4]
    [xy_positive, xy_temp, countAdd, countMult] = subtraction(sumXY, True, xy_hi, True, b, countAdd, countMult)
    [positiveMix, xy_mix, countAdd, countMult] = subtraction(xy_temp, xy_positive, xy_lo, True, b, countAdd, countMult)
    output = [0] * n * 10

    for i in range(1, len(xy_lo) + 1):
        output[-i] += xy_lo[-i]
        countAdd += 1

    for i in range(1, len(xy_mix) + 1):
        if positiveMix:
            output[-(i + n)] += xy_mix[-i]
        else:
            output[-(i + n)] -= xy_mix[-i]
        countAdd += 1

    for i in range(1, len(xy_hi) + 1):
        output[-(i + 2 * n)] += xy_hi[-i]
        countAdd += 1

    for i in range(1, len(output) + 1):
        rem = 0
        if (output[-i] >= b):
            carry = output[-i] // b
            output[-i] = output[-i] % b
            output[-(i + 1)] += carry
            countAdd += 1
        elif (output[-i] < 0):
            output[-(i + 1)] -= 1
            rem = output[-i] + b
            output[-i] = rem
            countAdd += 2

    i = 0
    while i < (len(output) - 1):
        if (output[i] == 0):
            output.pop(0)
            continue
        break

    return [positiveOutput, output, countAdd, countMult]

def euclidean(inputX, positiveX, inputY, positiveY, b):
    x1, x2, y1, y2 = [True, [1]], [True, [0]], [True, [0]], [True, [1]]
    eqZero = False
    numberX, numberY = inputX.copy(), inputY.copy()

    while not eqZero:
        [r, q] = modular_reduction(numberX, True, numberY, b)[1:3]
        numberX, numberY = numberY, r
        qx2 = karatsuba(q, True, x2[1], x2[0], b)[0:2]
        qy2 = karatsuba(q, True, y2[1], y2[0], b)[0:2]
        x3 = subtraction(x1[1], x1[0], qx2[1], qx2[0], b)[0:2]
        y3 = subtraction(y1[1], y1[0], qy2[1], qy2[0], b)[0:2]
        x1, y1 = x2, y2
        x2, y2 = x3, y3

        i = 0;
        while i < (len(numberY)-1):
            if (numberY[i] == 0):
                numberY.pop(0)
                continue
            break

        if (numberY[0] == 0):
            eqZero = True

    gcd = numberX

    if positiveX:
        x = x1
    else:
        x = [not x1[0], x1[1]]

    if positiveY:
        y = y1
    else:
        y = [not y1[0], y1[1]]

    return [gcd, x, y]


def modular_reduction(inputX, positiveX, m, b):
    # len of input X and len of mod
    lenX = len(inputX)
    lenM = len(m)
    difLen = lenX - lenM
    coefficient = [0]*lenX
    positive = True
    eqZero = False
    output = inputX.copy()

    # step 2
    for i in range(0, difLen + 1):
        positive = True
        coeffCounter = -1
        n = difLen-i
        tempX = output.copy()
        modBase = m.copy()
        for j in range(n):
            modBase.append(0)
        while positive:
            coeffCounter += 1
            output = tempX.copy()
            [positive, tempX] = subtraction(output, True, modBase, True, b)[0:2] #pak de positive output ding
        coefficient[-(n+1)] = coeffCounter

    i = 0;
    while i < (len(output)-1):
        if (output[i] == 0):
            output.pop(0)
            continue
        break

    if (output[0] == 0):
        eqZero = True

    if (positiveX or eqZero):
        return [True, output, coefficient]
    else:
        return [True, subtraction(m, True, output, True, b)[1], coefficient]


def modular_addition(inputX, positiveX, inputY, positiveY, m, b):
    [positive, sumXY] = addition(inputX, positiveX, inputY, positiveY, b)[0:2]
    output = modular_reduction(sumXY, positive, m, b)[0:2]
    return output


def modular_subtraction(inputX, positiveX, inputY, positiveY, m, b):
    [positive, diffXY] = subtraction(inputX, positiveX, inputY, positiveY, b)[0:2]
    output = modular_reduction(diffXY, positive, m, b)[0:2]
    return output


def modular_multiplication(inputX, positiveX, inputY, positiveY, m, b):
    [positive, prodXY] = multiplication(inputX, positiveX, inputY, positiveY, b)[0:2]
    output = modular_reduction(prodXY, positive, m, b)[0:2]
    return output


def modular_inversion(inputX, positiveX, m , b):
    a = modular_reduction(inputX, positiveX, m, b)[1]
    [gcd, x] = euclidean(a, True, m, True, b)[0:2]

    if (gcd == [1]):
        return modular_reduction(x[1], x[0], m, b)[0:2]
    else:
        return "inverse does not exist"
