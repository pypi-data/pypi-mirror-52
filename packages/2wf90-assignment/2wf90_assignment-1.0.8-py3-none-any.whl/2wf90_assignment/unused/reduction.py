def reduce_function(x, m, b):
    x, m = str(x), str(m)
    x1 = x.strip('-')
    k, n = len(x1), len(m)

    for i in range(k-n, -1, -1):
        reduct_value = m
        if i == 0:
            pass
        else:
            #used to calculate m times the base to the power of i
            for j in range(0, i):
                reduct_value = reduct_value + '0'
        while subtract_function(x1, reduct_value , b)[0] is not "-":
            x1 = subtract_function(x1, reduct_value, b)

    if (x[0] is not "-") or (x1 == '0'):
        y = x1
    else:
        y = subtract_function(m, x1, b)

    return y
