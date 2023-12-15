import matplotlib as mpl
mpl.use('Agg')
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


def ReadWeather():

    global rain
    global rain_time
    global temp
    global temp_time
    global wind
    global wind_time
    global gw
    global gw_time
    global gps
    global gps_time
    global gps_sig
    global BWl

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

    temp=[]
    temp_time=[]
    f=open('/raid1/WATER/TEMP_1DAY/C0V820_temp.txt').readlines()

    for i in range(len(f)):
        t=f[i].split()[2]
        d2=datetime.datetime.strptime(t, '%Y%m%d')
        date=mdates.date2num(d2)
        if date>dd1 and date<dd2:
            temp_time.append(date)
            temp.append(float(f[i].split()[3]))
    
    wind=[]
    wind_time=[]
    f=open('/raid1/WATER/WIND_1DAY/C0V820_wind.txt').readlines()

    for i in range(len(f)):
        t=f[i].split()[2]
        d2=datetime.datetime.strptime(t, '%Y%m%d')
        date=mdates.date2num(d2)
        if date>dd1 and date<dd2:
            wind_time.append(date)
            wind.append(float(f[i].split()[3]))

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
            date=mdates.date2num(d2)
            if date>dd1 and date<dd2:
                gps_time[sta].append(date)
                gps[sta].append(float(Edis)*1000.0)
                gps_sig[sta].append(Edis_sig)


#----------------------------------------------------------------------------------------------------------------


ReadWeather()

dop_threshold = 0.75  #0.9
hv_dic  = defaultdict(list)
baz_dic = defaultdict(list)
baz_all = []
freq_dic = defaultdict(list)
path=os.listdir('./allsta_asc_202105-08')
path.remove('total_chulin_5-8_CL07_wlen8.asc')
hv_all = defaultdict(list)
freq_list=[]
count = defaultdict(list)


for fl in path:
    hv_dic  = defaultdict(list)
    baz_dic = defaultdict(list)
    baz_all = []
    freq_dic = defaultdict(list)
    hv_all = defaultdict(list)
    freq_list=[]
    count = defaultdict(list)
    cl=fl.split('_')[3]
    lines = open('./allsta_asc/total_chulin_all_'+cl+'_wlen8.asc').readlines()
    lines.append('0 0 0 0 0 0') 

    for i in range(0,len(lines)):
        if len(lines[i].split()) == 6:
            if lines[i].split()[0]==str(0):
                break
            else:
                date=int(lines[i].split()[1])
                num=0
                n=1
                while len(lines[i+n].split()) !=6:
                    freq = float(lines[i+n].split()[1])                   
                    if freq not in freq_list:
                        freq_list.append(freq)
                    baz=float(lines[i+n].split()[0])
                    dop=float(lines[i+n].split()[2])
                    if dop >= dop_threshold:
                        if baz <= -45.0 and baz >= -135.0:
                            hv = np.log10(float(lines[i+n].split()[5]))
                            hv_dic[date].append([freq,hv])
                            hv_all[freq].append(hv)
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
                num=0
                print(date)
                n=1
                while len(lines2[i+n].split()) !=6:
                    freq = float(lines2[i+n].split()[1])
                    baz=float(lines2[i+n].split()[0])
                    dop=float(lines2[i+n].split()[2])
                    if dop >= dop_threshold:
                        if baz <= -45.0 and baz >= -135.0:
                            hv = np.log10(float(lines2[i+n].split()[5]))
                            hv_dic[date].append([freq,hv])
                            hv_all[freq].append(hv)
                            num=num+1
                            if freq not in freq_dic[date]:
                                freq_dic[date].append(freq)
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
                num=0
                n=1
                while len(lines3[i+n].split()) !=6:
                    freq = float(lines3[i+n].split()[1])
                    baz=float(lines3[i+n].split()[0])
                    dop=float(lines3[i+n].split()[2])
                    if dop >= dop_threshold:
                        if baz <= -45.0 and baz >= -135.0:
                            hv = np.log10(float(lines3[i+n].split()[5]))
                            hv_dic[date].append([freq,hv])
                            hv_all[freq].append(hv)
                            num=num+1
                            if freq not in freq_dic[date]:
                                freq_dic[date].append(freq)
                    
                    n=n+1
                count[date].append(num)


    count2=[]
    count2_date=[]
    missing_date=[]

    all_date=[]
    for i in range(1,366):
        d=i
        d2=datetime.datetime.strptime('21'+str(d), '%y%j')
        date=mdates.date2num(d2)
        num=0
        for j in range(len(count[i])):
            num=num+count[i][j]
        if num !=0:
            count2.append(num)
            count2_date.append(date)
        else:
            missing_date.append(date)
        all_date.append(date)



    hv_all_median = defaultdict(list)
    for f in sorted(freq_list):
        hv_all_median[f].append(np.median(hv_all[f]))


    deltaE_f=[]
    deltaE_date=[]
    deltaE_dhv=[]

    #deltaE=defaultdict(list)
    for j in range(1,335,1):
        print(j)
        
        t=np.linspace(j,j+30,num=31,dtype=int)
        T_list1=[]
        hv_median1=[]
        hv_freq1=[]
        hv_freq1 = defaultdict(list)
        freq_list=[]
        for date1 in t:
            if date1 != 141:
                for freq in freq_dic[date1]:
                    T=1/freq
                    if T >= 0.125 and T <= 1.1:
                        for i in range(len(hv_dic[date1])):
                            if hv_dic[date1][i][0]==freq:
                                hv_freq1[freq].append(hv_dic[date1][i][1])
                            if freq not in freq_list:
                                freq_list.append(freq)


        for f in sorted(freq_list):
            if hv_freq1[f]:
                hv1=np.median(hv_freq1[f])
                dhv=hv1-hv_all_median[f]
                d=j
                d2=datetime.datetime.strptime('21'+str(d), '%y%j') 
            
                date=mdates.date2num(d2)       
                deltaE_date.append(date)
                deltaE_f.append(f)
                deltaE_dhv.append(float(dhv))


#------------------------------------------------------------------------------------------------------
    cm = plt.cm.get_cmap('bwr_r')
    fig = plt.figure(1,figsize=(12,20))
    fig.subplots_adjust(wspace=1.)
    ax1 = plt.subplot2grid((9, 10), (0, 0), colspan=9, rowspan=1)  # count
    ax2 = plt.subplot2grid((9, 10), (1, 0), colspan=9, rowspan=3)  # Ellip.
    ax3 = plt.subplot2grid((9, 10), (4, 0), colspan=9, rowspan=1)  # Rainfall
    ax4 = plt.subplot2grid((9, 10), (5, 0), colspan=9, rowspan=1)  # GWL
    ax5 = plt.subplot2grid((9, 10), (6, 0), colspan=9, rowspan=1)  # GPS
    ax7 = plt.subplot2grid((9, 10), (7, 0), colspan=9, rowspan=1)  # TEMP
    ax8 = plt.subplot2grid((9, 10), (8, 0), colspan=9, rowspan=1)  # WIND
    ax6 = plt.subplot2grid((9, 10), (1, 9), colspan=9, rowspan=3)  #colorbar

    ax1.plot(count2_date,count2,'-',color='black')
    ax1.set_ylabel('Counts',fontsize=10)


    ax2.scatter(deltaE_date,deltaE_f,c=deltaE_dhv,marker='s',s=8,vmin=-1.0,vmax=1.0,cmap=cm)
    ax2.set_xlabel('Time(date)')
    ax2.set_ylabel('Frequency(Hz)',fontsize=12)
    ax2.set_ylim(0.8,8.5)
    m1=plt.cm.ScalarMappable(cmap=cm)
    m1.set_array(deltaE_dhv)
    m1.set_clim(-1.0,1.0)
    clb=plt.colorbar(m1,ax=ax6, boundaries=np.linspace(-1.0,1.0,21),fraction=0.3,pad=0.005)
    clb.ax.set_title("$\Delta$Log(H/V)")
    ax6.axis('off')

    ax3.plot(rain_time,rain,'-',color='blue')
    ax3.set_ylabel('Precipitation (mm)',fontsize=10)
    ax3.set_ylim(0,max(rain)*1.2)

    gwl_color=['blue','deepskyblue','aqua','lightblue']
    for i in range(len(BWl)):
        bwn=BWl[i].split('_')[0]
        ax4.plot(gw_time[bwn],gw[bwn],'-',color=gwl_color[i])
    ax4.set_ylabel('GWL (m)',fontsize=10)
    
    ax5.plot(gps_time[gpsl[0]],gps[gpsl[0]],'.',color='black')
    ax5.set_ylabel('Displacement (mm)',fontsize=10)
    ax5.set_xlabel('Date')
    ax5.set_ylim(-520.0,0.0)    

    ax8.xaxis.set_major_locator(mdates.MonthLocator())
    ax8.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    for label in ax8.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')

    ax7.plot(temp_time,temp,'-',color='green')
    ax7.set_ylabel('Temperature ($^\circ$C)',fontsize=10)
    ax7.set_ylim(0.8*min(temp),max(temp)*1.2)

    ax8.plot(wind_time,wind,'-',color='tan')
    ax8.set_ylabel('Wind speed (m/s)',fontsize=10)
    ax8.set_ylim(0,max(wind)*1.2)

    ax1.set_xlim([all_date[0], all_date[-1]])
    ax2.set_xlim([all_date[0], all_date[-1]])
    ax3.set_xlim([all_date[0], all_date[-1]])
    ax4.set_xlim([all_date[0], all_date[-1]])
    ax5.set_xlim([all_date[0], all_date[-1]])
    ax7.set_xlim([all_date[0], all_date[-1]])
    ax8.set_xlim([all_date[0], all_date[-1]])


    ax1.axes.xaxis.set_visible(False)
    ax2.axes.xaxis.set_visible(False)
    ax3.axes.xaxis.set_visible(False)
    ax4.axes.xaxis.set_visible(False)
    ax5.axes.xaxis.set_visible(False)
    ax7.axes.xaxis.set_visible(False)

    ax1.set_title(cl+'_hv_dif')
    #plt.show()
    plt.savefig('./hv_plot_2021/'+cl+'_hvdifference_dop'+str(dop_threshold)+'_2021.png')



