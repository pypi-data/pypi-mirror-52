#!/usr/bin/env python

# built-in libraries
import os
import pickle
import random
from time import sleep
from Tkinter import END
from copy import deepcopy
# external libraries
import pandas as pd
import numpy as np
# my wrapper
from collect_selected_bstack import *
from recordIDX import *
# my core
from bdreg import *
from pca_bdreg import *
from clusterSM import *

def main(BuildModel,csv,entries,modelname,clnum=None,progress_bar=None):
	print('## main.py')
	figdst = os.path.join(os.path.dirname(csv),modelname)
	progress = 50
	datetimenow = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	N = int(entries['Number of coordinates'].get())
	if BuildModel:
		ch1,ch2 = collect_seleced_bstack(csv,BuildModel,entries)
		VamModel = {
		"N":[],
		"bdrn":[],
		"mdd":[],
		"sdd":[],
		"pc":[],
		"latent":[],
		"clnum":[],
		"pcnum":[],
		"mincms":[],
		"testmean":[],
		"teststd":[],
		"boxcoxlambda":[],
		"C":[],
		"Z":[]
		}
		VamModel_ch2 = deepcopy(VamModel)
		ch = 'ch1'
		bdpc, bnreg, sc, VamModel = bdreg_main(ch1,N,VamModel,BuildModel)
		progress_bar["value"] = progress+15
		progress_bar.update()
		pc, score, latent, VamModel = pca_bdreg_main(bdpc,VamModel,BuildModel,ch)
		pcnum=None
		progress_bar["value"] = progress+20
		progress_bar.update()
		IDX,IDX_dist,bdsubtype,C,VamModel,height,inertia = cluster_main(csv,modelname,score,pc,bdpc,clnum,pcnum,VamModel,BuildModel,ch,None,entries,datetimenow)
		progress_bar["value"] = progress+25
		progress_bar.update()
		if not os.path.exists(os.path.join(figdst,'model storage')):
			os.mkdir(os.path.join(figdst,'model storage'))
		if os.path.exists(os.path.join(os.path.join(figdst,'model storage'),modelname+'_ch1.pickle')):
			f=open(os.path.join(os.path.join(figdst,'model storage'),modelname + str(random.randint(0,100)) +'_ch1.pickle'),'wb')
			pickle.dump(VamModel,f)
			f.close()
		else:
			f=open(os.path.join(os.path.join(figdst,'model storage'),modelname+'_ch1.pickle'),'wb')
			pickle.dump(VamModel,f)
			f.close()
		ch = 'ch2'
		bdpc, bnreg, sc, VamModel_ch2 = bdreg_main(ch2,N,VamModel_ch2,BuildModel)
		progress_bar["value"] = progress+35
		progress_bar.update()
		pc , score, latent, VamModel_ch2 = pca_bdreg_main(bdpc,VamModel_ch2,BuildModel,ch)
		progress_bar["value"] = progress+40
		progress_bar.update()
		pcnum=None
		IDX,IDX_dist,bdsubtype,C,VamModel_ch2,height,intertia = cluster_main(csv,modelname,score,pc,bdpc,clnum,pcnum,VamModel_ch2,BuildModel,ch,None,entries,datetimenow)
		progress_bar["value"] = progress+45
		progress_bar.update()
		if os.path.exists(os.path.join(os.path.join(figdst,'model storage'),modelname+'_ch2.pickle')):
			f=open(os.path.join(os.path.join(figdst,'model storage'),modelname + str(random.randint(0,100)) +'_nuclei.pickle'),'wb')
			pickle.dump(VamModel_ch2,f)
			f.close()
		else:
			f=open(os.path.join(os.path.join(figdst,'model storage'),modelname+'_ch2.pickle'),'wb')
			pickle.dump(VamModel_ch2,f)
			f.close()

	else:
		model_list = [os.path.abspath(os.path.join(modelname,_)) for _ in os.listdir(modelname) if _.lower().endswith('pickle')]
		UI = pd.read_csv(csv)
		setpaths = UI['set location']
		ch1ui= UI['ch1']
		ch2ui= UI['ch2']    
		condition = UI['condition']
		UIcopy=deepcopy(UI)
		ns = []
		for setidx, setpath in enumerate(setpaths):
			pickles = [_ for _ in os.listdir(setpath) if _.lower().endswith('pickle')]

			c1_stack = [pd.read_pickle(os.path.join(setpath,pkl)) for pkl in pickles if ch1ui[setidx] in pkl]
			c2_stack = [pd.read_pickle(os.path.join(setpath,pkl)) for pkl in pickles if ch2ui[setidx] in pkl]
			
			ch1 = pd.concat(c1_stack,ignore_index=True)
			ch2 = pd.concat(c2_stack,ignore_index=True)

			progress_bar["value"] = 10
			progress_bar.update()

			try:
				f=open(model_list[0],'r')
			except:
				entries['Status'].delete(0,END) #global name END is not defined
				entries['Status'].insert(0,'the model does not exist. please replace model name to the one you built')
			VamModel = pickle.load(f)

			N = VamModel['N'] 
			ch = 'ch1'
			bdpc_new, bnreg_new, sc_new, VamModel = bdreg_main(ch1,N,VamModel,BuildModel)
			pc_new, score_new, latent_new, VamModel = pca_bdreg_main(bdpc_new,VamModel,BuildModel,ch)
			# if clnum != VamModel['clnum']:
			# 	raise NameError('Number of eigen-shape should remain same. To change the number, rebuild the model with the new number first')
			clnum=VamModel['clnum']
			pcnum=VamModel['pcnum']
			#pc_new goes in for sake of placing, but pc from the model is used in cluster_main
			IDX_ch1,IDX_dist_ch1,bdsubtype_new,C_new,VamModel,height1,inertia1 = cluster_main(csv,modelname,score_new,pc_new,bdpc_new,clnum,pcnum,VamModel,BuildModel,ch,condition[setidx],entries,datetimenow)	
			recordIDX(IDX_ch1,IDX_dist_ch1,UI,ch,setpath,inertia1)
			try:
				f=open(model_list[1],'r')
			except:
				entries['Status'].delete(0,END)
				entries['Status'].insert(0,'Please use exact name of the model you have built to apply here')
			VamModel = pickle.load(f)
			N = VamModel['N'] 
			ch = 'ch2'
			bdpc_new, bnreg_new, sc_new, VamModel = bdreg_main(ch2,N,VamModel,BuildModel)
			pc_new, score_new, latent_new, VamModel = pca_bdreg_main(bdpc_new,VamModel,BuildModel,ch)
			clnum=VamModel['clnum']
			pcnum=VamModel['pcnum']
			#pc_new goes in for sake of placing, but pc from the model is used in cluster_main
			IDX_ch2,IDX_dist_ch2,bdsubtype_new,C_new,VamModel,height2,inertia2 = cluster_main(csv,modelname,score_new,pc_new,bdpc_new,clnum,pcnum,VamModel,BuildModel,ch,condition[setidx],entries,datetimenow)
			recordIDX(IDX_ch2,IDX_dist_ch2,UI,ch,setpath,inertia2)
			progress_bar["value"] = progress+100*(setidx+1)/len(setpaths)
			progress_bar.update()
			avgfit1 = np.mean(IDX_dist_ch1[IDX_ch1<max(IDX_ch1)])
			avgfit2 = np.mean(IDX_dist_ch2[IDX_ch2<max(IDX_ch2)])
			samplesize = len(IDX_dist_ch1)
			fitnsize = np.array([avgfit1,avgfit2,samplesize])
			ns.append(np.append(np.append(height1,height2),fitnsize))			
		for idx,elem in enumerate(zip(*ns)):
			if idx+1>(len(zip(*ns))-3)/2: 
				colname = str(idx+1-(len(zip(*ns))-3)/2)+'_ch2'
				if idx+1==int(len(zip(*ns))-3):colname = 'trash_ch2'
			else:
				colname = str(idx+1)+'_ch1'
				if idx+1==int((len(zip(*ns))-3)/2):colname = 'trash_ch1'
			if elem==zip(*ns)[-1]:
				colname = 'sample size'
			if elem==zip(*ns)[-2]:
				colname = 'ch2 avg distance'			
			if elem==zip(*ns)[-3]: 
				colname = 'ch1 avg distance'
			UIcopy[colname]=pd.Series(elem)
		UIcopy.to_csv(os.path.join(os.path.dirname(modelname),'distribution table.csv'),index=False)

		entries['Status'].delete(0,END)
		entries['Status'].insert(0,'applied the model')

