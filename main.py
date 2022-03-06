"""
Hannah Burrows and Sabrina Fang
CSE 163 Section AB and SABRINA's SECTION

Van Gogh in the Age of Computers is a project that seeks to explore ____
"""

import pandas as pd

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import column

from query_api import query_api_topics
from machine_learning import highest_validation_accuracy, calculate_weights


def process_data(df, hex_df):
    """
    Takes two pandas dataframes, df and hex_df, where both contain information
    about the same paintings and where df contains information about the color
    names while hex_df contains information about the corresponding hex codes,
    and processes the data by removing formatting in columns as necessary and
    joining the two dataframes together. Returns the processed dataframe.
    """
    df.loc[1618, 'Year'] = '1888'
    hex_df = hex_df.rename(columns={'Name': 'Hex Name', 'Colors': 'Hex Code'})

    exploded_colors = remove_color_formatting(df['Colors'])
    df_exploded = df.merge(exploded_colors, left_index=True, right_index=True,
                           how='right')
    df_exploded.to_csv('data/df_reduced_exploded.csv')  # for testing

    exploded_hex = remove_color_formatting(hex_df['Hex Code'])
    df_colors_hex = pd.concat([df_exploded, exploded_hex], axis=1)
    df_colors_hex = df_colors_hex.rename(columns={'Colors_y': 'Color'})

    return df_colors_hex


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


def freq_colors_per_genre(df):
    """
    Takes a pandas dataframe df containing genre, color, and hex code
    information for paintings, and creates a single figure with bar graphs
    showing the top 10 most used colors and their counts for each genre in the
    dataframe. If a genre does not use 10 or more colors, the bar graph shows
    as many colors as the genre uses. The figure should open in the browser
    automatically, but is also saved in an html file, graphs/q2.html.
    """
    output_file('graphs/q2.html')
    plots = []

    # creates list of genres with more than 15 paintings
    genres_df = df.loc[:, ['Name', 'Genre']]
    genres_df['Count'] = genres_df.groupby('Genre').transform('count')
    genres = genres_df.loc[(genres_df['Count'] > 15), 'Genre']
    genres = genres.unique()

    # goes through each genre in the file and creates bar graph
    for genre in genres:
        # filters data for genre and counts colors
        # please note: there are sometimes mutliple hex codes per color (i.e.
        # "gray" might have hex codes of #D9D8D7, #BFBFBD, #262522, etc.).
        # Since hex codes are only being used to give a sense of what the color
        # being referenced in the graph might look like, this method selects
        # only the first hex code for a color, meaning the hex codes for colors
        # may differ between graphs (and for example, the bar for "gray" may
        # also look different between graphs).
        mask = df['Genre'] == genre
        temp_df = df.loc[mask, ['Color', 'Hex Code']]
        temp_df['Count'] = temp_df.groupby('Color').transform('count')
        temp_df = temp_df.drop_duplicates(subset=['Color'])

        # saves data for each genre to csv in q2_testing_data folder for
        # later testing (graphing using alternative software)
        file_name = 'data/q2_testing_data/' + genre + '.csv'
        df.to_csv(file_name)

        # selects the top 10 colors
        top_10 = temp_df.nlargest(10, 'Count')

        # creates bar graph of the colors and adds it to plots to be displayed
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


def most_frequent_topics(topics, title, filename):
    """
    Takes a dictionary topics where the keys are topics and the values are the
    counts for those topics, as well as a string title and a string filename,
    and creates a bar graph showing the top ten most common topics and their
    counts, with a title of title, and saved at the location filename. If the
    dictionary contains less than ten topics, the bar graph will have as many
    bars as there are topics in the dictionary.
    """
    # converts results from querying api to dataframe
    df = pd.DataFrame(list(topics.items()))
    df.columns = ['Topic', 'Count']

    # sorts dataframe and selects top 10
    top_10 = df.nlargest(10, 'Count')

    # graphs sorted dataframe
    output_file(filename)
    source = ColumnDataSource(top_10)
    topic = top_10['Topic'].tolist()

    f = figure(x_range=topic, width=1000, title=(title))
    f.vbar(x='Topic', top='Count', source=source, width=0.9)
    tooltips = [
        ('Topic', '@Topic'),
        ('Count', '@Count'),
    ]
    f.add_tools(HoverTool(tooltips=tooltips))
    f.title.text_font_size = '16pt'
    f.xgrid.grid_line_color = None

    show(f)


# def test_remove_color_formatting():
    # would have an assert_equals statement here - maybe a few - but not sure
    # how to get those assert_equals's


def test_most_frequent_topics():
    """
    Creates two smaller dictionaries and passes them to most_frequent_topics to
    test that the most_frequent_topics function works as expected - that it
    takes a dictionary with keys as terms and values as counts, sort them
    greatest to least, selects the top 10 terms by count, and creates a bar
    graph of them (and that if there are less than 10 terms in the dictionary,
    the bar graph has as many bars as the dictionary has terms.) Graphs should
    open in browser automatically, or can be accessed in graphs/q4_tests.
    """
    # dictionary with less than ten terms and with counts out of order. Should
    # create graph with 5 bars - men, women, clouds, stars, then shoes
    test_dict_1 = {"clouds": 22, "stars": 10, "women": 84, "men": 98,
                   "shoes": 2}
    # dictionary with 11 terms of varying counts, to ensure only top 10 terms
    # are graphed. Should graph cats, men, women, flower, dogs, clouds, boats,
    # parrots, stars and shoes - ice cream should not be included
    test_dict_2 = {"clouds": 22, "stars": 10, "women": 84, "men": 98,
                   "shoes": 2, "boats": 13, "flowers": 41, "dogs": 29,
                   "cats": 145, "parrots": 11, "ice cream": 1}

    most_frequent_topics(test_dict_1, 'Test 1: 5 Topics',
                         'graphs/q4_tests/test1.html')
    most_frequent_topics(test_dict_2, 'Test 2: 11 Topics',
                         'graphs/q4_tests/test2.html')


def main():
    # read in data
    df = pd.read_csv('data/df_reduced.csv')
    hex_df = pd.read_csv('data/df.csv')

    # process data - merge dataframes, remove formatting, etc.
    df_colors_hex = process_data(df, hex_df)

    # question 1 -
    # values_over_time(df_colors_hex, 'Color', 'graphs/q1-1.html')
    # values_over_time(df, 'Style', 'graphs/q1-2.html')

    # question 2 -
    freq_colors_per_genre(df_colors_hex)

    # question 3 -
    """
    max_accuracy = highest_validation_accuracy(df_colors_hex)
    max_depth = int(max_accuracy['Max Depth'].max())
    print('Max Depth for Highest Validation Accuracy: ' +
          str(max_depth))
    test_accuracy = float(max_accuracy.loc[max_accuracy['Max Depth']
                                           == max_depth, 'Test Accuracy'])
    print('Test Accuracy at Max Depth for Highest Validation Accuracy: ' +
          str(test_accuracy))
    print(calculate_weights(df_colors_hex, max_depth))
    """

    # question 4 - What topics did Van Gogh paint about the most?
    # topics = query_api_topics()
    # most_frequent_topics(topics, 'Most Frequent Topics in Van Gogh\'s \
    #                      Paintings', 'graphs/q4.html')

    # testing!
    test_most_frequent_topics()


if __name__ == '__main__':
    main()
