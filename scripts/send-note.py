#!/usr/bin/env python3
"""Send a handwritten note via Simply Noted API.

Usage:
  python3 send-note.py \
    --to-first "Elizabeth" --to-last "Stillwell" \
    --to-address "1598 Red Oak Lane" --to-city "Brentwood" \
    --to-state "TN" --to-zip "37027" \
    --message "Dear Liz,\n\nThank you..."

Defaults:
  --card-id      Hibbs Health card
  --sender-id    Robert Stillwell profile
"""

import argparse, os, sys, json
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv('SIMPLY_NOTED_API_KEY')
USER_ID = os.getenv('SIMPLY_NOTED_USER_ID')
BASE_URL = 'https://live.simplynoted.com/api/v2'

DEFAULT_CARD_ID     = '395c7798-3541-4548-8a55-16298551cb28'  # Hibbs Health
DEFAULT_SENDER_ID   = '09623e9c-3dd5-4e39-b9fb-e59bcb2e4d82'  # Robert Stillwell / Hoffman

def headers():
    return {'x-api-key': API_KEY, 'x-user-id': USER_ID, 'Content-Type': 'application/json'}

def main():
    if not API_KEY or not USER_ID:
        print('ERROR: Missing API credentials in .env')
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('--to-first',   required=True)
    parser.add_argument('--to-last',    required=True)
    parser.add_argument('--to-address', required=True)
    parser.add_argument('--to-city',    required=True)
    parser.add_argument('--to-state',   required=True)
    parser.add_argument('--to-zip',     required=True)
    parser.add_argument('--message',    required=True)
    parser.add_argument('--card-id',    default=DEFAULT_CARD_ID)
    parser.add_argument('--sender-id',  default=DEFAULT_SENDER_ID)
    parser.add_argument('--name',       default=None, help='Mailing name (optional)')
    args = parser.parse_args()

    mailing_name = args.name or f"Note to {args.to_first} {args.to_last}"
    message_text = args.message.replace('\\n', '\n')

    print('\n' + '='*50)
    print('HANDWRITTEN NOTE PREVIEW')
    print('='*50)
    print(f'To:      {args.to_first} {args.to_last}')
    print(f'Address: {args.to_address}, {args.to_city}, {args.to_state} {args.to_zip}')
    print(f'Card:    {args.card_id}')
    print(f'Sender:  {args.sender_id}')
    print(f'\nMessage:\n{message_text}')
    print('='*50)
    print(f'\n⚠️  This will use 1 credit (~$3.58) and send a REAL physical card.')

    confirm = input('\nSend this note? (y/N): ').strip().lower()
    if confirm != 'y':
        print('Aborted.')
        sys.exit(0)

    # Step 1: Create message
    print('\nCreating message...')
    msg_resp = requests.post(f'{BASE_URL}/messages',
        headers=headers(),
        json={'message': {'name': mailing_name, 'body': message_text}}
    )
    if msg_resp.status_code not in (200, 201):
        print(f'ERROR creating message: {msg_resp.status_code} — {msg_resp.text}')
        sys.exit(1)
    message_id = msg_resp.json()['id']
    print(f'Message created: {message_id}')

    # Step 2: Send single card mailing
    print('Sending card...')
    send_resp = requests.post(f'{BASE_URL}/single_card_mailings',
        headers=headers(),
        json={'single_card_mailing': {
            'name': mailing_name,
            'sender_profile_id': args.sender_id,
            'card_id': args.card_id,
            'message_id': message_id,
            'contact': {
                'first_name': args.to_first,
                'last_name':  args.to_last,
                'street_1':   args.to_address,
                'city':       args.to_city,
                'state':      args.to_state,
                'zipcode':    args.to_zip,
                'country':    'US',
            }
        }}
    )
    if send_resp.status_code not in (200, 201):
        print(f'ERROR sending: {send_resp.status_code} — {send_resp.text}')
        sys.exit(1)

    data = send_resp.json()
    print(f'\n✅ Card sent!')
    print(f'   Mailing ID: {data.get("mailing_id")}')
    print(f'   To: {args.to_first} {args.to_last}, {args.to_city} {args.to_state}')
    print(f'\nRemember to update STATE.md or your notes with this send.')

if __name__ == '__main__':
    main()
