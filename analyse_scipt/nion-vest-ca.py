#!/usr/bin/python

import re, sys, math
import MDAnalysis
import numpy as np

sel_ions = "name D0"                   # DIY

top = sys.argv[1]
trj = sys.argv[2]
#NDIV = int(sys.argv[3])
#rad = float(sys.argv[4])
NDIV = 160
rad = 15
crad = 5

u = MDAnalysis.Universe(top, trj)

sf = u.select_atoms("resid 226 518 810 1102 and name O")
zsf = np.average([atom.position[2] for atom in sf])
xsf = np.average([atom.position[0] for atom in sf])
ysf = np.average([atom.position[1] for atom in sf])

zup = 95
zdn = 15
vup = 75  # v --- vestibule
vdn = 72
uvup = 95
uvdn = 75  # uv --- upper vestibule
sfup = 72
sfdn = 55

ldiv = float(zdn - zup) / NDIV
ions = u.select_atoms(sel_ions)
nions = len(ions)
prof = [0.0]*NDIV

rad2 = rad*rad
crad2 = crad*crad
n_in_vestibule = 0
n_in_upper_vestibule = 0
n_in_central_vestibule = 0
n_in_central_sf = 0
n_in_sf = 0
for ts in u.trajectory:
    for i in ions:
        x = i.position[0] - xsf
        y = i.position[1] - ysf
        z = i.position[2]
        if z <= zup and z > zdn:
            if x*x + y*y < rad2:
                j = int(math.floor((z - zup)/ldiv))
                prof[j] += 1.0
                if z <= sfup and z > sfdn:
                    n_in_sf += 1.0
                    if x*x + y*y < crad2:
                        n_in_central_sf += 1.0
                elif z <= uvup and z > uvdn:
                    n_in_upper_vestibule += 1.0
                elif z <= vup and z > vdn:
                    n_in_vestibule += 1.0
                    if x*x + y*y < crad2:
                        n_in_central_vestibule += 1.0

nm = -1.0/(len(u.trajectory)*ldiv)
for j in range(NDIV):
    prof[j] *= nm
n_in_vestibule /= len(u.trajectory)
n_in_upper_vestibule /= len(u.trajectory)
n_in_central_vestibule /= len(u.trajectory)
n_in_central_sf /= len(u.trajectory)
n_in_sf /= len(u.trajectory)

print "# n_in_vestibule (up=%f, dn=%f, rad=%f) = %f" % (vup, vdn, rad, n_in_vestibule)
print "# n_in_upper_vestibule (up=%f, dn=%f, rad=%f) = %f" % (uvup, uvdn, rad, n_in_upper_vestibule)
print "# n_in_central_vestibule (up=%f, dn=%f, rad=%f) = %f" % (vup, vdn, crad, n_in_central_vestibule)
print "# n_in_sf (up=%f, dn=%f, rad=%f) = %f" % (sfup, sfdn, rad, n_in_sf)
print "# n_in_central_sf (up=%f, dn=%f, rad=%f) = %f" % (sfup, sfdn, crad, n_in_central_sf)
print "#set yrange [*:*] reverse"
print "#set logscale y"
print "set xlabel \"z (nm)\""
print "set ylabel \"residence time (arb. unit)\""
print "set arrow from %10.3f, graph 0 to %10.3f, graph 1 nohead" % (vup, vup)
print "set arrow from %10.3f, graph 0 to %10.3f, graph 1 nohead" % (vdn, vdn)
print "plot \"-\" w l"

for j in range(NDIV):
    print "%10.3f   %.10e" % (zup+j*ldiv, prof[j]) 
print "e"

