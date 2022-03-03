"""
Hannah Burrows and Sabrina Fang
CSE 163 Section AB and SABRINA's SECTION

Van Gogh in the Age of Computers is a project that seeks to explore ____
"""
# command to run code: python main.py
# if you have issues where it says pandas is not found/installed, kill
# terminals and start a new Command Line terminal
# plotly and sklearn and pandas should be fine, but if you're getting warnings
# about ipywidgets or eli5, google conda install [package] and run that and it
# should fix it

from os import remove
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool, CustomJS, Dropdown, ColumnDataSource, Select
from bokeh.layouts import row, gridplot, column

from ipywidgets import widgets
import eli5

# import the rest of the sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

from query_api import query_api_topics


def colors_genres(df, hex_df):
    """
    Comment
    """
    print('started colors_genres')

    genres = [('landscape', 'Landscape'),
              ('animal painting', 'Animal Painting'),
              ('Sketch and Study', 'sketch and study'),
              ('Still Life', 'still life'),
              ('Genre Painting', 'genre painting'),
              ('Cityscape', 'cityscape'),
              ('Portrait', 'portrait'),
              ('Nude Painting', 'nude painting (nu)'),
              ('Flower Painting', 'flower painting'),
              ('Vanitas', 'vanitas'),
              ('Figurative', 'figurative'),
              ('Self-Portrait', 'self-portrait'),
              ('Panorama', 'panorama'),
              ('Interior', 'interior'),
              ('Marina', 'marina'),
              ('Religious Painting', 'religious painting'),
              ('Cloudscape', 'cloudscape')]

    current_genre = 'still life'

    hex_df = hex_df.rename(columns={'Name': 'Hex Name', 'Colors': 'Hex Code'})
    df = df.rename(columns={'Colors': 'Color'})

    #mask = df['Genre'] == current_genre
    s_genre = df.loc[:, 'Genre']
    s_hex = hex_df.loc[:, 'Hex Code']
    s_hex = remove_color_formatting(s_hex)
    s_colors = df.loc[:, 'Color']
    s_colors = remove_color_formatting(s_colors)

    unfiltered = pd.concat([s_colors, s_hex, s_genre], axis=1)
    print(unfiltered[:10])

    count = s_colors.groupby(s_colors).count()
    print(count)

    # need to find a way to add count as a column to the unfiltered df
    # then filter for first, default genre
    # pass both unfiltered and filtered to callback function
    # filter data using JavaScript in callback and return those changes
    # use filtered data for graphing

    # merged['Count'] = merged.groupby('Color').transform('count')
    # merged = merged.drop_duplicates(subset=['Color'])

    """
    top_10 = merged.nlargest(10, 'Count')

    source = ColumnDataSource(top_10)
    df_source = ColumnDataSource(df)
    hex_df_source = ColumnDataSource(hex_df)

    # cannot get it to update graph with newly filtered data
    callback = CustomJS(args=dict(df=df_source, hex_df=hex_df_source), code="""
        # console.log(df[:10])
        # console.log(cb_obj.value)
    """)

    dropdown = Dropdown(label='Genre', menu=genres)
    dropdown.js_on_event('menu_item_click', callback)

    menu = Select(options=genres, value='Still Life', title='Genre')
    menu.js_on_change('value', callback)

    output_file('graphs/q2.html')

    colors = top_10['Color'].tolist()
    f = figure(x_range=colors, width=1000,
               title=('Most Frequently Used Colors For: ' + current_genre))
    f.vbar(x='Color', top='Count', color='Hex Code', source=source, width=0.9)
    """
    """
    # https://github.com/bokeh/bokeh/issues/3621
    tooltips = [
    ('Color', '@colors'),
    ('Count', '@count'),
    ]
    f.add_tools(HoverTool(tooltips=tooltips))
    """

    # show(row(f, menu))


def og(df, hex_df):
    """
    Graph with colored bars but no hover or filtering based on genre; could use
    for loop and make graphs for each genre, but they would not be interactive
    """
    print('started colors_genres')

    genres = [('landscape', 'Landscape'),
              ('animal painting', 'Animal Painting'),
              ('Sketch and Study', 'sketch and study'),
              ('Still Life', 'still life'),
              ('Genre Painting', 'genre painting'),
              ('Cityscape', 'cityscape'),
              ('Portrait', 'portrait'),
              ('Nude Painting', 'nude painting (nu)'),
              ('Flower Painting', 'flower painting'),
              ('Vanitas', 'vanitas'),
              ('Figurative', 'figurative'),
              ('Self-Portrait', 'self-portrait'),
              ('Panorama', 'panorama'),
              ('Interior', 'interior'),
              ('Marina', 'marina'),
              ('Religious Painting', 'religious painting'),
              ('Cloudscape', 'cloudscape')]

    current_genre = 'still life'

    hex_df = hex_df.rename(columns={'Name': 'Hex Name', 'Colors': 'Hex Code'})
    df = df.rename(columns={'Colors': 'Color'})

    mask = df['Genre'] == current_genre
    s_hex = hex_df.loc[mask, 'Hex Code']
    s_hex = remove_color_formatting(s_hex)
    s_colors = df.loc[mask, 'Color']
    s_colors = remove_color_formatting(s_colors)

    merged = pd.concat([s_colors, s_hex], axis=1)

    merged['Count'] = merged.groupby('Color').transform('count')
    merged = merged.drop_duplicates(subset=['Color'])
    top_10 = merged.nlargest(10, 'Count')
    print(top_10)

    source = ColumnDataSource(top_10)
    df_source = ColumnDataSource(df)
    hex_df_source = ColumnDataSource(hex_df)

    # cannot get it to update graph with newly filtered data
    callback = CustomJS(args=dict(df=df_source, hex_df=hex_df_source), code="""
        console.log(cb_obj.value)
    """)

    # dropdown = Dropdown(label='Genre', menu=genres)
    # dropdown.js_on_event('menu_item_click', callback)

    menu = Select(options=genres, value='Still Life', title='Genre')
    menu.js_on_change('value', callback)

    output_file('graphs/q2.html')

    colors = top_10['Color'].tolist()
    f = figure(x_range=colors, width=1000,
               title=('Most Frequently Used Colors For: ' + current_genre))
    f.vbar(x='Color', top='Count', color='Hex Code', source=source, width=0.9)
    """
    # https://github.com/bokeh/bokeh/issues/3621
    tooltips = [
    ('Color', '@colors'),
    ('Count', '@count'),
    ]
    f.add_tools(HoverTool(tooltips=tooltips))
    """

    show(row(f, menu))


def hover(df, hex_df):
    """
    has hovering and colored bars
    """
    print('started colors_genres')

    genres = [('landscape', 'Landscape'),
              ('animal painting', 'Animal Painting'),
              ('Sketch and Study', 'sketch and study'),
              ('Still Life', 'still life'),
              ('Genre Painting', 'genre painting'),
              ('Cityscape', 'cityscape'),
              ('Portrait', 'portrait'),
              ('Nude Painting', 'nude painting (nu)'),
              ('Flower Painting', 'flower painting'),
              ('Vanitas', 'vanitas'),
              ('Figurative', 'figurative'),
              ('Self-Portrait', 'self-portrait'),
              ('Panorama', 'panorama'),
              ('Interior', 'interior'),
              ('Marina', 'marina'),
              ('Religious Painting', 'religious painting'),
              ('Cloudscape', 'cloudscape')]

    current_genre = 'still life'

    hex_df = hex_df.rename(columns={'Name': 'Hex Name', 'Colors': 'Hex Code'})
    df = df.rename(columns={'Colors': 'Color'})

    mask = df['Genre'] == current_genre
    s_hex = hex_df.loc[mask, 'Hex Code']
    s_hex = remove_color_formatting(s_hex)
    s_colors = df.loc[mask, 'Color']
    s_colors = remove_color_formatting(s_colors)

    merged = pd.concat([s_colors, s_hex], axis=1)

    merged['Count'] = merged.groupby('Color').transform('count')
    merged = merged.drop_duplicates(subset=['Color'])
    top_10 = merged.nlargest(10, 'Count')
    print(top_10)

    source = ColumnDataSource(top_10)

    output_file('graphs/q2.html')

    colors = top_10['Color'].tolist()
    f = figure(x_range=colors, width=1000,
               title=('Most Frequently Used Colors For: ' + current_genre))
    f.vbar(x='Color', top='Count', color='Hex Code', source=source, width=0.9)

    tooltips = [
        ('Color', '@Color'),
        ('Count', '@Count'),
    ]
    f.add_tools(HoverTool(tooltips=tooltips))

    show(row(f))


def test(df, hex_df):
    """
    The one I think we should use: has hovering, colored bars, and graphs for
    all genres
    """
    print('started colors_genres')

    # for testing, could compare count of genres with count of
    # df['Genre'].unique()
    genres = [('Landscape', 'landscape'),
              ('Animal Painting', 'animal painting'),
              ('Sketch and Study', 'sketch and study'),
              ('Still Life', 'still life'),
              ('Genre Painting', 'genre painting'),
              ('Cityscape', 'cityscape'),
              ('Portrait', 'portrait'),
              ('Nude Painting', 'nude painting (nu)'),
              ('Flower Painting', 'flower painting'),
              ('Vanitas', 'vanitas'),
              ('Figurative', 'figurative'),
              ('Self-Portrait', 'self-portrait'),
              ('Panorama', 'panorama'),
              ('Interior', 'interior'),
              ('Marina', 'marina'),
              ('Religious Painting', 'religious painting'),
              ('Cloudscape', 'cloudscape')]

    hex_df = hex_df.rename(columns={'Name': 'Hex Name', 'Colors': 'Hex Code'})
    df = df.rename(columns={'Colors': 'Color'})

    output_file('graphs/q2.html')
    plots = []
    for genre in genres:
        mask = df['Genre'] == genre[1]
        s_hex = hex_df.loc[mask, 'Hex Code']
        s_hex = remove_color_formatting(s_hex)
        s_colors = df.loc[mask, 'Color']
        s_colors = remove_color_formatting(s_colors)

        merged = pd.concat([s_colors, s_hex], axis=1)

        merged['Count'] = merged.groupby('Color').transform('count')
        merged = merged.drop_duplicates(subset=['Color'])
        top_10 = merged.nlargest(10, 'Count')

        source = ColumnDataSource(top_10)

        colors = top_10['Color'].tolist()
        f = figure(x_range=colors, width=1000,
                   title=('Most Frequently Used Colors For: ' + genre[0]))
        f.vbar(x='Color', top='Count', color='Hex Code',
               source=source, width=0.9)

        tooltips = [
            ('Color', '@Color'),
            ('Count', '@Count'),
        ]
        f.add_tools(HoverTool(tooltips=tooltips))
        plots.append(f)

    show(column(*plots))


def remove_color_formatting(series):
    """
    """
    series = series.str.replace('\'', '')
    series = series.str.replace('(', '')
    series = series.str.replace(')', '')
    series = series.str.split(', ')
    series = series.explode()
    return series


def most_frequent_topics():
    """
    Answers question 4
    """
    # queries api
    topics = query_api_topics()

    # converts dictionary from querying api to dataframe
    df = pd.DataFrame(list(topics.items()))
    df.columns = ['Topic', 'Count']

    # sorts dataframe and selects top 10
    top_10 = df.nlargest(10, 'Count')

    # graphs sorted dataframe
    graph_top_10(top_10, 'Topic', 'Top 10 Topics in Van Gogh\'s Paintings')


def graph_top_10(top_10, xcol, title):
    """
    Takes a string xcol, a string title, and a sorted pandas dataframe top_10
    with columns for something specified in xcol (i.e. 'Topics' or 'Colors')
    and their number of occurences and creates a bar graph representing them.
    """
    fig = px.bar(top_10, x=xcol, y='Count', title=title)
    fig.show()  # semi-interactive - can hover
    # fig.write_image('graphs/question_4.png') - need to install kaleido


def main():
    print('running main...')
    df = pd.read_csv('df_reduced.csv')
    hex_df = pd.read_csv('df.csv')

    # question 2 -
    # colors_genres(df, hex_df)
    test(df, hex_df)

    # question 4 - What topics did Van Gogh paint about the most?
    # most_frequent_topics()

    # testing q4:
    """
    test_dict = {"clouds": 22, "stars": 10, "women": 84, "men": 187,
                 "shoes": 2}
    test = select_top_10(test_dict, ['Topic', 'Count'])
    print('test df: ', test)
    graph_top_10(test, 'Topic', 'Test')
    test2 = select_top_10(test_dict, ['Colors', 'Count']) # diff colnames works
    print(test2)
    """

    print('finished main!')


if __name__ == '__main__':
    main()
