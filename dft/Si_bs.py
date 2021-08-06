#!/usr/bin/env python3
"""Band structure of Si

Calculate the band structure of Si along high symmetry directions
Brillouin zone
"""
from gpaw import GPAW

# Restart from the ground state
c = GPAW('Si_gs.gpw', # read GS data file
         nbands=16,   # number of bands to calculate
         fixdensity=True, # non-SCF with fixed density
         symmetry='off',
         kpts={'path': 'GXWKL', 'npoints': 60}, # kpath description
         convergence={'bands': 8},
         txt='Si_bs.txt')

c.get_potential_energy()
c.write('Si_bs.gpw')
# plot the band, matplolib required
bs = c.band_structure()
bs.plot(filename='Si_bs.png', emax=16.0, emin=-4.0)
