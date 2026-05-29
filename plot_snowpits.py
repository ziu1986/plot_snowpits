import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.close('all')
plt.style.use('seaborn-v0_8')

b_print = False
b_snow_depth = False

src = os.environ['HOME'] + '/bwSyncShare/Data/2024-Snow_sampling/2024-snow_sampling.ods'

colors = ('#cf524e', 'steelblue', '#B8860B')
locations = ('Austre Brøggerbreen', 'Gruvebadet', 'Austre Lovénbreen')
sheets = ('0418-broe', '0423-gruv', '0427-alov')
data = {}
for each, ihead in zip(sheets,(4,8,10)):
    data.update({each:pd.read_excel(src, sheet_name=each, header=ihead,)})

kg = 1e3
cm3 = (1e2)**3
max_depth = (int(data['0418-broe']['Depth'][0][:3]),
             data['0423-gruv']['Depth from'][0],
             int(data['0427-alov']['Depth'][1][:3]))

# Plot it
# Density/Temperature
fig1, axs = plt.subplots(1,1)
axt = axs.twiny()

axs.plot(data['0418-broe']['Density (g/cm3)']/kg*cm3, data['0418-broe']['Depth from (cm)']-(data['0418-broe']['Depth from (cm)']-data['0418-broe']['Depth to (cm)'])*0.5, color='grey', marker='o')
axs.plot(data['0423-gruv']['Density (g)'], (max_depth[1]-data['0423-gruv']['Depth from'])+(data['0423-gruv']['Depth from']-data['0423-gruv']['Depth to'])*0.5, ls=':', color='grey', marker='s')
axt.plot(data['0418-broe']['Temperature (°C)'][1:], data['0418-broe']['Depth (cm)'][1:], color=colors[0], marker='o', label=locations[0])
axt.plot(data['0423-gruv']['Temp (degC)'], (max_depth[1]-data['0423-gruv']['Depth from'])+(data['0423-gruv']['Depth from']-data['0423-gruv']['Depth to'])*0.5, color=colors[1], ls=':', marker='s', label=locations[1])
axt.plot(data['0427-alov']['Temperature'][2:], data['0427-alov']['Depth'][2:], color=colors[2], ls='--', marker='^', label=locations[2])
axs.set_xlabel('$\\rho$ ($\mathrm{kg m^{-3}}$)', size=16, color='grey')
if b_snow_depth:
    axs.set_ylabel('Snow depth ($\mathrm{cm}$)', size=16)
    axs.invert_yaxis()
else:
    axs.set_ylabel('Snow height ($\mathrm{cm}$)', size=16)
axs.tick_params(axis='both', which='major', labelsize=14)
axs.tick_params(axis='x', colors='grey')
axt.set_xlabel('T ($\mathrm{^\circ C}$)', size=16)
axt.set_xlim(-13,0.5)
axt.grid(False)
axt.tick_params(axis='both', which='major', labelsize=14)

if b_print:
    axs.set_title('(a)', loc='left', x=-0.1, y=1, size=20)

axt.legend(fontsize=12)
plt.tight_layout()

# Bromide
fig2, axs2 = plt.subplots(1,1)

axs2.plot(data['0418-broe']['Br- (µmol/L) estimate from plot'], 
          np.concatenate(((pd.eval(data['0418-broe']['Depth'][0])*0.5,), (max_depth[0]-data['0418-broe']['Depth'][1:]).to_list())), color=colors[0], ls=':', marker='o', label=locations[0])
axs2.plot(data['0423-gruv']['Br- (µmol/L) estimate from plot'], (max_depth[1]-data['0423-gruv']['Depth from'])+(data['0423-gruv']['Depth from']-data['0423-gruv']['Depth to'])*0.5, color=colors[1], ls=':', marker='s', label=locations[1])
axs2.plot(data['0427-alov']['Br- estimate from plot'][1:], 
          np.concatenate(((pd.eval(data['0427-alov']['Depth'][1])*0.5,), (max_depth[2]-data['0427-alov']['Depth'][2:]).to_list())), ls=':', marker='^', color=colors[2], label=locations[2])

axs2.set_xlabel('$\mathrm{[Br^-]}$ ($\mathrm{\mu mol L^{-1}}$)', size=16)
if b_snow_depth:
    axs2.set_ylabel('Snow depth ($\mathrm{cm}$)', size=16)
    axs2.invert_yaxis()
else:
    axs2.set_ylabel('Snow height ($\mathrm{cm}$)', size=16)
axs2.tick_params(axis='both', which='major', labelsize=14)

if b_print:
    axs2.set_title('(b)', loc='left', x=-0.1, y=1, size=20)

axs2.legend(fontsize=12)
plt.tight_layout()

plt.show(block=False)

print("Background [Br-] (µmol/L) - mean - std")
print(locations[0], 
      data['0418-broe']['Br- (µmol/L) estimate from plot'][3:].mean(), 
      data['0418-broe']['Br- (µmol/L) estimate from plot'][3:].std())
print(locations[2], 
      data['0427-alov']['Br- estimate from plot'][6:].mean(), 
      data['0427-alov']['Br- estimate from plot'][6:].std())
print("BEE [Br-] (µmol/L) - mean - err")
print(locations[0], 
      np.mean(data['0418-broe']['Br- (µmol/L) estimate from plot'][:3]-data['0418-broe']['Br- (µmol/L) estimate from plot'][3:].mean()), 
      np.sqrt(np.std(data['0418-broe']['Br- (µmol/L) estimate from plot'][:3]-data['0418-broe']['Br- (µmol/L) estimate from plot'][3:].mean())**2+(data['0418-broe']['Br- (µmol/L) estimate from plot'][3:].std())**2))
print(locations[2], 
      np.mean(data['0427-alov']['Br- estimate from plot'][1:6]-data['0427-alov']['Br- estimate from plot'][6:].mean()), 
      np.sqrt(np.std(data['0427-alov']['Br- estimate from plot'][1:6]-data['0427-alov']['Br- estimate from plot'][6:].mean())**2+(data['0427-alov']['Br- estimate from plot'][6:].std())**2))


if b_print:
    postfix='pdf'
else:
    postfix='png'

fig1.savefig('./plots/2024-snowpits-temp-dens.%s' % (postfix))
fig2.savefig('./plots/2024-snowpits-bromide.%s' % (postfix))