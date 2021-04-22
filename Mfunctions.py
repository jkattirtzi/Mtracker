#from google.oauth2.service_account import Credentials
#import gspread
#from gspread_pandas import Spread, Client
import streamlit as st
import os
import numpy as np
import pandas as pd
import altair as alt
import datetime

import seaborn as sns 
#import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_localsheets():
    df0=pd.read_csv('Mtracker_original.csv')
    df1=pd.read_csv('Mtracker_2.csv')

    df0.rename(columns={'Quantity (ml)':'Quantity'}, inplace=True)
    df0['Date']=pd.to_datetime(df0['Date']).dt.date
    df0['Time']=pd.to_datetime(df0['Time']).dt.time
    df0['Quantity'].fillna(0,inplace=True)
    df0['Quantity']= df0['Quantity'].astype(int)
    df0=df0[['Date','Time','Pee', 'Poop', 'Food', 'Quantity']]
    df1.rename(columns={'Today or Yesterday?':'Yesterday'}, inplace=True)
    df1.rename(columns={'Quantity (ml or mins)':'Quantity'}, inplace=True)
    df1['Timestamp']=pd.to_datetime(df1['Timestamp'])
    df1['Date']=df1['Timestamp'].dt.date
    df1['Time']=pd.to_datetime(df1['Time']).dt.time
    df1.loc[(df1.Yesterday == 'Yesterday'),'Date']-=timedelta(days=1)
    df1['Quantity'].fillna(0,inplace=True)
    df1['Quantity'].replace('', 0, inplace=True)
    df1['Quantity'].replace('none', 0, inplace=True)
    df1['Quantity']=df1['Quantity'].astype(int)
    df1['Time2'] = df1.apply(get_time, axis=1)
    df1=df1[['Date','Time2','Pee', 'Poop', 'Food', 'Quantity']]
    df1.rename(columns={'Time2':'Time'}, inplace=True)
    return df0,df1

#def get_auth():
#    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#    credentials = Credentials.from_service_account_file('./MyProject.json', scopes=scope)
#    return scope, credentials

#def get_sheets():
#    scope,credentials=get_auth()
#    client = Client(scope=scope, creds=credentials)
#    spread = Spread("Marie_Tracker_2.0_(Responses)", client=client)
#    spread0 = Spread("Marie Tracker Responses", client=client)
#    df1=spread.sheet_to_df(index=0)
#    df0=spread0.sheet_to_df(index=0)
#    return df0,df1

def get_time(row):
    time=row['Time']
    date=row['Date']
    time2=datetime.combine(date, time)
    pm=row['AM or PM']
    hour=time.hour
    if pm=='PM':
        if hour > 12:
            pass
        else:
            time2+= timedelta(hours=12)
    elif pm=='AM':
        if hour==12:
            time2.replace(hour=0)
    time2=time2.time()
        
    return time2

def clean_newsheet(df):
    df.rename(columns={'Today or Yesterday?':'Yesterday'}, inplace=True)
    df.rename(columns={'Quantity (ml or mins)':'Quantity'}, inplace=True)
    df['Timestamp']=pd.to_datetime(df['Timestamp'])
    df['Date']=df['Timestamp'].dt.date
    df['Time']=pd.to_datetime(df['Time']).dt.time
    df.loc[(df.Yesterday == 'Yesterday'),'Date']-=timedelta(days=1)
    df['Time2'] = df.apply(get_time, axis=1)
    df['Quantity'].replace('', 0, inplace=True)
    df['Quantity'].replace('none', 0, inplace=True)
    df['Quantity']=df['Quantity'].astype(int)
    df=df[['Date','Time2','Pee', 'Poop', 'Food', 'Quantity']]
    df.rename(columns={'Time2':'Time'}, inplace=True)

    return df

def clean_oldsheet(df0):
    df0.rename(columns={'Quantity (ml)':'Quantity'}, inplace=True)
    df0['Date']=pd.to_datetime(df0['Date']).dt.date
    df0['Time']=pd.to_datetime(df0['Time']).dt.time
    df0['Quantity'].replace('', 0, inplace=True)
    df0['Quantity'].replace('none', 0, inplace=True)
    df0['Quantity']= df0['Quantity'].astype(int)
    df0=df0[['Date','Time','Pee', 'Poop', 'Food', 'Quantity']]
    return df0

def get_dayfood(df):
    tsum=0.0
    df_food=df[df['Food']!='']
    df_food=df['Food'].dropna()

    i_list=df_food['Food'].unique()
    fsum_dict={}
    for i in i_list:
        df_food_i=df_food[df_food['Food']==i]
        fsum=df_food_i['Quantity'].sum()
        fsum_dict[i]=(fsum)
        tsum+=fsum
    fsum_dict['Daily Total']=tsum
    return fsum_dict

def print_dict(fdict):
    for k in fdict.keys():
        st.write(k,fdict[k])
    return

def dict_mean(dict_list):
    mean_dict = {}
    for key in dict_list[0].keys():
        mean_dict[key] = sum(d[key] for d in dict_list) / len(dict_list)
    return mean_dict

def day_pp(yday_pp):
    pp_dict={}
    pp_dict['n_total']=len(yday_pp)
    pp_dict['n_pee']=yday_pp[yday_pp['Pee']=='Pee'].count()[0]
    pp_dict['n_poop']=yday_pp[yday_pp['Poop']=='Poop'].count()[0]
    return pp_dict

def food_chart(df1, var):
    df1_food=df1[df1['Food']!='']
    if var == 'Time':
        df1_food['Time']=pd.to_datetime(df1_food['Date'].astype(str) + ' ' + df1_food['Time'].astype(str)).dt.hour
    df1_food['Quantity']=df1_food['Quantity'].astype(int)
    df1_foodg=df1_food[[var,'Food', 'Quantity']].groupby([var,'Food']).sum()
    df1_foodg2=df1_foodg.to_records()
    df1_foodg2=pd.DataFrame.from_records(df1_foodg2)
    df1_foodg2_total=df1_foodg2.groupby(var).sum().reset_index()
    df1_foodg2_total = df1_foodg2_total.rename(columns = {'index':var})
    df1_foodg2_total['Food']='Total'
    df1_foodg2=df1_foodg2.append(df1_foodg2_total,ignore_index=True)
    C1=alt.Chart(df1_foodg2).mark_line(point=True).encode(
    x=var,
    y=alt.Y('Quantity', impute=alt.ImputeParams(value=0), scale=alt.Scale(domain=[0,750])),
    color='Food',
    tooltip = ['Food', 'Quantity', var]
).properties(width=800,height=400,title='Food Quantity').interactive()
 
    return C1

def diaper_chart(df1,var):
    df1_poo=df1[df1['Poop']=='Poop']
    df1_pee=df1[df1['Pee']=='Pee']
    df1_peepoo=df1[(df1['Pee']=='Pee')| (df1['Poop']=='Poop')]
    if var == 'Time':
        df1_poo['Time']=pd.to_datetime(df1_poo['Date'].astype(str) + ' ' + df1_poo['Time'].astype(str)).dt.hour
        df1_pee['Time']=pd.to_datetime(df1_pee['Date'].astype(str) + ' ' + df1_pee['Time'].astype(str)).dt.hour
        df1_peepoo['Time']=pd.to_datetime(df1_peepoo['Date'].astype(str) + ' ' + df1_peepoo['Time'].astype(str)).dt.hour
    df1_peepoo=df1_peepoo.groupby(var).count().reset_index()
    df1_peepoo['Total']=df1_peepoo['Pee']
    df1_peepoo=df1_peepoo[[var,'Total']]
    df1_poog1=df1_poo[[var,'Poop']].groupby(var).count().reset_index()
    df1_peeg1=df1_pee[[var, 'Pee']].groupby(var).count().reset_index()
    df1_diaper=df1_poog1.merge(df1_peeg1)

    df1_diaper=df1_diaper.merge(df1_peepoo)
    df1_diaper=df1_diaper.melt(var, var_name='Diaper', value_name='count')
    C2=alt.Chart(df1_diaper).mark_line(point=True).encode(
    x=var,
    y=alt.Y('count', impute=alt.ImputeParams(value=0), scale=alt.Scale(domain=[0,12])) ,
    color='Diaper',
    tooltip = ['Diaper', 'count',var]
).properties(width=800,height=400,title='Diaper Count').interactive()
 
    return C2





def charts(df1):
    st.header("Charts By Day")
    C1=food_chart(df1, 'Date')
    C2=diaper_chart(df1, 'Date')
    st.write(C1)
    st.write(C2)
    st.header("Charts By Time")
    C3=food_chart(df1, 'Time')
    C4=diaper_chart(df1, 'Time')
    st.write(C3)
    st.write(C4)

    return
