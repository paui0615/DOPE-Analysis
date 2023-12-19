import obspy
import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib
#import pylab
from scipy import signal      
import cmcrameri
import datetime
from matplotlib.dates import date2num
from obspy.core import UTCDateTime
import matplotlib.dates as mdates
from obspy.io.xseed import Parser
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange 
import matplotlib.ticker as tick
import math
import sys
from collections import defaultdict
import matplotlib.patches as patches


date1=datetime.datetime.strptime('20210101','%Y%m%d')
date2=datetime.datetime.strptime('20210102','%Y%m%d')
ddate=mdates.date2num(date1)-mdates.date2num(date2)


st = obspy.Stream()
st.clear()
MainPath = './'
RESP_Path = './RESP/'
OutFigPath = './PSD_figure/'
Component = ['HHZ']

clfile=os.listdir('./Chulin_bestmodel/fulllist/')
output=os.listdir('./PSD_figure')
clfile.append('CL07_full')
cltest=[]
for i in range(len(output)):
    cl=output[i].split('_')[0]
    if cl not in cltest:
        cltest.append(cl)
clfile2=[]
for i in range(len(clfile)):
    cln=clfile[i].split('_')[0]
    if cln not in cltest:
        clfile2.append(cln+'_full')

date1=datetime.datetime.strptime('20210725','%Y%m%d')
dd1=mdates.date2num(date1)
date2=datetime.datetime.strptime('20210825','%Y%m%d')
dd2=mdates.date2num(date2)
julian1=int(date1.strftime('%j'))
julian2=int(date2.strftime('%j'))

gpsl=['ZL02','ZL03']
gps=defaultdict(list)
gps_time=defaultdict(list)
gps_sig=defaultdict(list)
for sta in gpsl:
    f=open('/raid1/Chulin_data/GPS/'+sta+'.series').readlines()
    for i in range(len(f)):
        y=f[i].split()[11]
        m=f[i].split()[12].zfill(2)
        d=f[i].split()[13].zfill(2)
        Edis=f[i].split()[1]
        Edis_sig=f[i].split()[4]
        d2=datetime.datetime.strptime(y+m+d, '%Y%m%d')
        print(d2)
        date=mdates.date2num(d2)
        if date>dd1 and date<dd2:
            gps_time[sta].append(date)
            gps[sta].append(float(Edis)*1000.0)
            gps_sig[sta].append(Edis_sig)

rain=[]
rain_time=[]
f=open('/raid1/WATER/RAIN_1DAY/C1V231_rain.txt').readlines()
for i in range(len(f)):
    t=f[i].split()[2]
    d2=datetime.datetime.strptime(t, '%Y%m%d')
    date=mdates.date2num(d2)
    if date>dd1 and date<dd2:
        rain_time.append(date)
        rain.append(float(f[i].split()[3]))
clfile=['CL05','CL06','CL10','CL12','CL13','CL15','CL21']


WF=obspy.Stream()
Resp_Mode = 1

for cl in clfile:
    WF=obspy.Stream()
    missing_date=[]
    cln=cl
    for DIREC in Component:
        WF=obspy.Stream()

        for i in range(julian1,julian2):
            date=str(i).zfill(3)
            date_2=datetime.datetime.strptime('21'+str(date),'%y%j').date()
            d=mdates.date2num(date_2)

            RESP_Name = str(cln[0:2])+'_'+str(cln[2:4])+'.RESP'
            RESP_File = os.path.join(RESP_Path,RESP_Name)
            if not os.path.isfile('/raid1/Chulin_data/archive/2021/TW/'+cln+'/'+DIREC+'.D/TW.'+cln+'.00.'+DIREC+'.D.2021.'+str(date)):
                missing_date.append(d)


            try:
                WF += obspy.read('/raid1/Chulin_data/archive/2021/TW/'+cln+'/'+DIREC+'.D/TW.'+cln+'.00.'+DIREC+'.D.2021.'+str(date))
                WF.merge(method=1,fill_value='interpolate')
            except:
                pass

    tr=WF[0]
    if Resp_Mode == 0:
        print("No response correction")
        pass
    elif Resp_Mode == 1:
                ### Remove instrument response ###
        pre_filt = (0.05, 0.1, 30.0, 50.0)
                    #-- Remove mean
        tr.detrend(type='demean')
                      #-- Remove trend
        tr.detrend(type='linear')
                      #-- Read RESP file
        parser = Parser(RESP_Path + str(cln[0:2])+'_'+str(cln[2:4])+'.RESP')
                    #-- Calibration by RESP information
        tr.simulate(seedresp={'filename': parser, 'units': "VEL"},pre_filt=pre_filt)

    tr.taper(max_percentage=0.05, type='cosine', max_length=len(tr[0].data), side='both')
    time = tr.times("matplotlib")

    npts=len(tr.data)
    xd = range(1, npts + 1)
    dt = 0.01
    NFFT = int(math.pow(2,10))
    print(NFFT)
    num_overlap=NFFT/2
    Fs = tr.stats.sampling_rate
    x0 = np.arange(0, npts/Fs, np.round(dt,2))

    fig = plt.figure(1,figsize=(16,10))
    fig.subplots_adjust(wspace=1.)
    ax1 = plt.subplot2grid((5, 10), (0, 0), colspan=9, rowspan=3)  # Spec
    ax2 = plt.subplot2grid((5, 10), (0, 9), colspan=1, rowspan=3)  # spec.colorbar
    ax3 = plt.subplot2grid((5, 10), (3, 0), colspan=9, rowspan=1)  # Rain
    ax4 = plt.subplot2grid((5, 10), (4, 0), colspan=9, rowspan=1)  # GPS


    im=ax1.specgram(tr.data,NFFT=NFFT,Fs=Fs,noverlap=num_overlap,vmin=-250,vmax=-120,scale='dB',mode='magnitude', cmap='cmc.roma_r', xextent=(dd1,dd2))
    ax1.set_ylabel('Frequency [Hz]',fontsize=16)
    ax1.set_xlabel('Time [date]',fontsize=16)
    ax1.set_ylim(0.0,50.0)
    ax1.set_xlim(dd1,dd2)
    ax1.set_title(cln+'_Spectrogram',fontsize=20)

    cm = plt.cm.get_cmap('cmc.roma_r')
    m1=plt.cm.ScalarMappable(cmap=cm)
    m1.set_clim(-250.0,-120.0)
    clb=plt.colorbar(m1,ax=ax2, boundaries=np.linspace(-250.0,-120.0,21),fraction=0.3,pad=0.005)
    clb.ax.set_title('$(m$ $s^{-1})^2$ $/$ $Hz$')

    for i in range(len(missing_date)):
        ax1.add_patch(patches.Rectangle((missing_date[i],0.0),ddate,50.0,facecolor='white',fill=True))


    ax2.axis('off')
    ax1.axes.xaxis.set_visible(False)
    ax3.axes.xaxis.set_visible(False)

    ax3.plot(rain_time,rain,'-',color='blue')
    ax4.plot(gps_time[gpsl[0]],gps[gpsl[0]],'-',color='black')
    ax3.set_ylim(0, 400)
    ax4.set_ylim(-500, 0.0)
    ax3.set_ylabel('Precipitation (mm)',fontsize=10)
    ax4.set_ylabel('Displacement (mm)',fontsize=10)
    ax4.set_xlabel('Time [date]',fontsize=16)
    ax3.set_xlim(dd1,dd2)
    ax4.set_xlim(dd1,dd2)

    ax4.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    for label in ax4.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')


    plt.savefig('./PSD_figure/'+cln+'_Spectrogram_Lupit_50Hz.png')
    plt.close('all')
