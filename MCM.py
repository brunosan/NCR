

#Import all runner info from the csv prepared with Google Refine
import csv
runner=[]
f = open('MCM.csv', 'rt')
try:
    reader = csv.DictReader(f)
    for row in reader:
        runner.append(row)
finally:
    f.close()

#Get a list of cities and Ages
#Count uniques
from collections import Counter

Places=[r['Location'] for r in runner if 'Location' in r]
Places_counts = Counter(Places)
len(Places_counts)
Places_counts.most_common(10)


#Make a dictionary with Places, their location, and number of runners
Places_dic={}
for r in runner:
    for P in Places_counts:
	
	if r['Location']==P:  #runner is from that place
		if P in Places_dic:
		  #not the first time, add info to this location
		  Places_dic[P]['runners']+=1
		  Places_dic[P]['Time'].append(int(r['ChipTimeSeconds']))
		  Places_dic[P]['Ages'].append(int(r['Age']))
		  Places_dic[P]['Gender'].append(r['Sex'])
		  if Places_dic[P]['lat']=='':
			Places_dic[P]['lat']=r['lat']
			print 'gotcha'
		  if Places_dic[P]['lng']=='':
			Places_dic[P]['lng']=r['lat']
			print 'gotcha'
		else:
		  #first time, add dictionary
		  Places_dic[P]={}
		  Places_dic[P]['runners']=1
		  Places_dic[P]['Time']=[int(r['ChipTimeSeconds'])]
		  Places_dic[P]['Ages']=[int(r['Age'])]
		  Places_dic[P]['Gender']=[r['Sex']]
		  Places_dic[P]['lat']=r['lat']
		  Places_dic[P]['lng']=r['lng']
		  print 'new place:',P

#add pertentiles to Places
from scipy import stats
for P in Places_dic:
	ages=np.asarray(Places_dic[P]['Ages'])
	times=np.asarray(Places_dic[P]['Time'])
	Places_dic[P]['Age_p']=[stats.scoreatpercentile(ages,10),stats.scoreatpercentile(ages,50),stats.scoreatpercentile(ages,90)]
	Places_dic[P]['Times_p']=[stats.scoreatpercentile(times,10),stats.scoreatpercentile(times,50),stats.scoreatpercentile(times,90)]
	Places_dic[P]['Gender']=[Places_dic['WASHINGTON,DC']['Gender'].count('M'),Places_dic['WASHINGTON,DC']['Gender'].count('F')]	
	Places_dic[P]['fastest']=np.min(times)
	Places_dic[P]['median']=np.median(times)


#Save aggregated data to csv
writer = csv.writer(open("MCM-a.csv", 'w'), delimiter=',',quoting=csv.QUOTE_ALL)
header=['Location']
for key in Places_dic["WASHINGTON,DC"]:
	header.append(key)
writer.writerow(header)

for P in Places_dic:
	row=[P]
	for key in Places_dic[P]:
		row.append(Places_dic[P][key])
	writer.writerow(row)




Ages=[r['Age'] for r in runner if 'Age' in r]
Age_counts = Counter(Ages)
len(Age_counts)
Age_counts.most_common(10)


import numpy as np
import matplotlib.pyplot as plt
#Histogram of Ages
Ages=np.array(map(float,[r['Age'] for r in runner if 'Age' in r]))
Ages_m=np.array(map(float,[r['Age'] for r in runner if r['Sex']=='M']))
Ages_f=np.array(map(float,[r['Age'] for r in runner if r['Sex']=='F']))

plt.hist((Ages_f,Ages_m),np.arange(1,20.)*5,histtype='bar',label=('Female','Male'),color=('red','blue'))
plt.legend()
plt.xticks(np.arange(1,20)*5)
plt.xlabel('Age')
plt.ylabel('Runners')
plt.title('Age histogram by Gender')
plt.show()

#Histogram of Time
Time=np.array(map(float,[r['ChipTimeSeconds'] for r in runner if 'ChipTimeSeconds' in r]))/60/60
Time_m=np.array(map(float,[r['ChipTimeSeconds'] for r in runner if r['Sex']=='M']))/60/60
Time_f=np.array(map(float,[r['ChipTimeSeconds'] for r in runner if r['Sex']=='F']))/60/60

plt.hist((Time_f,Time_m),np.arange(2*5,7.5*5)/5.,histtype='bar',label=('Female','Male'),color=('red','blue'))
plt.legend()
plt.xticks(np.arange(2*5,7.5*5)/5.,rotation=45)
plt.xlabel('Hours')
plt.ylabel('Runners')
plt.title('Time histogram by Gender')
plt.show()

#scatter

plt.scatter(Ages_f,Time_f,marker='.',color='red',label='Female')
plt.scatter(Ages_m,Time_m,marker='.',color='blue',label='Male')
plt.scatter(Ages_f,Time_f,marker='.',color='red')
plt.xlabel('Age')
plt.ylabel('Hours')
plt.title('Scatterplot Hours by Age')
plt.legend()
plt.show()

#Scatter with subsample of pairs
import random
subl=random.sample(np.arange(1,len(Ages)),1000)
subl_m=random.sample(np.arange(1,len(Ages_m)),7000)
subl_f=random.sample(np.arange(1,len(Ages_f)),7000)
sub_Time_m=list( Time_m[i] for i in subl_m)
sub_Time_f=list( Time_f[i] for i in subl_f )
sub_Ages_m=list( Ages_m[i] for i in subl_m )
sub_Ages_f=list( Ages_f[i] for i in subl_f )

plt.scatter(sub_Ages_f,sub_Time_f,marker='.',color='red')
plt.scatter(sub_Ages_m,sub_Time_m,marker='.',color='blue')
plt.scatter(sub_Ages_f,sub_Time_f,marker='.',color='red')
plt.xlabel('Age')
plt.ylabel('Hours')
plt.title('Scatterplot Hours by Age')
plt.show()

#Get Half marathon time in seconds:
for run in runner:
  if run['Half']:
	time=run['Half'].split(':')
	run['HalfTime']=(float(time[0])*60*60)+(float(time[1])*60)+(float(time[2]))


#Histogram of Half Time
HTime_m=np.array(map(float,[r['HalfTime'] for r in runner if ('HalfTime' in r and r['Sex']=='M')]))/60/60
HTime_f=np.array(map(float,[r['HalfTime'] for r in runner if ('HalfTime' in r and r['Sex']=='F') ]))/60/60
HTime=np.array(map(float,[r['HalfTime'] for r in runner if 'HalfTime' in r]))/60/60

Time_H=np.array(map(float,[r['ChipTimeSeconds'] for r in runner if 'HalfTime' in r]))/60/60
Ages_H=np.array(map(float,[r['Age'] for r in runner if 'HalfTime' in r]))
Time_H_m=np.array(map(float,[r['ChipTimeSeconds'] for r in runner if ('HalfTime' in r and r['Sex']=='M')]))/60/60
Time_H_f=np.array(map(float,[r['ChipTimeSeconds'] for r in runner if ('HalfTime'  in r and r['Sex']=='F')]))/60/60
Ages_H_f=np.array(map(float,[r['Age'] for r in runner if ('HalfTime' in r and r['Sex']=='F') ]))
Ages_H_m=np.array(map(float,[r['Age'] for r in runner if ('HalfTime' in r and r['Sex']=='M') ]))

#Scatter
plt.scatter(Time_H_m-(HTime_m*2),Ages_H_m, color='blue',label='Male')
plt.scatter(Time_H_f-(HTime_f*2),Ages_H_f, color='red', label='Female')
plt.xlabel('Excess hours from 2*Half_time')
plt.ylabel('Age')
plt.title('Scatterplot Excess Time by Age')
plt.legend()
plt.show()


