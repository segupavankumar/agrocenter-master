import numpy as np
import re
f1 = open('vege.txt')
a1 = f1.readlines()
f2 = open('frui.txt')
a2 = f2.readlines()
result1 = []
result2 = []
for i in range(len(a1)):
    if(a1[i] != '\n' and a1[i] != 'Kg / Pcs\n'):
        result1.append(a1[i])

for i in range(len(a2)):
    if(a2[i] != '\n' and a2[i] != 'Kg / Pcs\n'):
        result2.append(a2[i])
fruits = []
i = 5
while(i < len(result1)):
    fruits.append(result1[i:i+4])
    i += 4
j = 5
while(j < len(result2)):
    fruits.append(result2[j:j+4])
    j += 4

print(fruits)
for i in fruits:
    u = len(i[0])
    i[0] = i[0][:u-1]
   
    x = len(i[1])
    i[1] = i[1][5:x-1]
    print(i[1])
    y = len(i[2])
    i[2] = i[2][5:y-1]
    print(i[2])
    z = len(i[3])
    i[3] = i[3][5:z-1]
    print(i[3])

fruits = np.array(fruits)
eq = '[0-9][0-9]*'

range_of = []
for i in fruits[:, 2]:
    range_of.append(re.findall(eq, i))

print("----")
print(range_of)

print(fruits[:,0])

