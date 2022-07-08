#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pyomo.environ as pyo
import numpy as np
import numpy_financial as npf
import random
import pandas as pd
import matplotlib.pyplot as plt
import math


def selfDispatch(H,pmaxDic,demandData,priceData,WindNewCapacityFactor,PVNewCapacityFactor):

    Tech=['Coal', 'LNG', 'Wind', 'PV']

    Age=['New', 'Mid', 'Old']

    Thermal=['Coal', 'LNG']

    VRE=['Wind', 'PV']
    T = np.array([t for t in range(0, H)])
    n_tech=range(0,4)
    n_thermal=range(0,2)
    n_vre=range(0,2)
    n_age=range(0,3)
    
    thermalmaxDic={}
    vremaxDic={}
    pminDic={}
    fuelCostDic={}
    emissionFactor={}

    startUpRateDic={}
    startUpCostDic={}
    startUpTimeDic={}
    shutDownRateDic={}
    shutDownCostDic={}
    shutDownTimeDic={}

    rampUpDic={}
    rampDownDic={}


    maintanceCost={}
    for k in Thermal:
        for p in Age:
            thermalmaxDic[k,p]=pmaxDic[k,p]

    for k in VRE:
        for p in Age:
            vremaxDic[k,p]=pmaxDic[k,p]


    
    #读取计算风光capacityFactor
    #df_Wind=pd.read_excel('hourlyData2019.xlsx',sheet_name='2019WindCut',header=None)

    #df_PV=pd.read_excel('hourlyData2019.xlsx',sheet_name='2019SolarCut',header=None)

    #WindNewCapacityFactor=df_Wind.to_numpy().flatten()
    WindMidCapacityFactor=WindNewCapacityFactor*0.8
    WindOldCapacityFactor=WindNewCapacityFactor*0.5

    #PVNewCapacityFactor=df_PV.to_numpy().flatten()
    PVMidCapacityFactor=PVNewCapacityFactor*0.8
    PVOldCapacityFactor=PVNewCapacityFactor*0.5
    
    # PVNewCapacityFactor=df_Wind.to_numpy().flatten()
    # PVMidCapacityFactor=WindNewCapacityFactor*0.8
    # PVOldCapacityFactor=WindNewCapacityFactor*0.5



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
    

    WindNewHourlyOutput=np.round(vremaxDic['Wind','New']*WindNewCapacityFactor,decimals=2)
    WindMidHourlyOutput=np.round(vremaxDic['Wind','Mid']*WindMidCapacityFactor,decimals=2)
    WindOldHourlyOutput=np.round(vremaxDic['Wind','Old']*WindOldCapacityFactor,decimals=2)
    PVNewHourlyOutput=np.round(vremaxDic['PV','New']*PVNewCapacityFactor,decimals=2)
    PVMidHourlyOutput=np.round(vremaxDic['PV','Mid']*PVMidCapacityFactor,decimals=2)
    PVOldHourlyOutput=np.round(vremaxDic['PV','Old']*PVOldCapacityFactor,decimals=2)
    
    #每小时总出力            
    totalWind=list(map(lambda x :x[0]+x[1]+x[2] ,zip(WindNewHourlyOutput,WindMidHourlyOutput,WindOldHourlyOutput)))
    totalSolar=list(map(lambda x :x[0]+x[1]+x[2] ,zip(PVNewHourlyOutput,PVMidHourlyOutput,PVOldHourlyOutput)))
    
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

    #[MW/hour]
    startUpRateDic['Coal','New']=0.417
    startUpRateDic['Coal','Mid']=0.417*0.8
    startUpRateDic['Coal','Old']=0.417*0.5
    startUpRateDic['LNG','New']=59.3
    startUpRateDic['LNG','Mid']=59.3*0.8
    startUpRateDic['LNG','Old']=59.3*0.5
    # startUpRateDic['PV','New']=0
    # startUpRateDic['PV','Mid']=0
    # startUpRateDic['PV','Old']=0
    # startUpRateDic['Wind','New']=0
    # startUpRateDic['Wind','Mid']=0
    # startUpRateDic['Wind','Old']=0

    #[$]
    startUpCostDic['Coal','New']=thermalmaxDic['Coal','New']*155
    startUpCostDic['Coal','Mid']=thermalmaxDic['Coal','Mid']*155*1.2
    startUpCostDic['Coal','Old']=thermalmaxDic['Coal','Old']*155*1.5
    startUpCostDic['LNG','New']=thermalmaxDic['LNG','New']*79.5
    startUpCostDic['LNG','Mid']=thermalmaxDic['LNG','Mid']*79.5*1.2
    startUpCostDic['LNG','Old']=thermalmaxDic['LNG','Old']*79.5*1.5
    # startUpCostDic['PV','New']=vremaxDic['PV','New']*0
    # startUpCostDic['PV','Mid']=vremaxDic['PV','Mid']*0
    # startUpCostDic['PV','Old']=vremaxDic['PV','Old']*0
    # startUpCostDic['Wind','New']=vremaxDic['Wind','New']*0
    # startUpCostDic['Wind','Mid']=vremaxDic['Wind','Mid']*0
    # startUpCostDic['Wind','Old']=vremaxDic['Wind','Old']*0

    #[hour]
    startUpTimeDic['Coal','New']=48
    startUpTimeDic['Coal','Mid']=round(48*1.2)
    startUpTimeDic['Coal','Old']=round(48*1.5)
    startUpTimeDic['LNG','New']=12
    startUpTimeDic['LNG','Mid']=round(12*1.2)
    startUpTimeDic['LNG','Old']=round(12*1.5)
    # startUpTimeDic['PV','New']=vremaxDic['PV','New']*0
    # startUpTimeDic['PV','Mid']=vremaxDic['PV','Mid']*0
    # startUpTimeDic['PV','Old']=vremaxDic['PV','Old']*0
    # startUpTimeDic['Wind','New']=vremaxDic['Wind','New']*0
    # startUpTimeDic['Wind','Mid']=vremaxDic['Wind','Mid']*0
    # startUpTimeDic['Wind','Old']=vremaxDic['Wind','Old']*0

    shutDownRateDic['Coal','New']=0.83
    shutDownRateDic['Coal','Mid']=0.83*0.8
    shutDownRateDic['Coal','Old']=0.83*0.5
    shutDownRateDic['LNG','New']=89
    shutDownRateDic['LNG','Mid']=89*0.8
    shutDownRateDic['LNG','Old']=89*0.5
    # shutDownRateDic['PV','New']=vremaxDic['PV','New']*0
    # shutDownRateDic['PV','Mid']=vremaxDic['PV','Mid']*0
    # shutDownRateDic['PV','Old']=vremaxDic['PV','Old']*0
    # shutDownRateDic['Wind','New']=vremaxDic['Wind','New']*0
    # shutDownRateDic['Wind','Mid']=vremaxDic['Wind','Mid']*0
    # shutDownRateDic['Wind','Old']=vremaxDic['Wind','Old']*0

    shutDownCostDic['Coal','New']=startUpCostDic['Coal','New']*0.05
    shutDownCostDic['Coal','Mid']=startUpCostDic['Coal','Mid']*0.05
    shutDownCostDic['Coal','Old']=startUpCostDic['Coal','Old']*0.05
    shutDownCostDic['LNG','New']=startUpCostDic['LNG','New']*0.05
    shutDownCostDic['LNG','Mid']=startUpCostDic['LNG','Mid']*0.05
    shutDownCostDic['LNG','Old']=startUpCostDic['LNG','Old']*0.05
    # shutDownCostDic['PV','New']=startUpCostDic['PV','New']*0
    # shutDownCostDic['PV','Mid']=startUpCostDic['PV','Mid']*0
    # shutDownCostDic['PV','Old']=startUpCostDic['PV','Old']*0
    # shutDownCostDic['Wind','New']=startUpCostDic['Wind','New']*0
    # shutDownCostDic['Wind','Mid']=startUpCostDic['Wind','Mid']*0
    # shutDownCostDic['Wind','Old']=startUpCostDic['Wind','Old']*0

    shutDownTimeDic['Coal','New']=24
    shutDownTimeDic['Coal','Mid']=round(24*1.2)
    shutDownTimeDic['Coal','Old']=round(24*1.5)
    shutDownTimeDic['LNG','New']=8
    shutDownTimeDic['LNG','Mid']=round(8*1.2)
    shutDownTimeDic['LNG','Old']=round(8*1.5)
    # shutDownTimeDic['PV','New']=vremaxDic['PV','New']*0
    # shutDownTimeDic['PV','Mid']=vremaxDic['PV','Mid']*0
    # shutDownTimeDic['PV','Old']=vremaxDic['PV','Old']*0
    # shutDownTimeDic['Wind','New']=vremaxDic['Wind','New']*0
    # shutDownTimeDic['Wind','Mid']=vremaxDic['Wind','Mid']*0
    # shutDownTimeDic['Wind','Old']=vremaxDic['Wind','Old']*0

    #[MW/hour]
    rampUpDic['Coal','New']=thermalmaxDic['Coal','New']*0.006*60
    rampUpDic['Coal','Mid']=thermalmaxDic['Coal','Mid']*0.006*60*0.8
    rampUpDic['Coal','Old']=thermalmaxDic['Coal','Old']*0.006*60*0.5
    rampUpDic['LNG','New']=thermalmaxDic['LNG','New']*0.01*60
    rampUpDic['LNG','Mid']=thermalmaxDic['LNG','Mid']*0.01*60*0.8
    rampUpDic['LNG','Old']=thermalmaxDic['LNG','Old']*0.01*60*0.5
    # rampUpDic['PV','New']=vremaxDic['PV','New']*0
    # rampUpDic['PV','Mid']=vremaxDic['PV','Mid']*0
    # rampUpDic['PV','Old']=vremaxDic['PV','Old']*0
    # rampUpDic['Wind','New']=vremaxDic['Wind','New']*0
    # rampUpDic['Wind','Mid']=vremaxDic['Wind','Mid']*0
    # rampUpDic['Wind','Old']=vremaxDic['Wind','Old']*0

    rampDownDic['Coal','New']=thermalmaxDic['Coal','New']*0.006*60
    rampDownDic['Coal','Mid']=thermalmaxDic['Coal','Mid']*0.006*60*0.8
    rampDownDic['Coal','Old']=thermalmaxDic['Coal','Old']*0.006*60*0.5
    rampDownDic['LNG','New']=thermalmaxDic['LNG','New']*0.01*60
    rampDownDic['LNG','Mid']=thermalmaxDic['LNG','Mid']*0.01*60*0.8
    rampDownDic['LNG','Old']=thermalmaxDic['LNG','Old']*0.01*60*0.5
    # rampDownDic['PV','New']=vremaxDic['PV','New']*0
    # rampDownDic['PV','Mid']=vremaxDic['PV','Mid']*0
    # rampDownDic['PV','Old']=vremaxDic['PV','Old']*0
    # rampDownDic['Wind','New']=vremaxDic['Wind','New']*0
    # rampDownDic['Wind','Mid']=vremaxDic['Wind','Mid']*0
    # rampDownDic['Wind','Old']=vremaxDic['Wind','Old']*0

    #*************  *************************  *******************  *******************  *******************  *******************  ******************* 
    # [$/MW/yr]
    maintanceCost['Coal','New']=119047
    maintanceCost['Coal','Mid']=119047*1.2
    maintanceCost['Coal','Old']=119047*1.5
    maintanceCost['LNG','New']=57142
    maintanceCost['LNG','Mid']=57142*1.2
    maintanceCost['LNG','Old']=57142*1.5
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

    #print(pmaxDic,'\n',pminDic,'\n',shutDownRateDic,'\n',startUpRateDic)


    # #随机生成成本曲线
    # a = np.array([[0.5 + 0.2*np.random.randn() for a in Age] for tech in Tech])
    # b = np.array([[10*np.random.uniform() for a in Age] for tech in Tech])
    # #起停成本
    # c = np.array([[10*np.random.uniform() for a in Age] for tech in Tech])
    # e = np.array([[10*np.random.uniform() for a in Age] for tech in Tech])



#     #惯例，快速指定图像区域和x轴位置
#     fig, ax = plt.subplots(1,1,figsize=(25,3))
#     #画需求折线图
#     ax.plot(T+1, demandData)
#     ax.set_xlabel('Time Period')
#     ax.set_title('Demand')

#     fig, ax = plt.subplots(1,1,figsize=(25,3))
#     #画电价折线图
#     ax.plot(T+1, priceData)
#     ax.set_xlabel('Time Period')
#     ax.set_title('Price')

#     fig, ax = plt.subplots(1,1,figsize=(25,3))
#     #画风出力折线图
#     ax.plot(T+1, WindNewHourlyOutput,WindMidHourlyOutput,WindOldHourlyOutput)
#     ax.set_xlabel('Time Period')
#     ax.set_title('Wind Power')

#     fig, ax = plt.subplots(1,1,figsize=(25,3))
#     #画光出力折线图
#     ax.plot(T+1, PVNewHourlyOutput,PVMidHourlyOutput,PVOldHourlyOutput)
#     ax.set_xlabel('Time Period')
#     ax.set_title('Solar Power')   



#     #画火力成本图
#     powerOtpt = np.linspace(1, round(max(thermalmaxDic.values())))
#     #假设发电量。在指定的间隔内返回均匀间隔的数字，保证绘图的线性化。理想情况下是从pmin，pmax。

#     fig, ax = plt.subplots(1,1,figsize=(10,8))

#     #对于每一个发电机画一条线,访问数据中的燃料成本和开机成本
#     saveForMaxCost={}
#     for i in Thermal:
#         for j in Age:
#             ax.plot(powerOtpt, fuelCostDic[i,j]*powerOtpt + startUpCostDic[i,j],label=str(i+j))
#             saveForMaxCost[i,j]= fuelCostDic[i,j]*thermalmaxDic[i,j] + startUpCostDic[i,j]    #将各技术的最大成本临时保存备用。
#     #画图布局
#     ax.set_xlim(0, round(max(thermalmaxDic.values())))
#     #ax.set_ylim(0, 100)
#     ax.set_xlabel('Unit Production')
#     ax.set_ylabel('Unit Operating Cost')
#     ax.grid(axis="y")
#     plt.legend()
    #建立具象模型
    m = pyo.ConcreteModel()
    
    #标值
    S0,U0=0,1 #发动机t0时刻均开机1小时.S0已进行关机时间，U0已运行时间
    #rampCost=450 #$/MW，ramp不需要额外成本
    curtailPenalty=100  #$/MWh，等同于FiT价格
    importPenalty=200000/105   #电价上限$/MWh,200yen/kWh
    VOLL=5890000/105       #停電コストの再調査 5890yen/kWh
    
    #集合，下标
    m.tech = pyo.Set(initialize=Thermal)    #技术分类 
    m.t=pyo.Set(initialize=T)      #小时
    m.age = pyo.Set(initialize=Age)    #发电机年龄
    #m.vre= pyo.Set(initialize=VRE)
    
    #参数，数据
    m.hisPrice = pyo.Param(m.t,initialize=priceData)    #历史电价
 
    m.startUpCost = pyo.Param(m.tech,m.age,initialize=startUpCostDic)     #起停费用
    m.shutDownCost = pyo.Param(m.tech,m.age,initialize=shutDownCostDic)
   
    m.fuel = pyo.Param(m.tech,m.age,initialize=fuelCostDic)    #燃料成本    
     
    m.pmax = pyo.Param(m.tech,m.age,initialize=thermalmaxDic)  #最大出力，读取字典，（‘Coal，New’）    
    m.pmin = pyo.Param(m.tech,m.age,initialize=pminDic)  #最小出力     
    
    m.rampUp = pyo.Param(m.tech,m.age,initialize=rampUpDic)   #ramp limit MW/h
    m.rampDown = pyo.Param(m.tech,m.age,initialize=rampDownDic)
   
    m.startUpRate = pyo.Param(m.tech,m.age,initialize=startUpRateDic)    #起停速度 limit MW/h
    m.shutDownRate = pyo.Param(m.tech,m.age,initialize=shutDownRateDic)
    
    m.totalWind = pyo.Param(m.t,initialize=totalWind)    #总Wind每时刻发电量
    m.totalSolar = pyo.Param(m.t,initialize=totalSolar)    #总Solar每时刻发电量
    
    
    #     uT>=math.ceil(pmin/startuplimit) 开机时间,向上取整，保证开过pmin
    #     dT<=math.ceil(pmax/shutdownlimit)关机时间，向上取整，保证关过pmax
    #使用input数据来代替计算
    m.startUpTime = pyo.Param(m.tech,m.age,initialize=startUpTimeDic)    #起停时间 h
    m.shutDownTime = pyo.Param(m.tech,m.age,initialize=shutDownTimeDic)

    #变量，计算输出
    m.x = pyo.Var(m.tech,m.age,m.t,domain=pyo.NonNegativeReals)  #发电量
    m.importElec = pyo.Var(m.t,domain=pyo.NonNegativeReals)  #紧急进口量
    m.rejectLoad = pyo.Var(m.t,domain=pyo.NonNegativeReals)  #紧急甩负荷 load rejection，发电大于需求
    
    #假设New,Mid,Old按照容量比例分配削减和消纳
    m.curtailWind = pyo.Var(m.t,domain=pyo.NonNegativeReals) #Wind消减量
    m.consumeWind = pyo.Var(m.t,domain=pyo.NonNegativeReals) #Wind消纳量
    m.curtailSolar = pyo.Var(m.t,domain=pyo.NonNegativeReals) #Solar消减量
    m.consumeSolar = pyo.Var(m.t,domain=pyo.NonNegativeReals) #Solar消纳量
    
    #发电机状态变量
    m.u = pyo.Var(m.tech,m.age,m.t, domain=pyo.Binary)    #升降
    # for i in Tech:
    #     for j in Age:
    #         #m.u[i,j,0].fixed = True    #若固定可能暂时无解
    #         m.u[i,j,0].value = 1
    #指定初始状态，t0时刻所有发电机均在线,且已运行1小时（即UT=1）。参数中不能有变量，所以直接使用数字1代替
    
    m.y = pyo.Var(m.tech,m.age,m.t, domain=pyo.Binary)    #启动
    m.z = pyo.Var(m.tech,m.age,m.t, domain=pyo.Binary)    #停止

        
    def L_init(m,tch,a):  #t0时刻开机的初始状态必须给定，参数中不能有变量。如果指定是1，则全部技术都开机。*m.u[tch,a,0]，假设m.u[tch,a,0]=1，即都开机1小时
        return min(H,(m.startUpTime[tch,a]-U0)*1)    # 总时间，开机时间-已运行时间，之间的较小值。
    m.L= pyo.Param(m.tech,m.age,initialize=L_init)   
    #  m模型写入函数变量m，m.tech,m.age作为输入变量写入函数变量tch，a中。
    
    def F_init(m,tch,a): #t0时刻开机的初始状态必须给定，参数中不能有变量。*(1-m.u[tch,a,0]),假设m.u[tch,a,0]=1，即都开机1小时
        return min(H,(m.shutDownTime[tch,a]-S0)*(1-1))  # 总时间，关机时间-已关闭时间，之间的较小值。
    m.F= pyo.Param(m.tech,m.age,initialize=F_init)
    

    #约束
    #发电机状态约束
    #发电机在u，y，z中每个时刻只有一个状态。
    def state_constraint(m,tch,a,h):
        if h==m.t.first():
            return m.y[tch,a,h]-m.z[tch,a,h]== m.u[tch,a,h+1]-m.u[tch,a,h]  #重写以满足t0时刻
        else:
            return m.y[tch,a,h]-m.z[tch,a,h]== m.u[tch,a,h]-m.u[tch,a,h-1]   #uh,uh+1=1.则yh,zh都为0.y=1时，z=0，所以uh和uh+1只有一个为1，另一个是0. y=0时同理。
    
    m.state = pyo.Constraint(m.tech,m.age,m.t, rule=state_constraint)
    m.onoff = pyo.Constraint(m.tech,m.age,m.t, rule=lambda m,tch,a,h:m.y[tch,a,h]+m.z[tch,a,h]<=1)  #y,z在h时只有一个为1.
    

    # demand约束。直接使用装饰器来定义约束。也可以先定义函数再另rule等于所定义的约束函数。
    # demand下标T，约束函数变量声明m，T。对于发电机tch累加(for中定义了tch，a，累加后tch，a消失)，在每个时间T，demand恒等于需求数组d中的第[T]个
    #m.demand = pyo.Constraint(m.t, rule=lambda m,T: sum(m.x[tch,a,T] for a in m.age for tch in m.tech) == demandData[T])
    m.supdem = pyo.Constraint(m.t, rule=lambda m,T: sum(m.x[tch,a,T]for a in m.age for tch in m.tech)+ m.consumeWind[T] + m.consumeSolar[T] + m.importElec[T] - m.rejectLoad[T]  == demandData[T])

    
    #VRE约束
    m.solarBalance = pyo.Constraint(m.t, rule=lambda m,T:  m.totalSolar[T]-m.consumeSolar[T] == m.curtailSolar[T])
    m.windBalance = pyo.Constraint(m.t, rule=lambda m,T:  m.totalWind[T]-m.consumeWind[T] == m.curtailWind[T]) 

    
    #ramp约束
    
    # semi-continuous。简单上下限约束用于调试。如果u等于0，则发电量x为0(0<=x<=0)。如果u等于1，则发电量pmin<=x<=pmax
    m.xlb = pyo.Constraint(m.tech,m.age,m.t, rule=lambda m,tch,a,h: m.x[tch,a,h] >= m.pmin[tch,a]*m.u[tch,a,h])
    m.xub = pyo.Constraint(m.tech,m.age,m.t, rule=lambda m,tch,a,h: m.x[tch,a,h] <= m.pmax[tch,a]*m.u[tch,a,h])

    
    #下限约束。时间点之间的最大下降不能大于降ramp或关停ramp。t0初始值大于最小出力，状态不定。
    #如果条件判断涉及到变量（内生），则不能使用if。但是时间t不是变量（外部），所以可以使用。
    
    def rlb_constraint(m,tch,a,h):
        if h==m.t.first():
            return m.x[tch,a,h] >= m.pmin[tch,a]*m.u[tch,a,h]
        else: 
            return m.x[tch,a,h] >= m.x[tch,a,h-1]-m.rampDown[tch,a]*m.u[tch,a,h]-m.shutDownRate[tch,a]*m.z[tch,a,h]
    
    #上限约束。时间点之间的最大上升不能大于升ramp或开机ramp。t0初始值小于最大出力，状态不定。
    def rub_constraint(m,tch,a,h):
        if h==m.t.first():
            return m.x[tch,a,h] <= m.pmax[tch,a]*(m.u[tch,a,h]+m.y[tch,a,h]+m.z[tch,a,h])
        else:
            return m.x[tch,a,h] <= m.x[tch,a,h-1]+m.rampUp[tch,a]*m.u[tch,a,h-1]+m.startUpRate[tch,a]*m.y[tch,a,h]
        
    #关停约束。下一个时间点关停时，上一个时间点的出力要小于关停ramp。t末尾值是小于最大出力，状态不定。    
    def rsb_constraint(m,tch,a,h):
        if h==m.t.last():
            return m.x[tch,a,h] <= m.pmax[tch,a]*(m.u[tch,a,h]+m.y[tch,a,h]+m.z[tch,a,h])
        else:
            return m.x[tch,a,h] <= m.pmax[tch,a]*(m.u[tch,a,h]-m.z[tch,a,h+1])+m.shutDownRate[tch,a]*m.z[tch,a,h+1]
    m.rlb = pyo.Constraint(m.tech,m.age,m.t, rule=rlb_constraint)
    m.rub = pyo.Constraint(m.tech,m.age,m.t, rule=rub_constraint)
    m.rsb = pyo.Constraint(m.tech,m.age,m.t, rule=rsb_constraint)
    #未包含了pmin,pmax约束

    #最小开机时间约束
    def upTimeCon1rule(m,tch,a):
        if m.L[tch,a]>0:    #从1到L时刻内（L=uT-已开机）内无开机（u均等于1） 
            return sum(1-m.u[tch,a,h] for h in range(m.L[tch,a]+1)) == 0
        else:
            return m.upTimeCon1.Skip # uT<=u0，已运行时间大于等于开机时间，或本身不在线u=0. 暂定均为0
    m.upTimeCon1 = pyo.Constraint(m.tech,m.age,rule=upTimeCon1rule)
    
    def upTimeCon2rule(m,tch,a,h):      
        if m.L[tch,a]<=(H-m.startUpTime[tch,a]):     #所有满足uT大小的集合。若k时刻on，u=1，则在uT时间内无开机。 when h>m.L.   
            return sum(m.u[tch,a,h] for h in range(m.L[tch,a]+1,H-m.startUpTime[tch,a]+1)) >= m.startUpTime[tch,a]*m.y[tch,a,h]
        else:
            return m.upTimeCon2.Skip    
    m.upTimeCon2 = pyo.Constraint(m.tech,m.age,m.t,rule=upTimeCon2rule)

    def upTimeCon3rule(m,tch,a):        
        if m.startUpTime[tch,a] >=2:    #如果有一个时刻y=1，则期间内必有一个时刻u=1。即保持on状态。#when h<H-m.startUpTime+2
            return sum(m.u[tch,a,h]-m.y[tch,a,h] for h in range(H-m.startUpTime[tch,a]+1,H) ) >= 0  #+1避免当sT=2时range（H，H）返回0。实际算式是+2.
        else:
            return m.upTimeCon3.Skip
    m.upTimeCon3 = pyo.Constraint(m.tech,m.age,rule=upTimeCon3rule)

    
    #最小关机时间约束
    def downTimeCon1rule(m,tch,a):
        if m.F[tch,a]>0:    
            return sum(m.u[tch,a,h] for h in range(m.F[tch,a]+1)) == 0
        else:
            return m.downTimeCon1.Skip 
    m.downTimeCon1 = pyo.Constraint(m.tech,m.age,rule=downTimeCon1rule)
    
    def downTimeCon2rule(m,tch,a,h):      
        if m.F[tch,a]<=(H-m.shutDownTime[tch,a]):     
            return sum(m.u[tch,a,h] for h in range(m.F[tch,a]+1,H-m.shutDownTime[tch,a]+1)) >= m.shutDownTime[tch,a]*m.y[tch,a,h] 
        else:
            return m.downTimeCon2.Skip    
    m.downTimeCon2 = pyo.Constraint(m.tech,m.age,m.t,rule=downTimeCon2rule)

    def downTimeCon3rule(m,tch,a):        
        if m.shutDownTime[tch,a] >=2:    
            return sum(1-m.u[tch,a,h]-m.z[tch,a,h] for h in range(H-m.shutDownTime[tch,a]+1,H) ) >= 0
        else:
            return m.downTimeCon3.Skip
    m.downTimeCon3 = pyo.Constraint(m.tech,m.age,rule=downTimeCon3rule)
    
    # objective。运用解析式定义且写入循环用下标。（应该重新命名变量以便于区分），a[Tech.index(tch)][Age.index(a)]理应工作，但是不成。
    # m.income = pyo.Objective(expr = sum(m.hisPrice[h]*m.x[tch,a,h]-m.x[tch,a,h]*a[Tech.index(str(tch))][Age.index(a)] - m.u[tch,a,h]*b[Tech.index(tch)][Age.index(a)]\
    #                                      for h in T for a in Age for tch in Tech)-500*Num, sense=pyo.maximize)
    #m.t,m.age,m.tech换成T，Age，Tech后相同。
    
    
    #objective。运用解析式定义且写入循环用下标。（重新命名临时循环变量以便于区分）
    #将发电机成本的二次曲线简化为了简单的ax+b模式。a是燃料成本，b是开机费用【需要考虑ramp罚金】
    m.obj = pyo.Objective(expr = sum((m.hisPrice[h]-m.fuel[tch,a])*m.x[tch,a,h]- m.y[tch,a,h]*m.startUpCost[tch,a]- m.z[tch,a,h]*m.shutDownCost[tch,a]-(m.curtailWind[h]+m.curtailSolar[h])*curtailPenalty - m.importElec[h]*importPenalty - m.rejectLoad[h]*VOLL for h in m.t for a in m.age for tch in m.tech), sense=pyo.maximize)
    
    #- m.u[tch,a,h]*rampCost \ ramp不需要特定成本
    # + m.consumeWind[h] + m.consumeSolar[h]   VRE不参与火电厂调度收入，其收入来自FiT，可以单独计算消纳量和收入。
    
    #print(range(m.L['Coal','New']+1))
    #print(m.age['New'])

    return m