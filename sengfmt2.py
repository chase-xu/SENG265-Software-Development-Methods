#!/opt/local/bin/python

# File: sengfmt2.py 
# Student Name  : Peng Xu 
# Student Number: V00924503 
# SENG 265 - Assignment 3

import sys
import fileinput
from formatter import Formatter

def main():
	getInput()


def getInput():
	text = []
	filename = None
	with fileinput.input() as f:
		for line in f:
			if(f.filename() != None):
				filename = f.filename()
				break
			else:
				text.append(line)
	if(filename != None):
		f = Formatter(filename = filename)
		t = f.get_lines()
		print_out(t)
	else:
		f = Formatter(inputlines = text)
		t = f.get_lines()
		print_out(t)
				
	fileinput.close()	

def print_out(lines):
	for line in lines:
		print(line)
	
		

if __name__ == "__main__":
    main()
