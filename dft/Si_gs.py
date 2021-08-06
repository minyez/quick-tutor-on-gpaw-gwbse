#!/usr/bin/env python3
"""Perform standard ground state calculation (with plane wave basis)
"""
from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac

atms = bulk('Si', 'diamond', 5.43)
c = GPAW(mode=PW(400), xc='PBE', # basis and functional
         kpts={'size': (8, 8, 8), 'gamma': True}, # k-points setup
         eigensolver='dav', # 'dav' for Davidson quasi-Newton and 'cg' for CG
         random=False,     # random guess (needed if many empty bands required)
         occupations=FermiDirac(0.01),
         txt='Si_gs.txt')
atms.calc = c
atms.get_potential_energy()
c.write('Si_gs.gpw')

