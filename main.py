"""
Hannah Burrows and Sabrina Fang
CSE 163 Section AB and SABRINA's SECTION

Van Gogh in the Age of Computers is a project that seeks to explore ____
"""
# command to run code: python main.py

import pandas as pd
import requests
import plotly
import eli5

# import the rest of the sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


def colors_genres(df):
    """
    Comment
    """
    print('started colors_genres')


def van_gogh_topics(df):
    """
    Comment
    """
    print('started van_gogh_topics - this may take a while')
    terms = {}

    # should we define this outside this function? won't be referenced anywhere but is technically a constant
    MET_MUSEUM_API = 'https://collectionapi.metmuseum.org/public/collection/v1'
    paintings_ids = requests.get(MET_MUSEUM_API + '/search?q=Van_Gogh')
    for id in paintings_ids.json()['objectIDs']:
        painting_info = requests.get(MET_MUSEUM_API + '/objects/' + str(id))
        if painting_info.json()['tags']:
            for tag in painting_info.json()['tags']:
                term = tag['term']
                if term in terms:
                    terms[term] += 1
                else:
                    terms[term] = 1
    print(terms)
    # next: sort dictionary
    # splice for top 10
    # graph with plotly


def main():
    print('running main...')
    df = pd.read_csv('df_reduced.csv')
    colors_genres(df)
    van_gogh_topics(df)
    print('finished main!')


if __name__ == '__main__':
    main()
