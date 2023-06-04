import requests
import os
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()


def get_random_gif_url():
    api_key = os.getenv('GIPHY_API_KEY')
    url = f'https://api.giphy.com/v1/gifs/random?api_key={api_key}&rating=g'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pprint(data)

        if 'data' in data and 'images' in data['data']:
            images = data['data']['images']
            gif_url = images['original']['url']
            return gif_url
        else:
            print("Unexpected API response format. Missing 'image_original_url' key.")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {str(e)}")
        return None







