#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configs.credentials import token

import time
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
from dateutil import tz
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello here\nI am a `CTFTIME NOTIFIER BOT`\nActually I don\'t do much, just send you current\(2 weeks from now\) available CTFs\n/getlist \- *get current list of CTFs*\n', parse_mode='MarkdownV2')


def parseTime(time_str):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Moscow')
    time_str = time_str.replace("T", " ").split("+")[0]
    utc = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)
    local = local.strftime("%H:%M %d-%m-%Y")
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
        full_str += "Format:  " + r[i]['format'] + "\n"
        update.message.reply_text(full_str)


def next(update, context):
    limit = 1
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
        full_str += "Format:  " + r[i]['format'] + "\n"
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
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getlist", getlist))
    dp.add_handler(CommandHandler("next", next))
    dp.add_handler(CommandHandler("help", help))

    # answer reply to user
    #dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
