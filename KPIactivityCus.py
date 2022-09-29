# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:49:07 2019
"""


import pandas as pd

file = "tableInput.txt"

def getData(nameFile):
    """idCus dateSales"""
    dataSet = pd.read_csv(nameFile, sep=';', low_memory=False, dtype={"idCus":'str'})
    return dataSet


mainFrame = getData(file)
mainFrame['dateSales'] = pd.to_datetime(mainFrame.loc[:,'dateSales']) #date format for all dates

listCus = mainFrame['idCus'].drop_duplicates().tolist()
#listCus = ['10089018']

t1 = pd.DataFrame(columns=('idCus','status','dni','status2','avg','std'))

maxDate = mainFrame['dateSales'].max()
maxYear = mainFrame['dateSales'].dt.year.max()
maxYearMonth = mainFrame.loc[mainFrame.dateSales.dt.year == maxYear,'dateSales'].dt.month.max()

rowNum = 0

CusidList = list()
for i in listCus:
    dta = mainFrame.loc[mainFrame.idCus ==  i,'dateSales'].sort_values(ascending=False) # data for user
    
    t = mainFrame.loc[(mainFrame.idCus == i) & (mainFrame.dateSales.dt.year == maxYear),'dateSales'].sort_values(ascending=False).to_frame()
    
    t['date_new'] = t.dateSales.shift(periods=1, freq=None, axis=0)
    t = t.iloc[1:]
    t['df_date'] = (t['date_new'] - t['dateSales']).dt.days.fillna(0).astype(int)
    avg = round(t.df_date.mean(),3)
    std = round(t.df_date.std(),3)
    
    DaysFromMaxDays = (maxDate-dta.max()).days
    DaysFromMaxDays_ = (maxDate-dta[dta.dt.month != maxYearMonth].max()).days
    
    x = 0
    if dta[(dta.dt.year == maxYear) & (dta.dt.month == maxYearMonth)].count() == 0:
        
        for a in range(1,4):
            if dta[dta.dt.month == (maxDate - pd.DateOffset(months=a)).month].count() > 0:
                x += 1
            else: break

    if x == 3:
        t1.loc[rowNum] = [i,0,DaysFromMaxDays,'neglected',avg,std]
    elif int(dta[(dta.dt.year == maxYear)& (dta.dt.month == maxYearMonth)].count())  >= 1 and int(dta[(dta.dt.year == maxYear) & (dta.dt.month != maxYearMonth)].count()) == 0:
        t1.loc[rowNum] = [i,'newThisYear',DaysFromMaxDays,0,avg,std]
    elif DaysFromMaxDays >= 180:
        t1.loc[rowNum] = [i,'lost6M',DaysFromMaxDays,0,avg,std]
    elif DaysFromMaxDays >= 90:
        t1.loc[rowNum] = [i,'lost3M',DaysFromMaxDays,0,avg,std]
    elif DaysFromMaxDays >= 60:
        t1.loc[rowNum] = [i,'lost2M',DaysFromMaxDays,0,avg,std]
    elif dta[(dta.dt.year == maxYear) & (dta.dt.month == maxYearMonth)].count() > 0 and DaysFromMaxDays_ >= 210:
        t1.loc[rowNum] = [i,'backToLife6M',DaysFromMaxDays_,0,avg,std]
    elif dta[(dta.dt.year == maxYear) & (dta.dt.month == maxYearMonth)].count() > 0 and DaysFromMaxDays_ >= 120:
        t1.loc[rowNum] = [i,'backToLife3M',DaysFromMaxDays_,0,avg,std]        
    else:
        t1.loc[rowNum] = [i,'normal',DaysFromMaxDays,0,avg,std]
    
    rowNum += 1
    
    CusidList.append(i)
    
    if len(CusidList) % 10 == 0:
        print("Qty_user: ",len(CusidList), "/",len(listCus))
    else:
        continue

t1.loc[t1.status != 'normal'].to_csv('KPIuser2.txt',sep=';',index=False, header=True)
print('koniec!')
