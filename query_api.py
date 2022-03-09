"""
Hannah Burrows and Sabrina Fang
CSE 163 Section AB and AC

This module contains all the code involving dealing with the Met Museum API
(documentation found at https://metmuseum.github.io/). Involves querying the
API for data on Van Gogh's paintings.
"""

import requests

MET_MUSEUM_API = 'https://collectionapi.metmuseum.org/public/collection/v1'


def query_api_topics():
    """
    Queries the Met Museum API for the topics in each of Van Gogh's
    paintings that they have, and returns a dictionary where the keys are
    topics and the values are counts for the number of occurences for that
    topic. Due to the API limiting requests per second, this function may take
    a while to run.
    """
    print('started querying api - this may take a while')
    terms = {}

    paintings_ids = requests.get(MET_MUSEUM_API + '/search?q=Van_Gogh')
    for id in paintings_ids.json()['objectIDs']:
        response = requests.get(MET_MUSEUM_API + '/objects/' + str(id))
        painting_info = response.json()
        tags = painting_info.get('tags')
        if tags:
            for tag in tags:
                term = tag['term']
                if term in terms:
                    terms[term] += 1
                else:
                    terms[term] = 1
    return terms
