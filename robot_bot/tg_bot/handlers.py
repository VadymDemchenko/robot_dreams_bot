import requests
from .weather_services import WeatherService, WeatherServiceException
from .contactbook_services import ContactService, DuplicateContactException, InvalidContactException
import json
from pprint import pprint
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TOKEN')
TG_BASE_URL = 'https://api.telegram.org/bot'


class User:
    def __init__(self, first_name, id, is_bot, language_code, username=None, last_name=None):
        self.first_name = first_name
        self.id = id
        self.is_bot = is_bot
        self.language_code = language_code
        self.last_name = last_name
        self.username = username


class TelegramHandler:
    user = None

    def send_markup_message(self, text, markup):
        data = {
            'chat_id': self.user.id,
            'text': text,
            'reply_markup': markup
        }
        requests.post(f'{TG_BASE_URL}{TOKEN}/sendMessage', json=data)

    def send_message(self, text):
        data = {
            'chat_id': self.user.id,
            'text': text
        }
        requests.post(f'{TG_BASE_URL}{TOKEN}/sendMessage', json=data)


class MessageHandler(TelegramHandler):
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.text = data.get('text')

    def handle(self):
        match self.text.split():
            case '/weather', city:
                try:
                    geo_data = WeatherService.get_geo_data(city)
                    pprint(geo_data)
                except WeatherServiceException as wse:
                    self.send_message(str(wse))
                else:
                    buttons = []
                    for item in geo_data:
                        test_button = {
                            'text': f'{item.get("name")} - {item.get("admin1")} - {item.get("country_code")}',
                            'callback_data': json.dumps(
                                {'type': '/weather',
                                 'lat': item.get('latitude'),
                                 'lon': item.get('longitude')
                                 })
                        }
                        buttons.append([test_button])
                    markup = {
                        'inline_keyboard': buttons
                    }
                    self.send_markup_message('Choose a city from a list:', markup)


class CallbackHandler(TelegramHandler):
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.callback_data = json.loads(data.get('data'))

    def handle(self):
        callback_type = self.callback_data.pop('type')
        match callback_type:
            case '/weather':
                try:
                    weather = WeatherService.get_current_weather_by_geo_data(**self.callback_data)
                except WeatherServiceException as wse:
                    self.send_message(str(wse))
                else:
                    self.send_message(json.dumps(weather))


class EchoHandler(TelegramHandler):
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.text = data.get('text')

    def handle(self):
        echo_text = self.text[6:]
        self.send_message(echo_text)


class CommandsHandler(TelegramHandler):
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.text = data.get('text')

    def handle(self):
        commands = [
            '/start, /commands - All commands list',
            '/my_id - Send you your ID in Telegram',
            '/weather <city> - Get the weather for a specific city',
            '/currency - Returns the cost of EUR and USD in UAH',
            '/echo <message> - Echo back the provided message',
            '/add_contact <name> <phone> - Insert a new contact in contacts book',
            '/get_contacts - Show all contacts from contacts book',
            '/delete_contact <name> - Delete contact from contacts book'
        ]
        command_list = "\n".join(commands)
        self.send_message(f"Available commands:\n{command_list}")


class ContactHandler(TelegramHandler):
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.text = data.get('text')

    def handle(self):
        chat_id = self.user.id
        text = self.text

        if text.startswith('/add_contact'):
            try:
                _, name, phone_number = text.split()
                if len(name) < 2 or len(phone_number) < 5:
                    raise InvalidContactException('Name or phone is too short')
                elif not phone_number.isdigit():
                    raise InvalidContactException('Phone should contains digits not letters')
                ContactService.add_contact(chat_id, name, phone_number)
                response = 'Contact has been added successfully!'
                self.send_message(response)
            except DuplicateContactException as e:
                error_message = str(e)
                self.send_message(error_message)
            except InvalidContactException as e:
                error_message = str(e)
                self.send_message(error_message)
            except ValueError:
                error_message = "You need to write Name and Phone after command /add_contact "
                self.send_message(error_message)

        elif text == '/get_contacts':
            contacts = ContactService.get_contacts(chat_id)
            if contacts:
                response = "Your contacts:\n"
                for contact in contacts:
                    contact_id, name, phone_number = contact
                    response += f"Name: {name}, Phone: {phone_number}\n"
                self.send_message(response)
            else:
                response = "Your contacts book is empty"
                self.send_message(response)

        elif text.startswith('/delete_contact'):
            try:
                _, name = text.split()
                ContactService.delete_contact(chat_id, name)
                response = "Contact has been deleted successfully!"
                self.send_message(response)
            except InvalidContactException as e:
                error_message = str(e)
                self.send_message(error_message)


class MyIdHandler(TelegramHandler):
    def __init__(self, data):
        self.user = User(**data.get('from'))

    def handle(self):
        chat_id = self.user.id
        response = f"Your Telegram ID is : {chat_id}"
        self.send_message(response)


class CurrencyHandler(TelegramHandler):
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.text = data.get('text')

    def handle(self):
        response = self.get_currency_info()
        self.send_message(response)

    def get_currency_info(self):
        url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11"
        if self.text == '/currency':
            try:
                response = requests.get(url)
                data = response.json()

                result = ""
                for currency in data:
                    ccy = currency["ccy"]
                    buy = currency["buy"]
                    sale = currency["sale"]
                    result += f"\n{ccy}:\nBuy: {buy}\nSale: {sale}\n"
                return result
            except requests.RequestException as e:
                print("An error occurred:", str(e))
                return "Sorry, something went wrong. Please try again later"

