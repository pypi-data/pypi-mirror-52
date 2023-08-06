from ccpl.console import *

printc("Input the sting you want to cringify")
uRes = input(">> ")
clear()
for i in range(len(uRes)+1):
    print(uRes[0:i])

for j in range(1, len(uRes)):
    print(uRes[0:len(uRes)-j])
