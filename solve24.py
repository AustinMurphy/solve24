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
#    generate all unique & computable permutations of 
#    4 numbers and 3 operators
#
#  if we result in 24, print out the permutation
#
#    using reverse polish notation (RPN) allows us to avoid parens until the end
#


import sys
import itertools


def usage():
    print ""
    print " Solve 24.  You must provide 4 positive integers as arguments."
    print " ex.  " + sys.argv[0] + " 3 3 4 4  "
    print ""
    quit()




# from: http://danishmujeeb.com/blog/2014/12/parsing-reverse-polish-notation-in-python/
#  slightly modified
def parse_rpn(expression):
    """ Evaluate a reverse polish notation """

    stack = []

    for val in expression.split(' '):
        if val in ['-', '+', '*', '/']:
            op1 = stack.pop()
            op2 = stack.pop()
            if val=='-': result = op2 - op1
            if val=='+': result = op2 + op1
            if val=='*': result = op2 * op1
            if val=='/': result = op2 / op1
            stack.append(result)
        else:
            stack.append(float(val))

    return stack.pop()


def rpn_to_infix(expression):
    """ Convert a reverse polish notation equation to infix style with parens"""

    stack = []
    outstack = []

    for val in expression.split(' '):
        if val in ['-', '+', '*', '/']:
            op1 = stack.pop()
            op2 = stack.pop()
            out1 = outstack.pop()
            out2 = outstack.pop()
            if val=='-': result = op2 - op1
            if val=='+': result = op2 + op1
            if val=='*': result = op2 * op1
            if val=='/': result = op2 / op1
            stack.append(result)
            
            # we want to eliminate duplicate expressions
            #  A + B  is the same as B + A
            # our canonical style has the larger value on the left
            if (val=='+' or val=='*'):
                if op1 > op2:
                    outstack.append("("+ str(out1) + str(val) + str(out2) + ")")

                elif op1 < op2:
                    outstack.append("("+ str(out2) + str(val) + str(out1) + ")")
                # op1 == op2
                # if A & B are the same [ex: 3 == (5-2) ], we should put the longer expression on the left
                else:
                    if len(out1) < len(out2):
                        outstack.append("("+ str(out2) + str(val) + str(out1) + ")")
                    else:
                        outstack.append("("+ str(out1) + str(val) + str(out2) + ")")
            # sub and div are not swappable
            else:
                outstack.append("("+ str(out2) + str(val) + str(out1) + ")")
        else:
            stack.append(float(val))
            outstack.append(str(val))

    return str(outstack.pop() + " = " + str(stack.pop()))


def gen_rpn( rpn, nums, numcount, opercount ):
    """ recursive function to generate a list of rpn expressions for a given list of numbers"""

    # rpn is a list of numbers and operators intended to be computable
    #  since each operator replaces two numbers with one, there must be one more number than operator


    # when RPN is long enough, we spit it out
    #  long enough means all given numbers and sufficient operators have been included
    if len(nums)==0 and numcount - opercount == 1:
        # this lets us use this function as an iterator
        yield rpn


    # rpn is not long enough yet
    # extend it

    localrpn = list(rpn)

    # add an operator, if possible
    if numcount - opercount >= 2:
        for op in ['+', '-', '*', '/']:
            newrpn = list(localrpn)
            newrpn.append(op)
            for r in gen_rpn(newrpn, nums, numcount, opercount+1):
                yield r


    # add a number, if possible
    #   we only want to iterate over unique nums at this round
    unums = []
    for n in nums:
        if n not in unums:
            unums.append(n)

    for n in unums:
        localnums = list(nums)
        localnums.remove(n)
        newrpn = list(localrpn)
        newrpn.append(n)
        for r in  gen_rpn(newrpn, localnums, numcount+1, opercount):
            yield r


    #return

        

def revstr(str):
    """ helper function for sorting equations"""
    #  try to push the more complicated parts to the left
    return str[::-1].replace(')', 'Z')







if __name__ == '__main__':

    if len(sys.argv) != 5:
        usage()

    numslist = sys.argv[1:5]
    numslist.sort()



    tries = 0
    divbyzero = 0
    popnothing = 0
    computable = 0
    solves = 0
    solvelist = []

    #
    # Generate the list of possible RPN expressions
    #   using the given numbers and the 4 operators
    #
    # Test whether it computes to 24
    #
    # Format it using the Infix / Parens style
    #

    for r in gen_rpn([], numslist, 0, 0):
        #print "generated rpn:", r,
        rpn = ' '.join(r)
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

        # If we get here, we know the result is computable
        #   so we don't need to catch any execptions 
        #   with the rpn_to_infix() function below

        computable += 1
        #print "computable:", rpn, " = ", result
        #print " = ", result

        if result == 24:
            solves += 1
            #print "rpn:", rpn, " = ", result
            #print "infix:", rpn_to_infix(rpn)
            infixsol = rpn_to_infix(rpn)
            if infixsol not in solvelist:
                solvelist.append(infixsol)



    #
    # Show the results
    #

    print ""


    #print "tries:", tries
    #print "div by zero error:", divbyzero
    #print "operator with no operand situations:", popnothing
    #print "computable equations:", computable
    #print "solutions:", solves
    print "unique solutions:", len(solvelist)
    print ""
    for s in sorted(solvelist, key=revstr):
        print s

    print ""


