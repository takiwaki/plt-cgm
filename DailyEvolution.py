#!/usr/bin/python

#################################
# preparation
#################################
import sys # system call
import numpy as np
import datetime
import matplotlib
from matplotlib import pyplot as plt 
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

#################################
# parameters
#################################

# input file from freestyle libre
inputfile ="./fsl20210511.txt"
outputdir="figures/"

# the range of blood glucose in the figure
ymin=60
ymax=210

# the span of the major and minor ticks
ymjint=20
ymnint=10

# the range of desired blood glucose
ysafemin=70
ysafemax=140

#################################
# open files
#################################
try:
    finp = open(inputfile, 'r')
except IOError:
    print ('"%s" cannot be opened.' % inputfile)
    sys.exit()
print ("Reading " + inputfile + " Begin")

#################################
# Data Read
#################################
timeline=[]
BG=[] # Blood Glucose

ln=0 # number of the line
skipline=3
for line in finp:
    ln = ln+1
#    print ("Line num: ",ln) # for debug
# the number of line that you want to skip first.
    if ln < skipline:
        continue
# Read line
    data =line.split()
    flag=int(data[ 3])
    if flag !=0 :
        continue
    
    ymdtmp = data[ 1]
    ymd=ymdtmp.split("/")
    
    hmtmp = data[ 2]
    hm=hmtmp.split(":")
    timeline += [ datetime.datetime(int(ymd[0]),int(ymd[1]),int(ymd[2]),int(hm[0]), int(hm[1]), 0) ]
    BG += [int(data[ 4])] # [cm]

#    print(timeline[-1],BG[-1]) # last for debug
finp.close()
print ("Reading " + inputfile + " Ends")
print (" ")

#################################
# Plot data
#################################

#################################
# Plot all data
#################################
print("Total")

x=timeline
y=BG

fig = plt.figure()

plt.ylabel("Blood glucose [mg/dl]",fontsize=16)
plt.ylim([ymin,ymax])
plt.gca().yaxis.set_major_locator(MultipleLocator(ymjint)) 
plt.gca().yaxis.set_minor_locator(MultipleLocator(ymnint)) 
plt.axhspan(ysafemin,ysafemax,color="green",alpha=0.2)

plt.xlim(x[0],x[-1])
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1)) 
plt.plot(x, y, linewidth=2, color="black") # center the bars on their x-values


plt.gcf().autofmt_xdate()

ave=0.0
num=0
for index, item  in enumerate(x):
    ave = ave + y[index]
    num = num+1
    
ave = ave/num
hba = ave/30.0+1.7
print("average"+str(ave))

fig.text(0.15,0.85, "Average: "+str(round(ave,1))+" mg/dl", size=16)
fig.text(0.15,0.80, "HbA1c: "+str(round(hba,1))+" %", size=16)
    
#plt.show()
filename=outputdir+"total.png"
fig.savefig(filename)

#################################
# Plot data in each day
#################################

start = x[0].date()
end   = x[-1].date()

def daterange(_start, _end):
    for n in range((_end - _start).days):
        yield _start + datetime.timedelta(n)


for today in daterange(start, end):
    print (today)
    tomorrow=today+datetime.timedelta(days=1)
    xbeg = datetime.datetime.combine(today,datetime.time())
    xend = datetime.datetime.combine(tomorrow,datetime.time())
    ave=0.0
    num=0
    for index, item  in enumerate(x):
        if item >= xbeg and item <= xend :
            ave = ave + y[index]
            num = num+1
    ave = ave/num
    hba = ave/30.0+1.7
    print("average"+str(ave))
    
    plt.xlim(today,tomorrow)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.gca().xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    fig.text(0.15,0.85, "Average: "+str(round(ave,1))+" mg/dl", size=16)
    fig.text(0.15,0.80, "HbA1c: "+str(round(hba,1))+" %", size=16)
    
    plt.title(str(today))
    filename=outputdir+str(today)+".png"
    fig.savefig(filename)
    
    for txt in fig.texts:
        txt.set_visible(False)

    
