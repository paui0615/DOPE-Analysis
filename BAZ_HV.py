import matplotlib as mpl
mpl.use('TkAgg')
import os
import sys
import matplotlib.pylab as plt
import math
import matplotlib
import numpy as np
import datetime
from collections import defaultdict
import time
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist

rain=[]
rain_time=[]
f=open('/raid1/WATER/RAIN_1DAY/C1V231_rain.txt').readlines()

date1=datetime.datetime.strptime('20210101','%Y%m%d')
dd1=mdates.date2num(date1)
date2=datetime.datetime.strptime('20211231','%Y%m%d')
dd2=mdates.date2num(date2)

for i in range(len(f)):
    t=f[i].split()[2]
    d2=datetime.datetime.strptime(t, '%Y%m%d')
    date=mdates.date2num(d2)
    if date>dd1 and date<dd2:
        rain_time.append(date)
        rain.append(float(f[i].split()[3]))
BWl=[]
path=os.listdir('/raid1/Chulin_data/Groundwater_NCKU/')
for a in path:
    if len(a.split('_')) != 2:
        BWl.append(a)

gw_time=defaultdict(list)
gw=defaultdict(list)
for bw in BWl:
    bwn=bw.split('_')[0]
    f=open('/raid1/Chulin_data/Groundwater_NCKU/'+bw).readlines()
    for i in range(len(f)):
        t=f[i].split()[0]
        d2=datetime.datetime.strptime(t, '%Y-%m-%d')
        date=mdates.date2num(d2)
        if date>dd1 and date<dd2:
            gw_time[bwn].append(date)
            gw[bwn].append(float(f[i].split()[2]))



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

#-------------------------------------------------------------------------------------------


dop_threshold = 0.9  #0.9

hv_dic  = defaultdict(list)
baz_dic = defaultdict(list)
baz_all = []
freq_dic = defaultdict(list)
count = defaultdict(list)
path=os.listdir('./allsta_asc_202105-08')

for fl in path:
    cl=fl.split('_')[3]
    lines = open('./allsta_asc/total_chulin_all_'+cl+'_wlen8.asc').readlines()
    lines.append('0 0 0 0 0 0') 
    hv_dic  = defaultdict(list)
    baz_dic = defaultdict(list)
    baz_all = []
    freq_dic = defaultdict(list)
    count = defaultdict(list)
    for i in range(0,len(lines)):
        if len(lines[i].split()) == 6:
            if lines[i].split()[0]==str(0):
                break
            else:
                date=int(lines[i].split()[1])
                n=1
                num=0
                while len(lines[i+n].split()) !=6:
                    freq = float(lines[i+n].split()[1])                   
                    baz=float(lines[i+n].split()[0])
                    dop=float(lines[i+n].split()[2])
                    baz_dic[date].append([freq,baz])
                    if dop >= dop_threshold:
                        hv = float(lines[i+n].split()[5])
                        hv_dic[date].append([freq,hv])
                        num=num+1
                        if freq not in freq_dic[date]:
                            freq_dic[date].append(freq)
                    n=n+1
                count[date].append(num)

    lines2 = open('./allsta_asc_202105-08/total_chulin_5-8_'+cl+'_wlen8.asc').readlines()
    lines2.append('0 0 0 0 0 0')
    for i in range(0,len(lines2)):
        if len(lines2[i].split()) == 6:
            if lines2[i].split()[0]==str(0):
                break
            else:
                date=int(lines2[i].split()[1])
                n=1
                num=0
                while len(lines2[i+n].split()) !=6:
                    freq = float(lines2[i+n].split()[1])
                    baz=float(lines2[i+n].split()[0])
                    dop=float(lines2[i+n].split()[2])
                    baz_dic[date].append([freq,baz])
                    if dop >= dop_threshold:
                        hv = float(lines2[i+n].split()[5])        
                        hv_dic[date].append([freq,hv])
                        num=num+1
                        if freq not in freq_dic[date]:
                            freq_dic[date].append(freq)
                #print(n)
                    n=n+1
                count[date].append(num)

    lines3 = open('./allsta_asc_202108-12/total_chulin_8-12_'+cl+'_wlen8.asc').readlines()
    lines3.append('0 0 0 0 0 0')
    for i in range(0,len(lines3)):
        if len(lines3[i].split()) == 6:
            if lines3[i].split()[0]==str(0):
                break
            else:
                date=int(lines3[i].split()[1])
                n=1
                num=0
                while len(lines3[i+n].split()) !=6:
                    freq = float(lines3[i+n].split()[1])
                    baz=float(lines3[i+n].split()[0])
                    dop=float(lines3[i+n].split()[2])
                    baz_dic[date].append([freq,baz])
                    if dop >= dop_threshold:
                        hv = float(lines3[i+n].split()[5])
                        hv_dic[date].append([freq,hv])
                        num=num+1
    
                        if freq not in freq_dic[date]:
                            freq_dic[date].append(freq)
                    n=n+1
                count[date].append(num)

    deltaE_f=[]
    deltaE_date=[]
    deltaE_dhv=[]
    deltaE_baz=[]
    for j in range(1,366):
        date1=j        
        T_list1=[]
        hv_median1=[]
        hv_freq1=[]
        hv_freq1 = defaultdict(list)
        baz_freq1 = defaultdict(list)
        freq_list=[]
        if date1 != 141:
            for freq in freq_dic[date1]:
                T=1/freq
                if T >= 0.125 and T <= 1.1:
                    for i in range(len(hv_dic[date1])):
                        if hv_dic[date1][i][0]==freq:
                            hv_freq1[freq].append(hv_dic[date1][i][1])
                            baz_freq1[freq].append(baz_dic[date1][i][1])
                            if freq not in freq_list:
                                freq_list.append(freq)

        T_list=[]
        hv_median2=[]
        hv_freq2=[]
        hv_freq2 = defaultdict(list)
        for f in sorted(freq_list):
            if hv_freq1[f]:
                hv1=np.median(hv_freq1[f])
                baz=np.median(baz_freq1[f])
                d=j
                d2=datetime.datetime.strptime('21'+str(d), '%y%j') 
            
                date=mdates.date2num(d2)       
        
                deltaE_date.append(date)
                deltaE_f.append(f)
                deltaE_dhv.append(hv1)
                deltaE_baz.append(baz)
                T_list.append(1/f)

    all_date=[]
    count2=[]
    count2_date=[]
    for i in range(1,366):
        d=i
        d2=datetime.datetime.strptime('21'+str(d), '%y%j')
        date=mdates.date2num(d2)
        all_date.append(date)
        num=0
        for j in range(len(count[i])):
            num=num+count[i][j]
        if num !=0:
            count2.append(num)
            count2_date.append(date)




    deltaE_baz2=[]
    for i in range(len(deltaE_baz)):
        if deltaE_baz[i]<0.0:
            deltaE_baz2.append(deltaE_baz[i]+360.0)
        else:
            deltaE_baz2.append(deltaE_baz[i])
    
    cm = plt.cm.get_cmap('coolwarm_r')
    fig = plt.figure(1,figsize=(20,12))
    fig.subplots_adjust(wspace=1.)
    ax1 = plt.subplot2grid((7, 10), (0, 0), colspan=9, rowspan=1)  # count
    ax2 = plt.subplot2grid((7, 10), (1, 0), colspan=9, rowspan=3)  # Ellip.
    ax3 = plt.subplot2grid((7, 10), (4, 0), colspan=9, rowspan=3)  # BAZ
    ax4 = plt.subplot2grid((7, 10), (1, 9), colspan=1, rowspan=3)  # Ellip. colorbar
    ax5 = plt.subplot2grid((7, 10), (4, 9), colspan=1, rowspan=3)  # BAZ colorbar

    ax1.plot(count2_date,count2,'-',color='black')
    ax1.set_ylabel('Counts',fontsize=14)
    ax1.set_title(cl,fontsize=18)
    #for i in range(len(deltaE)):
    ax2.scatter(deltaE_date,deltaE_f,c=deltaE_dhv,marker='s',s=12,vmin=0.5,vmax=2.0,cmap=cm)
    ax2.set_xlabel('Time(date)',fontsize=16)
    ax2.set_ylabel('Frequency(Hz)',fontsize=16)
    ax2.set_ylim(0.8,8.1)
    ax2.set_xlim([all_date[0], all_date[121]])

    m1=plt.cm.ScalarMappable(cmap=cm)
    m1.set_array(deltaE_dhv)
    m1.set_clim(0.5,2.0)
    clb=plt.colorbar(m1,ax=ax4, boundaries=np.linspace(0.5,2.0,21),fraction=0.3,pad=0.005)
    clb.ax.set_title('H/V',fontsize=14)



    ax3.scatter(deltaE_date,deltaE_f,c=deltaE_baz2,marker='s',s=12,vmin=0.0,vmax=360.0)
    ax3.set_xlabel('Time(date)',fontsize=16)
    ax3.set_ylabel('Frequency(Hz)',fontsize=16)
    ax3.set_xlim([all_date[0], all_date[121]])
    ax3.set_ylim(0.8,8.1)
    ax3.xaxis.set_major_locator(mdates.MonthLocator())
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    for label in ax3.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')

    m2=plt.cm.ScalarMappable()
    m2.set_array(deltaE_baz2)
    m2.set_clim(0,360.0)
    clb=plt.colorbar(m2,ax=ax5, boundaries=np.linspace(0.0,360.0,19),fraction=0.3,pad=0.005)
    clb.ax.set_title('BAZ',fontsize=14)
    ax4.axis('off')
    ax5.axis('off')
    ax1.axes.xaxis.set_visible(False)
    ax2.axes.xaxis.set_visible(False)
    ax1.set_xlim([all_date[0], all_date[121]])
    ax2.set_xlim([all_date[0], all_date[121]])
    ax3.set_xlim([all_date[0], all_date[121]])



    plt.savefig('BAZ_plot/'+cl+'_bazandhv_202101-04.png')

