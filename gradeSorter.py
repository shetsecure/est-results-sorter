# - *- coding: utf- 8 - *-

# MADE WITH LOVE BY AMINE MARZOUKI

import re
import operator

filename = 'INF1-S1-M1.csv'
#filename = raw_input('Enter the filename: ')
module_name = [ line for line in open(filename, 'r') if 'Elément pédagogique' in line]
if (len(module_name) > 0):
	print(module_name[0])
num_lines = sum(1 for line in open(filename))
f = open(filename, 'r')

# getting number of subjects in the module
ff = open(filename, 'r')
sss = ''.join(ff.readlines())
num_u_p = int(sss.count("CNE"))
num_subj = int(sss.count("Ado / 20")/num_u_p) - 1 # will be used to solve the name problem (it varies in the list) -> SOLVED
# doesn't work with multiple pages, gives bad results need to update it -> SOLVED
for i in range(1,num_lines):
	if(f.readline().find("CNE") >= 0):
		res = f.readlines()
		break

length = len(res)
#string = ""

for i in range(0,length):
#	string += res[i]
	if(res[i].find("Nombre total d'étudiants : ") > 0):
		nString = res[i]
		n = re.findall(r'\d+', nString)[0] # number of students

#string = re.findall(r'"([^"]*)"', string)
#print(string)

#res = sorted(res, key=lambda x: (x[len(x)-num_subj-1]))
resultList = []
n = int(n)
j = 0
bad = False
#for j in range(0, n):
k = 0
while k <= n:
	try:
		l = res[j].split('"')[1].split()
		ll = []
		bad = False
		#print(n)
		j += 1
		if(l):
			if re.match(r"^(([A-Z]|[0-9])[0-9]{9})$", l[0]):
				#print(l[0])
				k += 1
				#print(k)
				for i in range(3, len(l)-num_subj): 
			#print(l[i] + ' ', end='')
					ll.append(l[i])
		#print('')
				resultList.append(ll)
			else:
				#print(j)
				bad = True
				continue
		else:
			#print(j)
			bad = True
			continue
		if(bad):
			j -= 1
	except IndexError:
		break
#print(k)

#resultList = sorted(resultList, key=lambda x: x[len(x)-2], reverse=True)
resultList.sort(key = lambda x : float(x[len(x)-2]), reverse=True)
for i in range(0,n):
	print(str(i+1).zfill(2) + ': ' + ' '.join([str(x) for x in resultList[i]]))
