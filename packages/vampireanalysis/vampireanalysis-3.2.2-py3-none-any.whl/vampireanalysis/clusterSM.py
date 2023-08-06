#!/usr/bin/env python

# internal libraries
from __future__ import division
from copy import deepcopy
from inspect import getargspec
import time
import os
from Tkinter import END
from datetime import datetime
# external libraries
import pandas as pd
import numpy as np
from scipy import stats, cluster, spatial
from sklearn.cluster import KMeans
from sklearn import preprocessing
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
# my files
from PCA import *

def clusterSM(csv,modelname,score,pc,bdpc,clnum=None,pcnum=None,VamModel=None,BuildModel=None,ch=None,condition=None,entries=None,datetimenow='None'):
    print('# clusterSM')
    csvdir = os.path.dirname(csv)
    figdst = os.path.join(csvdir,modelname)
    if BuildModel : figdst = os.path.join(figdst,ch+'_buildmodel_'+datetimenow)
    else : figdst = os.path.join(os.path.dirname(modelname),ch+'_applymodel_'+datetimenow)
    if not os.path.exists(figdst): 
        try:
            os.makedirs(figdst)
        except:
            entries['Status'].delete(0,END)
            entries['Status'].insert(0,'Please fill in model name correctly')

    Nuu=int(round(len(bdpc.T[0])))
    Nbb=int(round(len(bdpc[0]) / 2))
    mmx=np.dot(np.ones([Nuu,1]),np.mean([bdpc],axis=1))
    smx=np.ones(bdpc.shape)
    mdd=mmx[0]
    sdd=smx[0]
    mss=np.mean(score,axis=0)
    sss=np.std(score,axis=0)

    NN=10

    if clnum==None:
        clnum=15
    if pcnum==None:
        pcnum=20

    if BuildModel:
        VamModel['clnum']=clnum
        VamModel['pcnum']=pcnum
    else:
        clnum = VamModel['clnum']
        pcnum = VamModel['pcnum']
        pc = VamModel['pc']

    cms00 = score[:,0:pcnum]
    cms = deepcopy(cms00)

    if BuildModel:
        mincms=np.amin(cms,axis=0)
        VamModel['mincms']=mincms
        VamModel['boxcoxlambda']=np.zeros(len(cms.T))
        VamModel['testmean']=np.zeros(len(cms.T))
        VamModel['teststd']=np.zeros(len(cms.T))
    else:
        mincms=VamModel['mincms']

    for k in range(len(cms.T)):
        test=cms.T[k]
        test=test - mincms[k] + 1
        if BuildModel:
            test[test<0]=0.000000000001
            test,maxlog=stats.boxcox(test)
            test = np.asarray(test)
            #####################
            VamModel['boxcoxlambda'][k]=maxlog
            VamModel['testmean'][k]=np.mean(test)
            VamModel['teststd'][k]=np.std(test)
            #####################
            cms.T[k]=(test-np.mean(test))/np.std(test)
        else:
            test[test<0]=0.000000000001
            test=stats.boxcox(test,VamModel['boxcoxlambda'][k])
            cms.T[k]=(test-VamModel['testmean'][k])/VamModel['teststd'][k]

    cms0=deepcopy(cms)
    cmsn=deepcopy(cms)

    if BuildModel:
        cmsn_Norm = preprocessing.normalize(cmsn)
        if isinstance(clnum, basestring):
            clnum = int(clnum)

        kmeans=KMeans(n_clusters=clnum,init='k-means++',n_init=3,max_iter=300).fit(cmsn_Norm) #init is plus,but orginally cluster, not available in sklearn
        IDX = kmeans.labels_
        C = kmeans.cluster_centers_
        ##################
        VamModel['C']=C
        # IDX = None
        # IDX_dist = None
        # inertia = None
        D = spatial.distance.cdist(cmsn,C,metric='euclidean')
        IDX = np.argmin(D,axis=1)
        IDX_dist = np.amin(D,axis=1)
        inertia = [np.around(np.sum(np.square(IDX_dist[IDX==_]))/len(IDX_dist[IDX==_]),decimals=2) for _ in range(clnum)]
    else:
        if isinstance(clnum, basestring):
            clnum = int(clnum)
        C = VamModel['C']
        D = spatial.distance.cdist(cmsn,C,metric='euclidean')
        # why amin? D shows list of distance to cluster centers. 
        IDX = np.argmin(D,axis=1)
        IDX_dist = np.around(np.amin(D,axis=1),decimals=2)
        inertia = [np.around(np.sum(np.square(IDX_dist[IDX==_]))/len(IDX_dist[IDX==_]),decimals=2) for _ in range(clnum)]
    
    offx,offy=np.meshgrid(range(clnum),[0])
    offx=np.multiply(offx,1)+1
    offx=offx[0]*1-0.5
    offy=np.subtract(np.multiply(offy,1), 1.5)+1
    offy=offy[0]
    # define normalized colormap
    cmap = plt.cm.jet
    vmax = int(clnum*10)
    norm = mpl.colors.Normalize(vmin=0,vmax=vmax)
    cid = plt.cm.ScalarMappable(norm=norm,cmap=cmap)

    clshape=np.zeros([clnum,len(cms00[0])])
    clshapesdv=deepcopy(clshape)
    bdst0=np.empty(len(bdpc.T))
    bdst=deepcopy(bdst0)
    for kss in range(clnum):
        c88=IDX == kss
        bdpcs=bdpc[c88,:]
        mbd=np.mean(bdpcs,axis=0)
        bdst0=np.vstack((bdst0,mbd))
    bdst0=bdst0[1:]
    # dendrogram of the difference between different shape
    mpl.rcParams['lines.linewidth'] = 2
    if BuildModel:
        Y=spatial.distance.pdist(bdst0,'euclidean')
        Z=cluster.hierarchy.linkage(Y,method='complete') #4th row is not in matlab
        Z[:,2] = Z[:,2]*5 #multiply distance manually 10times to plot better.
        VamModel['Z'] = Z
    else:
        Z = VamModel['Z']
    cluster.hierarchy.set_link_color_palette(['k'])
    fig289,ax289 = plt.subplots(figsize=(6,2),linewidth=2.0,frameon=False)
    plt.yticks([])
    R=cluster.hierarchy.dendrogram(Z,p=0,truncate_mode='mlab',orientation='bottom',ax=None,above_threshold_color='k')
    leaflabel = np.array(R['ivl'])
    dendidx = leaflabel
    cluster.hierarchy.set_link_color_palette(None)
    mpl.rcParams['lines.linewidth'] = 1
    plt.axis('equal')
    plt.axis('off')
    IDXsort=np.zeros(len(IDX))
    for kss in range(clnum):
        c88=IDX == int(dendidx[kss])
        IDXsort[c88]=kss
    IDX=deepcopy(IDXsort)
    bdsubtype=np.empty((int(max(IDX)+1),2,Nbb+1)) #need more specific preallocation: 2 for x and y, Nbb+1 for len(x)
    fig922,ax922 = plt.subplots(figsize=(17,2))
    fig291,ax291 = plt.subplots(figsize=(6,3))
    for kss in range(int(max(IDX))+1):
        c88=IDXsort == kss
        clshape[kss]=np.mean(cms00[c88],axis=0)
        clshapesdv[kss]=np.std(cms00[c88],axis=0)
        pnn=np.zeros(len(pc.T[0]))
        for kev in range(len(cms00[0])):
            pnn=np.add(pnn,np.multiply(pc.T[kev],clshape[kss,kev]))
            pnnlb=np.add(pnn,np.multiply(np.multiply(pc.T[kev],-2),clshapesdv[kss,kev]))
            pnnhb=np.add(pnn,np.multiply(np.multiply(pc.T[kev],2),clshapesdv[kss,kev]))
        pnn=np.multiply(pnn,sdd) + mdd
        pnnlb=np.multiply(pnnlb,sdd) + mdd
        pnnhb=np.multiply(pnnhb,sdd) + mdd  #pnn,pnnlb&hb are all randomized
        xx=pnn[0:Nbb]
        yy=pnn[Nbb:]
        xlb=pnnlb[0:Nbb]
        ylb=pnnlb[Nbb:]
        xhb=pnnhb[0:Nbb]
        yhb=pnnhb[Nbb:]
        xx=np.append(xx,xx[0])
        yy=np.append(yy,yy[0])
        xxhb=np.append(xhb,xhb[0])
        yyhb=np.append(yhb,yhb[0])
        xxlb=np.append(xlb,xlb[0])
        yylb=np.append(ylb,ylb[0])
        fss=4
        # this plots what? figeach together?
        ax291.plot((xx/fss+offx.T[kss])*10, (yy/fss+offy.T[kss])*10, '-',color=cid.to_rgba(kss),linewidth=5) #this is not plotted in matlab as well
        plt.axis('equal')

        bdsubtype[kss][0]=xx/fss
        bdsubtype[kss][1]=yy/fss
        bdpcs=bdpc[c88]
        mbd=np.mean(bdpcs,axis=0)
        bdNUM=int(round(len(mbd)/2))
        bdst=np.vstack((bdst,mbd))
        xaxis = np.add(np.divide(np.append(mbd[0:bdNUM],mbd[0]),fss),offx[kss])*10
        yaxis = np.add(np.divide(np.append(mbd[bdNUM:],mbd[bdNUM]),fss),offy[kss])*10
        #! figeach number does not match dendrogram


        figeach,axeach= plt.subplots()
        axeach.plot(xaxis,yaxis,'-',linewidth=15)
        # plt.gca().invert_yaxis()
        plt.axis('off')
        if BuildModel : 
            figeach.savefig(os.path.join(figdst,"eigen-shape "+str(int(dendidx[kss])+1)+".png"),format='png',transparent=True)
            figeach.savefig(os.path.join(figdst,"eigen-shape "+str(int(dendidx[kss])+1)+".svg"),format='svg',transparent=True)
        plt.clf()

        #fig289,ax289 = plt.subplots(figsize=(6,3))
        ax289.plot(xaxis,yaxis,'-',linewidth=2) #this is the shape of the dendrogram
        plt.gca().invert_yaxis()
        plt.axis('equal')
        plt.axis('off')

        sid=np.argsort(np.random.rand(sum(c88),1),axis=0)
        if len(sid)<NN: enum = len(sid)
        else:enum = NN
        
        for knn in range(enum):
            x99=bdpcs[sid[knn],np.append(range(bdNUM),0)]
            y99=bdpcs[sid[knn],np.append(np.arange(bdNUM,(bdNUM*2),1),bdNUM)]
            xax = np.add(np.divide(x99,fss),offx[kss])
            yax = np.add(np.divide(y99,fss),offy[kss])
            ax922.plot(xax,yax,'r-',linewidth=1)
            ax922.axis('off')
    bdst = bdst[1:]
    if BuildModel :
        fig922.savefig(os.path.join(figdst,"registered objects "+ch+".png"),format='png',transparent=True)
        fig922.savefig(os.path.join(figdst,"registered objects "+ch+".svg"),format='svg',transparent=True) 
        fig289.savefig(os.path.join(figdst,"eigen-shape dendrogram "+ch+".png"),format='png',transparent=True)
        fig289.savefig(os.path.join(figdst,"eigen-shape dendrogram "+ch+".svg"),format='svg',transparent=True)
    crap=np.sort(IDX)
    sid=np.argsort(IDX)
    BMsort=cmsn[sid]

    # fig20,ax20=plt.subplots()
    # plt.imshow(cmsn,extent=[0,1,0,1])
    # plt.clim(-1,1)
    # plt.gca().xaxis.set_minor_formatter(NullFormatter())
    # plt.yticks()
    # plt.gca().yaxis.set_minor_formatter(NullFormatter())
    # fig21=plt.figure(21)
    # plt.imshow(BMsort,extent=[0,1,0,1])
    # plt.gca().tick_params(direction='out')
    # plt.yticks()
    # plt.gca().yaxis.set_minor_formatter(NullFormatter())
    # fig23=plt.figure(23)
    # crap = np.expand_dims(crap,axis=1)
    # imgplot = plt.imshow(crap,cmap='jet',extent=[0,1,0,1]) #imagesc(crap)
    # plt.axis('on')
    # plt.xticks()
    # plt.gca().xaxis.set_minor_formatter(NullFormatter())
    # plt.yticks()
    # plt.gca().yaxis.set_minor_formatter(NullFormatter())
    # plt.close()

    IDX = IDX+1

    #dump by percent
    dumpamount = entries['Fraction of discarded outliers [%]'].get()
    dumpamount = float(dumpamount)
    # dumpamount = dumpamount/100

    # num_of_large_dist = int(dumpamount*len(IDX_dist))
    # # argpartition move all k large numbers to the back
    # ind = np.argpartition(IDX_dist,-num_of_large_dist)[-num_of_large_dist:]
    # IDX[ind]=clnum+1

    #dump by distance
    #IDX[IDX_dist>dumpamount]=clnum+1

    n,bins,patches = plt.hist(IDX,bins=range(clnum+3)[1:])
    fig22,ax22 = plt.subplots(figsize = (10,5))
    n=np.divide(n,np.sum(n))
    n=np.multiply(n,100)
    n=np.around(n,2)
    height = n
    ax22.bar(x=(np.delete(bins,0)-1)/2,height=height,width=0.4,align='center',color=(0.2, 0.4, 0.6, 0.6),edgecolor='black')
    #plt.xticks(np.delete(bins,0)-1)
    #ax22.set_xticks([])
    #ax22.set_yticks([])
    ax22.set_ylabel('%')
    ax22.set_xlabel('shape mode')
    ax22.set_ylim([0,38])
    # only for paper
    #ax22.set_ylim([0,35])
    ax22.set_title('shape mode distribution (n='+str(len(IDX_dist))+')')
    bartick = map(str, np.arange(int(np.max(IDX)))[1:])
    ax22.set_xticks((np.arange(np.max(IDX)+1)/2)[1:])
    ax22.set_xticklabels(tuple(bartick+['trash']))
   
    # for i,v in enumerate(height):
    #     ax22.text((i-0.3+1)/2,v+0.25, str(np.around(v,decimals=1)),color='black',fontweight='bold')
    for axis in ['top','bottom','left','right']:
        ax22.spines[axis].set_linewidth(3)

    if not BuildModel:
        fig22.savefig(os.path.join(figdst,'shape mode distribution_'+ch+'_'+condition+'.png'),format='png',transparent=True)
        fig22.savefig(os.path.join(figdst,'shape mode distribution_'+ch+'_'+condition+'.svg'),format='svg',transparent=True)

    plt.close('all')
    return IDX,IDX_dist,bdsubtype,C,VamModel,height,inertia

def cluster_main(csv,modelname,score,pc,bdpc,clnum=None,pcnum=None,VamModel=None,BuildModel=None,cellornuc=None,condition=None,entries=None,datetimenow='None'):
    print('## clusterSM.py')
    start = time.time()
    if not isinstance(condition,basestring): condition = str(condition)
    IDX,IDX_dist,bdsubtype,C,VamModel,height,inertia=clusterSM(csv,modelname,score,pc,bdpc,clnum,pcnum,VamModel,BuildModel,cellornuc,condition,entries,datetimenow)
    end = time.time()
    print('For cluster, elapsed time is ' + str(end-start) + 'seconds...')
    return IDX,IDX_dist,bdsubtype,C,VamModel,height,inertia