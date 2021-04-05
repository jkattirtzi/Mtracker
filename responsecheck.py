import pandas as pd
import os 
#os.system("cp ~/Downloads/Marie_Tracker_Responses1.csv ./MarieTrackerResponses1.csv")
df1=pd.read_csv("MarieTrackerResponses1.csv")
df1['Date']=pd.to_datetime(df1['Date'], format='%d/%m/%Y')
df1['Date']=pd.to_datetime(df1['Date']).dt.strftime("%Y-%m-%d")
df1=df1[['Date','Time','Pee','Poop','Food','Quantity (ml)','Notes']]
df1=df1.replace('none', 0)
df1.to_csv('Marie_Tracker_Responses1.csv')
