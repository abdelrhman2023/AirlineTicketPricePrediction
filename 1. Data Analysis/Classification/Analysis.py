# -*- coding: utf-8 -*-
"""Analysis (classification).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WXM6lEnN2PM17AVvMiy6n6eeEibLhT9u
"""

from google.colab import drive
drive.mount("/content/gdrive")

pip install dataprep

import numpy as np
import pandas as pd
import seaborn as sns
from dataprep.eda import create_report

"""## Load Data"""

dataset = pd.read_csv('/content/gdrive/My Drive/airline-price-classification.csv')
dataset.head()

dataset.info()

np.sum(dataset.isna())

"""## Check for duplicates & Remove them"""

np.sum(dataset.duplicated())

dataset.drop_duplicates(subset=None, keep='first', inplace=True)

"""# Format Date"""

from dataprep.clean import clean_date
dataset = clean_date(dataset, 'date',output_format='YYYY-MM-DD', fix_missing='minimum', report=True)

dataset["date"] = pd.to_datetime(dataset["date_clean"],infer_datetime_format=True)
dataset.drop(["date_clean"], axis = 1, inplace = True)

"""## Extract day & month of each flight"""

dataset["Journey_day"] = dataset["date"].dt.day
dataset["Journey_month"] = dataset["date"].dt.month
dataset["Day"] = dataset["date"].dt.day_name()
dataset["Month"] = dataset["date"].dt.month_name()
#dataset.drop(["Date"], axis = 1, inplace = True)
dataset.head()

"""## Split route into source & destination"""

import ast

def split_route(item):
  dictionary = ast.literal_eval(item)
  source = dictionary['source']
  destination = dictionary['destination']
  return source,destination

dataset['source'] = dataset["route"].apply(lambda x:split_route(x)[0])
dataset['destination']  = dataset["route"].apply(lambda x:split_route(x)[1])
dataset.drop(["route"], axis = 1, inplace = True)
dataset.head()

"""## get the number of stops for each flight"""

def stops(item):
  if item[:3] == 'non':
    return 0
  else:
    num = item[:1]
    return num

dataset['stop'] = dataset["stop"].apply(lambda x:stops(x))
dataset.head()

dataset.drop(["ch_code", "num_code"], axis = 1, inplace = True)

dataset.dtypes

dataset['Journey_day']=dataset['Journey_day'].astype(str)
dataset['Journey_month']=dataset['Journey_month'].astype(str)

report = create_report(dataset)
report

from dataprep.eda import plot
plot(dataset)

from google.colab import files
dataset.to_csv('Airline-Data-Analysis-Classification.csv')
files.download('Airline-Data-Analysis-Classification.csv')
