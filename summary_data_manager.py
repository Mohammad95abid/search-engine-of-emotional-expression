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


def make_all_existing_emotion_words():
    x = [ key for key, val in summary['Emotional-Words'].items() if val > 0]
    y = [ summary['Emotional-Words'][key] for key in x ]
    existing_emotion_words_data = { 'Existing-Emotional-Words': x, 'Appearance Amount': y}
    existing_emotion_words_data = pd.DataFrame( existing_emotion_words_data )
    return existing_emotion_words_data


def make_all_existing_trust_words():
    x = [ key for key, val in summary['Trust-Words'].items() if val > 0]
    y = [ summary['Trust-Words'][key] for key in x ]
    existing_emotion_words_data = { 'Existing-Trust-Words': x, 'Appearance Amount': y}
    existing_emotion_words_data = pd.DataFrame( existing_emotion_words_data )
    return existing_emotion_words_data


def make_summary_table_fig():
    columns_titles = ['<b>Subject</b>', '<b>Exisiting In The Dataset</b>', '<b>Total</b>', '<b>Percentage</b>']

    emw_len = len(summary['Emotional-Words'])
    trw_len = len(summary['Trust-Words'])
    tep_len = len(summary['Trust-Emotional-Pairs'])

    emw = [ key for key, val in summary['Emotional-Words'].items() if val > 0 ]
    trw = [ key for key, val in summary['Trust-Words'].items() if val > 0 ]

    
    subjects = [ 'Files Numbers', 'Sentences Numbers', 'Emotion Words', 'Trust Words', 'Trust-Emotional Pairs' ]
    eitds = [ 773, 24174, len(emw), len(trw), tep_len ]
    total = [ 773, 24174, emw_len, trw_len, (emw_len * trw_len) ]

    emwp = ( len(emw) / emw_len ) * 100
    trwp = ( len(trw) / trw_len ) * 100
    tepp = ( tep_len / (emw_len * trw_len)) * 100

    percentage = [ '100%', '100%', "{:.2f}%".format(emwp), "{:.2f}%".format(trwp), "{:.2f}%".format(tepp)]

    summary_data = {
        columns_titles[0]: subjects,
        columns_titles[1]: eitds,
        columns_titles[2]: total,
        columns_titles[3]: percentage
    }

    summary_data = pd.DataFrame( summary_data )
    return summary_data


def load_dashboard_data( ):
    dashboard_data = { }
    dashboard_data['trust_words_data'] = make_trust_words_fig_data()
    dashboard_data['trust_emotional_pairs_data'] = make_trust_emotional_pairs_fig_data()
    dashboard_data['emotional_words_data'] = make_emotional_words_fig_data()
    dashboard_data['existing_emotional_words_data'] = make_all_existing_emotion_words()
    dashboard_data['existing_trust_words_data'] = make_all_existing_trust_words()
    dashboard_data['summary_data'] = make_summary_table_fig()
    return dashboard_data


if __name__ == "__main__":
    make_emotional_words_fig_data()