#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pyomo.environ as pyo
import numpy as np
import numpy_financial as npf
import random
import pandas as pd
import matplotlib.pyplot as plt
import math
from SDonlyNew import SDsupplyDemand

def summary(H,pmaxDic,demandData,WindNewCapacityFactor,PVNewCapacityFactor,carbonPrice,carbonSwitch,capacitySwitchCoal,capacitySwitchLNG,capacityBasePrice):

    Tech=['Coal', 'LNG', 'Wind', 'PV']

    Age=['New', 'Mid', 'Old']

    Thermal=['Coal', 'LNG']

    VRE=['Wind', 'PV']
    thermalmaxDic={}
    vremaxDic={}
    T = np.array([t for t in range(0, H)])
    n_tech=range(0,4)
    n_thermal=range(0,2)
    n_vre=range(0,2)
    n_age=range(0,3)
    pminDic={}
    fuelCostDic={}
    emissionFactor={}


    maintanceCost={}
    
    for k in Thermal:
        for p in Age:
            thermalmaxDic[k,p]=pmaxDic[k,p]

    for k in VRE:
        for p in Age:
            vremaxDic[k,p]=pmaxDic[k,p]





    #数组没有标签。pmax[1][2],代表LNGMid
    #pmaxList=np.array([[2*max(d)/Num*random.uniform(0,2) for a in Age] for tech in Tech])

    #字典有标签。直接对应名字无视顺序


    # #使用公式生成pmax数据
    # for k in Tech:
    #     for p in Age:
    #          pmaxDic[k,p]=2*max(d)/Num*random.uniform(0,2)


    #读取excel写入字典
    #读取各个技术最大容量





    CoalMaxNewInvest=1000
    LNGMaxNewInvest=1000
    PVMaxNewInvest=1000
    WindMaxNewInvest=1000
    totalMaxNewInvest=CoalMaxNewInvest+LNGMaxNewInvest+PVMaxNewInvest+WindMaxNewInvest

    CoalMaxRetire=1000
    LNGMaxRetire=1000
    PVMaxRetire=1000
    WindMaxRetire=1000
    totalMaxRetire=CoalMaxRetire+LNGMaxRetire+PVMaxRetire+WindMaxRetire

    unitInvestCoal=200
    unitInvestLNG=200
    unitInvestWind=10
    unitInvestPV=10

    #在python内部计算技术参数
    pminDic['Coal','New']=thermalmaxDic['Coal','New']*0.4
    pminDic['Coal','Mid']=thermalmaxDic['Coal','Mid']*0.5
    pminDic['Coal','Old']=thermalmaxDic['Coal','Old']*0.6
    pminDic['LNG','New']=thermalmaxDic['LNG','New']*0.1
    pminDic['LNG','Mid']=thermalmaxDic['LNG','Mid']*0.2
    pminDic['LNG','Old']=thermalmaxDic['LNG','Old']*0.3
    # pminDic['PV','New']=vremaxDic['PV','New']*0
    # pminDic['PV','Mid']=vremaxDic['PV','Mid']*0
    # pminDic['PV','Old']=vremaxDic['PV','Old']*0
    # pminDic['Wind','New']=vremaxDic['Wind','New']*0
    # pminDic['Wind','Mid']=vremaxDic['Wind','Mid']*0
    # pminDic['Wind','Old']=vremaxDic['Wind','Old']*0

    #[$/MWh]
    fuelCostDic['Coal','New']=35.8314
    fuelCostDic['Coal','Mid']=35.8314*1.2
    fuelCostDic['Coal','Old']=35.8314*1.5
    fuelCostDic['LNG','New']=66.6887
    fuelCostDic['LNG','Mid']=66.6887*1.2
    fuelCostDic['LNG','Old']=66.6887*1.5
    # fuelCostDic['PV','New']=0
    # fuelCostDic['PV','Mid']=0
    # fuelCostDic['PV','Old']=0
    # fuelCostDic['Wind','New']=0
    # fuelCostDic['Wind','Mid']=0
    # fuelCostDic['Wind','Old']=0

    #[ton/MWh] (未重复计算)
    emissionFactor['Coal','New']=0.943
    emissionFactor['Coal','Mid']=0.943*1.2
    emissionFactor['Coal','Old']=0.943*1.5
    emissionFactor['LNG','New']=0.474
    emissionFactor['LNG','Mid']=0.474*1.2
    emissionFactor['LNG','Old']=0.474*1.5
    # emissionFactor['PV','New']=0
    # emissionFactor['PV','Mid']=0
    # emissionFactor['PV','Old']=0
    # emissionFactor['Wind','New']=0
    # emissionFactor['Wind','Mid']=0
    # emissionFactor['Wind','Old']=0

    #*************  *************************  *******************  *******************  *******************  *******************  ******************* 
    # [$/MW/yr]
    maintanceCost['Coal','New']=119047
    maintanceCost['Coal','Mid']=119047*1.2
    maintanceCost['Coal','Old']=119047*1.5
    maintanceCostCoalAve=  (maintanceCost['Coal','New'] + maintanceCost['Coal','Mid'] + maintanceCost['Coal','Old'])/3
    maintanceCost['LNG','New']=57142
    maintanceCost['LNG','Mid']=57142*1.2
    maintanceCost['LNG','Old']=57142*1.5
    maintanceCostLNGAve=  (maintanceCost['LNG','New'] + maintanceCost['LNG','Mid'] + maintanceCost['LNG','Old'])/3
    maintanceCost['PV','New']=2.8
    maintanceCost['PV','Mid']=2.8
    maintanceCost['PV','Old']=2.8
    maintanceCost['Wind','New']=2590
    maintanceCost['Wind','Mid']=2590
    maintanceCost['Wind','Old']=2590

    #[$/MW]
    fixedCostCoal=2380952.38
    fixedCostLNG=1142857.14 
    fixedCostWind=2590476.19  #4904761.91 off-shore wind
    fixedCostPV=2371428.57   #2838095.24 residential PV


    importElectricity,\
    WindNewHourlyConsume,WindMidHourlyConsume,WindOldHourlyConsume,PVNewHourlyConsume,PVMidHourlyConsume,PVOldHourlyConsume,\
    WindNewHourlyCurtail,WindMidHourlyCurtail,WindOldHourlyCurtail,PVNewHourlyCurtail,PVMidHourlyCurtail,PVOldHourlyCurtail,\
    CoalNewHourlyOutput,CoalMidHourlyOutput,CoalOldHourlyOutput,LNGNewHourlyOutput,LNGMidHourlyOutput,LNGOldHourlyOutput\
    =SDsupplyDemand(H,pmaxDic,demandData,WindNewCapacityFactor,PVNewCapacityFactor)
    


    #总发电量
    totalCoal=np.sum([CoalNewHourlyOutput,CoalMidHourlyOutput,CoalOldHourlyOutput],axis=0)
    totalLNG=np.sum([LNGNewHourlyOutput,LNGMidHourlyOutput,LNGOldHourlyOutput],axis=0)
    totalVREConsume=np.sum([WindNewHourlyConsume,WindMidHourlyConsume,WindOldHourlyConsume,PVNewHourlyConsume,PVMidHourlyConsume,PVOldHourlyConsume],axis=0)
    totalSupply=np.sum([totalCoal,totalLNG,totalVREConsume,importElectricity],axis=0)


    #总容量
    CoalCapacity=thermalmaxDic['Coal','New']+thermalmaxDic['Coal','Mid']+thermalmaxDic['Coal','Old']
    LNGCapacity=thermalmaxDic['LNG','New']+thermalmaxDic['LNG','Mid']+thermalmaxDic['LNG','Old']
    WindCapacity=vremaxDic['Wind','New']+vremaxDic['Wind','Mid']+vremaxDic['Wind','Old']
    PVCapacity=vremaxDic['PV','New']+vremaxDic['PV','Mid']+vremaxDic['PV','Old']




    #电价计算  *************  *************************  *******************  *******************  *******************  *******************          
    hourlyPrice=[]
    #计算最大燃费的边际电厂的价格提升斜率，达到最大边际容量时，电价是上限200000/105的一半。(引发过量收入，放弃)
    #slopeElecPrice=thermalmaxDic[max(fuelCostDic,key=fuelCostDic.get)]/(400000/105-fuelCostDic[max(fuelCostDic,key=fuelCostDic.get)])
    for i in range(H):
        if demandData[i] <= totalVREConsume[i]:
            hourlyPrice.append(0)
        elif totalVREConsume[i] < demandData[i] <= totalVREConsume[i]+CoalNewHourlyOutput[i]:
            hourlyPrice.append(fuelCostDic['Coal','New'])
        elif totalVREConsume[i]+CoalNewHourlyOutput[i] < demandData[i] <= totalVREConsume[i]+CoalNewHourlyOutput[i]+CoalMidHourlyOutput[i]:
            hourlyPrice.append(fuelCostDic['Coal','Mid'])
        elif totalVREConsume[i]+CoalNewHourlyOutput[i]+CoalMidHourlyOutput[i] < demandData[i] <= totalVREConsume[i]+totalCoal[i]:
            hourlyPrice.append(fuelCostDic['Coal','Old'])
        elif totalVREConsume[i]+totalCoal[i] < demandData[i] <= totalVREConsume[i]+totalCoal[i]+LNGNewHourlyOutput[i]:
            hourlyPrice.append(fuelCostDic['LNG','New'])
        elif totalVREConsume[i]+totalCoal[i]+LNGNewHourlyOutput[i] < demandData[i] <= totalVREConsume[i]+totalCoal[i]+LNGNewHourlyOutput[i]+LNGMidHourlyOutput[i]:
            hourlyPrice.append(fuelCostDic['LNG','Mid'])        
        elif totalVREConsume[i]+totalCoal[i]+LNGNewHourlyOutput[i]+LNGMidHourlyOutput[i] < demandData[i] <= totalVREConsume[i]+totalCoal[i]+totalLNG[i]+1:#+1避免了极小值跳出区间
            hourlyPrice.append(fuelCostDic['LNG','Old'] )      # fuelCostDic['LNG','Old']      LNGOldHourlyOutput[i]*slopeElecPrice
        else:
            hourlyPrice.append(200000/105)      
            #直接跳跃至顶价，若结合缩放系数则会导致超额收入

    #若电价未触及上限，而产生进口，则说明调整力不够。若电价触及上限，且产生进口，说明总发电不够。
    count=[]
    for i in range(H):
        if hourlyPrice[i]<(200000/105) and importElectricity[i]>0:
            count.append(1)
    print('Not sufficient flexibility(Import but Not ElecPriceCap)',sum(count),'Times')
    count.clear()
    for i in range(H):
        if hourlyPrice[i]==(200000/105) and importElectricity[i]>0:
            count.append(1)
    print('Not sufficient capacity(Import & ElecPriceCap)',sum(count),'Times')
    count.clear()

    #FIT=20000yen/MWh,20yen/kwh   
    FIP=[20000/105 if i < 20000/105 else i for i in hourlyPrice ]

    # ************************
    # fig, ax = plt.subplots(1,1,figsize=(25,5))
    # #画当前年电价折线图
    # ax.plot(T+1,hourlyPrice,label='price' )
    # ax.plot(T+1,FIP ,label='FIP')
    # ax.set_xlabel('Time Period')
    # ax.set_title('Current Year Price and FIP[$/MWh]')  
    # ax.legend()
    # fig, ax = plt.subplots(1,1,figsize=(25,5))
    # #画当前年FIP电价折线图
    # 
    # ax.set_xlabel('Time Period')
    # ax.set_title('Current Year FIP [$/MWh]') 





    #是否可以将决策部分全部放在python中，SD只负责建模老化链？与过去时间无关的量可以在python中建模。与过去时间相关的量要在SD中建模
    #*************  *************************  *******************  *******************  *******************  *******************  
    # #碳价格，碳排放上限随年份变化，在SD内部建模更方便
    # #[$/ton]
    #*************  *************************  *******************  *******************  *******************  *******************  


    #容量价格*************  *************************  *******************  *******************  *******************  *******************  
    #[$/MW]
    windCapacityValue=0.266963886
    PVCapacityValue=0.159827451 

    #VRE容量系数=年间总发电量/（容量*8760）(或按照同等EUE的火力来计算VRE容量系数)
    totalCapacity=CoalCapacity+LNGCapacity+WindCapacity*windCapacityValue+PVCapacity*PVCapacityValue

    basePrice=capacityBasePrice
    capacityPriceCap=basePrice*1.5
    #max(demandData)*1.15+totalMaxNewInvest
    #相当于促进新投资的预算分配给不同技术

    slopeCapaPrice1=(basePrice-capacityPriceCap)/(max(demandData)*0.15)
    slopeCapaPrice2= - basePrice/totalMaxNewInvest
    if totalCapacity <= max(demandData):
        capacityPrice=capacityPriceCap
        print('Not enough capacity:',round(max(demandData) - totalCapacity,2), 'MW') 
    elif max(demandData) < totalCapacity <= max(demandData)*1.15:
        capacityPrice=capacityPriceCap+(totalCapacity- max(demandData))*slopeCapaPrice1
        print('Not enough reserve capacity:',round(max(demandData)*1.15 - totalCapacity,2), 'MW') 
    elif max(demandData)*1.15 < totalCapacity <= max(demandData)*1.15+totalMaxNewInvest:
        capacityPrice=basePrice+(totalCapacity- max(demandData)*1.15)*slopeCapaPrice2
        print('Sufficient capacity:',round(max(demandData)*1.15+totalMaxNewInvest - totalCapacity,2), 'MW') 
    else:
        capacityPrice=0
        print('Capacity excess:',round(totalCapacity-max(demandData)*1.15+totalMaxNewInvest,2), 'MW') 

    #print('Capacity Price Cap:',capacityPriceCap,'$/MW')    
    print('Current Year Capacity Price:',round(capacityPrice,2),'$/MW')


# In[ ]:



   
    interestRate=0.03
    scalingFactor=8760/H
    #*************  *************************  *******************  *******************  *******************  *******************  *******************  

    CoalNewincome=sum([CoalNewHourlyOutput[t]*hourlyPrice[t]*scalingFactor for t in T])
    unitCoalNewincome= 0 if thermalmaxDic['Coal','New'] == 0 else CoalNewincome/thermalmaxDic['Coal','New']
    CoalMidincome=sum([CoalMidHourlyOutput[t]*hourlyPrice[t]*scalingFactor for t in T])
    unitCoalMidincome= 0 if thermalmaxDic['Coal','Mid'] == 0 else CoalMidincome/thermalmaxDic['Coal','Mid']
    CoalOldincome=sum([CoalOldHourlyOutput[t]*hourlyPrice[t]*scalingFactor for t in T])
    unitCoalOldincome= 0 if thermalmaxDic['Coal','Old'] == 0 else CoalOldincome/thermalmaxDic['Coal','Old']
    LNGNewincome=sum([LNGNewHourlyOutput[t]*hourlyPrice[t]*scalingFactor for t in T])
    unitLNGNewincome= 0 if thermalmaxDic['LNG','New'] == 0 else LNGNewincome/thermalmaxDic['LNG','New']
    LNGMidincome=sum([LNGMidHourlyOutput[t]*hourlyPrice[t]*scalingFactor for t in T])
    unitLNGMidincome= 0 if thermalmaxDic['LNG','Mid'] == 0 else LNGMidincome/thermalmaxDic['LNG','Mid']
    LNGOldincome=sum([LNGOldHourlyOutput[t]*hourlyPrice[t]*scalingFactor for t in T])
    unitLNGOldincome= 0 if thermalmaxDic['LNG','Old'] == 0 else LNGOldincome/thermalmaxDic['LNG','Old']
    WindNewincome=sum([WindNewHourlyConsume[t]*FIP[t]*scalingFactor for t in T])  
    unitWindNewincome=0 if vremaxDic['Wind','New'] == 0 else WindNewincome/vremaxDic['Wind','New']  
    WindMidincome=sum([WindMidHourlyConsume[t]*FIP[t]*scalingFactor for t in T])  
    unitWindMidincome=0 if vremaxDic['Wind','Mid'] == 0 else WindMidincome/vremaxDic['Wind','Mid']  
    WindOldincome=sum([WindOldHourlyConsume[t]*FIP[t]*scalingFactor for t in T])  
    unitWindOldincome=0 if vremaxDic['Wind','Old'] == 0 else WindOldincome/vremaxDic['Wind','Old']  
    PVNewincome=sum([PVNewHourlyConsume[t]*FIP[t]*scalingFactor for t in T])  
    unitPVNewincome=0 if vremaxDic['PV','New'] == 0 else PVNewincome/vremaxDic['PV','New']  
    PVMidincome=sum([PVMidHourlyConsume[t]*FIP[t]*scalingFactor for t in T])  
    unitPVMidincome=0 if vremaxDic['PV','Mid'] == 0 else PVMidincome/vremaxDic['PV','Mid']  
    PVOldincome=sum([PVOldHourlyConsume[t]*FIP[t]*scalingFactor for t in T])  
    unitPVOldincome=0 if vremaxDic['PV','Old'] == 0 else PVOldincome/vremaxDic['PV','Old']  
    
    
    CoalNewEmission=sum(CoalNewHourlyOutput[t]*emissionFactor['Coal','New']*scalingFactor for t in T)
    CoalNewVariableCost= sum(CoalNewHourlyOutput[t]*fuelCostDic['Coal','New']*scalingFactor for t in T)+CoalNewEmission*carbonPrice*carbonSwitch
    unitCoalNewVariableCost=0 if thermalmaxDic['Coal','New'] == 0 else CoalNewVariableCost/thermalmaxDic['Coal','New']
    CoalMidEmission=sum(CoalMidHourlyOutput[t]*emissionFactor['Coal','Mid']*scalingFactor for t in T)
    CoalMidVariableCost= sum(CoalMidHourlyOutput[t]*fuelCostDic['Coal','Mid']*scalingFactor for t in T)+CoalMidEmission*carbonPrice*carbonSwitch
    unitCoalMidVariableCost=0 if thermalmaxDic['Coal','Mid'] == 0 else CoalMidVariableCost/thermalmaxDic['Coal','Mid']
    CoalOldEmission=sum(CoalOldHourlyOutput[t]*emissionFactor['Coal','Old']*scalingFactor for t in T)
    CoalOldVariableCost= sum(CoalOldHourlyOutput[t]*fuelCostDic['Coal','Old']*scalingFactor for t in T)+CoalOldEmission*carbonPrice*carbonSwitch
    unitCoalOldVariableCost=0 if thermalmaxDic['Coal','Old'] == 0 else CoalOldVariableCost/thermalmaxDic['Coal','Old']
    LNGNewEmission=sum(LNGNewHourlyOutput[t]*emissionFactor['LNG','New']*scalingFactor for t in T)
    LNGNewVariableCost= sum(LNGNewHourlyOutput[t]*fuelCostDic['LNG','New']*scalingFactor for t in T)+LNGNewEmission*carbonPrice*carbonSwitch
    unitLNGNewVariableCost=0 if thermalmaxDic['LNG','New'] == 0 else LNGNewVariableCost/thermalmaxDic['LNG','New']
    LNGMidEmission=sum(LNGMidHourlyOutput[t]*emissionFactor['LNG','Mid']*scalingFactor for t in T)
    LNGMidVariableCost= sum(LNGMidHourlyOutput[t]*fuelCostDic['LNG','Mid']*scalingFactor for t in T)+LNGMidEmission*carbonPrice*carbonSwitch
    unitLNGMidVariableCost=0 if thermalmaxDic['LNG','Mid'] == 0 else LNGMidVariableCost/thermalmaxDic['LNG','Mid']
    LNGOldEmission=sum(LNGOldHourlyOutput[t]*emissionFactor['LNG','Old']*scalingFactor for t in T)
    LNGOldVariableCost= sum(LNGOldHourlyOutput[t]*fuelCostDic['LNG','Old']*scalingFactor for t in T)+LNGOldEmission*carbonPrice*carbonSwitch
    unitLNGOldVariableCost=0 if thermalmaxDic['LNG','Old'] == 0 else LNGOldVariableCost/thermalmaxDic['LNG','Old']
    
    totalEmission=CoalNewEmission+CoalMidEmission+CoalOldEmission+LNGNewEmission+LNGMidEmission+LNGOldEmission
    coalEmission=CoalNewEmission+CoalMidEmission+CoalOldEmission
    LNGEmission=LNGNewEmission+LNGMidEmission+LNGOldEmission
    totalEmissionFund=totalEmission*carbonPrice
    
    unitWindNewVariableCost=0
    WindNewVariableCost=0
    unitWindMidVariableCost=0
    WindMidVariableCost=0
    unitWindOldVariableCost=0
    WindOldVariableCost=0
    unitPVNewVariableCost=0
    PVNewVariableCost=0
    unitPVMidVariableCost=0
    PVMidVariableCost=0
    unitPVOldVariableCost=0
    PVOldVariableCost=0
    cashflowCoalNew=0 if pmaxDic['Coal','New'] == 0 else unitCoalNewincome - unitCoalNewVariableCost - maintanceCost['Coal','New'] +capacityPrice*capacitySwitchCoal
    print('cashflowCoalNew:',cashflowCoalNew)
    cashflowCoalMid=0 if pmaxDic['Coal','Mid'] == 0 else unitCoalMidincome - unitCoalMidVariableCost - maintanceCost['Coal','Mid'] +capacityPrice*capacitySwitchCoal
    print('cashflowCoalMid:',cashflowCoalMid)
    cashflowCoalOld=0 if pmaxDic['Coal','Old'] == 0 else unitCoalOldincome - unitCoalOldVariableCost - maintanceCost['Coal','Old'] +capacityPrice*capacitySwitchCoal
    print('cashflowCoalOld:',cashflowCoalOld)
    cashflowLNGNew=0 if pmaxDic['LNG','New'] == 0 else unitLNGNewincome - unitLNGNewVariableCost - maintanceCost['LNG','New'] +capacityPrice*capacitySwitchLNG
    print('cashflowLNGNew:',cashflowLNGNew)
    cashflowLNGMid=0 if pmaxDic['LNG','Mid'] == 0 else unitLNGMidincome - unitLNGMidVariableCost - maintanceCost['LNG','Mid'] +capacityPrice*capacitySwitchLNG
    print('cashflowLNGMid:',cashflowLNGMid)
    cashflowLNGOld=0 if pmaxDic['LNG','Old'] == 0 else unitLNGOldincome - unitLNGOldVariableCost - maintanceCost['LNG','Old'] +capacityPrice*capacitySwitchLNG
    print('cashflowLNGOld:',cashflowLNGOld)
    cashflowWindNew=0 if pmaxDic['Wind','New'] == 0 else unitWindNewincome - unitWindNewVariableCost - maintanceCost['Wind','New'] 
    print('cashflowWindNew:',cashflowWindNew)
    cashflowWindMid=0 if pmaxDic['Wind','Mid'] == 0 else unitWindMidincome - unitWindMidVariableCost - maintanceCost['Wind','Mid'] 
    print('cashflowWindMid:',cashflowWindMid)
    cashflowWindOld=0 if pmaxDic['Wind','Old'] == 0 else unitWindOldincome - unitWindOldVariableCost - maintanceCost['Wind','Old'] 
    print('cashflowWindOld:',cashflowWindOld)
    cashflowPVNew=0 if pmaxDic['PV','New'] == 0 else unitPVNewincome - unitPVNewVariableCost - maintanceCost['PV','New'] 
    print('cashflowPVNew:',cashflowPVNew)
    cashflowPVMid=0 if pmaxDic['PV','Mid'] == 0 else unitPVMidincome - unitPVMidVariableCost - maintanceCost['PV','Mid'] 
    print('cashflowPVMid:',cashflowPVMid)
    cashflowPVOld=0 if pmaxDic['PV','Old'] == 0 else unitPVOldincome - unitPVOldVariableCost - maintanceCost['PV','Old'] 
    print('cashflowPVOld:',cashflowPVOld)
    #是否有capacity price补贴，是否有carbon price罚款和补贴。
    # cashflowCoalNew=unitCoalNewincome - unitVariableCostCoalNew - maintanceCost['Coal','New'] + capacityPrice 
    # cashflowWindNew=unitWindNewincome - unitVariableCostWindNew - maintanceCost['Wind','New'] + totalEmissionFund/(WindCapacity+PVCapacity)
    
    #*************  *************************  *******************  *******************  *******************  *******************  ******************* 
    

    
    Coalincome=CoalNewincome+CoalMidincome+CoalOldincome
    unitCoalincome= 0 if CoalCapacity == 0 else Coalincome/CoalCapacity
    LNGincome=LNGNewincome+LNGMidincome+LNGOldincome
    unitLNGincome= 0 if LNGCapacity == 0 else LNGincome/LNGCapacity
    Windincome=WindNewincome+WindMidincome+WindOldincome
    unitWindincome= 0 if WindCapacity == 0 else Windincome/WindCapacity
    PVincome=PVNewincome+PVMidincome+PVOldincome
    unitPVincome= 0 if PVCapacity == 0 else PVincome/PVCapacity
    

    
    CoalEmission=CoalNewEmission+CoalMidEmission+CoalOldEmission
    CoalVariableCost= CoalNewVariableCost+CoalMidVariableCost+CoalOldVariableCost
    unitCoalVariableCost= 0 if CoalCapacity == 0 else CoalVariableCost/CoalCapacity
    LNGEmission=LNGNewEmission+LNGMidEmission+LNGOldEmission
    LNGVariableCost= LNGNewVariableCost+LNGMidVariableCost+LNGOldVariableCost
    unitLNGVariableCost= 0 if LNGCapacity == 0 else LNGVariableCost/LNGCapacity
    
    WindVariableCost=0
    unitWindVariableCost=0
    PVVariableCost=0
    unitPVVariableCost=0

    
    cashflowCoal=0 if CoalCapacity == 0 else unitCoalincome - unitCoalVariableCost - maintanceCostCoalAve +capacityPrice*capacitySwitchCoal
    print('cashflowCoal:',cashflowCoal)
    cashflowLNG=0 if LNGCapacity == 0 else unitLNGincome - unitLNGVariableCost - maintanceCostLNGAve +capacityPrice*capacitySwitchLNG
    print('cashflowLNG:',cashflowLNG)
    cashflowWind=0 if WindCapacity == 0 else unitWindincome - unitWindVariableCost - maintanceCost['Wind','New'] #maintance都一样
    print('cashflowWind:',cashflowWind)
    cashflowPV=0 if PVCapacity == 0 else unitPVincome - unitPVVariableCost - maintanceCost['PV','New'] #maintance都一样
    print('cashflowPV:',cashflowPV)
    
    
    npvCashflowCoal=[cashflowCoal for i in range(0,41)]
    npvCashflowCoal[0]=-fixedCostCoal
    npvCashflowLNG=[cashflowLNG for i in range(0,41)]
    npvCashflowLNG[0]=-fixedCostLNG
    npvCashflowWind=[cashflowWind for i in range(0,21)]
    npvCashflowWind[0]=-fixedCostWind
    npvCashflowPV=[cashflowPV for i in range(0,21)]
    npvCashflowPV[0]=-fixedCostPV
    
    #(0,0.03,0.25),IRR，0.03是利率起始点，0.25是高利润行业。有论文建议12.5%作为通常的预期回报起始点。
    def investCoe(x):
        #return min(max(x*50/11-3/22,0),1) 
        return min(max(x*8-1,0),1) #（0，0.125，0.25） 

    # if npvCashflowCoal[0]<0: 
    #     IRRCoal=0 if math.isnan(npf.irr(npvCashflowCoal)) else round(npf.irr(npvCashflowCoal),3)
    #     newInvestCoal=min(math.ceil(CoalMaxNewInvest*investCoe(IRRCoal)/unitInvestCoal)*unitInvestCoal,CoalMaxNewInvest)
    #     print('IRRCoal:',IRRCoal,'NewInvestCoal:',newInvestCoal)
    # else:
    #     newInvestCoal=CoalMaxNewInvest
    #     print('IRRCoal:','overLimit','NewInvestCoal:',newInvestCoal)
    # if npvCashflowLNG[0]<0: 
    #     IRRLNG=0 if math.isnan(npf.irr(npvCashflowLNG)) else round(npf.irr(npvCashflowLNG),3)
    #     newInvestLNG=min(math.ceil(LNGMaxNewInvest*investCoe(IRRLNG)/unitInvestLNG)*unitInvestLNG,LNGMaxNewInvest)
    #     print('IRRLNG:',IRRLNG,'NewInvestLNG:',newInvestLNG)
    # else:
    #     newInvestLNG=LNGMaxNewInvest
    #     print('IRRLNG:','overLimit','NewInvestLNG:',newInvestLNG)
    # if npvCashflowWind[0]<0: 
    #     IRRWind=0 if math.isnan(npf.irr(npvCashflowWind)) else round(npf.irr(npvCashflowWind),3)
    #     newInvestWind=min(math.ceil(WindMaxNewInvest*investCoe(IRRWind)/unitInvestWind)*unitInvestWind,WindMaxNewInvest)
    #     print('IRRWind:',IRRWind,'NewInvestWind:',newInvestWind)
    # else:
    #     newInvestWind=WindMaxNewInvest
    #     print('IRRWind:','overLimit','NewInvestWind:',newInvestWind)
    # if npvCashflowPV[0]<0: 
    #     IRRPV=0 if math.isnan(npf.irr(npvCashflowPV)) else round(npf.irr(npvCashflowPV),3)
    #     newInvestPV=min(math.ceil(PVMaxNewInvest*investCoe(IRRPV)/unitInvestPV)*unitInvestPV,PVMaxNewInvest)
    #     print('IRRPV:',IRRPV,'NewInvestPV:',newInvestPV)
    # else:
    #     newInvestPV=PVMaxNewInvest
    #     print('IRRPV:','overLimit','NewInvestPV:',newInvestPV)
    IRRCoal=0 if math.isnan(npf.irr(npvCashflowCoal)) else round(npf.irr(npvCashflowCoal),3)
    newInvestCoal=min(math.ceil(CoalMaxNewInvest*investCoe(IRRCoal)/unitInvestCoal)*unitInvestCoal,CoalMaxNewInvest)
    print('IRRCoal:',IRRCoal,'NewInvestCoal:',newInvestCoal)
    IRRLNG=0 if math.isnan(npf.irr(npvCashflowLNG)) else round(npf.irr(npvCashflowLNG),3)
    newInvestLNG=min(math.ceil(LNGMaxNewInvest*investCoe(IRRLNG)/unitInvestLNG)*unitInvestLNG,LNGMaxNewInvest)
    print('IRRLNG:',IRRLNG,'NewInvestLNG:',newInvestLNG)
    IRRWind=0 if math.isnan(npf.irr(npvCashflowWind)) else round(npf.irr(npvCashflowWind),3)
    newInvestWind=min(math.ceil(WindMaxNewInvest*investCoe(IRRWind)/unitInvestWind)*unitInvestWind,WindMaxNewInvest)
    print('IRRWind:',IRRWind,'NewInvestWind:',newInvestWind)
    IRRPV=0 if math.isnan(npf.irr(npvCashflowPV)) else round(npf.irr(npvCashflowPV),3)
    newInvestPV=min(math.ceil(PVMaxNewInvest*investCoe(IRRPV)/unitInvestPV)*unitInvestPV,PVMaxNewInvest)
    print('IRRPV:',IRRPV,'NewInvestPV:',newInvestPV)
        
    return round(totalEmission,2),newInvestCoal,newInvestLNG,newInvestWind,newInvestPV,\
           round(cashflowCoalNew,2),round(cashflowCoalMid,2),round(cashflowCoalOld,2),\
           round(cashflowLNGNew,2),round(cashflowLNGMid,2),round(cashflowLNGOld,2),\
           round(cashflowWindNew,2),round(cashflowWindMid,2),round(cashflowWindOld,2),round(cashflowPVNew,2),round(cashflowPVMid,2),round(cashflowPVOld,2),\
           hourlyPrice,round(sum(importElectricity)*scalingFactor,1),round(capacityPrice,1),\
           round(sum(CoalNewHourlyOutput)*scalingFactor,1),round(sum(CoalMidHourlyOutput)*scalingFactor,1),round(sum(CoalOldHourlyOutput)*scalingFactor,1),\
           round(sum(LNGNewHourlyOutput)*scalingFactor,1),round(sum(LNGMidHourlyOutput)*scalingFactor,1),round(sum(LNGOldHourlyOutput)*scalingFactor,1),\
           round(sum(WindNewHourlyConsume)*scalingFactor,1),round(sum(WindMidHourlyConsume)*scalingFactor,1),round(sum(WindOldHourlyConsume)*scalingFactor,1),\
           round(sum(PVNewHourlyConsume)*scalingFactor,1),round(sum(PVMidHourlyConsume)*scalingFactor,1),round(sum(PVOldHourlyConsume)*scalingFactor,1),\
           round(sum(WindNewHourlyCurtail)*scalingFactor,1),round(sum(WindMidHourlyCurtail)*scalingFactor,1),round(sum(WindOldHourlyCurtail)*scalingFactor,1),\
           round(sum(PVNewHourlyCurtail)*scalingFactor,1),round(sum(PVMidHourlyCurtail)*scalingFactor,1),round(sum(PVOldHourlyCurtail)*scalingFactor,1)
