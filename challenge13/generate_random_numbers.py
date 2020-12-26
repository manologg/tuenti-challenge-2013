import random

ofile = open('my_test.in', 'w')
ofile.write('1\n')

N = (10**6)/5
M = (10**4)/5

ofile.write(str(N) + ' ' + str(M) + '\n')

for i in range(N):
    ofile.write(str(random.randrange(1, N)) + ' ')
ofile.write('\n')

for i in range(M):
    num1 = random.randrange(1, N)
    num2 = random.randrange(1, N)
    ofile.write(str(min(num1, num2)) + ' ' + str(max(num1, num2)) + '\n')
