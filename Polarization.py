import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from collections import defaultdict



def findt(array,ft,datet):
    t1=0.0
    for i in range(len(array)):
        if ft>array[i] and ft<array[i+1]:
            t1=array[i]
            break
    t2=float(datet)+(t1-array[0])/(array[0]-array[-1])
    return t2


sample_rate=100.0
dt=1/sample_rate

path2=[]
path=os.listdir("./allsta_asc")
dop_threshold=0.75

time_range=[]
for i in range(16):

    time_range.append(53640.0+float(i)*1490)


baz_dic=defaultdict(list)
dop_dic=defaultdict(list) 
time_list=[]
date_list=[]

for files in path:

    CLn=files.split('_')[3]

    lines=open("./allsta_asc/"+files).readlines()
    print(files)
    lines.append('0 0 0 0 0 0')  #For while judge
    for j in range(1,121):
        if float(j)>=1 and float(j)<=121:
            for i in range(0,len(lines)):
                if len(lines[i].split()) == 6:
                    date=lines[i].split()[1]
                    if date not in date_list:
                        date_list.append(date)

                    if date==str(j):
                        spst=float(lines[i+1].split()[3])
                        time=findt(time_range,spst,date)    #Findt function                                    
                        if time not in time_list:
                            time_list.append(time)

                        n=1
                        bazf_dic=defaultdict(list)
                        dopf_dic=defaultdict(list)
                        freq_list=[]
                        while len(lines[i+n].split()) !=6:
                            
                            freq = float(lines[i+n].split()[1])
                            baz=float(lines[i+n].split()[0])
                            dop=float(lines[i+n].split()[2])
                            bazf_dic[freq].append(baz)
                            dopf_dic[freq].append(dop)
                            n=n+1                        
                            if freq not in freq_list:
                                freq_list.append(freq)
                        for f in freq_list: 
                            
                            baz_mean=np.mean(bazf_dic[f])                        
                            dop_mean=np.mean(dopf_dic[f])
                            
                            baz_dic[time].append([f,baz_mean])   
                            dop_dic[time].append([f,dop_mean])
    time_list.sort()


    X1,X2,Y1,Y2,Z1,Z2=[],[],[],[],[],[]

    for t in time_list:
        for i in range(len(baz_dic[t])):
            x=float(t)
            y=baz_dic[t][i][0]
            z=float(baz_dic[t][i][1])*(-1)+180.0
            X1.append(x)
            Y1.append(y)
            Z1.append(z)
            du=1490.0/(time_range[-1]-time_range[0])
            seg=np.arange(x,x+du,0.01)
            for k in range(len(seg)):
                X1.append(seg[k])
                Y1.append(y)
                Z1.append(z)


    for t in time_list:
        for i in range(len(dop_dic[t])):
            x=float(t)
            y=dop_dic[t][i][0]
            z=dop_dic[t][i][1]
            X2.append(x)
            Y2.append(y)
            Z2.append(z)
            du=1490.0/(time_range[-1]-time_range[0])
            seg=np.arange(x,x+du,0.01)
            for k in range(len(seg)):
                X2.append(seg[k])
                Y2.append(y)
                Z2.append(z)

    cm = plt.cm.get_cmap('coolwarm')
    fig=plt.figure(figsize=(21,12))

    ax2=fig.add_subplot()
    cb2=ax2.scatter(X2,Y2,c=Z2,vmin=0.75,vmax=1.0,marker='s',s=2,cmap=cm)
    ax2.set_xlabel('Time(Julian day)')
    ax2.set_ylabel('Frequency(Hz)')
    ax2.set_xlim(0.0,120.0)
    ax2.set_ylim(0.0,8.0)
    ax2.set_yticks([0.5,2.0,4.0,6.0,8.0])

    m2=plt.cm.ScalarMappable(cmap=cm)
    m2.set_array(Z2)
    m2.set_clim(0.75,1.0)
    clb2=plt.colorbar(m2, boundaries=np.linspace(0.75,1.0,11))
    clb2.ax.set_title('DOP')


    plt.savefig('./pol_plot/poltmean'+CLn+'_120days_1daymean.png')

