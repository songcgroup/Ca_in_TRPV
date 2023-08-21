#!/usr/bin/env python

import re, sys, math
import MDAnalysis
import numpy as np

#sel_heads = "resname POPC and name P"  # DIY
sel_ions = "name D0"                   # DIY

top = sys.argv[1]
trj = sys.argv[2]
rad = float(sys.argv[3])

u = MDAnalysis.Universe(top, trj)

sf = u.select_atoms("resid 224 516 808 1100 and name CA")
gt = u.select_atoms("resid 257 549 841 1133 and name CA")
#zsf = np.average([atom.position[2] for atom in sf])
#zgt = np.average([atom.position[2] for atom in gt])

xsf = np.average([atom.position[0] for atom in sf])
ysf = np.average([atom.position[1] for atom in sf])
#xsf = 40.72 
#ysf = 40.85
#memb = u.select_atoms(sel_heads)
#zavg = np.average([atom.position[2] for atom in memb])
#zmembup = np.average([atom.position[2] for atom in memb if atom.position[2]>zavg]) - 0.0  # DIY
#zmembdn = np.average([atom.position[2] for atom in memb if atom.position[2]<zavg]) + 0.0   # DIY


ions = u.select_atoms(sel_ions)
nions = len(ions)
zmin = 1e100
zmax = -1e100
nframes = len(u.trajectory)
zr = np.empty([nframes, 2*nions])

f = 0
for ts in u.trajectory:
    j = 0
    for i in ions:
        x = i.position[0] - xsf
        y = i.position[1] - ysf
        z = i.position[2]
        if z > zmax:
            zmax = z
        if z < zmin:
            zmin = z
        zr[f][2*j] = z
        zr[f][2*j+1] = math.sqrt(x*x+y*y)
        j += 1
    f += 1

            
#print "set xlabel \"z (angstrom)\""
#print "set ylabel \"radius (angstrom)\""
#print "set arrow from %10.3f, graph 0 to %10.3f, graph 1 nohead" % (zmembup, zmembup)
#print "set arrow from %10.3f, graph 0 to %10.3f, graph 1 nohead" % (zmembdn, zmembdn)
#print "set arrow from %10.3f, graph 0 to %10.3f, graph 1 nohead" % (zsf, zsf)
#print "set arrow from %10.3f, graph 0 to %10.3f, graph 1 nohead" % (zgt, zgt)
#print "plot \"-\" w l"

#for j in range(nions):
#    for f in range(nframes):
#        print "%10.3f   %.10e" % (zr[f][2*j], zr[f][2*j+1]) 
#    print

for f in range(nframes):
    for j in range(nions):
        print "%10.3f   %.10e" % (zr[f][2*j], zr[f][2*j+1]) 
    print

#print "%10.3f   %.10e" % (zmin, rad) 
#print "%10.3f   %.10e" % (zmax, rad) 
#print "e"

#for f in range(nframes):
#    for j in range(nions):
#        sys.stderr.write(" %10.3f" % zr[f][2*j])
#        sys.stderr.write(" %.10e"  % zr[f][2*j+1])
#    sys.stderr.write("\n")
#
