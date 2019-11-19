import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns

# Importing the data

texas_d = pd.read_csv("houston_defense.csv", sep=',', header=0)
texas_d.head()