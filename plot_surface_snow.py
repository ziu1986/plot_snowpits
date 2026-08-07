import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.close('all')
plt.style.use('seaborn-v0_8')

b_print = True

src = os.environ['HOME'] + '/bwSyncShare/Data/2024-Snow_sampling/SurfaceSnow_Na+Br_2023-24.xlsx'

colors = ('steelblue', )
locations = ('Gruvebadet', )
sheets = ('AllSnow', )
data = {}

for each, ihead in zip(sheets,(0,)):
    data.update({each:pd.read_excel(src, sheet_name=each, header=ihead,)})

fig, axs = plt.subplots(1,1, figsize=(12,6))
axs.plot(data['AllSnow'].where(data['AllSnow']['Quality flag']==0)['Sampling date + time'].dropna(), data['AllSnow'].where(data['AllSnow']['Quality flag']==0)['Bromide'].dropna(), color=colors[0], ls=':', marker='s', label=locations[0])
axs.scatter(data['AllSnow'].where(data['AllSnow']['Quality flag']==666)['Sampling date + time'].dropna(), data['AllSnow'].where(data['AllSnow']['Quality flag']==666)['Bromide'].dropna(), color='red', ls='', marker='x', label='quality flagged')

axs.set_ylabel('$\mathrm{[Br^-]}$ ($\mathrm{ppbm}$)', size=16)
axs.set_xlabel('Time', size=16)
axs.tick_params(axis='both', which='major', labelsize=14)

axs.legend(fontsize=16)
plt.tight_layout()
plt.show(block=False)

if b_print:
    postfix='pdf'
else:
    postfix='png'

fig.savefig('./plots/2024-surface_snow-bromide.%s' % (postfix))
