#!/usr/bin/env python3
"""Send a handwritten note via Simply Noted API."""

import argparse
import json
import os
import sys

import requests
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv('SIMPLY_NOTED_API_KEY')
USER_ID = os.getenv('SIMPLY_NOTED_USER_ID')
BASE_URL = 'https://live.simplynoted.com/api/v2'

DEFAULT_FROM_NAME = 'Robert Stillwell'
DEFAULT_FROM_ADDRESS = '1598 Red Oak Lane'
DEFAULT_FROM_CITY = 'Brentwood'
DEFAULT_FROM_STATE = 'TN'
DEFAULT_FROM_ZIP = '37027'


def send_note(args):
    if not API_KEY:
        print('ERROR: SIMPLY_NOTED_API_KEY not found in .env file.')
        sys.exit(1)

    # Parse recipient address parts
    to_parts = parse_address(args.to_address)

    # Parse from address parts
    from_parts = parse_address(args.from_address)

    payload = {
        'productId': args.card_id,
        'handwritingStyle': args.handwriting_style,
        'customMessage': args.message,
        'signoff': args.signoff or f'Best, {args.from_name}',
        'recipientData': [
            {
                'First Name': args.to_name.split()[0] if args.to_name else '',
                'Last Name': ' '.join(args.to_name.split()[1:]) if args.to_name else '',
                'Address': to_parts['address'],
                'City': to_parts['city'],
                'State': to_parts['state'],
                'Zip': to_parts['zip'],
            }
        ],
        'returnAddress': {
            'name': args.from_name,
            'address': from_parts['address'],
            'city': from_parts['city'],
            'state': from_parts['state'],
            'zip': from_parts['zip'],
        },
    }

    # Preview
    print('\n' + '=' * 60)
    print('HANDWRITTEN NOTE PREVIEW')
    print('=' * 60)
    print(f"To:    {args.to_name}")
    print(f"       {args.to_address}")
    print(f"From:  {args.from_name}")
    print(f"       {args.from_address}")
    print(f"Card:  {args.card_id}")
    print(f"Style: {args.handwriting_style}")
    print('-' * 60)
    print(f"\n{args.message}\n")
    print(f"{payload['signoff']}")
    print('-' * 60)
    msg_len = len(args.message)
    print(f"Message length: {msg_len}/400 characters", end='')
    if msg_len > 400:
        print(' *** WARNING: EXCEEDS 400 CHAR LIMIT ***')
    else:
        print()
    print('=' * 60)

    # Require explicit confirmation
    confirm = input('\nSend this note? This will use 1 credit ($3.58). (y/N): ')
    if confirm.strip().lower() != 'y':
        print('Cancelled. Note was NOT sent.')
        sys.exit(0)

    # Send
    headers = {
        'x-api-key': API_KEY,
        'x-user-id': USER_ID,
        'Content-Type': 'application/json',
    }

    print('\nSending note...')
    resp = requests.post(f'{BASE_URL}/orders', headers=headers, json=payload)

    if resp.status_code in (200, 201):
        data = resp.json()
        print(f'Note sent successfully!')
        print(f'Order ID: {data.get("id", data.get("orderId", "N/A"))}')
        print(json.dumps(data, indent=2))
    else:
        print(f'ERROR: API returned status {resp.status_code}')
        print(resp.text)
        sys.exit(1)


def parse_address(address_str):
    """Parse a single-line address into components.

    Expected format: "Street, City, ST ZIP" or "Street, City ST ZIP"
    """
    parts = [p.strip() for p in address_str.split(',')]

    if len(parts) >= 3:
        address = parts[0]
        city = parts[1]
        state_zip = parts[2].strip().split()
    elif len(parts) == 2:
        address = parts[0]
        city_state_zip = parts[1].strip().split()
        if len(city_state_zip) >= 3:
            city = ' '.join(city_state_zip[:-2])
            state_zip = city_state_zip[-2:]
        else:
            city = city_state_zip[0] if city_state_zip else ''
            state_zip = city_state_zip[1:] if len(city_state_zip) > 1 else []
    else:
        return {'address': address_str, 'city': '', 'state': '', 'zip': ''}

    state = state_zip[0] if state_zip else ''
    zip_code = state_zip[1] if len(state_zip) > 1 else ''

    return {'address': address, 'city': city, 'state': state, 'zip': zip_code}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a handwritten note via Simply Noted')
    parser.add_argument('--to-name', required=True, help='Recipient full name')
    parser.add_argument('--to-address', required=True,
                        help='Recipient address (format: "Street, City, ST ZIP")')
    parser.add_argument('--message', required=True, help='Note message (max 400 chars)')
    parser.add_argument('--card-id', required=True, help='Card design ID (run list-cards.py to see options)')
    parser.add_argument('--from-name', default=DEFAULT_FROM_NAME, help='Sender name')
    parser.add_argument('--from-address',
                        default=f'{DEFAULT_FROM_ADDRESS}, {DEFAULT_FROM_CITY}, {DEFAULT_FROM_STATE} {DEFAULT_FROM_ZIP}',
                        help='Sender address (format: "Street, City, ST ZIP")')
    parser.add_argument('--handwriting-style', default='Tarzan',
                        help='Handwriting style (default: Tarzan)')
    parser.add_argument('--signoff', default=None,
                        help='Sign-off text (default: "Best, <from-name>")')

    args = parser.parse_args()

    if len(args.message) > 400:
        print(f'WARNING: Message is {len(args.message)} characters (limit is 400).')
        print('The message may be truncated by Simply Noted.')

    send_note(args)
