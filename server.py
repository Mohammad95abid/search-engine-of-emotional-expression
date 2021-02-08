from flask import Flask, render_template, request, send_from_directory, redirect, send_file
from search_engine_api import search_query, get_file_path



app = Flask( __name__ )


@app.route("/")
def emotional_search_engine( ):
    return render_template( 'EmotionalSearchEngine.html' )


@app.route('/search', methods = ["POST"])
def search():
    search_text = request.form['search_field']
    search_results = search_query( search_text )
    return render_template( 'SearchResults.html', search_results = search_results, results_size = len(search_results))


@app.route('/show_document/<document_name>')
def show_document( document_name ):
    directory, filename = get_file_path( document_name )
    if filename is None:
        return redirect('/', code = 302)
    return send_file( directory + filename )




if __name__ == "__main__":
    app.run( port = 5002 )