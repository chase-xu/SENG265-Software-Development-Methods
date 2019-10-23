#!/usr/bin/env python3 

# File: formatter.py 
# Student Name  : Peng Xu 
# Student Number: V00924503 
# SENG 265 - Assignment 3

import argparse
import sys
import fileinput
import re
import calendar


class Formatter:
	def __init__(self, filename=None, inputlines=None):
		self.filename = filename
		self.inputlines = inputlines
		self.margin = 0
		self.maxwidth = 0
		self.fmt = 0
		self.cap = 0
		self.final_list = []


	#Fuction to return a list of correct formatted strings
	def get_lines(self):

		lines = ""
		words = []
		paragraph = []
		inpt_name = ""
		replace = 0
		rep = ""       #word to be replaced
		disp = "" 	#word to repalce
		month = 0	#indicate if the month formate is on
		if(self.filename == None):
			inpt_name = self.inputlines
		elif(self.inputlines == None):
			inpt_name = self.filename
		
		for lines in fileinput.input(inpt_name):

			if(replace == 1):
				lines = self.replace_word(rep = rep, disp = disp, lines = lines)

			if(month != 0):
				lines = self.replace_month(lines = lines)

			lines = lines.strip()
			words = lines.split()

			if(len(words) == 0):
				if(self.maxwidth != 0 and self.fmt == 1):
					self.fmt_output(paragraph = paragraph, lines = lines, words = words)
					paragraph.clear()
					paragraph = []
				
				self.final_list.append("")
			elif(words[0] == "?maxwidth"):
				self.maxwidth = int(words[1])
				self.fmt = 1
			elif(len(words) == 3 and words [0] == "?replace"):
				replace = 1
				self.fmt = 1
				rep = words[1]
				disp = words[2]
			elif(len(words) == 2 and words[0][0] == "?"):
				command = words[0]
				if(self.maxwidth != 0 and len(paragraph) != 0):		
					self.fmt_output(paragraph = paragraph, lines = lines, words = words)
					paragraph.clear()
					paragraph = []
				elif(command == "?monthabbr"):
					if(words[1] == "on"):
						month = 1
						self.fmt = 1
					else:
						month = 0
				elif(command == "?mrgn"):
					self.mrgn(num = words[1], words = words)
					self.fmt = 1
				elif(command == "?fmt"):
					if(words[1] == "off"):
						self.fmt = 0
					else:
						self.fmt = 1
				elif(command == "?cap"):
					if(words[1] == "off"):
						self.cap = 0
					else:
						self.cap = 1
						self.fmt = 1
				else:
					if(self.maxwidth == 0):	
						self.fmt_output(paragraph = paragraph, lines = lines, words = words)
					elif(self.fmt == 1 and self.maxwidth != 0):
						paragraph.extend(words)
					else:
						self.fmt_output(paragraph = paragraph, lines = lines, words = words)
			
			else:
				if(self.maxwidth != 0 and self.fmt == 1):
					paragraph.extend(words)
				else:
					self.fmt_output(paragraph = paragraph, lines = lines, words = words)
	
		if(self.maxwidth != 0):
			self.fmt_output(paragraph = paragraph, lines = lines, words = words)
		fileinput.close()
		#while(self.final_list[len(self.final_list)-1] == "\n"):
		#	self.final_list.pop()
		return self.final_list
	

	#Function use to print out everything
	def fmt_output(self, lines = None, words = None, paragraph = None, replace = None):
	
			if(self.cap == 1 and self.fmt == 1):
				if(self.maxwidth == 0):
					for w in range(len(words)):
						words[w] = words[w].upper()
				else:
					for w in range(len(paragraph)):
						paragraph[w] = paragraph[w].upper()
		
			if(self.fmt == 0):
				self.final_list.append(lines)
				#self.final_list.append("\n")
			elif(self.fmt == 1):
				if(self.maxwidth == 0):
					s = self.margin*" " + lines
					self.final_list.append(s)
					#self.final_list.append("\n")
				else:
					if(self.maxwidth - 20 >= self.margin):
						space = self.maxwidth - self.margin
						index = 0
						temp = []
						string = ""
						while(index < len(paragraph)):
							temp.clear()
							temp=[]
							chars = 0
							string = ""
				
							while(index<len(paragraph)):
								next_char= len(paragraph[index])
								if(chars + next_char + len(temp) +1-1 <= space):
									temp.append(paragraph[index])
									chars+= next_char
									index+=1
								else:
									break
							
							string += self.margin*" "
							if(len(temp) != 1):
								ept_char = (space - chars) / (len(temp) - 1)
								if(len(temp)== 2):
									s = temp[0] + int(ept_char) * " " + temp[1]
									string += s			
								elif(ept_char % 2.0 == 0):
									s = ""
									for j in range(len(temp)):
										s+=temp[j]
										if(j != len(temp) - 1):
											s+= int(ept_char) * " "

									string += s				
						
								else:
									ept_char = int ((space - chars) // (len(temp) - 1))
									remainder = (space - chars) - (len(temp) - 1) * ept_char
									s = ""
									for k in range(len(temp)):
										s+=temp[k]
										
										if(k != len(temp)-1):
											s+=ept_char*" "
											if(remainder != 0):
												s+=" "
												remainder-=1
									string += s
							elif(len(temp) == 1):
								ept_char = int (space - len(temp[0]))
								string += temp[0]
							self.final_list.append(string)
							
	
	#Function to change margin
	def mrgn (self, num = None, words = None):
		if(self.margin + int(num) <= self.maxwidth -20 and (words[1][0] == "+" or words[1][0]=="-")):
			self.margin += int(num)
		elif(words[1][0] == "+" or words[1][0] == "-"):
			self.margin += int(num)
		else:
			self.margin = int(num)
		if(self.margin < 0):
			self.margin = 0
	
	#Function to replace the word
	def replace_word(self, rep = None, disp = None, lines = None):
		line = lines.strip()
		lines = line.split()
		p = re.compile(".*" + rep + ".*")
		
		words = ""
		for j in range(len(lines)):
			m = p.match(lines[j])
			if(m):
				lines[j] = re.sub(rep, disp, lines[j])
			if(j != len(lines) - 1):
				words+=lines[j]+" "
			else:
				words= words + lines[j] + "\n"
		return words

	#Function to replace the month formatt
	def replace_month(self, lines = None):
		line = lines.strip()
		lines = line.split()
		words = ""
		pat = re.compile("(\d{2})[-/.](\d{2})[-/.](\d{4})")
		for j in range(len(lines)):
			m = pat.match(lines[j])
			if(m):
				lines[j] = calendar.month_abbr[int(m.group(1))] + "." + " " + m.group(2) + "," + " " + m.group(3)
			if( j != len(lines) - 1):
				words+= lines[j]+ " "
			else:
				words= words + lines[j]
		return words





