#!/usr/bin/env python3
"""Check remaining Simply Noted credits."""

import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv('SIMPLY_NOTED_API_KEY')
BASE_URL = 'https://api.simplynoted.com/api'


def check_balance():
    if not API_KEY:
        print('ERROR: SIMPLY_NOTED_API_KEY not found in .env file.')
        sys.exit(1)

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    print('Checking Simply Noted credit balance...\n')
    resp = requests.get(f'{BASE_URL}/credits', headers=headers)

    if resp.status_code == 200:
        data = resp.json()
        if isinstance(data, dict):
            credits = data.get('credits', data.get('balance', 'Unknown'))
            print(f'Remaining credits: {credits}')
            if isinstance(credits, (int, float)):
                cost_per_note = 3.58
                print(f'Estimated notes remaining: {int(credits)}')
                print(f'Estimated value: ${credits * cost_per_note:.2f}')
        else:
            print(f'Credits info: {data}')
    else:
        print(f'ERROR: API returned status {resp.status_code}')
        print(resp.text)
        if resp.status_code == 401:
            print('\nTip: Check that your SIMPLY_NOTED_API_KEY in .env is correct.')
            print('Get your API key from your Simply Noted account under Account Details.')
        sys.exit(1)


if __name__ == '__main__':
    check_balance()
