import pandas as pd 
import json



def load_json_file( file_path ):
    with open( file_path ) as json_file:
        return json.load(json_file)


#  preparing the data
summary_root_dir = 'Resources/Summary.json'
summary = load_json_file( summary_root_dir )



def make_trust_words_fig_data():
    x = [ key for key in summary['Trust-Words'] ]
    y = [ val for key, val in summary['Trust-Words'].items() ]
    trust_words_data = { 'Trust Words': x, 'Appearance Amount': y}
    trust_words_data = pd.DataFrame( trust_words_data )
    return trust_words_data


def make_trust_emotional_pairs_fig_data():
    x = [ key for key in summary['Trust-Emotional-Pairs'] ]
    y = [ val for key, val in summary['Trust-Emotional-Pairs'].items() ]
    emotional_words_data = { 'Trust-Emotional Pairs': x, 'Appearance Amount': y}
    emotional_words_data = pd.DataFrame( emotional_words_data )
    return emotional_words_data


def make_emotional_words_fig_data():
    x = [ key for key in summary['Emotional-Words'] ]
    y = [ val for key, val in summary['Emotional-Words'].items() ]
    emotional_words_data = { 'Emotional-Words': x, 'Appearance Amount': y}
    emotional_words_data = pd.DataFrame( emotional_words_data )
    ranges = [ -1, 0, 10, 50, 100, 200, 300 ]
    df_temp = emotional_words_data.groupby(pd.cut(emotional_words_data['Appearance Amount'], ranges)).count()
    ranges = [ '0 - Missing in the dataset', '(0, 10]', '(10, 50]', '(50, 100]', '(100, 200]', '(200, 300]' ]
    data = { 'Appearance Ranges': ranges, 'Emotion Words Number': list( df_temp.iloc[:, 0] )}
    df_temp = pd.DataFrame( data )
    return df_temp


def load_dashboard_data( ):
    dashboard_data = { }
    dashboard_data['trust_words_data'] = make_trust_words_fig_data()
    dashboard_data['trust_emotional_pairs_data'] = make_trust_emotional_pairs_fig_data()
    dashboard_data['emotional_words_data'] = make_emotional_words_fig_data()
    return dashboard_data


if __name__ == "__main__":
    make_emotional_words_fig_data()