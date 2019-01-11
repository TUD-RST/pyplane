    # -*- coding: utf-8 -*-

#    Copyright (C) 2015
#    by Jan Winkler, jan.winkler@tu-dresden.de
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Some helper functions

Created on Wed Jul 29 09:24:52 2015

@author: winkler
"""


import os
import subprocess as subproc
import matplotlib.pyplot as plt


def check_if_latex():
    """This function checks if the commands latex and dvipng are 
       installed on the systems and callable
    """
    FNULL = open(os.devnull, 'w')

    # Check if latex and dvipng commands respond
    try:
        subproc.check_call(["latex", "--version"], stdout=FNULL, stderr=subproc.STDOUT)
        subproc.check_call(["dvipng", "--version"], stdout=FNULL, stderr=subproc.STDOUT)
    except OSError:
        return False
        
    FNULL.close()   
        
    return True
