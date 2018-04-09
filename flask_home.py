from flask import Flask, request, render_template, Markup
from nltk.sentiment.util import *
from nltk.corpus import opinion_lexicon
import requests
import datetime


app = Flask(__name__)
api_key = "test"
#https://content.guardianapis.com/commentisfree?api-key=test&from-date=2018-04-07&to-date=2018-04-07
print('starting download')
nltk.download('opinion_lexicon')
print('downloaded data')

word_score = {}
print('caching positive words')
for word in opinion_lexicon.positive():
    word_score[word] = word_score.get(word, 0) + 1
print('caching negative words')
for word in opinion_lexicon.negative():
    word_score[word] = word_score.get(word, 0) - 1
print('done caching')

@app.route('/')
def home():
    date = request.args.get("date") or datetime.datetime.now().strftime("%Y-%m-%d")
    request_url = "https://content.guardianapis.com/commentisfree?api-key={}&from-date={}&to-date={}&show-fields=trailText,body".format(api_key, date, date)
    results = requests.get(request_url).json()['response']['results']

    links = [{"title": result["webTitle"], "url": result["webUrl"], "summary": result['fields']["trailText"], "sentiment": sentiment(result['fields']['body'])} for result in results]
    return render_template('home.html', links=links)

def sentiment(body):
    from nltk.tokenize import treebank
    stripped = Markup(body).striptags()
    tokenizer = treebank.TreebankWordTokenizer()
    return sum([word_score.get(word.lower(), 0) for word in tokenizer.tokenize(stripped)])

app.run(debug=True)