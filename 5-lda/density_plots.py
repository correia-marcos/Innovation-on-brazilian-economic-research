"""
Script to make plot of inovation, transience and resonance.

Script aparently complex, but is easy.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

%matplotlib inline

mpl.rcParams['axes.labelsize'] = 10
mpl.rcParams['axes.titlesize'] = 11
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['legend.fontsize'] = 'small'
mpl.rcParams['font.family'] = 'serif'


local = 'C:\\Users\\Usuário\\Projects\\monografia\\dados\\data_final'
NTR_df = pd.read_pickle(f'{local}\\data_KLDv3.pkl')

NTR_df.columns = ['Novelty', 'Transience', 'Resonance']

centininch = 2.54
inchincent = .3937


def centtoinch(cents):
    """Cents to inch."""
    return .3937*cents


def inchtocent(inches):
    """Inch to cent."""
    return 2.54*inches


figsize = (centtoinch(15), 2.8)
fig = plt.figure(figsize=figsize)


def plot_quants_2Dhist(quants, NTR_df, ax, xbins, ybins, make_cbar=True,
                       cbar_axis=False, cbar_orientation='vertical',
                       colorvmax=None):
    """Plota em 2h (histogramas)."""
    q0 = NTR_df[quants[0]]
    q1 = NTR_df[quants[1]]

    q0bins = xbins
    q1bins = ybins

    H, xedges, yedges = np.histogram2d(q0.values,
                                       q1.values,
                                       bins=[q0bins, q1bins])

    # H needs to be rotated and flipped
    H = np.rot90(H)
    H = np.flipud(H)

    # Mask zeros
    Hmasked = np.ma.masked_where(H == 0, H)  # Mask pixels with a value

    # Plot 2D histogram using pcolor
    if colorvmax:
        usemax = colorvmax
    else:
        usemax = H.max()
    pcolm = ax.pcolormesh(xedges, yedges, Hmasked,
                          norm=mpl.colors.LogNorm(vmin=1, vmax=usemax))

    if make_cbar:
        if cbar_axis:
            cbar = fig.colorbar(pcolm, cax=cbar_axis,
                                orientation=cbar_orientation)
        else:
            cbar = fig.colorbar(pcolm, ax=ax, orientation=cbar_orientation)
        cbar.ax.set_ylabel('counts')

    ax.set_xlabel(quants[0])
    ax.set_ylabel(quants[1])

    if make_cbar:
        return H, cbar
    else:
        return H

# =============================================================================
# Plots
# =============================================================================


# fig.add_axes([0.1, 0.19, 0.4, 0.72])
ax = fig.add_axes([0.28, 0.42, 0.44, 0.792])

cbaxes = fig.add_axes([0.55, 0.53, 0.02, 0.2])

quants = ['Novelty', 'Transience']

xbins = np.linspace(0, 5, 50)
ybins = np.linspace(0, 5, 50)

H, cbar = plot_quants_2Dhist(quants, NTR_df, ax, xbins, ybins,
                             make_cbar=True, cbar_axis=cbaxes,
                             cbar_orientation='vertical')
cbar.ax.set_ylabel('')
cbar.ax.set_xlabel('counts', fontsize=7)
cbar.ax.xaxis.set_label_position('bottom')
cbar.ax.yaxis.set_ticks_position('left')
cbar.ax.tick_params(labelsize=7)

# Identity (x=y) line
ax.plot([0, 4], [0, 4], 'k--', linewidth=1.5)

ax.legend([mpl.lines.Line2D([0], [0], color='k', linewidth=1.5,
                            linestyle='--')],
          ['x=y'],
          loc='upper center', fontsize=8, ncol=2, handlelength=2.7)

ax.set_ylabel(r'Transitoriedade  $\mathcal{T}$')
ax.set_xlabel(r'Novidade $\mathcal{N}$')

ax.set_title('Transitoriedade v. Novidade')

ax.set_aspect('equal')

# Hide the right and top spines.
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# Show ticks only on the left and bottom spines.
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Limit spine range
ax.spines['left'].set_bounds(0, 4)
ax.set_yticks([0, 1, 2, 3, 4])
ax.spines['bottom'].set_bounds(0, 4)
ax.set_xticks([0, 1, 2, 3, 4])

ax.set_ylim(0, 5)
ax.set_xlim(0, 5)


# =============================================================================
# Outro plot
# =============================================================================

# Plot Reson v. Novelty
# ([0.2, 0.29, 0.44, 0.792])
ax = fig.add_axes([0.8, 0.45, 0.44, 0.792])

cbaxes = fig.add_axes([1.2, 0.53, 0.02, 0.2])

quants = ['Novelty', 'Resonance']

xbins = np.linspace(0, 6, 40)
ybins = np.linspace(-2, 2, 40)

H, cbar = plot_quants_2Dhist(quants, NTR_df, ax, xbins, ybins,
                             make_cbar=True, cbar_axis=cbaxes,
                             cbar_orientation='vertical')
cbar.ax.set_ylabel('')
cbar.ax.set_xlabel('counts', fontsize=7)
cbar.ax.xaxis.set_label_position('bottom')
cbar.ax.yaxis.set_ticks_position('left')
cbar.ax.tick_params(labelsize=7)

ax.axhline(color='k', linewidth=1.5, linestyle=':')

ax.set_xlim(-1, 6)
ax.set_ylim(-1, 1.5)

# Hide the right and top spines.
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# Show ticks only on the left and bottom spines.
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Limit spine range
ax.spines['left'].set_bounds(-1, 1)
ax.set_yticks([-1, 0, 1])
ax.spines['bottom'].set_bounds(0, 6)
ax.set_xticks([0, 2, 4, 6])

ax.set_ylabel(r'Ressonância $\mathcal{R}}$')
ax.set_xlabel(r'Novidade $\mathcal{N}$')

_ = ax.set_title('Ressonância v. Novidade')
plt.plot()

os.chdir('C:\\Users\\Usuário\\Projects\\monografia\\dados')
fig.savefig('teste.png', dpi=120)
