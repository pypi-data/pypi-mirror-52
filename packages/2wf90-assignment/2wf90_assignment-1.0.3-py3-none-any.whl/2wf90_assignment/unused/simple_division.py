def simple_division(x, y, b):
    #very slow for big x and small y, only used to calculate the floor of r / y*b^i in the long division function
    q, r = '0', x
    sumy = '0'
    #this covers the base case, which is also the worst case for this algorithm
    if y == '1':
        q, r = x, '0'
    #the while loop counts how many times y is in x, outputs that number (which is the quotient) and the remainder
    while subtract_function(x, add_function(sumy, y, b), b)[0] is not "-":
    #keeps track of q times y
        sumy = add_function(sumy, y, b)
    #updates the remainder
        r = str(subtract_function(r, y, b))
    #adds 1 to the quotient
        q = str(add_function(q, 1, b))

    # print(str(q) +"*" + str(y) + "+" + str(r) + "=" + str(x))
    return [q, r]
