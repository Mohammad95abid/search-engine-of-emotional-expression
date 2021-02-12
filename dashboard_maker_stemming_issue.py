import dash
import dash_core_components as dcc 
import dash_html_components as html
import plotly.express as px
from summary_data_manager import load_dashboard_data, load_dashboard_wp_data
from plotly import graph_objects as go
from plotly.subplots import make_subplots



# load all dashboard data
dashboard_data = load_dashboard_data( )
dashboard_data_wp = load_dashboard_wp_data( )


# implement the dashboard server
app = dash.Dash( __name__ )


# a function to make trust words chart figure
def make_trust_words_fig():
    tw_x = dashboard_data['trust_words_data']['Trust Words']
    tw_y = dashboard_data['trust_words_data']['Number of appearances']
    tw_with_stemming_y = dashboard_data_wp['trust_words_data']['Number of appearances']
    trust_words_fig = go.Figure( data = [
        go.Bar(
            name = 'Without Stemming', x = tw_x , y = tw_y, text = tw_y, 
            textposition = 'auto', marker_color = 'indianred'
        ),
        go.Bar(
            name = 'With Stemming', x = tw_x, y = tw_with_stemming_y, 
            text = tw_with_stemming_y, textposition = 'auto', marker_color = 'lightsalmon'
        )
    ] )
    trust_words_fig.update_layout( 
        barmode = 'group', 
        title_text = '<b> 1) Comparing between trust words with and without stemming</b>',
        legend = dict( 
            x = 0,
            y = 1.0,
            bgcolor = 'rgba(255, 255, 255, 0)',
            bordercolor = 'rgba(255, 255, 255, 0)'
        ),
        # gap between bars of adjacent location coordinates.
        bargap = 0.15,
        # gap between bars of the same location coordinate. 
        bargroupgap = 0.1 ,
        xaxis = dict(
            title = 'Trust Words',
            titlefont_size = 16,
        ),
        yaxis = dict(
            title = 'Number of appearances',
            titlefont_size = 16,
            tickfont_size = 14
        )
    )
    return trust_words_fig


# a function to make trust words chart figure
def make_emotional_pairs_fig():
    labels = dashboard_data_wp['trust_emotional_pairs_data']['Trust-Emotional Pairs']
    values = dashboard_data_wp['trust_emotional_pairs_data']['Number of appearances']
    fig = go.Figure( data = [ go.Pie( labels = labels, values = values, hole = .6 ) ] )
    fig.update_traces( 
        textposition = 'inside', 
        textfont_size = 14
    )
    fig.update_layout( title_text = '<b> 2) Trust-Emotion pairs with stemming</b>' )
    return fig



# a function to make emotion words chart figure
def make_emotional_words_fig():
    emotional_words_fig = go.Figure()

    emotional_words_fig.add_trace(
        go.Funnel(
            name = 'Without Stemming',
            y = list(dashboard_data['emotional_words_data']['Appearance Ranges']),
            x = list(dashboard_data['emotional_words_data']['Emotion Words Number']),
            textinfo = 'value+percent initial',
            textposition = 'inside'
        )
    )

    emotional_words_fig.add_trace(
        go.Funnel(
            name = 'With Stemming',
            y = list(dashboard_data_wp['emotional_words_data']['Appearance Ranges']),
            x = list(dashboard_data_wp['emotional_words_data']['Emotion Words Number']),
            textinfo = 'value+percent initial',
            textposition = 'inside'
        )
    )

    emotional_words_fig.update_layout(
            title_text = '<b> 3) Comparing between emotion words with and without stemming</b>',
        )

    return emotional_words_fig


# a function to make emotion words chart figure
def make_existing_emotion_words_fig(): 
    fig = make_subplots(1, 2, specs = [[ {'type': 'domain'}, {'type': 'domain'} ]],
                            subplot_titles = ['Without Stemming', 'With Stemming']
                        )
    
    labels = dashboard_data['existing_emotional_words_data']['Existing-Emotional-Words']
    y_wp = dashboard_data['existing_emotional_words_data']['Number of appearances']
    y_wop = dashboard_data_wp['existing_emotional_words_data']['Number of appearances']
    fig.add_trace( go.Pie( labels = labels, values = y_wp, scalegroup = 'one', name = 'Without Stemming'), 1, 1 )
    fig.add_trace( go.Pie( labels = labels, values = y_wop, scalegroup = 'one', name = 'With Stemming'), 1, 2 )

    fig.update_layout( title_text = '<b> 4) Comparing emotion words with and without stemming</b>')

    fig.update_traces( 
            textposition = 'inside', 
            textfont_size = 14
        )

    return fig


# a function to show summary in table figure
def make_summary_table_fig():
    titles = [ key for key in dashboard_data_wp['summary_data'] ]
    first_column = dashboard_data_wp['summary_data'][ titles[0] ]
    last_column = dashboard_data_wp['summary_data'][ titles[1] ]
    third_column = dashboard_data_wp['summary_data'][ titles[2] ]
    fourth_column = dashboard_data_wp['summary_data'][ titles[3] ]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'
    width = 1000

    fig = go.Figure(
                        data = [ 
                                go.Table(   columnwidth = [0.25 * width, 0.25 * width, 0.18 * width, 0.15 * width],
                                            header = dict( 
                                                values = titles,
                                                line_color = 'darkslategray',
                                                fill_color = 'grey',
                                                align = ['left','center'],
                                                font = dict( color = 'white', size = 16 )
                                            ),
                                            cells = dict( 
                                                values = [ first_column, last_column, third_column, fourth_column ],
                                                line_color='darkslategray',
                                                fill_color = [ 
                                                                [ rowOddColor, rowEvenColor, rowOddColor, rowEvenColor, rowOddColor ] * 5 
                                                             ],
                                                align = ['left', 'center'],
                                                height = 40,
                                                font = dict( color = 'darkslategray', size = 14 )
                                            ) 
                                        )
                            ] 
                    )
    fig.update_layout( title_text = '<b> 6) Summary </b>', height = 600 )
    return fig




app.layout = html.Div( 
    children = [ 
            html.H1( children = 'The problematic nature of stemming', style = { 'text-align': 'center' } ), 
            dcc.Graph( figure = make_trust_words_fig() ),
            dcc.Graph( figure = make_emotional_pairs_fig() ),
            dcc.Graph( figure = make_emotional_words_fig() ),
            dcc.Graph( figure = make_existing_emotion_words_fig() ),
            dcc.Graph( figure = make_summary_table_fig() )
        ]
 )



if __name__ == '__main__':
    app.run_server( debug = True, port = 8051 )