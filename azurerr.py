#!/usr/bin/env python
# coding: utf-8

# # Resource Utilization - A Predictive Analytics Story

# In[263]:


#Module importing and data setup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

csv = pd.read_csv('azurerr.csv')
data = csv.copy()


# ### Define Classes/Functions

# In[231]:


#Prints all unique values in each column of the dataset
#df input = the dataset
def unicol(dataframe):
    columns = list(dataframe)
    for col in columns:
        print(col,'\n',dataframe[col].unique(), '\n')
        
def rolling_hours(data):
    data = data.set_index("created").sort_index()
    hours = data.rolling("360D")["hours"].sum()
    data["addhours"] = hours
    return data


# In[225]:


#Return unique values in each row
unicol(data)


# In[226]:


#Create new names for columns that are easier to manage
#Assign new names back to dataframe
data.columns = ['id','priority','status','suggested_resource','project','role','start','end','hours','schedule','held','resource','rate','created','pm']
data_drop = data.drop(columns=['id','suggested_resource','priority','status','schedule','held','rate'])
data_drop.head()


# In[239]:


#Check columns and types
#Create df copy
data_drop.info()
data_drop_clean = data_drop.copy()


# In[242]:


#Identify columns that should be a datetime type. Add to list
#Update columns to be of datetime type
# datecols = ['start','end','created']
# data_drop_clean[datecols] = data_drop[datecols].apply(pd.to_datetime,errors='coerce')
data_drop_clean['created'] = data_drop['created'].apply(pd.to_datetime,errors='coerce')


# In[243]:


#Validating dtype conversions
data_drop_clean.info()


# In[244]:


#Creating rolling window for cumulative hours by date
grouped_hours = data_drop_clean.groupby('resource').apply(rolling_hours)


# In[245]:


zach = grouped_hours.loc['Zach Milleson']


# In[246]:


zach


# In[264]:


plot = px.bar(zach, x='resource',y='addhours',animation_frame='start',range_y=[0,2000])


# In[ ]:


app = dash.Dash()
app.layout = html.Div([dcc.Graph(figure=plot)])

app.run_server()

