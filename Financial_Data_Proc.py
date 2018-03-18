# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import parse_santander as ps
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
## Takes inputs from Santander API to calculate the possible mortgage repayment rate and total value of the mortgage you can afford

#Inputs - Pandas data table from Emma Index/Date/Money out (-ve if incoming) / Balance / Who / Transaction Type / Account_Number, Savings from UI double
#Outputs - Repayment_Rate = Double , Max_Mortgage_Value = Double 

def Analyse_Account():
    
    #%% 
    #Load input data
    df=ps.get_transactions()
    
    #%%
    #Select relevant input data
    
    #Filter last year of data
    df.sort_values(by=['Date'])
    Transactions=df.shape[0]
    dates=np
    #MostRecentDate=df.loc[:,'Date'].iloc[Transactions-1]
    #MostRecentDate=dt.datetime.strptime(MostRecentDate, '%Y-%m-%d')
    MostRecentDate=df['Date'].iloc[Transactions-1]
    LastYearTransactions=df[df['Date']>=pd.datetime(MostRecentDate.year-1,MostRecentDate.month,MostRecentDate.day)]
    
    #%%
    #Calculate net income over the year, salaryand rent
    
    #Calculate the delta in balance over last year for each account
    Incomes=-1*np.sum(np.array(LastYearTransactions['Amount'],dtype='double'))
    
    #If the time of the transactions is less than one year, make adjstment to annual savings    
    Beg_Date=LastYearTransactions['Date'].iloc[0]
    End_Date=LastYearTransactions['Date'].iloc[-1]
    Dates_Elapsed=End_Date-Beg_Date
    Net_Annual_Savings=np.sum(Incomes)*365/Dates_Elapsed.days
    
    #Finding your annual salary using median of 12 months of records
    Salaries=np.zeros(12,dtype='double')
    start_date=dt.datetime(MostRecentDate.year-1,MostRecentDate.month,MostRecentDate.day)
    Year=start_date.year
    for month in range(1,13):
        Last_Day_In_Month=dt.date(Year,np.mod(start_date.month+month-1,12)+1,1)-dt.timedelta(days=1)
        if np.mod(start_date.month+month-1,12)== 11 :
            Year=Year+1
        First_Day_In_Month=dt.date(Last_Day_In_Month.year,Last_Day_In_Month.month,1)   
        Temp1=df[df['Date'] >= First_Day_In_Month]
        Temp2=Temp1[Temp1['Date'] <=Last_Day_In_Month]['Amount']
        try:
            Salaries[month-1]=np.min(np.array(Temp2,dtype='double')) #Use min as income is negative
        except ValueError:
            Salaries[month-1]=np.nan
    Annual_Salary=np.nanmedian(Salaries)*-12
    #%%  
    
    #Finding rent payments using same method as salary
    Rents=np.zeros(12,dtype='double')
    start_date=dt.datetime(MostRecentDate.year-1,MostRecentDate.month,MostRecentDate.day)
    Year=start_date.year
    for month in range(1,13):
        Last_Day_In_Month=dt.date(Year,np.mod(start_date.month+month-1,12)+1,1)-dt.timedelta(days=1)
        if np.mod(start_date.month+month-1,12)== 11 :
            Year=Year+1
        First_Day_In_Month=dt.date(Last_Day_In_Month.year,Last_Day_In_Month.month,1)   
        Temp1=df[df['Date'] >= First_Day_In_Month]
        Temp2=Temp1[Temp1['Date'] <=Last_Day_In_Month]['Amount']
        #print(np.max((np.array(Temp2,dtype='double'))))
        try:
            Rents[month-1]=np.max((np.array(Temp2,dtype='double'))) #Use min as income is negative
        except ValueError:
            Rents[month-1]=np.nan
    Rent=np.nanmedian(Rents)
    
    #print('Net_Annual_Savings',Net_Annual_Savings)
    #print('Annual Salary',Annual_Salary)
    #print('Rent',Rent)
    return Net_Annual_Savings,Annual_Salary,Rent
    
#%% 
#Time Increasing Functions

#How your salary or savings are projected to rise, F_metric is the value at t=0
def FinancialGrowth(F_Metric,YearsPredic):
    WageGrowthRate=0.01
    PredSalaries=np.zeros((YearsPredic,1),dtype='double')
    PredSalaries[0]=F_Metric
    for k in range(1,YearsPredic):
        PredSalaries[k]=PredSalaries[k-1]*(1+WageGrowthRate)
    return PredSalaries        
#Each entry is the cumulative value of your savings in that year
def CumSavings(InitialSavings,PredictedSavings):
    #Length=np.shape(PredictedSavings)[0]
    CumSavings=InitialSavings + np.sum(PredictedSavings)
    return CumSavings
