#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BSE calculation of silicon

Note: a set of small parameters are used in this tutorial script.
Convergence are not tested.
"""

# load basic modules
from ase.build import bulk
from gpaw import GPAW

# you may need to increase kx (and kxscf) to obtain converged spectra
kx = 8
kxscf = 8

def bse_step1_scf(atms, gpw):
    """Step 1: SCF calculation

    Args:
        gpw: the name of gpw data file
    """
    from gpaw import FermiDirac
    from gpaw.wavefunctions.pw import PW

    c = GPAW(mode=PW(250), xc='PBE', # a rather small cutoff
             kpts={'size': (kxscf, kxscf, kxscf), 'gamma': True},
             convergence={'energy': 1e-8}, # a tight convergence for accurate wfc
             occupations=FermiDirac(0.001),
             txt='gs.txt')
    atms.calc = c
    # run the SCF
    atms.get_potential_energy()
    c.write(gpw)

def bse_step2_nscf_empty_states(gpwscf, gpwfull, kx=kxscf):
    """Step 2: non-self-consistent calculation for all empty states

    Args:
        gpwscf: the name of SCF gpw data file for input
        gpwfull: the name of gpw data file for full bands output
    """
    if kx == kxscf:
        c = GPAW(gpwscf, txt=None)
    else:
        c = GPAW(gpwscf, txt=None, fixdensity=True,
                 kpts={'size': (kx, kx, kx), 'gamma': True})
    c.diagonalize_full_hamiltonian()
    c.write(gpwfull, mode='all')

def bse_step3_gw(gpwfull, gwfn, nblocks=1):
    """Step 3: the GW calculation

    Args:
        gpwfull: the name of gpw data file for full bands input
        gwfn: the prefix of all GW output files
    """
    from gpaw.response.g0w0 import G0W0
    gw = G0W0(calc=gpwfull, bands=(1, 7), # 6 bands, 3 occupied and 3 empty
              nbands=144, # number of bands used in sum of states
              ecut=50,   # cut-off energy for response/dielectric matrix
              nblocks=nblocks,
              filename=gwfn)
    result = gw.calculate()

def bse_step4_bse(gpw, gwfn, bsefn):
    """Step 4: the BSE calculation

    Args:
        gpw: the name of gpw data file to find KS states
        gwpckl: the filename of GW
        bsefn: the prefix of all GW output files
    """
    import pickle
    import numpy as np
    from gpaw.response.bse import BSE

    qp = pickle.load(open(f'{gwfn}_results.pckl', 'rb'))['qp']
    # initialize BSE object
    bse = BSE(gpw, ecut=20,
              gw_skn=qp[:, :, :],
              valence_bands=[1, 2, 3],
              conduction_bands=[4, 5, 6],
              nbands=48, mode='BSE', txt=f'{bsefn}.txt')

    # start real work
    bse.get_dielectric_function(q_c=[0.0, 0.0, 0.0], eta=0.05,
                                write_eig=f"eig-Gamma_{bsefn}.dat",
                                w_w=np.linspace(0, 10, 2001),
                                filename=f"dielec-Gamma_{bsefn}.csv")


if __name__ == "__main__":
    # the atomic model and file names
    atms = bulk('Si', 'diamond', 5.43)
    gpwscf = 'Si_gs.gpw'
    gpwfull = f'Si_gs_full-k{kx}.gpw'
    gwfn = f'Si_g0w0-k{kx}-ecut50'
    bsefn = f'Si_bse-k{kx}-ecut20'

    # the real work starts here
    # you may do step by step by commenting out the other steps
    bse_step1_scf(atms, gpwscf)
    bse_step2_nscf_empty_states(gpwscf, gpwfull)
    bse_step3_gw(gpwfull, gwfn)
    bse_step4_bse(gpwfull, gwfn, bsefn)

