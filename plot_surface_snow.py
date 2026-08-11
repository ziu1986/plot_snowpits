import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.close('all')
plt.style.use('seaborn-v0_8')

b_print = True
orig_units = False # if False mugg-1 is used
if orig_units:
    units = 1
    yunit_label = '$\mathrm{ppbm}$'
else:
    units = 1e-3
    yunit_label = '$\mathrm{\mu gg^{-1}}$'

src = os.environ['HOME'] + '/bwSyncShare/Data/2024-Snow_sampling/SurfaceSnow_Na+Br_2023-24.xlsx'

colors = ('steelblue', )
locations = ('Gruvebadet', )
sheets = ('AllSnow', )
data = {}

for each, ihead in zip(sheets,(0,)):
    data.update({each:pd.read_excel(src, sheet_name=each, header=ihead,)})

fig = []
for icolumn in ('Bromide', 'nss-Bromide', 'nss-Bromide/Bromide'):
    ifig, axs = plt.subplots(1,1, figsize=(12,6))
    xdata = data['AllSnow'].where(data['AllSnow']['Quality flag']==0)['Sampling date + time'].dropna()
    xdata_flagged = data['AllSnow'].where(data['AllSnow']['Quality flag']==666)['Sampling date + time'].dropna()
    if icolumn != 'nss-Bromide/Bromide':
        ydata = data['AllSnow'].where(data['AllSnow']['Quality flag']==0)[icolumn].dropna()*units
        ydata_flagged = data['AllSnow'].where(data['AllSnow']['Quality flag']==666)[icolumn].dropna()*units
    else:
        ydata = data['AllSnow'].where(data['AllSnow']['Quality flag']==0)['nss-Bromide'].dropna()/data['AllSnow'].where(data['AllSnow']['Quality flag']==0)['Bromide'].dropna()
        ydata_flagged = data['AllSnow'].where(data['AllSnow']['Quality flag']==666)['nss-Bromide'].dropna()/data['AllSnow'].where(data['AllSnow']['Quality flag']==666)['Bromide'].dropna()
    axs.plot(xdata, ydata, color=colors[0], ls=':', marker='s', label=locations[0])
    axs.scatter(xdata_flagged, ydata_flagged, color='red', ls='', marker='x', label='quality flagged')
        
    if icolumn == 'Bromide':
        axs.set_ylabel('$\mathrm{[Br^-]}$ (%s)' % yunit_label, size=16)
    elif icolumn == 'nss-Bromide':
        axs.set_ylabel('$\mathrm{[Br^--nss]}$', size=16)
        axs.axhline(0, color='white', lw=3, zorder=0)
    else:
        axs.set_ylabel('$\\frac{\mathrm{[Br^--nss]}}{\mathrm{[Br^-]}}$', size=16)
        axs.axhline(0, color='white', lw=3, zorder=0)

    axs.set_xlabel('Time', size=16)
    axs.tick_params(axis='both', which='major', labelsize=14)

    axs.legend(fontsize=16)
    plt.tight_layout()
    plt.show(block=False)
    fig.append(ifig)

if b_print:
    postfix='pdf'
else:
    postfix='png'

for ifig, ilabel in zip(fig, ('', 'nss-Br', 'rel_nss-Br')):
    ifig.savefig('./plots/2024-surface_snow-bromide%s.%s' % (ilabel, postfix))
