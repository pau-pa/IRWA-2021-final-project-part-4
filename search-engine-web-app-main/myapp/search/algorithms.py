from gensim.models import word2vec
import numpy as np

def search_in_corpus(query_terms, tweet2vec):
    # 1. create create_tfidf_index
    query2vec = tweet_2_vec(query_terms)[0]

    # 2. apply ranking
    ranking = cosine_similarity(tweet2vec, query2vec)
    return ranking

def tweet_2_vec(tweet_terms):
    tweet2vec = []
    for tweet in tweet_terms:
        vec = np.zeros(100)
        try:
            #Word2vec for each word in the current tweet
            model = word2vec.Word2Vec(
                tweet, vector_size=100, window=10, min_count=1, negative=15, sg=0)
            for word in model.wv.index_to_key:
                vec += model.wv[word]
            tweet2vec.append(vec / len(model.wv.index_to_key))
        except:
            tweet2vec.append(np.ones(100))
    return tweet2vec

def cosine_similarity(tweet2vec,query2vec):
    cos_sim = np.ones(len(tweet2vec))
    for i, tweet_vec in enumerate(tweet2vec):
        cos_sim[i] = np.dot(tweet_vec, query2vec) / (np.linalg.norm(tweet_vec)*np.linalg.norm(query2vec))
    ordered_positions = np.flip(np.argsort(cos_sim))
    return ordered_positions
