import numpy as np 
import pandas as pd 
import os
from time import sleep
from scipy import stats
from matplotlib import pyplot as plt
workspace = os.path.abspath('E:/JHU Research/Nature Protocol 2019/WorkSpace/nat prot/corrected_v5_cp/fig10')
names = [_ for _ in os.listdir(workspace) if _.endswith('csv')]
print names
csv = np.array([pd.read_csv(os.path.join(workspace,_),usecols=range(17,27)).values for _ in os.listdir(workspace) if _.endswith('csv')])[3:]
csv2 = np.array([pd.read_csv(os.path.join(workspace,_),usecols=range(6,16)).values for _ in os.listdir(workspace) if _.endswith('csv')])[3:]
mother = pd.read_csv(os.path.abspath('E:/JHU Research/Nature Protocol 2019/WorkSpace/nat prot/corrected_v5_cp/fig10/distribution table all.csv'),usecols=range(17,27)).values
mother2 = pd.read_csv(os.path.abspath('E:/JHU Research/Nature Protocol 2019/WorkSpace/nat prot/corrected_v5_cp/fig10/distribution table all.csv'),usecols=range(6,16)).values
fig,ax=plt.subplots()
# fig2,ax2=plt.subplots()
# fig3,ax3=plt.subplots()
cell =[[],[],[]]
for idx,c in enumerate(csv):
	dist = [np.around(_/np.sum(c[0])*100,3) for _ in c[0]]
	dist2 = [np.around(_/np.sum(c[1])*100,3) for _ in c[1]]
	dist3 = [np.around(_/np.sum(c[2])*100,3) for _ in c[2]]
	#print dist
	#print mother[0]
	cor= stats.pearsonr(dist,mother[0])[0]
	cor2= stats.pearsonr(dist2,mother[1])[0]
	cor3= stats.pearsonr(dist3,mother[2])[0]
	corr = (cor+cor2+cor3)/3
	cell[0].append(cor)
	cell[1].append(cor2)
	cell[2].append(cor3)
	# ax.scatter(idx,cor,c='r')
	# ax.scatter(idx,cor2,c='g')
	# ax.scatter(idx,cor3,c='b')
	# ax.scatter(idx,corr,c='k')
nuc =[[],[],[]]	
for idx2,c2 in enumerate(csv2):
	dist = [np.around(_/np.sum(c2[0])*100,3) for _ in c2[0]]
	dist2 = [np.around(_/np.sum(c2[1])*100,3) for _ in c2[1]]
	dist3 = [np.around(_/np.sum(c2[2])*100,3) for _ in c2[2]]
	#print dist
	#print mother[0]
	cor= stats.pearsonr(dist,mother2[0])[0]
	cor2= stats.pearsonr(dist2,mother2[1])[0]
	cor3= stats.pearsonr(dist3,mother2[2])[0]
	corr = (cor+cor2+cor3)/3
	nuc[0].append(cor)
	nuc[1].append(cor2)
	nuc[2].append(cor3)
x = [2,2.5,3,3.5,4,4.5,5,5.5,6]
cellval = np.mean(cell,axis=0)
cellerr = stats.sem(cell,axis=0)
nucval = np.mean(nuc,axis=0)
nucerr = stats.sem(nuc,axis=0)/2
print cellval
print nucerr
ax.scatter(x,cellval,c='b',linewidths=5)
ax.errorbar(x,cellval,yerr=cellerr,c='b',capsize=7,elinewidth=2)
ax.scatter(x,nucval,c='r',linewidths=5)
ax.errorbar(x,nucval,yerr=nucerr,c='r',capsize=7,elinewidth=2)
ax.set_ylim([0.5,1])
ax.set_yticks([0.5,0.75,1])
[i.set_linewidth(3) for i in ax.spines.itervalues()]
ax.tick_params(width=3,length=6)
plt.show()

	
	# print np.corrcoef(mother[0],dist)
# for c in csv:
# 	print c
# 	table = pd.read_csv(c,usecols=range(6,16)).values
# 	newtable = np.array([])
# 	for col in table:
# 		print [np.around(_/np.sum(col)*100,3) for _ in col]


