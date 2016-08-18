import os
import random
import time

from slackclient import SlackClient

from nflh.nfl_highlight_bot import get_highlight_list
from nflh.videos import Video

"""
Base logic taken from https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
"""

BOT_ID = os.environ.get("BOT_ID")

AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "highlight"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    if command.startswith(EXAMPLE_COMMAND):
        highlights = get_highlight_list()
        if len(highlights) > 0:
            response = format_clip(random.choice(highlights))
        else:
            response = "Sorry, no highlights have been posted today."
    else:
        response = "Suspended!"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


def format_clip(clip: Video):
    return "<{0}|{1}>".format(clip.url, clip.desc)


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")