from flask import Flask, request, render_template
import requests
import datetime


app = Flask(__name__)
api_key = "test"
#https://content.guardianapis.com/commentisfree?api-key=test&from-date=2018-04-07&to-date=2018-04-07

@app.route('/')
def home():
    date = request.args.get("date") or datetime.datetime.now().strftime("%Y-%m-%d")
    request_url = "https://content.guardianapis.com/commentisfree?api-key={}&from-date={}&to-date={}".format(api_key, date, date)
    results = requests.get(request_url).json()['response']['results']
    links = [{"title": result["webTitle"], "url": result["webUrl"]} for result in results]
    return render_template('home.html', links=links)

app.run(debug=True)