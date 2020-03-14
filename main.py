'''

from forex_python.converter import CurrencyRates

c = CurrencyRates()
print(c.get_rates('USD'))
'''

import random

import requests
from requests import HTTPError
from telegram.ext import CommandHandler, Updater

POKEMON_API_URL = 'https://pokeapi.co/api/v2/'
TELEGRAM_BOT_TOKEN = '921718883:AAGXDn3YNT-trE5j1Kbljkk4iiYfPr84L3Y'
DEFAULT_POKEMON = 1


def get_sprite(pokemon_id=None, pokemon_name=None):
    method = 'pokemon/{}'
    if pokemon_id:
        method = method.format(pokemon_id)
    elif pokemon_name:
        method = method.format(pokemon_name)
    else:
        return {}

    pokemon_data = do_request(POKEMON_API_URL + method)
    if pokemon_data is None:
        return

    is_shiny = random.randint(0, 1)
    sprite_key = 'front_shiny' if is_shiny else 'front_default'
    sprite_url = pokemon_data['sprites'][sprite_key]
    sprite_name = pokemon_data['name']
    return {'url': sprite_url, 'name': sprite_name, 'is_shiny': is_shiny}


def do_request(url):
    try:
        req = requests.get(url)
        req.raise_for_status()
    except HTTPError:
        return None
    return req.json()


def get_pokemon(update, context):
    caption = 'you got a '
    pokedex_reference = context.args[0] if context.args else random.randint(0, 500)
    try:
        pokemon_id = int(pokedex_reference)
        pokemon_data = get_sprite(pokemon_id)
    except ValueError:
        pokemon_data = get_sprite(pokemon_name=pokedex_reference)
        if not pokemon_data:
            pokemon_data = get_sprite(pokemon_id=DEFAULT_POKEMON)
            caption = 'you named no valid pokemon, so here we got a '

    caption += ('shiny ' if pokemon_data['is_shiny'] else '') + pokemon_data['name']

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=pokemon_data['url'],
                           caption=caption)


# print(get_sprite(pokemon_random_id))
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('get_pokemon', get_pokemon)
dispatcher.add_handler(start_handler)
updater.start_polling()
