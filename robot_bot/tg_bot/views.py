from . import app
from flask import request
from .handlers import MessageHandler, CallbackHandler, EchoHandler, CommandsHandler, ContactHandler, MyIdHandler, CurrencyHandler, GifHandler
from pprint import pprint


@app.route('/', methods=["GET", "POST"])
def hello():
    if message := request.json.get('message'):
        handler = MessageHandler(message)
    elif callback := request.json.get('callback_query'):
        handler = CallbackHandler(callback)
    if message := request.json.get('message'):
        if 'text' in message:
            text = message['text']
            if text == '/commands' or text == '/start':
                handler = CommandsHandler(message)
            elif text.startswith('/echo'):
                handler = EchoHandler(message)
            elif text.startswith('/add_contact') or text == '/get_contacts' or text.startswith('/delete_contact'):
                handler = ContactHandler(message)
            elif text == '/my_id':
                handler = MyIdHandler(message)
            elif text == '/currency':
                handler = CurrencyHandler(message)
            elif text == '/gif':
                handler = GifHandler(message)
    pprint(request.json)
    handler.handle()
    return 'ok'
