import sys

str = ""
for index, arg in enumerate(sys.argv):
    if index > 0:
        str += "{0} ".format(arg.upper())
        
print(str.upper())
