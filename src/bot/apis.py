import os
import aiohttp
import random
from typing import Union, Tuple, Dict, Any

MEME_API_URL = 'https://meme-api.herokuapp.com/gimme'
GIPHY_API_URL = 'https://api.giphy.com/v1/stickers/search?api_key={0}&limit=1'.format(os.getenv('GIPHY_API_KEY'))
OPEN_WEATHER_MAP_API_URL = 'https://api.openweathermap.org/data/2.5/weather?appid={0}'.format(os.getenv('OPEN_WEATHER_MAP_APP_ID_KEY'))
ICANHAZDADJOKE_API_URL = 'https://icanhazdadjoke.com'

ACCEPT_JSON_RESPONSE_HEADER = { 
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

ACCEPT_JSON_VND_RESPONSE_HEADER = {
    'Accept': 'application/vnd.api+json',
    'Content-Type': 'application/json'
}

ACCEPT_TEXT_RESPONSE_HEADER = {
    'Accept': 'text/plain',
    'Content-Type': 'application/json'
}

class BotAPIs:
    NOT_FOUND = -2
    RATE_LIMITED = -3

    def __init__(self):
        self.client_session = aiohttp.ClientSession()

    async def get_weather(self, city: str) -> Union[int, Dict[str, Any]]:
        async with self.client_session.get(f'{OPEN_WEATHER_MAP_API_URL}&q={city}&units=metric', headers = ACCEPT_JSON_RESPONSE_HEADER) as response:
            body = await response.json()
            if body.get('cod') == '404':
                return self.NOT_FOUND

            elif body.get('weather') != None:
                coordinates = body.get('coord')
                weather = body.get('weather')[0]
                description = weather.get('description')
                icon_id = weather.get('icon')
                city_name = body.get('name')
                main = body.get('main')

                if description == None or icon_id == None or city_name == None or coordinates == None or main == None:
                    raise Exception('Openweathermap didn\'t return the required weather information.')

                else:
                    icon_url = 'https://openweathermap.org/img/wn/{0}@2x.png'.format(icon_id)
                    return {
                        'latitude': coordinates.get('lat'),
                        'longitude': coordinates.get('lon'),
                        'description': description,
                        'icon_url': icon_url,
                        'city': city_name,
                        'temperature': main.get('temp'),
                        'feels_like': main.get('feels_like')
                    }

    async def get_sticker_from_tag(self, tag: str) -> Union[int, str]:
        tag = tag.lower().strip()

        async with self.client_session.get('{0}&q={1}'.format(GIPHY_API_URL, tag), headers = ACCEPT_JSON_RESPONSE_HEADER) as response:
            body = await response.json()

            if body['meta'] != None and body['meta']['status'] == 429:
                return self.RATE_LIMITED

            data = None

            try:
                data = body['data'][0]

            except:
                return self.NOT_FOUND

            images = data['images']['original']
            url = images['url']
            return url

    async def get_random_meme(self) -> Union[int, Tuple[str, str]]:
        async with self.client_session.get(MEME_API_URL, headers = ACCEPT_JSON_RESPONSE_HEADER) as response:
            body = await response.json()
            title = body['title']
            url = body['url']
            return (title, url)

    async def get_random_joke(self) -> Union[int, str]:
        async with self.client_session.get(ICANHAZDADJOKE_API_URL, headers = ACCEPT_TEXT_RESPONSE_HEADER) as response:
            joke = await response.text()

            if joke == None:
                return self.NOT_FOUND

            else:
                return joke
