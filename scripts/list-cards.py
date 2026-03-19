#!/usr/bin/env python3
"""List available card designs from Simply Noted."""

import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv('SIMPLY_NOTED_API_KEY')
USER_ID = os.getenv('SIMPLY_NOTED_USER_ID')
BASE_URL = 'https://live.simplynoted.com/api/v2'


def list_cards():
    if not API_KEY:
        print('ERROR: SIMPLY_NOTED_API_KEY not found in .env file.')
        sys.exit(1)

    headers = {
        'x-api-key': API_KEY,
        'x-user-id': USER_ID,
        'Content-Type': 'application/json',
    }

    print('Fetching available card designs...\n')
    resp = requests.get(f'{BASE_URL}/cards', headers=headers)

    if resp.status_code == 200:
        cards = resp.json()
        if isinstance(cards, list):
            print(f'Found {len(cards)} card designs:\n')
            print(f'{"ID":<40} {"Title"}')
            print('-' * 80)
            for card in cards:
                card_id = card.get('id', 'N/A')
                title = card.get('title', 'Untitled')
                image = card.get('image', '')
                print(f'{card_id:<40} {title}')
                if image:
                    print(f'{"":40} {image}')
        elif isinstance(cards, dict) and 'data' in cards:
            card_list = cards['data']
            print(f'Found {len(card_list)} card designs:\n')
            print(f'{"ID":<40} {"Title"}')
            print('-' * 80)
            for card in card_list:
                card_id = card.get('id', 'N/A')
                title = card.get('title', 'Untitled')
                print(f'{card_id:<40} {title}')
        else:
            print('Response:')
            print(json.dumps(cards, indent=2))
    else:
        print(f'ERROR: API returned status {resp.status_code}')
        print(resp.text)
        sys.exit(1)


if __name__ == '__main__':
    list_cards()
