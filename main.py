"""
Hannah Burrows and Sabrina Fang
CSE 163 Section AB and SABRINA's SECTION

Van Gogh in the Age of Computers is a project that seeks to explore ____
"""
# command to run code: python main.py
# if you have issues where it says pandas is not found/installed, kill
# terminals and start a new Command Line terminal
# plotly and sklearn and pandas should be fine, but if you're getting warnings
# about bokeh or eli5, google conda install [package] and run that and it
# should fix it

from os import remove
import pandas as pd
import plotly.express as px

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import column

import eli5

# import the rest of the sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

from query_api import query_api_topics


def freq_colors_per_genre(df, hex_df):
    """
    Takes two pandas dataframes each containing data on paintings, where df
    contains the word versions of colors and hex_df contains the hex code
    versions of colors, and creates a single figure with bar graphs showing the
    top 10 most used colors and their counts for each genre in the dataframes.
    If a genre does not use 10 or more colors, the bar graph shows as many
    colors as the genre uses. Assumes each row in df corresponds with a row
    in hex_df. The figure is saved in an html file, graphs/q2.html.
    """
    # clarify difference between columns of dataframes by renaming them
    hex_df = hex_df.rename(columns={'Name': 'Hex Name', 'Colors': 'Hex Code'})
    df = df.rename(columns={'Colors': 'Color'})

    output_file('graphs/q2.html')
    plots = []

    # creates list of genres with more than 15 paintings
    genres_df = df.loc[:, ['Name', 'Genre']]
    genres_df['Count'] = genres_df.groupby('Genre').transform('count')
    genres = genres_df.loc[(genres_df['Count'] > 15), 'Genre']
    genres = genres.unique()

    # goes through each genre in the file and creates bar graph
    for genre in genres:
        # filters and processes data
        mask = df['Genre'] == genre
        s_hex = hex_df.loc[mask, 'Hex Code']
        s_hex = remove_color_formatting(s_hex)
        s_colors = df.loc[mask, 'Color']
        s_colors = remove_color_formatting(s_colors)

        merged = pd.concat([s_colors, s_hex], axis=1)
        merged['Count'] = merged.groupby('Color').transform('count')
        merged = merged.drop_duplicates(subset=['Color'])
        top_10 = merged.nlargest(10, 'Count')

        # creates bar graph adds it to plots to be displayed
        source = ColumnDataSource(top_10)
        colors = top_10['Color'].tolist()
        f = figure(x_range=colors, width=1000,
                   title=('Most Frequently Used Colors For: ' + genre.title()))
        f.vbar(x='Color', top='Count', color='Hex Code',
               source=source, width=0.9)
        tooltips = [
            ('Color', '@Color'),
            ('Count', '@Count'),
        ]
        f.add_tools(HoverTool(tooltips=tooltips))
        f.title.text_font_size = '16pt'
        f.xgrid.grid_line_color = None
        plots.append(f)

    # opens html file in the browser and shows all bar graphs in column layout
    show(column(*plots))


def remove_color_formatting(series):
    """
    Takes a pandas series where values are formatted as ('x', 'y', 'z') and
    returns a series without the parentheses and quotes, and with only one
    value per cell.
    """
    series = series.str.replace('\'', '')
    series = series.str.replace('(', '')
    series = series.str.replace(')', '')
    series = series.str.split(', ')
    series = series.explode()
    return series


def most_frequent_topics():
    """
    Queries the Met Museum API to find the most frequently used tags (topics)
    for their collection of Van Gogh paintings, and creates a bar graph showing
    the top ten most common topics and their counts.
    """
    # queries api
    topics = query_api_topics()

    # converts results from querying api to dataframe
    df = pd.DataFrame(list(topics.items()))
    df.columns = ['Topic', 'Count']

    # sorts dataframe and selects top 10
    top_10 = df.nlargest(10, 'Count')

    # graphs sorted dataframe
    fig = px.bar(top_10, x='Topic', y='Count',
                 title='Top 10 Topics in Van Gogh\'s Paintings')
    fig.update_traces(marker_color='lightslategray')
    fig.update_layout(title_font_size=20)
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=14
        )
    )
    fig.show()  # semi-interactive - can hover


def main():
    # read in data
    df = pd.read_csv('df_reduced.csv')
    hex_df = pd.read_csv('df.csv')

    # question 2 -
    freq_colors_per_genre(df, hex_df)

    # question 4 - What topics did Van Gogh paint about the most?
    # most_frequent_topics()


if __name__ == '__main__':
    main()
