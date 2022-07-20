#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : William Robert Evans [wre]
# Created Date: 20/07/2022
# version ='1.0'
# ---------------------------------------------------------------------------
""" Description, to be added"""
# ---------------------------------------------------------------------------

#put this in the directory with all the files that are to be combined

from random import randrange

testFileName = 'test'
trainFileName = 'train'
extension = '.csv'
rand1 = 0
rand2 = 1
runs = 5

files = ["run1.csv", "run2.csv", "run3.csv", "run4.csv", "run5.csv", "run6.csv", "run7.csv", "run8.csv", "run9.csv", "run10.csv"]

for x in range(runs):
	print("Run " + str(x+1))
	#determine test files
	rand1 = randrange(10)
	rand2 = randrange(10)
	if (rand1==rand2):
		while(rand1==rand2):
			rand2 = randrange(10)
	print("Test datasets are " + str(rand1+1) + " and " + str(rand2+1))	
	#combine training files
	with open(trainFileName+str(x+1)+extension, 'w') as outfile:
		outfile.write("time,lidar_array,angular_velocity\n")
		for idn, n in enumerate(files):
			if(idn==rand1 or idn==rand2):
				continue
			else:
				with open(n) as infile:
					#next(infile)
					for line in infile:
						outfile.writelines(infile.read())
	outfile.close()
	
	#combine test files
	with open(testFileName+str(x+1)+extension, 'w') as outfile:
		outfile.write("time,lidar_array,angular_velocity\n")
		for idn, n in enumerate(files):
			if(idn==rand1 or idn==rand2):
				with open(n) as infile:
					#next(infile)
					for line in infile:
						outfile.writelines(infile.read())
			else:
				continue
				
	outfile.close()
				
print("Files combined")
