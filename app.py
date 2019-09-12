from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode


app = Flask(__name__)
ask = Ask(app, '/beddit/')

def get_headlines():
    user_pass_dict = {
        'user' : 'bid-dev',
        'passwd' : 'bir1010bar',
        'api_type': 'json',
    }
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa : Bidhan'})
    sess.post('https://www.reddit.com/api/login', data=user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/worldnews/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [
        unidecode.unidecode(listing['data']['title'])
        for listing in data['data']['children']
    ]
    titles = '... '.join([i for i in titles])
    return titles

titles = get_headlines()
print(titles, '\n')


@app.route('/')
def index():
    return 'Hi there! Welcome to Andromeda..'

@ask.launch
def start_skill():
    welcome_message = 'Hello there! Do you want to hear todays top 10 reddit news?'
    return question(welcome_message)

@ask.intent('YesIntent')
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent('NoIntent')
def no_intent():
    bye_text = 'No problem, you can ask me for  .'
    return statement(bye_text)



if __name__ == '__main__':
    app.run(debug=True)
