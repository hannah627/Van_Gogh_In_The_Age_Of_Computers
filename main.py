"""
Hannah Burrows and Sabrina Fang
CSE 163 Section AB and AC

Van Gogh in the Age of Computers is a project that seeks to explore Van Gogh's
works digitally using the Colors of Van Gogh dataset made by Kaggle user
Konstantinos and found at https://www.kaggle.com/pointblanc/colors-of-van-gogh.
Our aim is to explore trends and patterns in his work to both better understand
his works and his career, as well as to help the archival and restoration
process of paintings by creating an interpretable machine learning model.
This will predict the most important identifying information about a painting,
which could make the process more efficient overall.

This module is the main page of our code. It creates the graphs for analyzing
how colors and styles changed over time, what colors were most frequently used
in which genres, and what topics Van Gogh most frequently painted about, as
well as create the machine learning model and test our code.
"""

import pandas as pd

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import column
from bokeh.palettes import Spectral

from query_api import query_api_topics
from machine_learning import best_depth, sorted_feature_importances


def process_data(df, hex_df):
    """
    Takes two pandas dataframes, df and hex_df, where both contain information
    about the same paintings and where df contains information about the color
    names while hex_df contains information about the corresponding hex codes.
    Processes the data by removing formatting in columns as necessary and
    joining the two dataframes together. Returns the processed dataframe.
    """
    # corrects an error in the dataset
    df.loc[1618, 'Year'] = 1888
    hex_df = hex_df.rename(columns={'Name': 'Hex Name', 'Colors': 'Hex Code'})

    exploded_colors = remove_color_formatting(df['Colors'])
    df_exploded = df.merge(exploded_colors, left_index=True, right_index=True,
                           how='right')
    # saves dataframe to a .csv file for testing
    df_exploded.to_csv('data/df_testing.csv')

    exploded_hex = remove_color_formatting(hex_df['Hex Code'])
    df_colors_hex = pd.concat([df_exploded, exploded_hex], axis=1)
    df_colors_hex = df_colors_hex.rename(columns={'Colors_y': 'Color'})

    return df_colors_hex


def remove_color_formatting(series):
    """
    Takes a pandas series where values are formatted as ('x', 'y', 'z') and
    returns a series without the parentheses and quotes, and with only one
    value per row.
    """
    series = series.str.replace('\'', '')
    series = series.str.replace('(', '')
    series = series.str.replace(')', '')
    series = series.str.split(', ')
    series = series.explode()

    return series


def format_time_series(p, column, column2):
    """
    Takes a bokeh figure p and two strings, column and column2.
    Returns the bokeh figure with added formatting, including
    tooltips for the x and y columns, an increased title size
    of 16pt, and no vertical gridlines.
    """
    # creates and adds tooltip
    tooltips = [
        ('Year', '@Year{%F}'),
        (column, ('@' + column)),
        (column2, ('@' + column2))
    ]
    p.add_tools(HoverTool(tooltips=tooltips,
                          formatters={'@Year': 'datetime'},
                          mode='vline'))

    # changes font sizes and other formatting
    p.title.text_font_size = '16pt'
    p.xaxis.major_label_text_font_size = '11pt'
    p.yaxis.major_label_text_font_size = '11pt'
    p.xaxis.axis_label_text_font_size = '11.5pt'
    p.yaxis.axis_label_text_font_size = '11.5pt'
    p.xgrid.grid_line_color = None

    return p


def colors_over_time(df):
    """
    Takes a pandas dataframe df containing year, color, and hex code
    information for paintings and creates a time series for each color
    in the dataframe showing the number of times the color was used each year.
    Each figure is encoded with the first occuring (if there are multiple)
    hex code corresponding with that color. If the hex code is the same as the
    hex code for the background color, the background color is changed.
    The figure should open in the browser automatically, but is also saved
    in an html file, graphs/q1-1.html.
    """
    colors = df['Color'].unique()
    # only index 0 (inclusive) to 6 (exclusive) to limit runtime
    colors = colors[0:6]

    output_file('graphs/q1-1.html')
    plots = []

    # goes through each color in the file and creates time series
    for color in colors:
        # filters data for color and counts
        # the number of times color is used over time
        years = pd.DataFrame({'Year': df['Year'].unique()})
        color_count = df.loc[df['Color'] == color, ['Year', 'Color']]
        color_count = years.merge(color_count, left_on='Year', right_on='Year',
                                  how='left')
        color_count['Count'] = \
            color_count.groupby('Year')['Color'].transform('count')
        color_count['Color'] = color_count['Color'].fillna(color)
        color_count['Year'] = pd.to_datetime(color_count['Year'], format='%Y')

        # saves data for each color to csv in q1-1_testing_data folder for
        # later testing (graphing using alternative software)
        color_count = color_count.set_index('Year')
        file_name = 'data/q1-1_testing_data/' + color + '.csv'
        color_count.to_csv(file_name)

        source = ColumnDataSource(color_count)
        hex_code = df.loc[df['Color'] == color, 'Hex Code'].iloc[0]

        # creates time series of the number of times color is used
        # and adds it to plots to be displayed
        p = figure(width=1000,
                   title=('Use of ' + color + ' Over Time'),
                   x_axis_label='Year',
                   y_axis_label=(color + ' Count'),
                   x_axis_type='datetime')
        p.line('Year', 'Count', color=hex_code, line_width=5,
               source=source)

        # change graph background to gray for lines that are white
        if hex_code == '#FFFFFF':
            p.background_fill_color = 'gray'

        # adds formating to the graph - changes title size, adds tooltips, etc.
        p = format_time_series(p, 'Count', 'Color')

        plots.append(p)

    # opens html file in the browser and shows all time series in column layout
    show(column(*plots))


def styles_over_time(df):
    """
    Takes a pandas dataframe df containing year and style information
    for paintings and creates a stacked time series of all the styles
    in the dataframe showing the number of times each style was used each year.
    The line representing each style is encoded with a unique hex code from
    the list colors and labeled in the legend. The figure should open
    in the browser automatically, but is also saved in an html file,
    graphs/q1-2.html.
    """
    output_file('graphs/q1-2.html')

    p = figure(width=1000,
               title=('Styles Over Time'),
               x_axis_label='Year',
               y_axis_label='Style Count',
               x_axis_type='datetime')

    # lines colors that accomodate colorblindness
    colors = ['#DC267F', '#785EF0', '#648FFF', '#FE6100', '#FFB000']

    # goes through each style in the file and creates time series
    for style, color in zip(df['Style'].unique(), colors):
        # filters data for style and counts
        # the number of times style is used over time
        years = pd.DataFrame({'Year': df['Year'].unique()})
        style_count = df.loc[df['Style'] == style, ['Year', 'Style']]
        style_count = years.merge(style_count, left_on='Year', right_on='Year',
                                  how='left')
        style_count['Count'] = \
            style_count.groupby('Year')['Style'].transform('count')
        style_count['Style'] = style_count['Style'].fillna(style)
        style_count['Year'] = pd.to_datetime(style_count['Year'], format='%Y')

        # saves data for each color to csv in q1-2_testing_data folder for
        # later testing (graphing using alternative software)
        style_count = style_count.set_index('Year')
        file_name = 'data/q1-2_testing_data/' + style + '.csv'
        style_count.to_csv(file_name)

        source = ColumnDataSource(style_count)

        # creates and stacks the time series of the number of times
        # style is used
        p.line('Year', 'Count', legend_label=style, line_width=5,
               color=color, source=source)
        p.legend.location = 'top_left'

        # adds formating to the graph - changes title size, adds tooltips, etc.
        p = format_time_series(p, 'Count', 'Style')

    show(p)


def list_unique_from_file(df, col, x):
    """
    Takes a pandas dataframe df, column name column, and integer x.
    Returns a list of the unique values from col where those values
    appear x times or more in df.
    """
    genres_df = df.loc[:, ['Name', col]]
    genres_df['Count'] = genres_df.groupby(col).transform('count')

    # filters for values that occur more than x times
    genres = genres_df.loc[(genres_df['Count'] >= x), col]
    genres = genres.unique()
    return genres


def format_bar_graph(f, x_axis_column, y_axis_column):
    """
    Takes a bokeh figure f and two strings, x_axis_column and y_axis_column,
    and returns the bokeh figure with added formatting, including tooltips for
    the x and y columns, an increased title size of 16pt, and no vertical
    gridlines.
    """
    # creates and adds tooltip
    tooltips = [
        (x_axis_column, ('@' + x_axis_column)),
        (y_axis_column, ('@{' + y_axis_column + '}')),
    ]
    f.add_tools(HoverTool(tooltips=tooltips))

    # changes font sizes and other formatting
    f.title.text_font_size = '16pt'
    f.xaxis.major_label_text_font_size = '11.5pt'
    f.xgrid.grid_line_color = None

    return f


def freq_colors_per_genre(df, genres):
    """
    Takes a pandas dataframe df containing genre, color, and hex code
    information for paintings and a list genres. Creates a single figure with
    bar graphs showing the top 10 most used colors and their counts for each
    genre in df. Each bar is encoded with the first occuring (if there are
    multiple) hex code corresponding with that color. If a genre does not
    use 10 or more colors, the bar graph shows as many colors as the genre
    uses. The figure should open in the browser automatically, but is also
    saved in the html file, graphs/q2.html.
    """
    output_file('graphs/q2.html')
    plots = []

    for genre in genres:
        # filters data for genre and counts colors
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
        f = figure(x_range=colors, width=1200,
                   title=('Most Frequently Used Colors For: ' + genre.title()))
        f.vbar(x='Color', top='Count', color='Hex Code',
               source=source, width=0.9)

        # adds formating to the graph - changes title size, adds tooltips, etc.
        f = format_bar_graph(f, 'Color', 'Count')

        plots.append(f)

    # opens html file in the browser and shows all bar graphs in column layout
    show(column(*plots))


def top_ten_importances(feature_importances):
    """
    Takes a list feature_importances containing tuples with feature names and
    feature importances and creates a bar graph showing the top 10 most
    important features in the list and their importances. The figure should
    open in the browser automatically, but is also saved in the html file,
    graphs/q3.html.
    """
    output_file('graphs/q3.html')
    # selects the top 10 feature importances
    top_10 = feature_importances[0:10]

    # further processes data
    data = []
    for feature, importance in top_10:
        feature = feature.replace('_', ': ')
        data.append({'Feature': feature,
                     'Importance': importance})
    data = pd.DataFrame(data)
    data['Color'] = ['#171723', '#490092', '#b66dff', '#ff6db6', '#006ddb',
                     '#22cf22', '#ffdf4d', '#db6d00', '#8f4e00', '#920000']

    # saves data for top 10 most important features to csv in q3_testing_data
    # folder for later testing (graphing using alternative software)
    data = data.set_index('Feature')
    file_name = 'data/q3_testing_data/top_ten_importances.csv'
    data.to_csv(file_name)

    source = ColumnDataSource(data)

    # creates bar graph of the features
    f = figure(x_range=data.index.tolist(), width=1200, height=950,
               title='Top 10 Features By Importance',
               y_axis_label='Importance')
    f.vbar(x='Feature', top='Importance',
           color='Color', width=0.9, source=source)

    # adds formating to the graph - changes title size, adds tooltips, etc.
    f = format_bar_graph(f, 'Feature', 'Importance')
    f.yaxis.axis_label_text_font_size = '11.5pt'
    f.xaxis.major_label_orientation = 'vertical'

    # opens html file in the browser and shows bar graph
    show(f)


def most_frequent_topics(topics, title, filename):
    """
    Takes a dictionary topics where the keys are topics and the values are
    the counts for those topics, as well as a string title and a string
    filename. Creates a bar graph showing the top ten most common topics and
    their counts, with a title of title, saved at the location filename. If
    the dictionary contains less than ten topics, the bar graph will have as
    many bars as there are topics in the dictionary.
    """
    # converts results from querying api to dataframe
    df = pd.DataFrame(list(topics.items()))
    df.columns = ['Topic', 'Count']

    # sorts dataframe and selects top 10
    top_10 = df.nlargest(10, 'Count')
    top_10['Color'] = Spectral[len(top_10)]

    # graphs sorted dataframe
    output_file(filename)
    source = ColumnDataSource(top_10)
    topic = top_10['Topic'].tolist()

    f = figure(x_range=topic, width=1000, title=(title))
    f.vbar(x='Topic', top='Count', color='Color', source=source, width=0.9)

    # adds formating to the graph - changes title size, adds tooltips, etc.
    f = format_bar_graph(f, 'Topic', 'Count')

    show(f)


def test_most_frequent_topics():
    """
    Tests that the most_frequent_topics function works as expected by
    creating two smaller dictionaries and passing them to most_frequent_topics.
    The most_frequent_topics function is expected to take a dictionary with
    keys as terms and values as counts, sort them from greatest to least,
    select the top 10 terms by count, and create a bar graph. If there are
    less than 10 terms in the dictionary, the bar graph has as many bars as
    the dictionary has terms. Smaller dictionaries were used to ensure the
    function works on inputs other than the values returned from querying
    the Met Museum API. Graphs should open in browser automatically, or can
    be accessed in graphs/q4_tests.
    """
    # dictionary with less than ten terms and with counts out of order
    # creates graph with 5 bars - men, women, clouds, stars, then shoes
    test_dict_1 = {"clouds": 22, "stars": 10, "women": 84, "men": 98,
                   "shoes": 2}
    # dictionary with 11 terms of varying counts, to ensure only top 10
    # terms are graphed
    # graphs cats, men, women, flower, dogs, clouds, boats, parrots,
    # stars and shoes - ice cream should not be included
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

    # processes data - merges dataframes, removes formatting, etc.
    df_colors_hex = process_data(df, hex_df)

    # question 1 - How did the colors and styles Van Gogh use change over time?
    colors_over_time(df_colors_hex)
    styles_over_time(df)

    # question 2 - What colors were used most in each genre?
    genres = list_unique_from_file(df, 'Genre', 15)
    freq_colors_per_genre(df_colors_hex, genres)

    # question 3 - Can we create an accurate model to predict the style of a
    # painting based on data such as the colors it contains and the year it was
    # painted? and According to our model, what is the most important feature
    # for determining the style of a painting?
    accuracy_at_depth = best_depth(df_colors_hex)
    print('Predicting test set using the depth of: ' +
          str(accuracy_at_depth[0]))
    print('Test set accuracy: ' + str(accuracy_at_depth[1]))
    top_ten_importances(sorted_feature_importances(df_colors_hex,
                                                   accuracy_at_depth[0]))

    # question 4 - What topics did Van Gogh paint about the most?
    topics = query_api_topics()
    most_frequent_topics(topics, 'Most Frequent Topics in Van Gogh\'s \
Paintings', 'graphs/q4.html')

    # testing
    test_most_frequent_topics()


if __name__ == '__main__':
    main()
