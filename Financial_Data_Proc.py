# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import datetime as dt
## Takes inputs from Santander API to calculate the possible mortgage repayment rate and total value of the mortgage you can afford

#Inputs - Pandas data table from Emma Index/Date/Money out (-ve if incoming) / Balance / Who / Transaction Type / Account_Number, Savings from UI double
#Outputs - Repayment_Rate = Double , Max_Mortgage_Value = Double 

#%% 
#Load input data

#Temp Data
Instances=100
dates=pd.date_range('20130101', periods=Instances)
df= pd.DataFrame({'Date' : dates,
                  'MoneyOut' : np.random.rand(Instances,1)[:,0],
                  'Balance': np.random.rand(Instances,1)[:,0],                
                  'Who': 'Johnny Appleseed',
                  'TransactionType': 'DD',
                  'Account_Number': 1
                  })


#%%
###Select relevant input data
Number_of_accounts=np.max(df['Account_Number'])

#Filter last year of data
df.sort_values(by=['Date'])
Transactions=df.shape[0]
MostRecentDate=df['Date'][Transactions-1]
LastYearTransactions=df[df['Date']>=pd.datetime(MostRecentDate.year-1,MostRecentDate.month,MostRecentDate.day)]

#%%
#Calculate net income over the year, salaryand rent

#Calculate the delta in balance over last year for each account
Incomes=np.zeros((Number_of_accounts,1),dtype='double')
for i in range(Number_of_accounts+1):
    Incomes[i-1]=np.sum(LastYearTransactions[LastYearTransactions['Account_Number']==i]['Balance'])

#If the time of the transactions is less than one year, make adjstment to annual savings    
Beg_Date=LastYearTransactions['Date'][Transactions-LastYearTransactions.shape[0]+1]
End_Date=LastYearTransactions['Date'][Transactions-1]
Dates_Elapsed=End_Date-Beg_Date
Net_Annual_Savings=np.sum(Incomes)*-365/Dates_Elapsed.days

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
    Temp2=Temp1[Temp1['Date'] <=Last_Day_In_Month]['MoneyOut']
    Salaries[month-1]=np.min(Temp2) #Use min as income is negative
    
Annual_Salary=np.nanmedian(Salaries)*-12
  
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
    Temp2=Temp1[Temp1['Date'] <=Last_Day_In_Month]['MoneyOut']
    Rents[month-1]=np.max(Temp2) #Use min as income is negative
    
Rent=np.nanmedian(Rents)

print('Net_Annual_Savings',Net_Annual_Savings)
print('Annual Salary',Annual_Salary)
print('Rent',Rent)
    
        

