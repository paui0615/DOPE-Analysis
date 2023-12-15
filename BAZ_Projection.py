import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from io import StringIO
import numpy as np
from shapely import geometry
import math
from random import randint
import os
import sys
import matplotlib.pylab as plt
import matplotlib
import math
from math import radians
import numpy as np
from collections import defaultdict
from scipy import stats
from numpy import *
from scipy.spatial import distance
import matplotlib.image as img
from matplotlib.patches import Rectangle
import heapq
from geopy.distance import geodesic

#Distance from the river
Far=['CL18','CL13','CL12','CL15','CL14']
Near=['CL17','CL19','CL03','CL16','CL20','CL10']


CLloc=[]
f=open('./station.loc_noCL07').readlines()
for i in range(len(f)):
    cllat=float(f[i].split('  ')[2])
    cl=f[i].split('  ')[0]
    cllon=float(f[i].split('  ')[1])
    CLloc.append([cl,cllon,cllat])

#Decide whether points in the grid
def if_inPoly(polygon, Points):
        line=geometry.LineString(polygon)
        point=geometry.Point(Points)
        polygon=geometry.Polygon(line)
        return polygon.contains(point)

#Decide two lines intersect
def cross(p1,p2,p3):
    x1=p2[0]-p1[0]
    y1=p2[1]-p1[1]
    x2=p3[0]-p1[0]
    y2=p3[1]-p1[1]
    return x1*y2-x2*y1

def segment(p1,p2,p3,p4):
        if(max(p1[0],p2[0])>=min(p3[0],p4[0]) 
        and max(p3[0],p4[0])>=min(p1[0],p2[0])
        and max(p1[1],p2[1])>=min(p3[1],p4[1])
        and max(p3[1],p4[1])>=min(p1[1],p2[1])):
                if(cross(p1,p2,p3)*cross(p1,p2,p4)<=0 and cross(p3,p4,p1)*cross(p3,p4,p2)<=0):
                        D=1
                else:
                        D=0
        else:
                D=0
        return D


region=[(120.68,23.07),(120.77,23.07),(120.77,23.14),(120.68,23.14)]

#Generate grids
grids=[]
stepsize = 0.09/90
lon0=np.linspace(120.68,120.77,num=90,endpoint=True)
lat0=np.linspace(23.07,23.14,num=70,endpoint=True)
lonlon, latlat = np.meshgrid(lon0, lat0)




for i in range(len(lon0)):
        for j in range(len(lat0)):
                p=(lon0[i],lat0[j])
                grids.append(p)

#Read all station asc
path=os.listdir("./allsta_asc")
path.remove('total_chulin_all_CL07_wlen8.asc')
path.remove('total_chulin_all_CL21_wlen8.asc')
path2=[]
for i in range(len(path)):

    if path[i].split('_')[3] in Near:
        path2.append(path[i])


directall=[]
lineallx=[]
lineally=[]
linep1=[]
linep2=[]
directn=[]
for clfile in path:
    CLn=clfile.split('_')[3]
    print(CLn)
    results_file = './allsta_asc/'+clfile

    dop_threshold = 0.9  #0.9

    hv_dic  = defaultdict(list)
    baz_dic = defaultdict(list)
    baz_all = []
    freq_list = []


    lines = open(results_file).readlines()
    for i in range(0,len(lines)):
        if len(lines[i].split()) != 6:
            freq = float(lines[i].split()[1])
            T = 1/freq
            dop = float(lines[i].split()[2])
            baz = float(lines[i].split()[0])
            if freq not in freq_list :
                freq_list.append(freq)
            hv = np.log10(float(lines[i].split()[5]))
            if dop >= dop_threshold:
                hv_dic[freq].append(hv)
                baz_dic[freq].append(baz)


    f_out = open("periods_list.txt","w")
    f_out.write("Periods\n")
    for f in sorted(freq_list, reverse=True):
        f_out.write(str(round(1/f,3))+"\n")
    f_out.close()

    baz_f=[]
    # calc mean and std and plot
    fig = plt.figure(1, figsize=(11.69, 8.27))
    T_list, hv_mean, hv_std, hv_median, hv_err_perc, baz_median = [],[],[], [],[],[]
    for freq in sorted(freq_list):
        T = 1/freq
        if T <= 1.0 and T >= 0.125:
            hv_mean_freq = np.mean(hv_dic[freq])
            hv_sd_freq = np.std(hv_dic[freq])

            if not math.isnan(hv_mean_freq):
                TT = [T] * len(hv_dic[freq])
                T_list.append(T)
                hv_mean.append(np.mean(hv_dic[freq]))
                hv_std.append(np.std(hv_dic[freq]))
                baz_f.append(baz_dic[freq])
                median = np.median(hv_dic[freq])
                percentile_min = np.percentile(hv_dic[freq], 15.9)
                percentile_max = np.percentile(hv_dic[freq], 84.1)
                err_inf = abs(percentile_min - median)
                err_sup = abs(percentile_max - median)
                error = (err_inf + err_sup) / 2.0
                hv_median.append(median)
                hv_err_perc.append(error)
            else:
                pass

    #baz_f2 is the direction in 1-8Hz
    baz_f2=[y for x in baz_f for y in x]
    
    eachd_num,b=np.histogram(baz_f2,bins=1000)
    eachd=[]
    for i in range(len(b)-1):
        eachd.append((b[i]+b[i+1])/2)

    #Generate Stations sites
    for i in range(len(CLloc)):
        if CLn==CLloc[i][0]:
            stalon=CLloc[i][1]
            stalat=CLloc[i][2]


    for i in range(len(eachd)):
        p1=(stalon,stalat)
        p0=p1
        num=eachd_num[i]
        dir_cor=(float(eachd[i])*(-1)+90)*math.pi*(1/180)
        diro=(float(eachd[i])*math.pi)*(1/180)
        
        a=math.tan(diro)
        b=stalat-a*stalon
        
        #like infinte loop
        for j in range(1000):
            p1=(p1[0]+(stepsize*1)*math.cos(dir_cor),p1[1]+(stepsize*1)*math.sin(dir_cor))
        
            if if_inPoly(region,p1)==False:
                break
        p1=(p1[0]+(stepsize*1)*math.cos(dir_cor),p1[1]+(stepsize*1)*math.sin(dir_cor))
        linep1.append(p0)
        linep2.append(p1)
        directn.append(num)
#------------------------------------------------------------------------------


#Count direct num of each grid
countl=[]
midpointl=[]
midpointx=[]
midpointy=[]

for j in range(len(lat0)-1):
    for i in range(len(lon0)-1):
        grid=[(lon0[i],lat0[j]),(lon0[i+1],lat0[j]),(lon0[i+1],lat0[j+1]),(lon0[i],lat0[j+1])]
        midpoint=((lon0[i]+lon0[i+1])/2,(lat0[j]+lat0[j+1])/2)
        midpointl.append(midpoint)
        count=0
        for k in range(len(linep1)):
            insectn=0
            if segment(linep1[k],linep2[k],grid[0],grid[1])==1:
                insectn=insectn+1
            if segment(linep1[k],linep2[k],grid[1],grid[2])==1:
                insectn=insectn+1
            if segment(linep1[k],linep2[k],grid[2],grid[3])==1:
                insectn=insectn+1
            if segment(linep1[k],linep2[k],grid[3],grid[0])==1: 
                insectn=insectn+1
            
            if insectn>=1:
                radius=geodesic((midpoint[1],midpoint[0]),(linep1[k][1],linep1[k][0])).km  #Distance with km
                count=count+1*directn[k]*(radius**0.75)*(math.exp((-2*3.14*5*radius)/(2*100))) 
        countl.append(count)


#Normalization
countlmax_index=[]
countlmax=max(countl)
test=heapq.nlargest(4,countl)
for i in range(len(test)):
    countlmax_index.append(countl.index(test[i]))
countl2=[]
countl2=[i*(1/countlmax) for i in countl]


#Generate midpoint of each grid

for i in range(len(lon0)-1):
    midpointx.append((lon0[i]+lon0[i+1])/2)
for j in range(len(lat0)-1):
    midpointy.append((lat0[j]+lat0[j+1])/2)
direct_num=np.reshape(countl2,(-1,len(midpointx)))


#Read stream and river
f=open('./grdtxt/chulin_tri.txt').readlines()
trilon=[]
trilat=[]
for i in range(len(f)):
        lon=float(f[i].split('\t')[0])
        lat=float(f[i].split('\t')[1])

        if 120.71<lon<120.75 and 23.11<lat<23.115:
                trilon.append(lon)
                trilat.append(lat-0.002)
f2=open('./grdtxt/chulin_mainstream.txt').readlines()
mainlon=[]
mainlat=[]
for i in range(len(f2)):
        lon=float(f2[i].split('\t')[0])
        lat=float(f2[i].split('\t')[1])
        mainlon.append(lon)
        mainlat.append(lat-0.002)

#        if 120.71<lon<120.75 and 23.09<lat<23.13:

#                mainlon.append(lon)
#                mainlat.append(lat)

cm = plt.cm.get_cmap('coolwarm')


#Plotting line------------------------------------------------------------------

plt.figure(figsize=(18,14))
midpointx2,midpointy2=np.meshgrid(midpointx,midpointy)

#plot image
image = img.imread('./MAP_plot/Chulin_paper.png')
plt.imshow(image,aspect='auto',origin='upper',extent=(120.68,120.77,23.07,23.14))

plt.plot(trilon,trilat,'-',linewidth=2,color='blue')
plt.plot(mainlon,mainlat,'o',markersize=4,color='blue')


#plot contour and colorbar
cnt=plt.contourf(midpointx2,midpointy2,direct_num,levels=100,cmap=cm,alpha=0.7,vmin=0.5,vmax=1.0)
for c in cnt.collections:
   c.set_edgecolor("face")
   c.set_linewidth(0.00000000001)
m=plt.cm.ScalarMappable(cmap=cm)
m.set_array(direct_num)
m.set_clim(0.5,1.0)
clb=plt.colorbar(m, boundaries=np.linspace(0.5,1.0,21),ticks=[0.5,0.6,0.7,0.8,0.9,1.0])
clb.ax.set_title('Density',fontsize=14)


#plot stations
for i in range(len(CLloc)):
    plt.plot(CLloc[i][1],CLloc[i][2], color='black', marker='^',markersize=8)

#plot grids
for i in range(len(lon0)):

    plt.vlines(lon0[i],23.07,23.14,linestyles='solid',linewidth=0.3)
for i in range(len(lat0)):
    plt.hlines(lat0[i],120.68,120.77,linestyle='solid',linewidth=0.3)

#plot max grid
lond=lon0[1]-lon0[0]
latd=lat0[1]-lat0[0]


plt.xlim(120.68,120.77)
plt.ylim(23.07,23.14)
plt.xlabel('Longitude',fontweight='bold',fontsize=16)
plt.ylabel('Latitude',fontweight='bold',fontsize=16)
plt.xticks([120.68,120.70,120.72,120.74,120.77],fontsize=12)
plt.yticks([23.07,23.09,23.11,23.14],fontsize=12)
plt.ticklabel_format(axis='both',style='plain',useOffset=False)
plt.title('1-8Hz',fontsize=14)
plt.savefig('./BAZ_plot/Chulin_paper_BAZ_projection_f1-8.png')
