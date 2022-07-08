#!/usr/bin/env python
# coding: utf-8

# In[15]:


from BPTK_Py import Model
from BPTK_Py import sd_functions as sd
import numpy as np
import pandas as pd
import BPTK_Py




def SDsupplyDemand(H,pmaxDic,demandData,WindNewCapacityFactor,PVNewCapacityFactor):
    

    #从时间0开始计算
    start=0
    steps=H#模型期间,即使改变dt也无需改变期间，dt变的只是期间内的间隔。

    model = Model(starttime=start,stoptime=steps,dt=1,name='HoursSD') 
    #二进制计算，所以尽量将时间间隔设定为以2为底的幂乘,4,2,1,0.5,0.25,0.125，否则会增大误差
    #如果不得不设定其他数字的dt，多保留小数位数，或者可以尝试改变整个模型的时间单位，例如从年改为月，从而减少截断误差
    #****************************************************************************************
    #*********************************  SD balance *******************************************************
    #****************Demand*****************************************************************



    allDemandList=list(map(list,zip([i for i in range(0,steps)],np.array(demandData).flatten())))

    model.points["allDemand"] = allDemandList 

    electricityConsumption= model.converter("electricityConsumption")
    electricityConsumption.equation = sd.lookup(sd.time(),"allDemand")

    #****************Wind_PV_CF*****************************************************************

    #读取计算风光capacityFactor
#     df_Wind=pd.read_excel('hourlyData2019.xlsx',sheet_name='2019WindCut',header=None)

#     df_PV=pd.read_excel('hourlyData2019.xlsx',sheet_name='2019SolarCut',header=None)

    # WindCapacityFactor=df_Wind.to_numpy().flatten()
    WindNewCapacityFactorList=WindNewCapacityFactor.tolist()  #数组乘以数字是每个元素乘以数字。列表乘以数字是将列表本身重复数字次数。
    WindMidCapacityFactorList=(WindNewCapacityFactor*0.8).tolist()
    WindOldCapacityFactorList=(WindNewCapacityFactor*0.5).tolist()
    
    WindNewCapacityFactor=list(map(list,zip([i for i in range(0,steps+1)],WindNewCapacityFactorList))) 
    WindMidCapacityFactor=list(map(list,zip([i for i in range(0,steps+1)],WindMidCapacityFactorList)))
    WindOldCapacityFactor=list(map(list,zip([i for i in range(0,steps+1)],WindOldCapacityFactorList)))

    model.points["WindNewCapacityFactor"] = WindNewCapacityFactor 
    model.points["WindMidCapacityFactor"] = WindMidCapacityFactor 
    model.points["WindOldCapacityFactor"] = WindOldCapacityFactor


    #PVCapacityFactor=df_PV.to_numpy().flatten()
    PVNewCapacityFactorList=PVNewCapacityFactor.tolist()  #数组乘以数字是每个元素乘以数字。列表乘以数字是将列表本身重复数字次数。
    PVMidCapacityFactorList=(PVNewCapacityFactor*0.8).tolist() 
    PVOldCapacityFactorList=(PVNewCapacityFactor*0.5).tolist()
   
    PVNewCapacityFactor=list(map(list,zip([i for i in range(0,steps+1)],PVNewCapacityFactorList))) 
    PVMidCapacityFactor=list(map(list,zip([i for i in range(0,steps+1)],PVMidCapacityFactorList)))
    PVOldCapacityFactor=list(map(list,zip([i for i in range(0,steps+1)],PVOldCapacityFactorList)))


    model.points["PVNewCapacityFactor"] = PVNewCapacityFactor 
    model.points["PVMidCapacityFactor"] = PVMidCapacityFactor 
    model.points["PVOldCapacityFactor"] = PVOldCapacityFactor 


    WindNewCF= model.converter("WindNewCF")
    WindMidCF= model.converter("WindMidCF")
    WindOldCF= model.converter("WindOldCF")
    PVNewCF= model.converter("PVNewCF")
    PVMidCF= model.converter("PVMidCF")
    PVOldCF= model.converter("PVOldCF")

    WindNewCF.equation = sd.lookup(sd.time(),"WindNewCapacityFactor")
    WindMidCF.equation = sd.lookup(sd.time(),"WindMidCapacityFactor")
    WindOldCF.equation = sd.lookup(sd.time(),"WindOldCapacityFactor")
    PVNewCF.equation = sd.lookup(sd.time(),"PVNewCapacityFactor")
    PVMidCF.equation = sd.lookup(sd.time(),"PVMidCapacityFactor")
    PVOldCF.equation = sd.lookup(sd.time(),"PVOldCapacityFactor")


    capacityCoalNewReceiver=model.converter("capacityCoalNewReceiver")
    capacityCoalMidReceiver=model.converter("capacityCoalMidReceiver")
    capacityCoalOldReceiver=model.converter("capacityCoalOldReceiver")
    capacityLNGNewReceiver=model.converter("capacityLNGNewReceiver")
    capacityLNGMidReceiver=model.converter("capacityLNGMidReceiver")
    capacityLNGOldReceiver=model.converter("capacityLNGOldReceiver")
    capacityWindNewReceiver=model.converter("capacityWindNewReceiver")
    capacityWindMidReceiver=model.converter("capacityWindMidReceiver")
    capacityWindOldReceiver=model.converter("capacityWindOldReceiver")
    capacityPVNewReceiver=model.converter("capacityPVNewReceiver")
    capacityPVMidReceiver=model.converter("capacityPVMidReceiver")
    capacityPVOldReceiver=model.converter("capacityPVOldReceiver")

    capacityCoalNewReceiver.equation =pmaxDic['Coal','New']
    capacityCoalMidReceiver.equation =pmaxDic['Coal','Mid']
    capacityCoalOldReceiver.equation =pmaxDic['Coal','Old']
    capacityLNGNewReceiver.equation =pmaxDic['LNG','New']
    capacityLNGMidReceiver.equation =pmaxDic['LNG','Mid']
    capacityLNGOldReceiver.equation =pmaxDic['LNG','Old']
    capacityWindNewReceiver.equation =pmaxDic['Wind','New']
    capacityWindMidReceiver.equation =pmaxDic['Wind','Mid']
    capacityWindOldReceiver.equation =pmaxDic['Wind','Old']
    capacityPVNewReceiver.equation =pmaxDic['PV','New']
    capacityPVMidReceiver.equation =pmaxDic['PV','Mid']
    capacityPVOldReceiver.equation =pmaxDic['PV','Old']

    capacityCoal=model.converter("capacityCoal")
    capacityLNG=model.converter("capacityLNG")
    capacityWind=model.converter("capacityWind")
    capacityPV=model.converter("capacityPV")
    capacityCoal.equation =capacityCoalNewReceiver+capacityCoalMidReceiver+capacityCoalOldReceiver
    capacityLNG.equation =capacityLNGNewReceiver+capacityLNGMidReceiver+capacityLNGOldReceiver
    capacityWind.equation =capacityWindNewReceiver+capacityWindMidReceiver+capacityWindOldReceiver
    capacityPV.equation =capacityPVNewReceiver+capacityPVMidReceiver+capacityPVOldReceiver

    #技术参数
    pminCoalNew= model.converter("pminCoalNew")
    pminCoalMid= model.converter("pminCoalMid")
    pminCoalOld= model.converter("pminCoalOld")
    pminLNGNew= model.converter("pminLNGNew")
    pminLNGMid= model.converter("pminLNGMid")
    pminLNGOld= model.converter("pminLNGOld")
    #在python内部计算技术参数
    pminCoalNew.equation =capacityCoalNewReceiver*0.4
    pminCoalMid.equation =capacityCoalMidReceiver*0.5
    pminCoalOld.equation =capacityCoalOldReceiver*0.6
    pminLNGNew.equation =capacityLNGNewReceiver*0.1
    pminLNGMid.equation =capacityLNGMidReceiver*0.2
    pminLNGOld.equation =capacityLNGOldReceiver*0.3



    #****************generation*****************************************************************
    sdBalance= model.converter("sdBalance")
    generateWindNew= model.converter("generateWindNew")
    generateWindMid= model.converter("generateWindMid")
    generateWindOld= model.converter("generateWindOld")
    generateWind= model.converter("generateWind")
    generatePVNew= model.converter("generatePVNew")
    generatePVMid= model.converter("generatePVMid")
    generatePVOld= model.converter("generatePVOld")
    generatePV= model.converter("generatePV")
    generateCoalNew= model.converter("generateCoalNew")
    generateCoalMid= model.converter("generateCoalMid")
    generateCoalOld= model.converter("generateCoalOld")
    generateLNGNew= model.converter("generateLNGNew")
    generateLNGMid= model.converter("generateLNGMid")
    generateLNGOld= model.converter("generateLNGOld")

    #balance<0,供小于求
    sdBalance.equation = generateWindNew + generateWindMid +generateWindOld +generatePVNew +generatePVMid +generatePVOld +\
    generateCoalNew + generateCoalMid +generateCoalOld+ generateLNGNew +generateLNGMid +generateLNGOld - electricityConsumption

    generateWindNew.equation = sd.min(capacityWindNewReceiver * WindNewCF,capacityWindNewReceiver)#多余电力可curtailment
    generateWindMid.equation = sd.min(capacityWindMidReceiver * WindMidCF,capacityWindMidReceiver)
    generateWindOld.equation = sd.min(capacityWindOldReceiver * WindOldCF,capacityWindOldReceiver)
    generateWind.equation = generateWindNew+generateWindMid+generateWindOld

    generatePVNew.equation = sd.min(capacityPVNewReceiver * PVNewCF,capacityPVNewReceiver)#多余电力可curtailment
    generatePVMid.equation = sd.min(capacityPVMidReceiver * PVMidCF,capacityPVMidReceiver)
    generatePVOld.equation = sd.min(capacityPVOldReceiver * PVOldCF,capacityPVOldReceiver)
    generatePV.equation = generatePVNew+generatePVMid+generatePVOld
    #VRE,Coal,LNG调度顺序
    #VRE固定但是可削减，Coal始终在发电无变化，LNG灵活
    operationFactor=1
    operationFactorCoalNew= model.converter("operationFactorCoalNew")
    operationFactorCoalMid= model.converter("operationFactorCoalMid")
    operationFactorCoalOld= model.converter("operationFactorCoalOld")
    operationFactorCoalNew.equation = operationFactor
    operationFactorCoalMid.equation = operationFactor
    operationFactorCoalOld.equation = operationFactor
    
    netload= model.converter("netload")
    netload.equation = electricityConsumption - generateWindNew - generateWindMid -generateWindOld -generatePVNew -generatePVMid -generatePVOld
    
    #难以决定这部分发电量。

    generateCoalNew.equation = sd.max(sd.min(netload,capacityCoalNewReceiver),0.0)
    generateCoalMid.equation = sd.max(sd.min(netload-generateCoalNew,capacityCoalMidReceiver),0.0)
    generateCoalOld.equation = sd.max(sd.min(netload-generateCoalNew-generateCoalMid,capacityCoalOldReceiver),0.0)
    # generateCoalNew.equation = sd.If(capacityCoal<1,0.0,sd.max(sd.min(capacityCoalNewReceiver * operationFactorCoalNew,3356*capacityCoalNewReceiver/capacityCoal),pminCoalNew))#作为基荷不能超过当年度的需求的最小值，2019,200h，3356.0
    # generateCoalMid.equation = sd.If(capacityCoal<1,0.0,sd.max(sd.min(capacityCoalMidReceiver * operationFactorCoalMid,3356*capacityCoalMidReceiver/capacityCoal),pminCoalMid))#三个技术按照容量比例分配
    # generateCoalOld.equation = sd.If(capacityCoal<1,0.0,sd.max(sd.min(capacityCoalOldReceiver * operationFactorCoalOld,3356*capacityCoalOldReceiver/capacityCoal),pminCoalOld))
    
    residualLoad= model.converter("residualLoad")
    residualLoad.equation = sd.max(electricityConsumption - generateWindNew - generateWindMid -generateWindOld -generatePVNew -generatePVMid -generatePVOld - \
                                   generateCoalNew-generateCoalMid-generateCoalOld,0.0)
    generateLNGNew.equation = sd.max(sd.min(residualLoad,capacityLNGNewReceiver),0.0)#min(剩余负荷，周间最大发电量)，且大于最小发电量
    generateLNGMid.equation = sd.max(sd.min(residualLoad-generateLNGNew,capacityLNGMidReceiver),0.0)#先减去的优先发电
    generateLNGOld.equation = sd.max(sd.min(residualLoad-generateLNGNew-generateLNGMid,capacityLNGOldReceiver),0.0)#最小出力为零，更接近优化结果，高估LNG灵活性
    # generateLNGNew.equation = sd.max(sd.min(residualLoad,capacityLNGNewReceiver),pminLNGNew)#min(剩余负荷，周间最大发电量)，且大于最小发电量
    # generateLNGMid.equation = sd.max(sd.min(residualLoad-generateLNGNew,capacityLNGMidReceiver),pminLNGMid)#先减去的优先发电
    # generateLNGOld.equation = sd.max(sd.min(residualLoad-generateLNGNew-generateLNGMid,capacityLNGOldReceiver),pminLNGOld)


    #netload.plot()
    #画图6200step需要1min 


    curtailWindNew= model.converter("curtailWindNew")
    curtailWindMid= model.converter("curtailWindMid")
    curtailWindOld= model.converter("curtailWindOld")
    curtailPVNew= model.converter("curtailPVNew")
    curtailPVMid= model.converter("curtailPVMid")
    curtailPVOld= model.converter("curtailPVOld")

    curtailWindNew.equation = sd.If(sdBalance>1,sdBalance*generateWindNew/(generateWind+generatePV),0.0)#削减量与发电量成比例
    curtailWindMid.equation = sd.If(sdBalance>1,sdBalance*generateWindMid/(generateWind+generatePV),0.0)# 大于1以避免极小值出现
    curtailWindOld.equation = sd.If(sdBalance>1,sdBalance*generateWindOld/(generateWind+generatePV),0.0)
    curtailPVNew.equation = sd.If(sdBalance>1,sdBalance*generatePVNew/(generateWind+generatePV),0.0)
    curtailPVMid.equation = sd.If(sdBalance>1,sdBalance*generatePVMid/(generateWind+generatePV),0.0)
    curtailPVOld.equation = sd.If(sdBalance>1,sdBalance*generatePVOld/(generateWind+generatePV),0.0)

    consumeWindNew= model.converter("consumeWindNew")
    consumeWindMid= model.converter("consumeWindMid")
    consumeWindOld= model.converter("consumeWindOld")
    consumePVNew= model.converter("consumePVNew")
    consumePVMid= model.converter("consumePVMid")
    consumePVOld= model.converter("consumePVOld")

    consumeWindNew.equation = sd.If(sdBalance>1,generateWindNew-curtailWindNew,generateWindNew)#发电量-削减量
    consumeWindMid.equation = sd.If(sdBalance>1,generateWindMid-curtailWindMid,generateWindMid)# 大于1以避免极小值出现
    consumeWindOld.equation = sd.If(sdBalance>1,generateWindOld-curtailWindOld,generateWindOld)
    consumePVNew.equation = sd.If(sdBalance>1,generatePVNew-curtailPVNew,generatePVNew)
    consumePVMid.equation = sd.If(sdBalance>1,generatePVMid-curtailPVMid,generatePVMid)
    consumePVOld.equation = sd.If(sdBalance>1,generatePVOld-curtailPVOld,generatePVOld)

    importElectricity= model.converter("importElectricity")
    importElectricity.equation = sd.If(sdBalance<1, sd.abs(sd.round( sdBalance, 0 )),0.0)# 小于1以避免极小值出现
    
    importElectricity=importElectricity.plot(return_df=True).to_numpy().flatten().tolist()
    WindNewHourlyConsume=consumeWindNew.plot(return_df=True).to_numpy().flatten().tolist()
    WindMidHourlyConsume=consumeWindMid.plot(return_df=True).to_numpy().flatten().tolist()
    WindOldHourlyConsume=consumeWindOld.plot(return_df=True).to_numpy().flatten().tolist()
    PVNewHourlyConsume=consumePVNew.plot(return_df=True).to_numpy().flatten().tolist()
    PVMidHourlyConsume=consumePVMid.plot(return_df=True).to_numpy().flatten().tolist()
    PVOldHourlyConsume=consumePVOld.plot(return_df=True).to_numpy().flatten().tolist()
    WindNewHourlyCurtail=curtailWindNew.plot(return_df=True).to_numpy().flatten().tolist()
    WindMidHourlyCurtail=curtailWindMid.plot(return_df=True).to_numpy().flatten().tolist()
    WindOldHourlyCurtail=curtailWindOld.plot(return_df=True).to_numpy().flatten().tolist()
    PVNewHourlyCurtail=curtailPVNew.plot(return_df=True).to_numpy().flatten().tolist()
    PVMidHourlyCurtail=curtailPVMid.plot(return_df=True).to_numpy().flatten().tolist()
    PVOldHourlyCurtail=curtailPVOld.plot(return_df=True).to_numpy().flatten().tolist()
    CoalNewHourlyOutput=generateCoalNew.plot(return_df=True).to_numpy().flatten().tolist()
    CoalMidHourlyOutput=generateCoalMid.plot(return_df=True).to_numpy().flatten().tolist()
    CoalOldHourlyOutput=generateCoalOld.plot(return_df=True).to_numpy().flatten().tolist()
    LNGNewHourlyOutput=generateLNGNew.plot(return_df=True).to_numpy().flatten().tolist()
    LNGMidHourlyOutput=generateLNGMid.plot(return_df=True).to_numpy().flatten().tolist()
    LNGOldHourlyOutput=generateLNGOld.plot(return_df=True).to_numpy().flatten().tolist()

    return importElectricity,\
WindNewHourlyConsume,WindMidHourlyConsume,WindOldHourlyConsume,PVNewHourlyConsume,PVMidHourlyConsume,PVOldHourlyConsume,\
WindNewHourlyCurtail,WindMidHourlyCurtail,WindOldHourlyCurtail,PVNewHourlyCurtail,PVMidHourlyCurtail,PVOldHourlyCurtail,\
CoalNewHourlyOutput,CoalMidHourlyOutput,CoalOldHourlyOutput,LNGNewHourlyOutput,LNGMidHourlyOutput,LNGOldHourlyOutput



