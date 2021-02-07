
import json


anger_index_dir = 'Resources/My-Dataset/Inverted-Indexes/anger_index.json'
trust_terms_index_dir = 'Resources/My-Dataset/Inverted-Indexes/trust_terms_index.json'
trust_emotional_pairs_index_dir = 'Resources/My-Dataset/Inverted-Indexes/trust_emotional_pairs_index.json'
sentences_documents_index_dir = 'Resources/My-Dataset/Inverted-Indexes/sentences_documents_index.json'


def load_json_file( file_path ):
    with open( file_path ) as json_file:
        return json.load(json_file)

anger_index = load_json_file( anger_index_dir )
trust_terms_index = load_json_file( trust_terms_index_dir )
trust_emotional_pairs_index = load_json_file( trust_emotional_pairs_index_dir )
sentences_documents_index = load_json_file( sentences_documents_index_dir )

anger_keys = anger_index.keys()
trust_words_keys = trust_terms_index.keys()




def clean_sentence( sentence: str ) -> list:
  result = ""
  for ch in sentence:
    if ch.isalpha() or ch.isdigit() or ch == ' ' or ch == '_':
      result += ch
  return result


def search_trust_emotional_pairs( query :str ) -> list:
    result = [ ]
    for key, sentence in trust_emotional_pairs_index.items():
        pairs = key.split('-')
        cond1 = query == ' '.join( pairs ) or query == ' '.join( pairs[::-1] )
        cond2 = pairs[0] in query and pairs[1] in query 
        if  cond1 or cond2:
            result = result +  sentence
    return result


def search_emotional_words( query :str ) -> list:
    intersect_keys = list( set( anger_keys ) & set( query.split(' ') )) 
    result = [ ]
    for key in intersect_keys:
        founded_sentences = list( set( result ) & set( anger_index[key] ) )
        if len( founded_sentences ) <= 0:
            result = result + anger_index[key]
    return result


def search_trust_words( query :str ) -> list:
    intersect_keys = list( set( trust_words_keys ) & set( query.split(' ') )) 
    result = [ ]
    for key in intersect_keys:
        founded_sentences = list( set( result ) & set( trust_terms_index[key] ) )
        if len( founded_sentences ) <= 0:
            result = result + trust_terms_index[key]
    return result 


def search_query( query :str ) -> list:
    query = clean_sentence( query.casefold() )

    result1 = search_trust_emotional_pairs( query )
    result2 = search_emotional_words( query )
    result3 = search_trust_words( query )

    result = list( set( result1 + result2 + result3 ) )
    return result
