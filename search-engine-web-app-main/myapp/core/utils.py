import datetime
import json
from random import random
import jsonpickle
import re
import colorsys
import datetime
import nltk

from faker import Faker
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from myapp.search.objects import Document, StatsDocument

fake = Faker()


# fake.date_between(start_date='today', end_date='+30d')
# fake.date_time_between(start_date='-30d', end_date='now')
#
# # Or if you need a more specific date boundaries, provide the start
# # and end dates explicitly.
# start_date = datetime.date(year=2015, month=1, day=1)
# fake.date_between(start_date=start_date, end_date='+30y')

def get_random_date():
    """Generate a random datetime between `start` and `end`"""
    return fake.date_time_between(start_date='-30d', end_date='now')


def get_random_date_in(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())), )


def load_json_file(path):
    """Load JSON content from file in 'path'

    Parameters:
    path (string): the file path

    Returns:
    JSON: a JSON object
    """

    # Load the file into a unique string
    with open(path) as fp:
        text_data = fp.readlines()[0]
    # Parse the string into a JSON object
    json_data = json.loads(text_data)
    return json_data

def remove_emojis(l):
    """If the string "l" is an emoji it deletes it.

    Arguments:
    l-- string word to be processed

    Returns:
    word-- string equal to "l" if it's not an emoji and "" otherwise.
    """
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    word = emoji_pattern.sub(r'', l)
    return word

def extract_terms(line):
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    ## START CODE
    line = line.lower()  ## Transform in lowercase
    line = line.split()  ## Tokenize the text to get a list of terms
    line = [l for l in line if l not in stop_words]  ##eliminate the stopwords (HINT: use List Comprehension)
    line = [l for l in line if l not in ["&amp", "&", "rt", "amp"]]
    line = [stemmer.stem(l) for l in line]  ## perform stemming (HINT: use List Comprehension)
    line = [l for l in line if "https://" not in l]  ##deletes the items that are url links

    line = [remove_emojis(l) for l in line]  ##deletes the items that are emojis
    line = [l for l in line if "" != l]

    return line


def load_documents_corpus():
    """
    Load documents corpus from dataset_tweets_WHO.txt file
    :return:
    """

    ##### demo replace ith your code here #####
    corpus_terms = []
    docs_path = 'tweets-data-who.txt'

    with open(docs_path) as f:
        for line in f:
            docs = jsonpickle.decode(line)
            full_txts = get_full_text(docs)
            for id_str in full_txts:
                corpus_terms.append({
                    'tweet_id' : id_str,
                    'terms' : extract_terms(full_txts[id_str])
                })

    tweets = documents_format(docs)
    return tweets,corpus_terms


def get_full_text(docs):

    # Put tweets (only full_text) in a list in order to apply Data Processing
    full_txts = {}
    for i in range(len(docs)):
        text = docs[str(i)]['full_text']
        full_txts[docs[str(i)]['id_str']] = text
    return full_txts


def documents_format(docs):
    tweets = []
    for doc in docs.values():
        url = 'https://twitter.com/' + doc['user']['screen_name'] + '/status/' + doc['id_str'] + ' '
        hashtags = [hashtag['text'] for hashtag in doc['entities']['hashtags']]
        full_text = doc['full_text']
        tweet_split = full_text.split()
        lenght = min(7, len(tweet_split))
        title = ""
        for i in range(lenght):
            title += tweet_split[i] + " "
        tweet = Document(
            doc['id_str'],
            title,
            full_text,
            doc['created_at'],
            doc['favorite_count'],
            doc['retweet_count'],
            url,
            hashtags,
        )
        tweets.append(tweet)
    return tweets


def parse_results(tweets,idxs):
    document_results = []
    for index in idxs:
        document_results.append(tweets[index])
    return document_results
