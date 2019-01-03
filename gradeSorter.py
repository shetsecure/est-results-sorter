# - *- coding: utf- 8 - *-

# MADE WITH LOVE BY AMINE MARZOUKI

import re
import operator

filename = raw_input('Enter the filename: ')
module_name = [ line for line in open(filename, 'r') if 'Elément pédagogique' in line]
if (len(module_name) > 0):
	print(module_name[0])
num_lines = sum(1 for line in open(filename))

# getting number of subjects in the module
ff = open(filename, 'r')
all_text = ''.join(ff.readlines())
num_u_p = int(all_text.count("CNE")) # number of CNE in the file = number of pages. It's used to calculate the
									 # number of subjects properly
num_subj = int(all_text.count("Ado / 20")/num_u_p) - 1 # number of subjects -> will be used to solve the name problem

f = open(filename, 'r') # to get all text after CNE line (the beginning of the students list)
for i in range(1,num_lines):
	if(f.readline().find("CNE") >= 0):
		res = f.readlines()
		break

length = len(res)

for i in range(0,length):
	if(res[i].find("Nombre total d'étudiants : ") > 0):
		nString = res[i]
		n = re.findall(r'\d+', nString)[0] # number of students
		break # found it, get out

resultList = [] # the list that will contain the results
n = int(n)
j = 0
bad = False # bool var to check if the string matchs the form of CNE
k = 0

while k <= n:
	try:
		l = res[j].split('"')[1].split()
		ll = []
		bad = False
		j += 1
		if(l):
			if re.match(r"^(([A-Z]|[0-9])[0-9]{9})$", l[0]):
				k += 1
				for i in range(3, len(l)-num_subj):
					ll.append(l[i])
				resultList.append(ll)
			else:
				bad = True
				continue
		else:
			bad = True
			continue
		if(bad):
			j -= 1
	except IndexError:
		break

resultList.sort(key = lambda x : float(x[len(x)-2]), reverse=True)

for i in range(0,n):
	print(str(i+1).zfill(2) + ': ' + ' '.join([str(x) for x in resultList[i]]))
