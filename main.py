"""
Sabrina Fang and Hannah Burrows
CSE 163 SECTIONS

PROJECT DESCRIPTION
"""
# command to run code: python home.py

import pandas as pd
import plotly
import eli5

# import the rest of the sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

def main():
    df = pd.read_csv('data/df_reduced.csv')
    print('hello')
    print(df.head())


if __name__ == '__main__':
    main()