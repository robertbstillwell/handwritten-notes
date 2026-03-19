#!/usr/bin/env python3
"""Check Simply Noted account status and payment method."""

import os, sys, json
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv('SIMPLY_NOTED_API_KEY')
USER_ID = os.getenv('SIMPLY_NOTED_USER_ID')
BASE_URL = 'https://live.simplynoted.com/api/v2'

def headers():
    return {'x-api-key': API_KEY, 'x-user-id': USER_ID, 'Content-Type': 'application/json'}

if not API_KEY or not USER_ID:
    print('ERROR: Missing SIMPLY_NOTED_API_KEY or SIMPLY_NOTED_USER_ID in .env')
    sys.exit(1)

print('Checking Simply Noted account...\n')

# Payment method
resp = requests.get(f'{BASE_URL}/payments/payment_method_status', headers=headers())
if resp.status_code == 200:
    data = resp.json()
    pm = data.get('payment_method', {})
    print(f'Payment method: {pm.get("brand","?").upper()} ending in {pm.get("last4","?")}')
else:
    print(f'ERROR: {resp.status_code} — {resp.text[:200]}')
    sys.exit(1)

# Cards
resp = requests.get(f'{BASE_URL}/cards', headers=headers())
cards = resp.json().get('cards', [])
print(f'\nCards in account ({len(cards)}):')
for c in cards:
    print(f'  [{c["id"]}] {c["name"]} ({c["orientation"]})')

# Sender profiles
resp = requests.get(f'{BASE_URL}/sender_profiles', headers=headers())
profiles = resp.json().get('sender_profiles', [])
print(f'\nSender profiles ({len(profiles)}):')
for p in profiles:
    print(f'  [{p["id"]}] {p["first_name"]} {p["last_name"]} — {p["return_address"].split(chr(10))[0]}')
    print(f'    Handwriting: {p["handwriting_style"]}')

# Recent mailings
resp = requests.get(f'{BASE_URL}/mailings', headers=headers())
mailings = resp.json().get('mailings', [])
print(f'\nRecent mailings ({len(mailings)}):')
for m in mailings:
    print(f'  [{m["id"][:8]}...] {m["name"]} — Status: {m["status"]}')
