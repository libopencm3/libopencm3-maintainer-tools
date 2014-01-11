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

import subprocess

def shortrev(path):
	return subprocess.check_output(\
		"git --git-dir=%s/.git rev-parse --short=10 HEAD" % (path),
		shell=False, universal_newlines=True).rstrip('\n')