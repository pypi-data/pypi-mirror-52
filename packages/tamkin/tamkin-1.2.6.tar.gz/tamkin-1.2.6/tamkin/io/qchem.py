# -*- coding: utf-8 -*-
# TAMkin is a post-processing toolkit for normal mode analysis, thermochemistry
# and reaction kinetics.
# Copyright (C) 2008-2012 Toon Verstraelen <Toon.Verstraelen@UGent.be>, An Ghysels
# <An.Ghysels@UGent.be> and Matthias Vandichel <Matthias.Vandichel@UGent.be>
# Center for Molecular Modeling (CMM), Ghent University, Ghent, Belgium; all
# rights reserved unless otherwise stated.
#
# This file is part of TAMkin.
#
# TAMkin is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# In addition to the regulations of the GNU General Public License,
# publications and communications based in parts on this program or on
# parts of this program are required to cite the following article:
#
# "TAMkin: A Versatile Package for Vibrational Analysis and Chemical Kinetics",
# An Ghysels, Toon Verstraelen, Karen Hemelsoet, Michel Waroquier and Veronique
# Van Speybroeck, Journal of Chemical Information and Modeling, 2010, 50,
# 1736-1750W
# http://dx.doi.org/10.1021/ci100099g
#
# TAMkin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --

from __future__ import print_function, division

from tamkin.data import Molecule

from molmod import angstrom, amu, calorie, avogadro
from molmod.periodic import periodic

import numpy as np


__all__ = ["load_molecule_qchem"]

def load_molecule_qchem(qchemfile, hessfile = None, multiplicity=1, is_periodic = False):
    """Load a molecule from a Q-Chem frequency run

       Arguments:
        | qchemfile  --  Filename of the Q-Chem computation output.

       Optional arguments:
        | hessfile  --  Filename of a separate Hessian file.
        | multiplicity  --  The spin multiplicity of the electronic system
                            [default=1]
        | is_periodic  --  True when the system is periodic in three dimensions.
                           False when the systen is nonperiodic. [default=False]

       Whether the Hessian is printed to a separate Hessian file, depends on the
       used version of Q-Chem. The use of the separate Hessian file is slightly
       more accurate, because the number of printed digits is higher than in the
       Q-Chem output file.

       **Warning**

       At present, the gradient is set to a Nx3 array of zero values, since the
       gradient is not printed out in the Q-Chem output file in general. This
       means that the value of the gradient should be checked before applying
       methods designed for partially optimized structures (currently PHVA,
       MBH and PHVA_MBH).
    """
    # TODO fill in keyword for printing hessian
    with open(qchemfile) as f:
        # get coords
        for line in f:
            if line.strip().startswith("Standard Nuclear Orientation (Angstroms)"):
                break
        next(f)
        next(f)
        positions = []
        symbols = []
        for line in f:
            if line.strip().startswith("----"): break
            words = line.split()
            symbols.append(words[1])
            coor = [float(words[2]),float(words[3]),float(words[4])]
            positions.append(coor)
        positions = np.array(positions)*angstrom
        N = len(positions)    #nb of atoms

        numbers = np.zeros(N,int)
        for i, symbol in enumerate(symbols):
            numbers[i] = periodic[symbol].number
        #masses = np.zeros(N,float)
        #for i, symbol in enumerate(symbols):
        #    masses[i] = periodic[symbol].mass

        # grep the SCF energy
        energy = None
        for line in f:
            if line.strip().startswith("Cycle       Energy         DIIS Error"):
                break
        for line in f:
            if line.strip().endswith("met"):
                energy = float(line.split()[1]) # in hartree
                break

        # get Hessian
        hessian = np.zeros((3*N,3*N),float)
        if hessfile is None:
          for line in f:
              if line.strip().startswith("Hessian of the SCF Energy") or line.strip().startswith("Final Hessian"):
                  break
          nb = int(np.ceil(N/2))
          for i in range(nb):
              next(f)
              row = 0
              for line in f:
                  words = line.split()
                  hessian[row, 6*i:6*(i+1)] = np.array(sum([[float(word)] for word in words[1:]],[])) #/ angstrom**2
                  row += 1
                  if row >= 3*N : break

        # get masses
        masses = np.zeros(N,float)
        for line in f:
            if line.strip().startswith("Zero point vibrational"):
                break
        next(f)
        count=0
        for line in f:
            masses[count] = float(line.split()[-1])*amu
            count += 1
            if count >= N : break

        # get Symm Nb
        for line in f:
            if line.strip().startswith("Rotational Symmetry Number is"):
                break
        symmetry_number = int(line.split()[-1])

    # or get Hessian from other file
    if hessfile is not None:
      with open(hessfile) as f:
          row = 0
          col = 0
          for line in f:
              hessian[row,col] = float(line.split()[0]) *1000*calorie/avogadro /angstrom**2
              col += 1
              if col >= 3*N:
                  row += 1
                  col = row
      for i in range(len(hessian)):
          for j in range(0,i):
              hessian[i,j] = hessian[j,i]

    # get gradient   TODO
    gradient = np.zeros((N,3), float)

    return Molecule(
        numbers, positions, masses, energy, gradient, hessian, multiplicity,
        symmetry_number, is_periodic
    )
