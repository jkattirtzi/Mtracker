def food_chart(df1, var):
    df1_food=df1[df1['Food']!='']
    if var == 'Time':
        df1_food['Time']=pd.to_datetime(df1_food['Time']).dt.hour
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

    return
