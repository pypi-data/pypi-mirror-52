# declare variables
integer1 = [5,6,14,1]#[4,2,8,2,3,4,5,7,8,8,3,4,6,3,5,6,4,3,5,6,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0]
integer2 = [0,0,3,11]#[6,4,0,9,4,6,7,8,6,4,7,5,7,5,3,6,7,8,6,1,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0]
radix1 = 16
radix2 = 16
positive1 = True
positive2 = False

# Regular multiplication alghorithm
def multiplication(integer1, interger2, radix1, radix2, positive1, positive2):
  # Define variables for wordlength, sign, output
  n = len(integer1)
  output = [0]*2*n
  positive = not (positive1 ^ positive2)

  # Multiply all digits seperately and add in the list
  for i in range(0, n):
    digit2 = integer2[-(i+1)]
    for j in range(0, n):
      digit1 = integer1[-(j+1)]
      outputNumber = digit1*digit2
      output[-(1+i+j)] += outputNumber

  # Calculate the carry and add to the next digit
  for i in range(1, len(output)+1):
    if output[-i] >= radix1:
      carry = output[-i]//radix1
      output[-i] = output[-i]%radix1
      output[-(i+1)] += carry

  # Return a tuple with the sign and output list
  return(positive, output)

multiplication(integer1, integer2, radix1, radix2, positive1, positive2)