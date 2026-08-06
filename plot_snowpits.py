import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.close('all')
plt.style.use('seaborn-v0_8')

b_print = True
b_snow_depth = False

src = os.environ['HOME'] + '/bwSyncShare/Data/2024-Snow_sampling/2024-snow_sampling.ods'

colors = ('#cf524e', 'steelblue', '#B8860B')
locations = ('Austre Brøggerbreen', 'Gruvebadet', 'Austre Lovénbreen')
sheets = ('0418-broe', '0423-gruv', '0427-alov')
data = {}
for each, ihead in zip(sheets,(4,8,10)):
    data.update({each:pd.read_excel(src, sheet_name=each, header=ihead,)})

kg = 1e3 #[g]
cm3 = (1e2)**3 # [m3]
snow_density = (data['0423-gruv']['Mass (g)']-141)*10 # mass -> density
max_depth = (int(data['0418-broe']['Depth'][0][:3]),
             data['0423-gruv']['Depth from'][0],
             int(data['0427-alov']['Depth'][1][:3]))

# Plot it
# Density
fig1, axd = plt.subplots(1,1)

# ABB
axd.plot(data['0418-broe']['Density (g/cm3)']/kg*cm3, 
         data['0418-broe']['Depth from (cm)']-(data['0418-broe']['Depth from (cm)']-data['0418-broe']['Depth to (cm)'])*0.5, 
         color=colors[0], marker='o', label=locations[0])
# G
axd.plot(snow_density, 
         (data['0423-gruv']['Depth from'])-(data['0423-gruv']['Depth from']-data['0423-gruv']['Depth to'])*0.5, 
         ls=':', color=colors[1], marker='s', label=locations[1])
# Indicate ground
ymin = axd.get_ylim()[0].round()
axd.axhspan(ymin,0, hatch='/', facecolor='none', edgecolor='black')
# Set axes
axd.set_ylabel('Height ($\mathrm{cm}$)', size=16)
axd.set_ylim(ymin,)
axd.tick_params(axis='both', which='major', labelsize=14)
axd.set_xlabel('$\\rho$ ($\mathrm{kg m^{-3}}$)', size=16)
if b_print:
    axd.set_title('(a)', loc='left', x=-0.1, y=1, size=20)

axd.legend(fontsize=12)
plt.tight_layout()

# Temperature
fig2, axt = plt.subplots(1,1)
# ABB
axt.plot(data['0418-broe']['Temperature (°C)'][1:], 
         data['0418-broe']['Depth (cm)'][1:], 
         color=colors[0], marker='o', label=locations[0])
# G
axt.plot(data['0423-gruv']['Temp (degC)'], 
         (data['0423-gruv']['Depth from'])-(data['0423-gruv']['Depth from']-data['0423-gruv']['Depth to'])*0.5, 
         color=colors[1], ls=':', marker='s', label=locations[1])
# ALB
axt.plot(data['0427-alov']['Temperature'][2:], 
         data['0427-alov']['Depth'][2:], 
         color=colors[2], ls='--', marker='^', label=locations[2])


# Temperature axis
# Indicate ground
axt.axhspan(ymin,0, hatch='/', facecolor='none', edgecolor='black')
# Set axes
axt.set_ylabel('Height ($\mathrm{cm}$)', size=16)
axt.set_ylim(ymin,)
axt.tick_params(axis='both', which='major', labelsize=14)
axt.set_xlabel('T ($\mathrm{^\circ C}$)', size=16)
axt.set_xlim(-13,0.5)
if b_print:
    axt.set_title('(b)', loc='left', x=-0.1, y=1, size=20)
axt.legend(fontsize=12)
plt.tight_layout()

# Bromide
fig3, axb = plt.subplots(1,1)

axb.plot(data['0418-broe']['Br- (µmol/L) estimate from plot'], 
          np.concatenate(((max_depth[0]-pd.eval(data['0418-broe']['Depth'][0])*0.5,), (data['0418-broe']['Depth'][1:]).to_list())), 
          color=colors[0], ls='-', marker='o', label=locations[0])
axb.plot(data['0423-gruv']['Br- (µmol/L) estimate from plot'], 
         (data['0423-gruv']['Depth from'])-(data['0423-gruv']['Depth from']-data['0423-gruv']['Depth to'])*0.5,  
          color=colors[1], ls=':', marker='s', label=locations[1])
axb.plot(data['0427-alov']['Br- estimate from plot'][1:], 
          np.concatenate(((max_depth[2]-pd.eval(data['0427-alov']['Depth'][1])*0.5,), (data['0427-alov']['Depth'][2:]).to_list())), 
          ls='--', marker='^', color=colors[2], label=locations[2])
# Set axes
# Indicate ground
axb.axhspan(ymin,0, hatch='/', facecolor='none', edgecolor='black')

axb.set_xlabel('$\mathrm{[Br^-]}$ ($\mathrm{\mu mol L^{-1}}$)', size=16)
axb.set_ylabel('Height ($\mathrm{cm}$)', size=16)
axb.tick_params(axis='both', which='major', labelsize=14)
axb.set_ylim(ymin,)
if b_print:
    axb.set_title('(c)', loc='left', x=-0.1, y=1, size=20)

axb.legend(fontsize=12)
plt.tight_layout()

# Bromide enhancement
fig4, axbh = plt.subplots(1,1)

axbh.plot(data['0418-broe']['nss-Br-/Br- estimate from plot'], 
          np.concatenate(((max_depth[0]-pd.eval(data['0418-broe']['Depth'][0])*0.5,), (data['0418-broe']['Depth'][1:]).to_list())), 
          color=colors[0], ls='-', marker='o', label=locations[0])
axbh.plot(data['0423-gruv']['nss-Br-/Br- estimate from plot'], 
         (data['0423-gruv']['Depth from'])-(data['0423-gruv']['Depth from']-data['0423-gruv']['Depth to'])*0.5,  
          color=colors[1], ls=':', marker='s', label=locations[1])
axbh.plot(data['0427-alov']['nss-Br-/Br- estimate from plot'][1:], 
          np.concatenate(((max_depth[2]-pd.eval(data['0427-alov']['Depth'][1])*0.5,), (data['0427-alov']['Depth'][2:]).to_list())), 
          ls='--', marker='^', color=colors[2], label=locations[2])
# Set axes
# Indicate ground
axbh.axhspan(ymin,0, hatch='/', facecolor='none', edgecolor='black')

axbh.set_xlabel('$\\frac{\mathrm{[Br^--nss]}}{\mathrm{[Br^-]}}$', size=16)
axbh.set_ylabel('Height ($\mathrm{cm}$)', size=16)
axbh.tick_params(axis='both', which='major', labelsize=14)
axbh.set_ylim(ymin,)
if b_print:
    axbh.set_title('', loc='left', x=-0.1, y=1, size=20)

axbh.legend(fontsize=12)
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

fig1.savefig('./plots/2024-snowpits-dens.%s' % (postfix))
fig2.savefig('./plots/2024-snowpits-temp.%s' % (postfix))
fig3.savefig('./plots/2024-snowpits-bromide.%s' % (postfix))
fig4.savefig('./plots/2024-snowpits-bromide_enhancement.%s' % (postfix))