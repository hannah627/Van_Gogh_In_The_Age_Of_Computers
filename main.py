"""
Hannah Burrows and Sabrina Fang
CSE 163 Section AB and SABRINA's SECTION

Van Gogh in the Age of Computers is a project that seeks to explore ____
"""
# command to run code: python main.py

import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from ipywidgets import widgets
import eli5

# import the rest of the sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

from query_api import query_api_topics


def colors_genres(df):
    """
    Comment
    """
    print('started colors_genres')

    fig = go.FigureWidget()
    fig.add_bar(x=df['Color'], y=df['Count'])
    fig.layout.title.text = 'Most Frequently Used Colors'

    genre = widgets.Dropdown(
        options=list(df['Genre'].unique()),
        value='still life',
        description='Genre: '
    )

    if genre.value in df['Genre'].unique():
        print('agh')
        filter_for_genre = df['Genre'] == genre.value
        temp_df = df[filter_for_genre]




def select_top_10(dictionary, columns_names):
    """
    Takes a dictionary where the keys are something specified by the first
    string in columns_names and the values are the counts for those keys, as
    well as a list of column names, and returns the top 10 of those keys and
    their counts as a pandas dataframe top_10.
    """
    df = pd.DataFrame(list(dictionary.items()))
    df.columns = columns_names
    top_10 = df.nlargest(10, 'Count')
    return top_10


def graph_top_10(top_10, xcol, title):
    """
    Takes a string xcol, a string title, and a sorted pandas dataframe top_10
    with columns for something specified in xcol (i.e. 'Topics' or 'Colors')
    and their number of occurences and creates a bar graph representing them.
    """
    fig = px.bar(top_10, x=xcol, y='Count', title=title)
    fig.show()  # semi-interactive - can hover
    fig.write_image('graphs/question_4.png', auto_open=True)


def main():
    print('running main...')
    df = pd.read_csv('df_reduced.csv')

    # colors_genres(df)

    # question 4 - What topics did Van Gogh paint about the most?
    """
    topics = query_api_topics()
    top_10_topics = select_top_10(topics, ['Topic', 'Count'])
    graph_top_10(top_10_topics, 'Topic', 'Top 10 Topics in Van Gogh\'s \
Paintings')
    """

    # testing q4:
    test_dict = {"clouds": 22, "stars": 10, "women": 84, "men": 187,
                 "shoes": 2}
    test = select_top_10(test_dict, ['Topic', 'Count'])
    print('test df: ', test)
    graph_top_10(test)
    """
    test2 = select_top_10(test_dict, ['Colors', 'Count']) # diff colnames works
    print(test2)
    """

    print('finished main!')


if __name__ == '__main__':
    main()
