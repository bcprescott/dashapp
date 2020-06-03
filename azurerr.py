#!/usr/bin/env python
# coding: utf-8

# # Resource Utilization - A Predictive Analytics Story

# In[1]:


#get_ipython().system('pip install numpy')
#get_ipython().system('pip install pandas')
#get_ipython().system('pip install matplotlib')
#get_ipython().system('pip install plotly')
#get_ipython().system('pip install dash')


# In[1]:


#Module importing and data setup
import os
from random import randint

from plotly.graph_objs import *

import flask
import dash.dependencies

##
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt


url = 'https://raw.githubusercontent.com/bcprescott/dashapp/master/azurerr.csv'

csv = pd.read_csv(url, error_bad_lines=False)
data = csv.copy()


# ### Define Classes/Functions

# In[2]:


#Prints all unique values in each column of the dataset
#df input = the dataset
def unicol(dataframe):
    columns = list(dataframe)
    for col in columns:
        print(col,'\n',dataframe[col].unique(), '\n')
        
def rolling_hours(data):
    data = data.set_index("start").sort_index()
    hours = data.rolling("360D")["hours"].sum()
    data["addhours"] = hours
    data = data.reset_index()
    return data


# In[3]:


#Return unique values in each row
unicol(data)


# In[4]:


#Create new names for columns that are easier to manage
#Assign new names back to dataframe
data.columns = ['id','priority','status','suggested_resource','project','role','start','end','hours','schedule','held','resource','rate','created','pm']
data_drop = data.drop(columns=['id','suggested_resource','priority','status','schedule','held','rate'])
data_drop.head()


# In[5]:


#Check columns and types
#Create df copy
data_drop.info()
data_drop_clean = data_drop.copy()


# In[6]:


#Identify columns that should be a datetime type. Add to list
#Update columns to be of datetime type
# datecols = ['start','end','created']
# data_drop_clean[datecols] = data_drop[datecols].apply(pd.to_datetime,errors='coerce')
data_drop_clean['start'] = data_drop['start'].apply(pd.to_datetime,errors='coerce')


# In[7]:


#Validating dtype conversions
data_drop_clean.info()


# In[16]:


#Creating rolling window for cumulative hours by date
grouped_hours = data_drop_clean.groupby('resource').apply(rolling_hours)


# In[17]:


zach = grouped_hours.loc['Zach Milleson']


# In[18]:


zach = zach.sort_values(by=['start'],ascending=True)


# In[19]:


zach['start'] = zach['start'].dt.strftime('%Y-%m-%d')


# In[22]:


plot = px.bar(zach, x='resource',y='addhours',animation_frame='start',range_x = ['2019-02-20','2020-05-19'],range_y=[0,2000])


# In[ ]:


# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)


# Put your Dash code here
app.layout = html.Div([dcc.Graph(figure=plot)])

# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
# In[ ]:




