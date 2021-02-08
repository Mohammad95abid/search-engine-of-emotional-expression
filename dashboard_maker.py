import dash
import dash_core_components as dcc 
import dash_html_components as html
import plotly.express as px
from summary_data_manager import load_dashboard_data 
from plotly import graph_objects as go



# load all dashboard data
dashboard_data = load_dashboard_data( )
# implement the dashboard server
app = dash.Dash( __name__ )


# a function to make trust words chart figure
def make_trust_words_fig():
    trust_words_fig = px.bar( dashboard_data['trust_words_data'], x = 'Trust Words', y = 'Appearance Amount', 
                    hover_data = ['Trust Words', 'Appearance Amount'], color = 'Trust Words', 
                    labels = { 'pop': 'Appearance of Trust Words' }, height = 400,
                    title = '<b> 1) Appearance of trust words in the given dataset </b>'
                )
    return trust_words_fig


# a function to make trust emotion pairs chart figure
def make_emotional_pairs_fig():
    trust_emotional_pairs_fig = px.scatter( 
                                            dashboard_data['trust_emotional_pairs_data'],
                                            x = 'Trust-Emotional Pairs', y = 'Appearance Amount',
                                            color = 'Trust-Emotional Pairs', 
                                            title = '<b> 2) Appearance of the trust-emotional pairs </b>',
                                            size='Appearance Amount', hover_data=['Appearance Amount'] 
                                      )
    return trust_emotional_pairs_fig


# a function to make emotion words chart figure
def make_emotional_words_fig():
    emotional_words_fig = go.Figure()

    emotional_words_fig.add_trace(go.Funnel(
            name = 'Company A',
            y = list(dashboard_data['emotional_words_data']['Appearance Ranges']),
            x = list(dashboard_data['emotional_words_data']['Emotion Words Number']),
            textinfo = 'value+percent initial',
            textposition = 'inside',
            opacity = 1.00, 
            marker = {
                        'color': ['#A93226', '#6C3483', '#2471A3', '#229954', '#616A6B', '#17202A'],
                        'line': {
                            'width': [4, 2, 2, 3, 1, 1], 
                            'color': ['wheat', 'wheat', 'blue', 'wheat', 'wheat']
                        }
                    },
        ))

    emotional_words_fig.update_layout(
            title_text = '<b> 3) Appearence of Emotion Words By Appearence Range</b>',
        )

    return emotional_words_fig


# a function to make emotion words chart figure
def make_existing_emotion_words_fig():
    fig = px.pie(   
                    dashboard_data['existing_emotional_words_data'] , 
                    values = 'Appearance Amount', names = 'Existing-Emotional-Words',
                    title = '<b> 4) Percentage of existing emotion words in the given dataset </b>'
                )
    fig.update_traces( 
            textposition = 'inside', 
            textfont_size = 14
        )
    return fig


# a function to make trust words chart figure
def make_existing_trust_words_fig():
    labels = dashboard_data['existing_trust_words_data']['Existing-Trust-Words']
    values = dashboard_data['existing_trust_words_data']['Appearance Amount']
    fig = go.Figure( data = [ go.Pie( labels = labels, values = values, hole = .6 ) ] )
    fig.update_traces( 
        textposition = 'inside', 
        textfont_size = 14
    )
    fig.update_layout( title_text = '<b> 5) Appearence of trust words in the given dataset </b>' )
    return fig


# a function to show summary in table figure
def make_summary_table_fig():
    titles = [ key for key in dashboard_data['summary_data'] ]
    first_column = dashboard_data['summary_data'][ titles[0] ]
    last_column = dashboard_data['summary_data'][ titles[1] ]
    third_column = dashboard_data['summary_data'][ titles[2] ]
    fourth_column = dashboard_data['summary_data'][ titles[3] ]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'
    width = 1000

    fig = go.Figure(
                        data = [ 
                                go.Table(   columnwidth = [0.15 * width, 0.35 * width, 0.18 * width, 0.15 * width, 0.15 * width],
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
    fig.update_layout( title_text = '<b> 6) Summary </b>' )
    return fig




app.layout = html.Div( 
    children = [ 
            html.H1( children = 'Assignment in Information Retrieval Course', style = { 'text-align': 'center' } ), 
            dcc.Graph( figure = make_trust_words_fig() ),
            dcc.Graph( figure = make_emotional_pairs_fig() ),
            dcc.Graph( figure = make_emotional_words_fig() ),
            dcc.Graph( figure = make_existing_emotion_words_fig() ),
            dcc.Graph( figure = make_existing_trust_words_fig() ),
            dcc.Graph( figure = make_summary_table_fig() )
        ]
 )



if __name__ == '__main__':
    app.run_server( debug = True )