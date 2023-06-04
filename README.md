# robot_dreams_bot
This repository contains my Telegram bot that is my final project after robot_dreams python developer course.

Main idea - to create a bot that works on a direct requests to Telegram, without using libraries that makes this process easier. For sure it's much harder but give you an excellent experience. 

With this bot, you can conveniently use a variety of functions. Here are the main functions:

Current weather for selected cities:

Specify the city for which you want to get the current weather and send a request.
The bot will collect the necessary data from reliable weather sources.
You will receive a detailed weather status including general conditions, temperature, wind speed for the selected city.

Exchange Rates:

Request the latest exchange rates.
The bot will obtain the latest exchange rate information from a reliable source.
Easily obtain accurate, real-time currency conversion rates.

Random GIF images:

Requesting random GIF images can add fun and spontaneity to a conversation.
Bots can retrieve random GIFs from GIPHY to share fun visuals with friends and liven up the chat.

Obtain a Telegram ID:

Get your unique Telegram ID using a dedicated command.
When you execute the command, the bot will identify your Telegram ID and provide it to you.
You can easily access your Telegram ID for a variety of uses, including user identification and integration with other services.

By incorporating these features, the bot provides a wide variety of functions to enrich your Telegram experience. Whether you need to check the weather, convert currency, get a random GIf or retrieve your Telegram ID, this bot can do it all, bringing convenience and efficiency to your interactions with Telegram!



Available commands:<br>
  /start, /commands - All commands list<br>
  /gif - Send you a random GIF from GIPHY service<br>
  /my_id - Send you your ID in Telegram<br>
  /weather <city> - Get the weather for a specific city<br>
  /currency - Returns the cost of EUR and USD in UAH<br>
  /echo <message> - Echo back the provided message<br>
  /add_contact <name> <phone> - Insert a new contact in contacts book<br>
  /get_contacts - Show all contacts from contacts book<br>
  /delete_contact <name> - Delete contact from contacts book<br>

Link on a landing of the bot:
https://vadymdemchenko.github.io/

Direct link to the bot:
https://t.me/Slev1n_bot

Link on a backend part of the bot:
https://github.com/VadymDemchenko/robot_dreams_bot/tree/main/robot_bot
  
  
P.S. use file setWebhook.py first. It will ask you about link for webhook (ngrok link for example) and after webhook will be setten you can start run.py file that will launch bot.
