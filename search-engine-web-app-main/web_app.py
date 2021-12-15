import os
from json import JSONEncoder

# pip install httpagentparser
import httpagentparser  # for getting the user agent as json
import nltk
from flask import Flask, render_template, session
from flask import request

from myapp.analytics.analytics_data import AnalyticsData, ClickedDoc
from myapp.search.load_corpus import load_corpus
from myapp.search.objects import Document, StatsDocument
from myapp.search.search_engine import SearchEngine
from myapp.core import utils


# *** for using method to_json in objects ***
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

# end lines ***for using method to_json in objects ***

# instantiate the Flask application
app = Flask(__name__)

# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'

# instantiate our search engine
search_engine = SearchEngine()
tweets, corpus_terms = utils.load_documents_corpus()
tweet_results = []

# instantiate our in memory persistence
analytics_data = AnalyticsData()

# print("current dir", os.getcwd() + "\n")
# print("__file__", __file__ + "\n")
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
# print(path + ' --> ' + filename + "\n")
# load documents corpus into memory.
file_path = path + "/tweets-data-who.json"

# file_path = "../../tweets-data-who.json"
corpus = load_corpus(file_path)
print("loaded corpus. first elem:", list(corpus.values())[0])


# Home URL "/"
@app.route('/')
def index():
    print("starting home url /...")

    # flask server creates a session by persisting a cookie in the user's browser.
    # the 'session' object keeps data between multiple requests
    session['some_var'] = "IRWA 2021 home"

    user_agent = request.headers.get('User-Agent')
    print("Raw user browser:", user_agent)

    user_ip = request.remote_addr
    agent = httpagentparser.detect(user_agent)

    print("Remote IP: {} - JSON user browser {}".format(user_ip, agent))

    print(session)

    return render_template('index.html', page_title="Welcome")

@app.route('/')
def search_form():

    analytics_data.add_main_page_visit(tracking_user())


    return render_template('index.html', page_title="Welcome")

@app.route('/search', methods=['POST'])
def search_form_post():
    global tweet_results
    search_query = request.form['search-query']
    results_idx = search_engine.search(search_query, corpus_terms)
    tweet_results = utils.parse_results(tweets, results_idx)
    found_count = len(results_idx)

    return render_template('results.html', results_list=tweet_results, page_title="Results", found_counter=found_count)


def tracking_user():
    ip_address = request.remote_addr
    requested_url = request.url
    referer_page = request.referrer
    page_name = request.path
    query_string = request.query_string
    user_agent = request.user_agent.string
    return UserTracked(ip_address,requested_url,referer_page,page_name,query_string,user_agent)

class UserTracked:
    def __init__(self, ip_address,requested_url,referer_page,page_name,query_string,user_agent):
        self.ip_address = ip_address
        self.requested_url = requested_url
        self.referer_page = referer_page
        self.page_name = page_name
        self.query_string = query_string
        self.user_agent = user_agent
    def __str__(self) -> str:
        return str(self.ip_address) + " " + str(self.requested_url) + \
            " " + str(self.referer_page) + " " + str(self.page_name) + " " + \
            str(self.query_string) + " " + str(self.user_agent)


@app.route('/doc_details', methods=['GET'])
def doc_details():
    clicked_position = int(request.args["position"])
    analytics_data.page_visited(
        tracking_user(), tweet_results[clicked_position].id)
    return render_template('doc_details.html', tweet=tweet_results[clicked_position], position=clicked_position)



@app.route('/stats', methods=['GET'])
def stats():
    """
    Show simple statistics example. ### Replace with dashboard ###
    :return:
    """
    ### Start replace with your code ###
    try:
        pos = request.args["pos"]
    except:
        pos = False
    if pos:
        return render_template('stats_for_doc.html', analytics_data=analytics_data, tweet=tweet_results[int(pos)])
    return render_template('stats.html', analytics_data=analytics_data,utils=utils)
    # ### End replace with your code ###


@app.route('/dashboard', methods=['GET'])
def dashboard():
    visited_docs = []
    print(analytics_data.fact_clicks.keys())
    for doc_id in analytics_data.fact_clicks.keys():
        d: Document = corpus[int(doc_id)]
        doc = ClickedDoc(doc_id, d.description, analytics_data.fact_clicks[doc_id])
        visited_docs.append(doc)

    # simulate sort by ranking
    visited_docs.sort(key=lambda doc: doc.counter, reverse=True)

    for doc in visited_docs: print(doc)
    return render_template('dashboard.html', visited_docs=visited_docs)


@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


if __name__ == "__main__":
    app.run(port=8088, host="0.0.0.0", threaded=False, debug=True)
