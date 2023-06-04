import requests
import os
from dotenv import load_dotenv

load_dotenv()


def set_webhook(url):
    bot_token = os.getenv('TOKEN')

    api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    data = {'url': url}

    try:
        response = requests.post(api_url, data=data)
        if response.status_code == 200:
            print("Webhook has been set successfully")
        else:
            print("Failed to set webhook")
            print("Response: ", response.text)

    except requests.RequestException as e:
        print("An error occurred:", str(e))


webhook_url = input("Insert your ngrok URL:\n")
set_webhook(webhook_url)

