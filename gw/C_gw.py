#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GW calculation of diamond

Note: a set of small parameters are used in this tutorial script.
Convergence, e.g. with respect to ecut, nbands, kmesh, frequency grids
and GW0 iterations are not tested.
"""

# load basic modules
from ase.build import bulk
from gpaw import GPAW

# the atomic model and file names
atms = bulk('C', 'diamond', a=3.567)
kx = 8
gpwscf = 'C_gs.gpw'
gpwfull = 'C_gs_full.gpw'
gwfn = f'C_g0w0-k{kx}-ecut100'

def gw_step1_scf(atms, gpw):
    """Step 1: SCF calculation

    Args:
        gpw: the name of gpw data file
    """
    from gpaw import FermiDirac
    from gpaw.wavefunctions.pw import PW

    c = GPAW(mode=PW(400), xc='PBE',
             kpts={'size': (kx, kx, kx), 'gamma': True},
             convergence={'energy': 1e-8}, # a tight convergence for accurate wfc
             occupations=FermiDirac(0.001),
             txt='gs.txt')
    atms.calc = c
    # run the SCF
    atms.get_potential_energy()
    c.write(gpw)

def gw_step2_nscf_empty_states(gpwscf, gpwfull):
    """Step 2: non-self-consistent calculation for all empty states

    Args:
        gpwscf: the name of SCF gpw data file for input
        gpwfull: the name of gpw data file for full bands output
    """
    c = GPAW(gpwscf, txt=None)
    c.diagonalize_full_hamiltonian()
    c.write(gpwfull, mode='all')

def gw_step3_gw(gpwfull, fn, nblocks=1):
    """Step 3: the GW calculation

    Args:
        gpwfull: the name of gpw data file for full bands input
        fn: the prefix of all GW output files
    """
    from gpaw.response.g0w0 import G0W0
    gw = G0W0(calc=gpwfull, bands=(0, 8),
              nbands=144, # number of bands used in sum of states
              ecut=100,   # cut-off energy for response/dielectric matrix
              nblocks=nblocks,
              filename=fn)
    result = gw.calculate()

if __name__ == "__main__":
    # the real work starts here
    # you may do step by step by commenting out the other steps
    gw_step1_scf(atms, gpwscf)
    gw_step2_nscf_empty_states(gpwscf, gpwfull)
    gw_step3_gw(gpwfull, gwfn)

    ## For nblocks test
    #for nb in [1, 2, 4]:
    #    gw_step3_gw(gpwfull, f'C_nblocks_{nb}', nblocks=nb)

