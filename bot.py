#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configs.credentials import token

import time
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
from dateutil import tz

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello here!\nI am a ctftime notifier bot!')

def parseTime(time_str):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Moscow')
    time_str = time_str.replace("T", " ").split("+")[0]
    utc = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)
    local = local.strftime("%Y-%m-%d %H:%M:%S")
    return local


def getlist(update, context):
    limit = 100
    start_time = int(time.time())
    # 1209600 - 2 weeks
    end_time = int(time.time() + 1209600)
    url = "https://ctftime.org/api/v1/events/?limit={0}&start={1}&finish={2}".format(limit, start_time, end_time)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    r = requests.get(url, headers=headers).json()
    if len(r) == 0:
        update.message.reply_text("Nothing here for you :(")
        return -1
    for i in range(len(r)):
        full_str = r[i]['title'] + "\n"
        full_str += "Start:   " + parseTime(r[i]['start']) + "\n"
        full_str += "Finish:  " + parseTime(r[i]['finish']) + "\n"
        full_str += "Url:     " + r[i]['url'] + "\n"
        update.message.reply_text(full_str)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getlist", getlist))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
