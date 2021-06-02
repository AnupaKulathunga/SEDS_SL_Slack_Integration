import slack
import json
from flask import Flask
from slackeventsapi import SlackEventAdapter as SEA

tokens = {}
with open('configs.json') as json_data:
    tokens = json.load(json_data)

app = Flask(__name__)
client = slack.WebClient(tokens.get("slack_bot_token"))
slack_event_adapter = SEA(tokens.get("slack_signing_secret"),'/slack/events',app)

client.chat_postMessage(channel='#test01', text="Hello World!")

if __name__ == "__main__":
    app.run(debug=True)