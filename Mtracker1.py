import streamlit as st
import os
import numpy as np
import pandas as pd
import altair as alt
import datetime




def get_inputs():
    st.header("Inputs")
    data={}
    today=datetime.datetime.utcnow()-datetime.timedelta(hours=4)
    today_date=today.date()
    today_time=today.time()
    d = st.date_input("Date",today_date)
    data['Date']=d
	#st.write('Date:', d)
    t=st.time_input('Time', today_time)
	#st.write('Time', t)
    data['Time']=t

    Foptions=['','Breast (Fed)', 'Breast (Pumped)', 'Formula (Similac)', 'Formula (Neopro)', 'Formula (Neopro Gentlease)']
    Food = st.selectbox('Food',Foptions)
    data['Food']=Food
    Quantity=st.number_input('Quantity (ml)', value=0, step=5)
    data['Quantity (ml)']=Quantity

    st.write("Diaper Inputs")
    pee = st.checkbox('pee')
    poo = st.checkbox('poo')
    if pee ==1:
        data['Pee']='Pee'
    else:
        data['Pee']=''
    if poo ==1:
        data['Poop']='Poop'
    else:
        data['Poop']=''
    notes= st.text_input("Notes", value = '')
    data['Notes'] =notes
#    cs=df1.columns.to_list()
#    st.write(cs)
    data_df=pd.DataFrame([data])
    data_df=data_df.replace('Empty', ' ')
#    st.write(data_df)
    data_df=data_df[['Date', 'Time', 'Pee', 'Poop', 'Food', 'Quantity (ml)', 'Notes']]
#    save=st.selectbox("End",['save or test?','save','test'])
#    if save=='save':
#       data_df.to_csv("temp.csv")
#       st.write("Saved")
#       st.write(df1.iloc[-1])
#    elif save=='test':
#       data_df.to_csv("temp.csv")
#       st.write("Written to temp")
#    save= st.selectbox('Delete will not include above input, Temp gives one shot, Save adds input to file',['Delete','Save','Temp'])
    save=st.button("Save")
    if save ==True:
        data_df.to_csv("temp.csv")
        st.write("Saved")
#        df2=get_fulldata()
#        df2.to_csv("Marie_Tracker_Responses1.csv")
#    elif save=='Delete':
#        os.remove("temp.csv")
#    elif save=='Temp':
#        pass
    return 

def get_data0():
    df1=pd.read_csv("Marie_Tracker_Responses1.csv")
    df1=df1[['Date','Time', 'Pee', 'Poop', 'Food', 'Quantity (ml)', 'Notes']]
    #df1['Date']=pd.to_datetime(df1['Date'], format='%d/%m/%Y')
    df1['Date']=pd.to_datetime(df1['Date'])
    df1['Date']=df1['Date'].dt.date
    df1=df1.replace(np.nan, '', regex=True)
    df1.loc[df1['Notes'].str.contains('Gentlease'),'Food']='Formula (Neopro Gentlease)'
    return df1

def get_fulldata():
    df1=get_data0()
    if os.path.isfile("temp.csv"):
        temp=pd.read_csv("temp.csv",index_col=0)
        temp['Date']=pd.to_datetime(temp['Date'])
        temp['Date']=temp['Date'].dt.date
        df1=df1.append(temp,ignore_index=True)
        df1.to_csv("Marie_Tracker_Responses1.csv")
        os.remove("temp.csv")
    return df1

st.title ("Marie Tracker")

def main():
    df1=get_fulldata()
    df1r=df1[::-1]
    df1f=df1r[df1r['Food']!='']
    df1f=df1f.iloc[0]
    st.header("Home")
    st.write("Last feeding", df1f['Date'], df1f['Time'], df1f['Food'], df1f['Quantity (ml)'],"ml")

    st.subheader("Last 3 days")
    date_uni=df1r['Date'].unique()
    days3=date_uni[1:4]    

    df1_1=df1[df1['Date']==days3[0]]
    df1_2=df1[df1['Date']==days3[1]]
    df1_3=df1[df1['Date']==days3[2]]
    df_list=[df1_1,df1_2,df1_3]


#    st.write("test", df1_1[(df1_1['Pee']=='Pee')| (df1_1['Poop']=='Poop')].count()[0])

#    var=['Total Diapers', 'Number Pee', 'Number Poop']
    days_d=[]
    for day in range(3):
        df_day=df_list[day]
        day_d={}
        day_d['Date']=days3[day]
        day_d['Total Diapers']= df_day[(df_day['Pee']=='Pee')| (df_day['Poop']=='Poop')].count()[0]
        day_d['N.o Poop']= df_day[(df_day['Poop']=='Poop')].count()[0]
        day_d['N.o Pee']= df_day[(df_day['Pee']=='Pee')].count()[0]
        days_d.append(day_d)
    days_df=pd.DataFrame(days_d)
    st.write(days_df)
    st.write("Feeding on ", days3[0])
    st.write(df1_1[['Date','Food', 'Quantity (ml)' ]].groupby('Food').sum())
    st.write("Feeding on ", days3[1])
    st.write(df1_2[['Date','Food', 'Quantity (ml)' ]].groupby('Food').sum())
    st.write("Feeding on ", days3[2])
    st.write(df1_3[['Date','Food', 'Quantity (ml)' ]].groupby('Food').sum())

        #st.write(df_i[['Date','Food', 'Quantity (ml)' ]].groupby('Food').sum())

    
    select_date = st.selectbox('Date',(days3[0], days3[1], days3[2]))
    if select_date==days3[0]:
        st.write(df1_1)
    elif select_date==days3[1]:
        st.write(df1_2)
    elif select_date==days3[2]:
        st.write(df1_3)



#    df1_yfood=df1_y[df1_y['Food']!='']
#    df1_yfood['Quantity (ml)']=df1_yfood['Quantity (ml)'].astype(int)
#    st.write(df1_y)
#    st.write("Number of Times Pee:",df1_y[df1_y['Pee']!='']['Pee'].count())
#    st.write("Number of Times Poop:",df1_y[df1_y['Poop']!='']['Poop'].count())
#    st.write("Total Feeding (ml):",df1_yfood['Quantity (ml)'].sum())
#    st.write(df1_yfood[['Food', 'Quantity (ml)' ]].groupby('Food').sum())
#    st.write("Full Data")
#    st.write(df1r)

    return

def full_data():
    df1=get_fulldata()
    df1r=df1[::-1]
    st.header("Full Data")
    st.write(df1r)
    return

def food_chart(df1, var):
    df1_food=df1[df1['Food']!='']
    if var == 'Time':
        df1_food['Time']=pd.to_datetime(df1_food['Time']).dt.hour
    df1_food['Quantity (ml)']=df1_food['Quantity (ml)'].astype(int)
    df1_foodg=df1_food[[var,'Food', 'Quantity (ml)']].groupby([var,'Food']).sum()
    df1_foodg2=df1_foodg.to_records()
    df1_foodg2=pd.DataFrame.from_records(df1_foodg2)
    df1_foodg2_total=df1_foodg2.groupby(var).sum().reset_index()
    df1_foodg2_total = df1_foodg2_total.rename(columns = {'index':var})
    df1_foodg2_total['Food']='Total'
    df1_foodg2=df1_foodg2.append(df1_foodg2_total,ignore_index=True)
    C1=alt.Chart(df1_foodg2).mark_line(point=True).encode(
    x=var,
    y=alt.Y('Quantity (ml)', impute=alt.ImputeParams(value=0), scale=alt.Scale(domain=[0,750])),
    color='Food',
    tooltip = ['Food', 'Quantity (ml)', var]
).properties(width=800,height=400,title='Food Quantity').interactive()
 
    return C1

def diaper_chart(df1,var):
    df1_poo=df1[df1['Poop']=='Poop']
    df1_pee=df1[df1['Pee']=='Pee']
    df1_peepoo=df1[(df1['Pee']=='Pee')| (df1['Poop']=='Poop')]
    if var == 'Time':
        df1_poo['Time']=pd.to_datetime(df1_poo['Time']).dt.hour
        df1_pee['Time']=pd.to_datetime(df1_pee['Time']).dt.hour
        df1_peepoo['Time']=pd.to_datetime(df1_peepoo['Time']).dt.hour
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



def charts():
    df1=get_fulldata()
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

page='Home'
page=st.sidebar.selectbox("Which Page Would you like to go to?", ('Home','Input', 'Full Data', 'Charts'))
if page=='Input':
    get_inputs()
if page=='Home':
    main()
if page=='Full Data':
    full_data()    
if page=='Charts':
    charts()
 
