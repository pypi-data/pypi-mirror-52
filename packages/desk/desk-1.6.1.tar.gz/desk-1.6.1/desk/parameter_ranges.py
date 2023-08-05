import astropy.units as u
import collections
import copy
import fnmatch
import importlib
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pdb
import pylab
import shutil
import time
from astropy.table import Table, Column, vstack
from astropy.units import astrophys
from desk import config
from numpy import ndarray

plt.rc('text', usetex=True)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'


def create_par():
    counter = 0
    input_file = Table.read('fitting_plotting_outputs.csv')
    model = input_file['grid_name'][0]
    full_path = str(__file__.replace('parameter_ranges.py', ''))
    par = Table.read(full_path + 'models/' + model + '_outputs.csv')

    for i in par.colnames:
        if fnmatch.fnmatch(par[i].dtype.str, '<U*'):
            par.remove_column(i)
        else:
            par.rename_column(i, i.replace('_', ' '))

    if len(par.colnames) > 18:
        par = par[par.colnames[:17]]

    if len(par.colnames) < 8:
        fig, axs = plt.subplots(math.ceil(len(par.colnames)), 1, figsize=(8, 10))
        plt.subplots_adjust(wspace=0, hspace=0.5)
    else:
        fig, axs = plt.subplots(math.ceil(len(par.colnames)), 1, figsize=(5, 10))
        plt.subplots_adjust(wspace=0, hspace=1)

    axs = axs.ravel()

    axs[0].set_title('Model grid: ' + model, size=20)

    for col in par.colnames:
        par_min = np.min(par[col])
        par_max = np.max(par[col])
        axs[counter].scatter(par[col], [0] * len(par), marker='|', alpha=0.3, c='royalblue')
        range_min = par_min - ((par_max - par_min) * 0.1)
        range_max = par_max + (par_max - par_min) * 0.1
        if range_min != range_max:
            axs[counter].set_xlim(range_min, range_max)
        elif par_min == 0 and par_max == 0:
            axs[counter].set_xlim(-0.9, 0.9)
        else:
            axs[counter].set_xlim(range_min * 0.6, range_min * 1.4)
        # print(str(par_min) + ' : ' + str(par_max))
        axs[counter].set_ylabel(col)
        axs[counter].set_yticklabels([])
        axs[counter].set_yticks([])
        counter += 1
    fig.savefig('parameter_ranges_' + model + '.png', dpi=200, bbox_inches='tight')


if __name__ == '__main__':
    create_par()
