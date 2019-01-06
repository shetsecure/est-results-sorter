# - *- coding: utf- 8 - *-
import re
import os.path
from bisect import bisect_left

def menu():
	print("ESTF results Sorter")
	print("What you want to do ?")
	print("[1] : Sort one CSV file")
	print("[2] : Sort multiple CSV files and merge the results")


	good = 0

	while not good:
		try:
			choice = int(raw_input("Your choice: "))
			if choice == 1 or choice == 2:
				good = 1
			else:
				print("Please choose 1 or 2")
		except ValueError, e:
			print ("%s is not a valid integer." % e.args[0].split(": ")[1])

	return choice

def extractStudentsList(path, sortByCne = False, onlyCNE = False):
	module_name = [ line for line in open(path, 'r') if 'Elément pédagogique' in line]
	if (len(module_name) > 0):
		print(module_name[0])
	num_lines = sum(1 for line in open(path))

	# getting number of subjects in the module
	ff = open(path, 'r')
	all_text = ''.join(ff.readlines())
	num_u_p = int(all_text.count("CNE")) # number of CNE in the file = number of pages. It's used to calculate the
										 # number of subjects properly
	num_subj = int(all_text.count("Ado / 20")/num_u_p) - 1 # number of subjects -> will be used to solve the name problem

	f = open(path, 'r') # to get all text after CNE line (the beginning of the students list)
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
					ll.append(l[0])

					if not onlyCNE:
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

	if sortByCne: # sorting by the primary key, most likely will be used in merging results
		resultList.sort(key = lambda x : x[0])

	return resultList

def sortByGrades(path):
	resultList = extractStudentsList(path, True)
	n = int(len(resultList))
	resultList.sort(key = lambda x : float(x[len(x)-2]), reverse=True)

	for i in range(0,n):
		iterS = iter(resultList[i])
		next(iterS) # don't display CNE
		print(str(i+1).zfill(2) + ': ' + ' '.join([str(x) for x in iterS]))

def binary_search(a, x, lo=0, hi=None):  # can't use a to specify default for hi
    hi = hi if hi is not None else len(a)  # hi defaults to len(a)
    pos = bisect_left(a, x, lo, hi)  # find insertion position
    return (pos if pos != hi and a[pos] == x else -1)  # don't walk off the end

def sortAndMerge(files):
	if isinstance(files, list) and files:
		n = int(len(files))
		if n == 1:
			sortByGrades(files[0])
		else:
			n -= 1
			listOfResults = CneList = []
			CneList = extractStudentsList(files[0], True, True) # get only CNEs, this will be the final list of CNE that contains the intersection of all lists of students
			#listOfResults = extractStudentsList(files[0], True)

			for i in range(1, n):
				tempL = extractStudentsList(files[i], True, True) # get the next list and do the intersection
				CneList = [k for k in CneList if k in tempL]

			# Now CneList contains all the commun students between all the files

			
			# grabe the list of CNE sorted for the 1st file, and keep playing with the same var for the others
			# each iteration, delete the not found students -> getting slowly the intersection of all files
			# once you have the commun students of all files, construct the list computing the average of each one
			# sort the last list and display the results
	else:
		print("no")


sortAndMerge(["info2.csv", "info.csv"])
# resultList = extractStudentsList("info.csv", True)
# n = int(len(resultList))
# for i in range(0,n):
# 	print(str(i+1).zfill(2) + ': ' + ' '.join([str(x) for x in resultList[i]]))
# choice = menu()

# if choice == 1:
# 	filename = raw_input('Enter the filename: ')
# 	if os.path.exists(filename):
# 		sortByGrades(filename)
# 	else:
# 		print("File Not Found")

#filename = raw_input('Enter the filename: ')
#sortByGrades(filename)
