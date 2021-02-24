<h3>Simple bot working on ctftime.org api

Lets you get the schedule of competitions
</h3>

<h2>INSTALL AND START</h2>

You should create folder **configs** and file **credentials.py** inside it.

`token = "your token of bot here"`

<h3>Commands</h3>

```
source env/bin/activate
pip3 install -r requirments.txt
python3 bot.py
```

In **BotFather** you should use `/setcommands` for your bot and add description to `/getlist` command.

When you add your bot to a chat, you can restrict it in **Embedding links** (in admin settings) so that it would not preview links
