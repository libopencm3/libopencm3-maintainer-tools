#!/usr/bin/env python

# This file is part of the libopencm3 project.
# 
# Copyright (C) 2014 Frantisek Burian <BuFran@seznam.cz>
# 
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this library. If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import os.path

def browse(path):
	dirs = [ ]
	for x in os.walk(path):
		dir = ("."+x[0]).replace(path, '').replace('\\','/')
		if dir.count("/") == 2:
			dirs.append(dir)
	return (dirs)

def splithdrs(file):
	(header, text, footer) = ([], [], [])
	curpos = 0
	
	with open(file) as f:
		for line in f:
			if line.find("END UPDATE") != -1:
				curpos = 2
			
			if curpos == 0:
				header.append(line)
			elif curpos == 1:
				text.append(line)
			elif curpos == 2:
				footer.append(line)
			
			if line.find("BEGIN UPDATE") != -1:
				curpos = 1

	return (header, text, footer)

def splittbl(text):
	rows = []
	total = ""
	for line in text:
		ln = line.rstrip('\n')
		if (len(ln) > 1):
			total += ln
		elif (len(total) > 0):
			rows.append([total.lstrip("|").split("|")])
			total = ""
	
	return (rows)

def row_put(f, value):
	for i in range(len(value)):
		f.write("|")
		f.write(value[i])
		if (len(value[i]) != 0) and (i % 2 == 0) :
			f.write("\n")
	f.write("\n")
	
def row_colorize(row, exver, libver):
	style = 'style="background:lime"'
	if (row[4].count(exver) == 0) or (row[6].count(libver) == 0): 
		style = 'style="background:yellow"'

	if (row[8].count("&mdash;") > 0):
		style = 'style="background:orange"'

	changed = row[1].find(style) == -1
	
	row[1] = style;
	row[3] = style;
	row[5] = style;
	row[7] = style;
	row[9] = style;
	
	return (changed)

def main():
	#infile = sys.argv[1]
	dirs = browse("../../libopencm3-examples/examples/stm32/f1")
	file = "../wiki/stm32f1.wiki"
	libver = "fe6b542357"
	exver = "fe6b542357"
	
	(header, text, footer) = splithdrs(file)
	table = splittbl(text)
	
	# check all dirs involved
	for tab in table:
		try:
			dirs.remove(tab[0][2].strip())
		except:
			print ("Example no longer exists '%s'" % (tab[0][2].strip()))
	
	# append nonexistent dirs
	for dir in dirs:
		print ("Example added '%s'" % (dir))
		table.append([['-valign="top"', '', dir, '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;']])

	# recolorize the table
	for tab in table:
		if row_colorize(tab[0], exver, libver):
			print ("Example state touched '%s'" % (tab[0][2].strip()))

	with open(file + ".parsed", "w") as f:
		for line in header:
			f.write(line)
		for tab in table:
			row_put(f, tab[0])
		for line in footer:
			f.write(line)


if __name__ == "__main__":
	main()