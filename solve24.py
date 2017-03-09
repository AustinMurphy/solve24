#!/usr/bin/python
#
#   take 4 natural numbers 
#   make a mathematical equation that uses all 4 numbers and +, -, *, /  (and parens)
#   to result in the number 24
#
#   This is a fun mental game, but if we get stuck 
#    a solver is nice
#


# strategy:
#   take 4 numbers from input
#    generate all unique permutations of 
#    4 numbers and 3 operators
#
#  if we result in 24, print out the permutation
#
#    using reverse polish notation (RPN) allows us to avoid parens


import sys
import itertools
from sets import Set


# from: http://danishmujeeb.com/blog/2014/12/parsing-reverse-polish-notation-in-python/
#  slightly modified
def parse_rpn(expression):
    """ Evaluate a reverse polish notation """

    stack = []

    for val in expression.split(' '):
        if val in ['-', '+', '*', '/']:
            ## don't operate on fewer than 2 numbers
            #if len(stack) < 2:
            #    return 0
            op1 = stack.pop()
            op2 = stack.pop()
            if val=='-': result = op2 - op1
            if val=='+': result = op2 + op1
            if val=='*': result = op2 * op1
            ## don't divide by zero
            #if op1 == 0:
            #    return 0
            if val=='/': result = op2 / op1
            stack.append(result)
        else:
            stack.append(float(val))

    return stack.pop()


#
#  for some definition of canonical...  (all operators are applied in pairs and wrapped in parens)
#
# converts to a canonical version of an infix w/ parens style equation
def rpn_to_infix(expression):
    """ Convert a reverse polish notation equation to infix style with parens"""

    stack = []
    outstack = []

    for val in expression.split(' '):
        if val in ['-', '+', '*', '/']:
            # don't operate on fewer than 2 numbers
            if len(stack) < 2:
                return 0
            op1 = stack.pop()
            op2 = stack.pop()
            out1 = outstack.pop()
            out2 = outstack.pop()
            if val=='-': result = op2 - op1
            if val=='+': result = op2 + op1
            if val=='*': result = op2 * op1
            # don't divide by zero
            if op1 == 0:
                return 0
            if val=='/': result = op2 / op1
            stack.append(result)
            
            if (val=='+' or val=='*') and op1 > op2:
                outstack.append("("+ str(out1) + str(val) + str(out2) + ")")
            else:
                outstack.append("("+ str(out2) + str(val) + str(out1) + ")")
        else:
            stack.append(float(val))
            outstack.append(str(val))

    return str(outstack.pop() + " = " + str(stack.pop()))




def usage():
    print ""
    print " Solve 24.  You must provide 4 positive integers as arguments."
    print " ex.  " + sys.argv[0] + " 3 3 4 4  "
    print ""
    quit()





if __name__ == '__main__':

    # arg0 is the comand name 
    if len(sys.argv) != 5:
        usage()

    numslist = sys.argv[1:5]
    numslist.sort()
    nums = tuple(numslist)

    operslist = [ '+', '-', '*', '/' ]


    tries = 0
    computable = 0
    solves = 0
    divbyzero = 0
    popnothing = 0

    # there are lots of duplicate permutations
    # Set enforces uniqueness 
    #   the combination function does not work as expected
    operset = Set()
    numoperset = Set()
    solveset = Set()

    for j in itertools.product(operslist, repeat=3):
        #print "j:", j
        lj = list(j)
        lj.sort()
        j = tuple(lj)
        operset.add(j)

    for ops in operset:
        #print "ops:", ops
        for k in itertools.permutations(nums+ops, 7):
            #print "k:", k
            numoperset.add(k)

    for m in numoperset:
        rpn = ' '.join(m)
        tries += 1
        result = 0
        try:
            result = parse_rpn(rpn)
        except ZeroDivisionError:
            divbyzero += 1
            #print "rpn:", rpn, " = UNDEF (div by zero)"
            continue
        except IndexError:
            popnothing += 1
            # can't pop 2 vars off stack if stack has fewer than 2 vars
            #print "IndexError:", rpn
            continue

        computable += 1
        #print "computable:", rpn, " = ", result

        if result == 24:
            solves += 1
            #print "rpn:", rpn, " = ", result
            #print "infix:", rpn_to_infix(rpn)
            solveset.add(rpn_to_infix(rpn))

    for s in sorted(solveset):
        print s

    print "unique solutions:", len(solveset)
    #print "solutions:", solves
    #print "computable equations:", computable
    #print "tries:", tries
    ##print "div by zero error:", divbyzero
    ##print "operator with no operand situations:", popnothing

    
