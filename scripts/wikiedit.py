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


def prt(lev, str):
	global options
	if options.verbose >= lev:
		print (str)

################################################################################
# A simple class holding the table
#
class WikiTable():
	
	########################################################################
	# The skeleton for the new additions
	#
	__skeleton = """\
== Skeleton ==

{| border="0" style="font-size: smaller; background-color: #eeeeee" bgcolor="#eeeeee"

|- valign="top"
|- bgcolor="#6699ff"
|Example || Example version || Library version || Who || Date || Status || BMP || OOCD || OOCD Serial || STLINK || STFLASH

<!-- BEGIN UPDATE -->

<!-- END UPDATE -->
|}

"""

	def __init__(self):
		self.parse(self.__skeleton.splitlines(1))
	
	########################################################################
	# Deserialize the table from the list of lines
	#
	def parse(self, lines):
		self.header = []
		self.footer = []
		self.table = []
		text = []
		curpos = 0
		for line in lines:
			if line.find("END UPDATE") != -1:
				curpos = 2
			
			if curpos == 0:
				self.header.append(line)
			elif curpos == 1:
				text.append(line)
			elif curpos == 2:
				self.footer.append(line)
			
			if line.find("BEGIN UPDATE") != -1:
				curpos = 1
		
		total = ""
		for line in text:
			ln = line.rstrip('\n')
			if (len(ln) > 1):
				total += ln
			elif (len(total) > 0):
				self.table.append(total.lstrip("|").split("|"))
				total = ""
		

	########################################################################
	# Serialize the table into the string
	#
	def serialize(self):
		text = []
		text.extend(self.header)
		for tab in self.table:
			for i in range(len(tab)):
				if (len(tab[i]) != 0) and (i % 2 == 0) :
					text.append("|" + tab[i] + "\n")
				else:
					text.append("|" + tab[i])
			text.append("\n")
		text.extend(self.footer)
		return (text)
	
	########################################################################
	# Append the missing directories
	#
	def do_append_rows(self,rows):
		for dir in rows:
			prt(1, "Example added '%s'" % (dir))
			self.table.append(['-valign="top"', '', dir, '', '&mdash;',
				'', '&mdash;', '', '&mdash;', '', '&mdash;',
				'', '&mdash;'])

	########################################################################
	# Update color of each row to match its status
	#
	def do_update_colors(self):
		for tab in self.table:
			style = 'style="background:lime"'
			if (tab[4].count(options.exver) == 0) \
				or (tab[6].count(options.libver) == 0): 
				style = 'style="background:yellow"'
	
			if (tab[8].count("&mdash;") > 0):
				style = 'style="background:orange"'
	
			if tab[1].find(style) == -1:
				prt(1, "Example state touched '%s'" % (tab[2].strip()))
		
			tab[1] = style;
			tab[3] = style;
			tab[5] = style;
			tab[7] = style;
			tab[9] = style;
	

def browse(path):
	dirs = [ ]
	for x in os.walk(path):
		dir = ("."+x[0]).replace(path, '').replace('\\','/')
		if dir.count("/") == 2:
			dirs.append(dir)
	return (dirs)



def write_file(wt):
	global options
	
	text = wt.serialize()
	
	if options.backup:
		shutil.copy2(options.file, options.file+".bak")
		prt(2, "Examples wiki file backupped to '%s'." % (options.file + ".bak"))

	with open(options.file, "w") as f:
		f.writelines(text)
	
	prt(1, "Examples wiki file updated.")


def git_ver(path):
	return subprocess.check_output("git --git-dir=%s/.git rev-parse --short=10 HEAD" % (path), shell=False, universal_newlines=True).rstrip('\n')



################################################################################
# Commands 
def cmd_init_tree():
	global options
	
	wt = WikiTable()	
	
	dirs = browse(options.tree + "/examples/stm32/f2")
	wt.do_append_rows(dirs)
	
	write_file(wt)

def cmd_update_tree():
	global options
	
	dirs = browse(options.tree + "/examples/stm32/f2")

	with open(options.file) as f:
		lines = f.readlines()
	
	wt = WikiTable()
	wt.parse(lines)

	# check all dirs involved
	for tab in wt.table:
		try:
			dirs.remove(tab[2].strip())
		except:
			prt(1, "Example no longer exists '%s'" % (tab[2].strip()))
	
	# append nonexistent dirs
	wt.do_append_rows(dirs)

	write_file(wt)

def cmd_update_gitver():
	global options

	with open(options.file) as f:
		lines = f.readlines()
	
	wt = WikiTable()
	wt.parse(lines)

	# recolorize the table
	wt.do_update_colors()

	write_file(wt)


def main():
	
	parser = OptionParser(
		"Usage: %prog [options] command arg \n\n"
		"Commands:\n"
		"  pass\t\t Mark selected examples in the specified tree as passed\n"
		"  fail\t\t Mark selected examples in the specified tree as failed\n"
		"  init-tree\t Initialize tree\n"
		"  update-tree\t Update the examples tree\n"
		"  update-gitver\t Update table to the actual git version\n\n"
		"Examples:\n"
		" > edit.py -f<file> -t<tree> [-u<user> -l<libver> -e<exver>] pass ./brd/example\n"
		" > edit.py -f<file> -t<tree> [-u<user> -l<libver> -e<exver>] fail ./brd/example\n"
		" > edit.py -f<file> -t<tree> init-tree\n"
		" > edit.py -f<file> -t<tree> update-tree\n"
		" > edit.py -f<file> -t<tree> [-l<libver> -e<exver>] update-gitver\n"
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
		options.file = "../wiki/stm32f2.wiki"
	
	if (options.tree == None):
		options.tree = os.environ.get('LOCM3_EXAMPLES')
		prt(2, "Using tree from the environment '%s'" % (options.tree))
		
	
	if (options.tree == None):
		#parser.error("git: Missing required arguments (-t)")
		options.tree = "../../libopencm3-examples/"
		
	
	if (options.user == None):
		options.user = os.getlogin()
		prt(2, "Using login of current logged user '%s' as username" % (options.user))

	needver = (args[0] == "update-gitver") or (args[0] == "pass") or (args[0] == "fail")
	
	if needver and (options.exver == None):
		options.exver = git_ver(options.tree)
		prt(2, "Using fetched version of examples '%s'" % (options.exver))
	
	if needver and (options.libver == None):
		options.libver = git_ver(options.tree + "libopencm3/")
		prt(2, "Using fetched version of examples '%s'" % (options.libver))
	
	
	
	# The main body
	
	if args[0] == "init-tree":
		cmd_init_tree()
	elif args[0] == "update-tree":
		cmd_update_tree()
	elif args[0] == "update-gitver":
		cmd_update_gitver()
	elif args[0] == "pass":
		pass
	elif args[0] == "fail":
		pass
	else:
		parser.error("Unknown command: '%s'" % (args[0]))



if __name__ == "__main__":
	main()