import random

from myapp.search.objects import ResultItem, Document
from myapp.search import algorithms
from myapp.core import utils
from myapp.search.load_corpus import *


def build_demo_results(corpus: dict, search_id):
    """
    Helper method, just to demo the app
    :return: a list of demo docs sorted by ranking
    """
    res = []
    size = len(corpus)
    ll = list(corpus.values())
    for index in range(random.randint(0, 40)):
        item: Document = ll[random.randint(0, size)]
        res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                              "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), random.random()))

    # for index, item in enumerate(corpus['Id']):
    #     # DF columns: 'Id' 'Tweet' 'Username' 'Date' 'Hashtags' 'Likes' 'Retweets' 'Url' 'Language'
    #     res.append(DocumentInfo(item.Id, item.Tweet, item.Tweet, item.Date,
    #                             "doc_details?id={}&search_id={}&param2=2".format(item.Id, search_id), random.random()))

    # simulate sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res


class SearchEngine:
    """educational search engine"""

    i = 12345
    tweet2vec = []

    def set_corpus(self, corpus_terms):
        terms = []
        for pair_term in corpus_terms:
            terms.append(pair_term['terms'])
        self.tweet2vec = algorithms.tweet_2_vec(terms)

    def search(self, search_query, corpus_terms):
        print("Search query:", search_query)
        self.set_corpus(corpus_terms)
        query_terms = utils.extract_terms(search_query)
        results_index = algorithms.search_in_corpus(query_terms, self.tweet2vec)  # We only have 1 query, acess to the position!
        return results_index

