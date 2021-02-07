from flask import Flask, render_template, request
from search_engine_api import search_query



app = Flask( __name__ )


@app.route("/")
def emotional_search_engine( ):
    return render_template( 'EmotionalSearchEngine.html' )


@app.route('/search', methods = ["POST"])
def search():
    search_text = request.form['search_field']
    search_results = search_query( search_text )
    return render_template( 'SearchResults.html', search_results = search_results, results_size = len(search_results))


if __name__ == "__main__":
    app.run( port = 5002 )