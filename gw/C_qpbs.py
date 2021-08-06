#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""script to draw PBE and GW bands along a kpath from GW calculations on a regular grids
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from gpaw.response.gw_bands import GWBands

gpwscf = 'C_gs.gpw'
# note that use a smaller kmesh (e.g. kx=4) will lead to worse band interpolation here
gwfn = 'C_g0w0-k8-ecut100'

L = np.array([0.5, 0.5, 0.5])
X = np.array([0.5, 0.5, 0.0])
G = np.array([0.0, 0.0, 0.0])
kpoints = np.array([L, G, X])
klabels = [r'$L$', r'$\Gamma$', r'$X$']

gwbands = GWBands(calc=gpwscf,
                  gw_file=f'{gwfn}_results.pckl',
                  kpoints=kpoints, bandrange=(0,8))
pbe = gwbands.get_gw_bands(nk_Int=50, dft=True, interpolate=True)
gw = gwbands.get_gw_bands(nk_Int=50, interpolate=True)

# extract 1D coordinates of kpath
x_x = gw['x_k']
# normalize
X = gw['X']/x_x[-1]
x_x /= x_x[-1]

# align VBM
ePBE_kn, eGW_kn = [d['e_kn'] - d['vbm'] for d in [pbe, gw]]

# plot with style
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
styles = [
          {'ls': '--', 'marker': '', 'color': 'k', "lw": 3},
          {'ls': '-', 'marker': '', 'color': '#393b79', "lw": 3},
         ]
for i, bands in enumerate([ePBE_kn, eGW_kn]):
    ax.plot(x_x, bands, **styles[i])

# draw energy zero
ax.axhline(0.0, color='k', linestyle=':', lw=2)
# legend
leg_handles = [mpl.lines.Line2D([], [], **style) for style in styles]
leg_labels = [r'PBE', r'G$_0$W$_0$']
ax.legend(leg_handles, leg_labels, fontsize=20)

# axis limits
ax.set_xlim(0, x_x[-1])
ax.set_ylim([-10, 20])
ax.set_ylabel('Energy (eV)', fontsize=24)

# draw special K points and lines
for p in X[:-1]:
    plt.axvline(p, color='#AAAAAA', ls='--', lw=2)
plt.xticks(X, klabels, fontsize=18)
plt.yticks(fontsize=17)

fig.tight_layout()
plt.savefig('C_bands.png', dpi=300)
#plt.show()

