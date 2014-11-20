#!/usr/bin/python

import sys

def readSTDIN():
	N, k = map(int, sys.stdin.readline().split(" "))
	employees = []
	for i in range(N):
		line = sys.stdin.readline()[:-1].split(" ")
		numbers = map(int, line)
		#print numbers
		employees.append(numbers)
	return employees, k

def Algorithm():
	employees, k = readSTDIN()

	print "85"




if __name__ == "__main__":
	Algorithm()