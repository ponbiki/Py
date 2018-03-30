#!/usr/local/env python

guess = 5
print "I want to find the square root of:"
answer = raw_input()
float(answer)
print "Guess - %i" % (guess)
for i in range(40):
    if float(guess) * float(guess) != float(answer):
        guess = (float(guess) + (float(answer) / float(guess)))/2
        print guess

