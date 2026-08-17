import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.close('all')
plt.style.use('seaborn-v0_8')

b_print = True
b_snow_depth = False

src = os.environ['HOME'] + '/bwSyncShare/Data/2024-Snow_sampling/2024-snow_sampling.ods'

locations = ('Austre Brøggerbreen', 'Gruvebadet', 'Austre Lovénbreen')
sheets = ('0418-broe', '0423-gruv', '0427-alov')
colors = ('#cf524e', 'steelblue', '#B8860B')
markers = ('o', 's', '^')
lines = ('-', ':', '--')
# Read data from sheets
data = {}
for each, ihead in zip(sheets,(4,8,10)):
    data.update({each:pd.read_excel(src, sheet_name=each, header=ihead,)})

kg = 1e3 #[g]
cm3 = (1e2)**3 # [m3]
snow_density = (data['0423-gruv']['Mass (g)']-141)*10 # mass -> density
max_depth = (int(data['0418-broe']['Depth'][0][:3]),
             data['0423-gruv']['Depth from'][0],
             int(data['0427-alov']['Depth'][1][:3]))

# Data to plot
depth = (np.concatenate(((max_depth[0]-pd.eval(data['0418-broe']['Depth'][0])*0.5,), (data['0418-broe']['Depth'][1:]).to_list())), (data['0423-gruv']['Depth from'])-(data['0423-gruv']['Depth from']-data['0423-gruv']['Depth to'])*0.5, np.concatenate(((max_depth[2]-pd.eval(data['0427-alov']['Depth'][1])*0.5,), (data['0427-alov']['Depth'][2:]).to_list())))

bromide = (data['0418-broe']['Br- (µmol/L) estimate from plot'], data['0423-gruv']['Br- (µmol/L) estimate from plot'], data['0427-alov']['Br- estimate from plot'][1:])
rel_bromide = (data['0418-broe']['nss-Br-/Br- estimate from plot'], data['0423-gruv']['nss-Br-/Br- estimate from plot'], data['0427-alov']['nss-Br-/Br- estimate from plot'][1:])

# Plot it
# Density
fig1, axd = plt.subplots(1,1)

for i, ixdata, iydata in zip(np.arange(0,2), (data['0418-broe']['Density (g/cm3)']/kg*cm3, snow_density), 
                             (data['0418-broe']['Depth from (cm)']-(data['0418-broe']['Depth from (cm)']-data['0418-broe']['Depth to (cm)'])*0.5, (data['0423-gruv']['Depth from'])-(data['0423-gruv']['Depth from']-data['0423-gruv']['Depth to'])*0.5)):
    axd.plot(ixdata, iydata,
         color=colors[i], ls=lines[i], marker=markers[i], label=locations[i])

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

for i, ixdata, iydata in zip(np.arange(0,2), 
                             (data['0418-broe']['Temperature (°C)'][1:], data['0423-gruv']['Temp (degC)'], data['0427-alov']['Temperature'][2:]), 
                             (data['0418-broe']['Depth (cm)'][1:], (data['0423-gruv']['Depth from'])-(data['0423-gruv']['Depth from']-data['0423-gruv']['Depth to'])*0.5, data['0427-alov']['Depth'][2:])):
    axt.plot(ixdata, iydata,
             color=colors[i], ls=lines[i], marker=markers[i], label=locations[i])

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
rel_error_x = 0.01

for i, ixdata, iydata in zip(np.arange(0,3), bromide, depth):
    axb.errorbar(ixdata, iydata, 
          xerr=ixdata*rel_error_x,
          ecolor=colors[i], color=colors[i], ls=lines[i], marker=markers[i], label=locations[i])

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

for i, izdata, iydata, ixdata in zip(np.arange(0,3), rel_bromide, depth, bromide):
    axbh.errorbar(izdata, iydata, 
          #xerr=((izdata/ixdata**2*rel_error_x)**2+(1/ixdata*rel_error_x)**2)**0.5,
          ecolor=colors[i], color=colors[i], ls=lines[i], marker=markers[i], label=locations[i])

# Set axes
# Indicate ground
axbh.axhspan(ymin,0, hatch='/', facecolor='none', edgecolor='black')

axbh.set_xlabel('$\\frac{\mathrm{[Br^--nss]}}{\mathrm{[Br^-]}}$', size=16)
axbh.set_ylabel('Height ($\mathrm{cm}$)', size=16)
axbh.tick_params(axis='both', which='major', labelsize=14)
axbh.set_ylim(ymin,)
if b_print:
    axbh.set_title('(a)', loc='left', x=-0.1, y=1, size=20)

axbh.legend(fontsize=12)
plt.tight_layout()

# Bromide enhancement relative height
fig5, axbhh = plt.subplots(1,1)

for i, izdata, iydata, ixdata, imaxd in zip(np.arange(0,3), rel_bromide, depth, bromide, max_depth):
    axbhh.errorbar(izdata, iydata/imaxd, 
          #xerr=((izdata/ixdata**2*rel_error_x)**2+(1/ixdata*rel_error_x)**2)**0.5,
          ecolor=colors[i], color=colors[i], ls=lines[i], marker=markers[i], label=locations[i])

# Set axes
# Indicate ground
ymin = -0.01
axbhh.axhspan(ymin,0, hatch='/', facecolor='none', edgecolor='black')

axbhh.set_xlabel('$\\frac{\mathrm{[Br^--nss]}}{\mathrm{[Br^-]}}$', size=16)
axbhh.set_ylabel('$\\frac{\mathrm{h}}{\mathrm{h_{max}}}$', size=16)
axbhh.tick_params(axis='both', which='major', labelsize=14)
axbhh.set_ylim(ymin,)
axbhh.axvline(0, color='white', lw=3, zorder=0)
if b_print:
    axbhh.set_title('(b)', loc='left', x=-0.1, y=1, size=20)

axbhh.legend(fontsize=12)
plt.tight_layout()

# Show it
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
fig5.savefig('./plots/2024-snowpits-bromide_enhancement_rel_height.%s' % (postfix))