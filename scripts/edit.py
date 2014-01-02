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
import shutil
import subprocess
from optparse import OptionParser, OptionGroup

global options

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
	
def row_colorize(row):
	global options
	
	style = 'style="background:lime"'
	if (row[4].count(options.exver) == 0) or (row[6].count(options.libver) == 0): 
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

def prt(lev, str):
	global options
	if options.verbose >= lev:
		print (str)

def git_ver(path):
	return subprocess.check_output("git --git-dir=%s/.git rev-parse --short=10 HEAD" % (path), shell=False, universal_newlines=True).rstrip('\n')


	
def main():
	
	parser = OptionParser(
		"Usage: %prog [options] command arg \n\n"
		"Commands:\n"
		"  pass\t\t Mark selected examples in the specified tree as passed\n"
		"  fail\t\t Mark selected examples in the specified tree as failed\n"
		"  treeupdate\t Update the examples tree\n"
		"  gitupdate\t Update table to the actual git version\n\n"
		"Examples:\n"
		" > edit.py -f<file> -t<tree> [-u<user> -l<libver> -e<exver>] pass ./brd/example\n"
		" > edit.py -f<file> -t<tree> [-u<user> -l<libver> -e<exver>] fail ./brd/example\n"
		" > edit.py -f<file> -t<tree> treeupdate\n"
		" > edit.py -f<file> -t<tree> [-l<libver> -e<exver>]  gitupdate\n"
		, version="%prog version 0.1")
	
	parser.add_option("-q", "--quiet", action="store_const", const=0, dest="verbose", default=1, help="Be very silent")
	parser.add_option("-v", "--verbose", action="store_const", const=2, dest="verbose", help="Print debugging messages")
	parser.add_option("-b", "--backup", action="store_true", dest="backup", default=0, help="Backup the wiki database file before parse")
	
	group = OptionGroup(parser, "Source options")
	group.add_option("-f", "--file", action="store", dest="file", help="Filename of the wiki database file")
	group.add_option("-t", "--tree", action="store", dest="tree", help="Path to the current examples repository. If not specified, the LOCM3_EXAMPLES environment variable will be used")
	parser.add_option_group(group)
	
	group = OptionGroup(parser, "Git Options")
	group.add_option("-u","--user", action="store", type="string", dest="user", 
		help="Nickname of the tester. [Current user login by default]");
	group.add_option("-l","--libver", action="store", type="string", dest="libver", 
		help="Git version of libopencm3 library. [Fetched from git tree by default]")
	group.add_option("-e","--exver", action="store", type="string", dest="exver",
		help="Git version of libopencm3-examples. [Fetched from git tree by default]")
	parser.add_option_group(group)
	

	global options
	(options,args) = parser.parse_args()
	
	#argument check
	if len(args) < 1:
		parser.error("Command parameter is required")

	if (options.file == None):
		#parser.error("git: Missing required arguments (-f)")
		options.file = "../wiki/stm32f1.wiki"
	
	if (options.tree == None):
		options.tree = os.environ.get('LOCM3_EXAMPLES')
		prt(2, "Using tree from the environment '%s'" % (options.tree))
		
	
	if (options.tree == None):
		#parser.error("git: Missing required arguments (-t)")
		options.tree = "../../libopencm3-examples/"
		
	
	if (options.user == None):
		options.user = os.getlogin()
		prt(2, "Using login of current logged user '%s' as username" % (options.user))

	needver = False
	if args[0] == "gitupdate":
		pass
		needver = 1
	elif args[0] == "treeupdate":
		pass
	elif args[0] == "pass":
		pass
		needver = 1
	elif args[0] == "fail":
		pass
		needver = 1
	else:
		parser.error("Unknown command: '%s'" % (args[0]))
	
	if needver and (options.exver == None):
		options.exver = git_ver(options.tree)
		prt(2, "Using fetched version of examples '%s'" % (options.exver))
	
	if needver and (options.libver == None):
		options.libver = git_ver(options.tree + "libopencm3/")
		prt(2, "Using fetched version of examples '%s'" % (options.libver))
	
	
	
	# The main body
	dirs = browse(options.tree + "/examples/stm32/f1")

	(header, text, footer) = splithdrs(options.file)
	table = splittbl(text)

	# check all dirs involved
	for tab in table:
		try:
			dirs.remove(tab[0][2].strip())
		except:
			prt(1, "Example no longer exists '%s'" % (tab[0][2].strip()))
	
	# append nonexistent dirs
	for dir in dirs:
		prt(1, "Example added '%s'" % (dir))
		table.append([['-valign="top"', '', dir, '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;', '', '&mdash;']])

	# recolorize the table
	for tab in table:
		if row_colorize(tab[0]):
			prt(1, "Example state touched '%s'" % (tab[0][2].strip()))

	if options.backup:
		shutil.copy2(options.file, options.file+".bak")
		prt(2, "Examples wiki file backupped to '%s'." % (options.file + ".bak"))
	
	with open(options.file, "w") as f:
		for line in header:
			f.write(line)
		for tab in table:
			row_put(f, tab[0])
		for line in footer:
			f.write(line)
	
	prt(1, "Examples wiki file updated.")


if __name__ == "__main__":
	main()