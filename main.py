import string
from fltk import *

alphabetMaj = string.ascii_uppercase

def makeDict():
    dict = {}
    for i in range(8):
        for j in range(1, 9):
            dict[alphabetMaj[i] + str(j)] = "N"
    return dict

