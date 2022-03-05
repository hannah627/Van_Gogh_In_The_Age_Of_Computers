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
from re import X
from tkinter import Y
import pandas as pd
import plotly.express as px

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import column

from query_api import query_api_topics
from machine_learning import highest_validation_accuracy, calculate_weights


def values_over_time(df, column_name, output_file_name):
    """
    DESCRIPTION, PARAMETERS, RETURNS
    """
    df = df[['Year', column_name]].dropna()
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')

    values = df[column_name].unique()
    # for testing, processing a large number of unique values slows the program
    values = values[0:5]

    output_file(output_file_name)

    plots = []

    # goes through each value in the file and creates time series
    for value in values:
        # filters and processes data
        years = df['Year'].unique()
        value_count = df[df[column_name] ==
                         value].groupby('Year')[column_name].count()

        # creates time series and adds it to plots to be displayed
        p = figure(width=1000, height=750,
                   title=('Use of ' + value + ' Over Time'),
                   x_axis_type='datetime')
        p.line(years, value_count, line_width=2)
        plots.append(p)

    # opens html file in the browser and shows all time series in column layout
    show(column(*plots))


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
    df.loc[1618, 'Year'] = '1888'
    hex_df = pd.read_csv('df.csv')

    exploded_colors = remove_color_formatting(df['Colors'])
    df_exploded = df.merge(exploded_colors, left_index=True, right_index=True,
                           how='right')

    # question 1 -
    values_over_time(df_exploded, 'Colors_y', 'graphs/q1-1.html')
    values_over_time(df, 'Style', 'graphs/q1-2.html')

    # question 2 -
    freq_colors_per_genre(df, hex_df)

    # question 3 -
    max_accuracy = highest_validation_accuracy(df_exploded)
    max_depth = int(max_accuracy['Max Depth'].max())
    print('Max Depth for Highest Validation Accuracy: ' +
          str(max_depth))
    test_accuracy = float(max_accuracy.loc[max_accuracy['Max Depth']
                                           == max_depth, 'Test Accuracy'])
    print('Test Accuracy at Max Depth for Highest Validation Accuracy: ' +
          str(test_accuracy))
    print(calculate_weights(df_exploded, max_depth))

    # question 4 - What topics did Van Gogh paint about the most?
    # most_frequent_topics()


if __name__ == '__main__':
    main()
