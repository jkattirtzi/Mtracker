from Mfunctions import *

st.header("Marie Tracker 2.0")

df0,df1=get_sheets()
df0=clean_oldsheet(df0)
if len(df1)==0:
    df=df0
else:
    df1=clean_newsheet(df1)
    df=df0.append(df1)
df=df.sort_values(by=['Date','Time'],ascending=False).reset_index(drop=True)


st.subheader("Last Feeding")
df_food=df[df['Food']!='']
last=df_food.loc[0]

st.write("Last Feeding" ,last['Date'], last['Time'], last['Food'], last['Quantity'])

st.subheader("Yesterday and Three Day Average")
st.subheader("Yesterday Food")
days=df['Date'].unique()
yesterday=days[1]
last3days=days[1:4]
yday=df[df['Date']==yesterday]
l3days=df[df['Date'].isin(last3days)]
fsum_dict=get_dayfood(yday)
print_dict(fsum_dict)
st.subheader("Three Day Average Food")
day_dict_list=[]
for day in days[1:4]:
    day=l3days[l3days['Date']==day]
    day_dict=get_dayfood(day)
    day_dict_list.append(day_dict)
mean_3days_food=dict_mean(day_dict_list)
print_dict(mean_3days_food)
st.subheader("Yesterday Pee and Poop")
yday_pp=yday[(yday['Pee']=='Pee')| (yday['Poop']=='Poop')]
pp_dict=day_pp(yday_pp)
print_dict(pp_dict)
st.subheader("Three Day Average Pee and Poop")
l3days_pp=l3days[(l3days['Pee']=='Pee')| (l3days['Poop']=='Poop')]

day_dict_list=[]
for day in days[1:4]:
    day=l3days_pp[l3days_pp['Date']==day]
    day_dict=day_pp(day)
    day_dict_list.append(day_dict)
mean_3days_pp=dict_mean(day_dict_list)
print_dict(mean_3days_pp)

charts(df)
