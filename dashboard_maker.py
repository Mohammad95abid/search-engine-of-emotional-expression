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
                    title = 'Appearance of trust words in the given dataset'
                )
    return trust_words_fig


# a function to make trust emotion pairs chart figure
def make_emotional_pairs_fig():
    trust_emotional_pairs_fig = px.scatter( 
                                            dashboard_data['trust_emotional_pairs_data'],
                                            x = 'Trust-Emotional Pairs', y = 'Appearance Amount',
                                            color = 'Trust-Emotional Pairs', title = 'Appearance of the trust-emotional pairs',
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
            width = 1000,
            height = 700,
            title_text = 'Appearence of Emotion Words By Appearence Range',
            margin = dict( l = 100, r = 100, t = 200, b = 100 )
        )

    return emotional_words_fig


# a function to make emotion words chart figure
def make_pie_charts():
    df = px.data.gapminder().query("continent == 'Asia' and year == 2007")
    fig = px.pie(df, values='pop', names='country')
    fig.update_traces(textposition='inside', textfont_size=14)
    return fig



app.layout = html.Div( 
    children = [ 
            html.H1( children = 'IR Analytics', ), 
            html.P( children = ' My analytics ', ), 
            dcc.Graph( figure = make_trust_words_fig() ),
            dcc.Graph( figure = make_emotional_pairs_fig() ),
            dcc.Graph( figure = make_emotional_words_fig() ),
            dcc.Graph( figure = make_pie_charts() )
        ]
 )



if __name__ == '__main__':
    app.run_server( debug = True )