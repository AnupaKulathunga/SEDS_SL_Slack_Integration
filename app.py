import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app =Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET_'], '/slack/events', app)

client =  slack.WebClient(token=os.environ['SLACK_TOKEN_'])
BOT_ID = client.api_call("auth.test")['user_id']

#client.chat_postMessage(channel='#test', text="Hello World!")
client.chat_postMessage(
  channel="seds_sl_slack_intergration",
  blocks=[
    {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hey there 👋 I'm TaskBot. I'm here to help you create and manage tasks in Slack.\nThere are two ways to quickly create tasks:"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*1️⃣ Use the `/task` command*. Type `/task` followed by a short description of your tasks and I'll ask for a due date (if applicable). Try it out by using the `/task` command in this channel."
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*2️⃣ Use the _Create a Task_ action.* If you want to create a task from a message, select `Create a Task` in a message's context menu. Try it out by selecting the _Create a Task_ action for this message (shown below)."
			}
		},
		{
			"type": "image",
			"title": {
				"type": "plain_text",
				"text": "image1",
				"emoji": True
			},
			"image_url": "https://api.slack.com/img/blocks/bkb_template_images/onboardingComplex.jpg",
			"alt_text": "image1"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "➕ To start tracking your team's tasks, *add me to a channel* and I'll introduce myself. I'm usually added to a team or project channel. Type `/invite @TaskBot` from the channel or pick a channel on the right."
			},
			"accessory": {
				"type": "conversations_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a channel...",
					"emoji": True
				}
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "👀 View all tasks with `/task list`\n❓Get help at any time with `/task help` or type *help* in a DM with me"
				}
			]
		}
  ]
)

@ slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if user_id != None and BOT_ID != user_id:
        client.chat_postMessage(channel='#test', text=text)

#@ app.

if __name__ == "__main__":
    app.run(debug=True)