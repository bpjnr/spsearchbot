from flask import Flask, render_template, request, json
import pymongo
from pymongo import MongoClient
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import tweepy
import re
 
app = Flask(__name__)


consumer_key = 'V0sRTpI1aHfzhFGt6daNwy6Jm'
consumer_secret = 'HjwNoplTLI04B7S9iZTrhyKaPID2cUJcvkQaktAYWWl6isaKoO'
access_token = '1037575169211084800-dQXHLpcDXZS1dO2Xkmd3uFizk4ABll'
access_token_secret = 'EqxfViZWqiCT81cqqqkdqCXBFbApnavsARADKoepmhT3H'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


collection = '-1'
ptweet = 0
netweet = 0
ntweet = 0

#try:
MONGODB_URI = "mongodb://arcane:arcane159@ds153814.mlab.com:53814/saypeacebot"
client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("saypeacebot") # Use saypeacebot database.   
collection = db.ng2019election
    #results = collection.find()
    #data = str(results.count())
    
    #return results
#except Exception as e:
#   print(e)


def streamTweet(tag):
    data = []
    for tweet in tweepy.Cursor(api.search, q="#"+tag, count=100, lang="en").items():
        data.append(tweet)

    return data
    

def getTweet(searchterm):
    global collection
    global ptweet
    global netweet
    global ntweet

    #results = collection.find()
    results = streamTweet(searchterm)
    data = ''
    #data = str(results.count())
    for emp in results:
        #dt = json.loads(emp)
        #txt = emp['text']
        txt = emp.text

        sentiment = get_tweet_sentiment(txt);

        #print(txt + " -- " + sentiment + " --- " + id_str + " --- " + name)
        if sentiment == 'positive':
            ptweet += 1
        elif sentiment == 'neutral':
            netweet += 1
        else:
            ntweet += 1
    myl = [ptweet, netweet, ntweet]
    total = sum(myl)
    pcent = round((ptweet / total) * 100, 2)
    necent = round((netweet / total) * 100, 2)
    ncent = round((ntweet / total) * 100, 2)
    mylist = [pcent, necent, ncent, total]
    return mylist
    #return str(results[0]['text'])
    

    return
    #return results

def clean_tweet(tweet):

    #clean tweet text by removing links, special characters using simple regex statements.
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):

    #classify sentiment of passed tweet using textblob's sentiment method
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

@app.route('/')
def homepage():

    title = "Epic Tutorials"
    paragraph = ["wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!","wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!"]
    #mylist = getTweet()

    try:
        return render_template("index.html", title = title, paragraph=paragraph)
    except Exception:
        return str(e)



@app.route('/about')
def aboutpage():

    title = "About this site"
    paragraph = ["blah blah blah memememememmeme blah blah memememe"]

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)


@app.route('/contact')
def contactPage():

    title = "About this site"
    paragraph = ["blah blah blah memememememmeme blah blah memememe"]

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)


@app.route('/searchHashTag', methods=['POST'])
def searchHashTag(chartID = 'chart_ID', chart_type = 'pie', chart_height = 600):
    term =  request.form['searchterm'];
    mylist = getTweet(term)
    #return json.dumps({'status':'OK','title_text':term});
    pageType = 'graph'
    title = term
    total_tweets = mylist[3]

    series = [{
                "name": 'Brands',
                "colorByPoint": "true",
                "data": [
                    {
                        "name": 'Positive '+str(mylist[0])+'%',
                        "y": mylist[0],
                        "sliced": "true",
                    }, 
                    {
                        "name": 'Negative '+str(mylist[2])+'%',
                        "y": mylist[2],
                    }, 
                    {
                        "name": 'Neutral '+str(mylist[1])+'%',
                        "y": mylist[1],
                    }
                ]
            }]
        

    return json.dumps(series)
    #return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, credits=credits)
 



@app.route('/graph')
def graph(chartID = 'chart_ID', chart_type = 'pie', chart_height = 600):
    #chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    chart = {
                "renderTo": chartID,
                "plotBackgroundColor": "#fff",
                "plotBorderWidth": "null",
                "plotShadow": "false",
                "type": chart_type
            }
    series = [{
                "name": 'Brands',
                "colorByPoint": "true",
                "data": [{
                    "name": 'Chrome',
                    "y": 61.41,
                    "sliced": "true",
                    "selected": "true"
                }, {
                    "name": 'Internet Explorer',
                    "y": 11.84
                }, {
                    "name": 'Firefox',
                    "y": 10.85
                }, {
                    "name": 'Edge',
                    "y": 4.67
                }, {
                    "name": 'Safari',
                    "y": 4.18
                }, {
                    "name": 'Other',
                    "y": 7.05
                }]
            }]
    title = {"text": 'My Title'}
    credits = {"text":"Junior Peter"}
    tooltip: { "pointFormat": '{series.name}: <b>{point.percentage:.1f}%</b>'}
    plotOptions: {
                    "pie": {
                        "allowPointSelect": "true",
                        "cursor": 'pointer',
                        "dataLabels": {
                            "enabled": "true"
                        },
                        "showInLegend": "true"
                    }
                }
    title: {
                "text": "title_text"
            }
    return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, credits=credits)
 


 
if __name__ == "__main__":
    app.run(debug = True, host='127.0.0.1', port=5000, passthrough_errors=True)
