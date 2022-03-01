"""
Hannah Burrows and Sabrina Fang
CSE 163 Section AB and SABRINA's SECTION

Van Gogh in the Age of Computers is a project that seeks to explore ____
"""
# command to run code: python main.py

import pandas as pd
import plotly
import eli5

# import the rest of the sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

import query_api

def colors_genres(df):
    """
    Comment
    """
    print('started colors_genres')


def graph_topics(top_10):
    """
    Takes a sorted list of tuples representing 10 topics and creates a bar graph representing them.
    """
    print(top_10)


def main():
    print('running main...')
    df = pd.read_csv('df_reduced.csv')
    colors_genres(df)
    top_10 = query_api.query_api_topics()
    graph_topics(top_10)
    print('finished main!')


if __name__ == '__main__':
    main()
