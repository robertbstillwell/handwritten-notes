# Simply Noted API V2 — Reference

**Official docs:** https://documenter.getpostman.com/view/3418100/2sAYHxoQAD
**Base URL:** `https://live.simplynoted.com/api/v2`

---

## Authentication

All requests require two headers:

```
x-api-key: <your api key>
x-user-id: <your user id>
```

Use `x-actor-id` to send on behalf of another user (must be same account or authorized via integrations).

---

## Payment

### GET /payments/payment_method_status
Check if a payment method is on file.

```bash
curl -H "x-api-key: $API_KEY" \
     -H "x-user-id: $USER_ID" \
     https://live.simplynoted.com/api/v2/payments/payment_method_status
```

Response:
```json
{
  "has_payment_method": true,
  "payment_method": { "brand": "visa", "last4": "3225" }
}
```

### POST /payments/charge
Charge a specific amount.

```json
{ "amount_cents": 1500, "description": "Service fee for order #12345" }
```

---

## Sender Profiles

### GET /sender_profiles
List all sender profiles on the account.

```bash
curl -H "x-api-key: $API_KEY" -H "x-user-id: $USER_ID" \
     https://live.simplynoted.com/api/v2/sender_profiles
```

Response includes: `id`, `first_name`, `last_name`, `return_address`, `handwriting_style`, `phone`, `email`

**Robert's sender profile ID:** `09623e9c-3dd5-4e39-b9fb-e59bcb2e4d82`
Handwriting: Hoffman | Address: 1598 Red Oak Lane, Brentwood TN 37027

---

## Cards

### GET /cards
List all card designs in the account.

```bash
curl -H "x-api-key: $API_KEY" -H "x-user-id: $USER_ID" \
     https://live.simplynoted.com/api/v2/cards
```

Response includes: `id`, `name`, `orientation`, `card_front_preview_url`

**Available cards:**
| ID | Name | Orientation |
|----|------|-------------|
| `395c7798-3541-4548-8a55-16298551cb28` | Hibbs Health | landscape |

---

## Messages / Templates

### GET /messages
List saved message templates.

### POST /messages
Create a message template.

```json
{
  "message": {
    "body": "Dear {{first_name}},\n\nThank you for your time...\n\nBest,\nRobert Stillwell"
  }
}
```

---

## Mailings (Multi-recipient)

### GET /mailings
List all mailings.

### POST /mailings
Create a new mailing (send to one or more recipients via a list).

```json
{
  "mailing": {
    "sender_profile_id": "09623e9c-3dd5-4e39-b9fb-e59bcb2e4d82",
    "card_id": "395c7798-3541-4548-8a55-16298551cb28",
    "message_id": "<message id>",
    "list_ids": ["<list id>"]
  }
}
```

Response: mailing object with `id`, `name`, `size`, `status`, `created_at`

---

## Single Card Mailings (One-off)

### POST /single_card_mailings
Send a single handwritten card without setting up lists.

```json
{
  "single_card_mailing": {
    "sender_profile_id": "09623e9c-3dd5-4e39-b9fb-e59bcb2e4d82",
    "card_id": "395c7798-3541-4548-8a55-16298551cb28",
    "message": "Dear Jane,\n\nThank you for your time...\n\nBest,\nRobert Stillwell",
    "contact": {
      "first_name": "Jane",
      "last_name": "Smith",
      "address1": "123 Main St",
      "city": "Nashville",
      "state": "TN",
      "postal_code": "37201",
      "country": "US"
    }
  }
}
```

---

## Contact Lists

### GET /lists
List all contact lists.

### POST /lists
Create a new contact list.

### POST /lists/:id/contacts
Add contacts to a list.

---

## Gotchas (Learned the Hard Way)

- **Wrong base URL:** Old docs say `api.simplynoted.com` — the real URL is `live.simplynoted.com`
- **Wrong auth:** Old docs say `Authorization: Bearer` — real auth is `x-api-key` + `x-user-id` headers
- **`/single_card_mailings` returns 404** — confirmed not available on this account tier; use `/mailings` with a list instead
- **Cost:** ~$3.58/note, credits pre-purchased — ALWAYS confirm with Robert before sending
- **Card must exist in account** — you can't reference a card ID from another account
- **Sender profile must exist** — set up in Simply Noted UI before using API

---

## Robert's Account Quick Reference

| Item | Value |
|------|-------|
| API Key | in `.env` as `SIMPLY_NOTED_API_KEY` |
| User ID | `bfc897c1-8805-4f3e-9e83-71802692ddf4` |
| Sender Profile ID | `09623e9c-3dd5-4e39-b9fb-e59bcb2e4d82` |
| Card (Hibbs Health) | `395c7798-3541-4548-8a55-16298551cb28` |
| Handwriting Style | Hoffman |
| Return Address | 1598 Red Oak Lane, Brentwood, TN 37027 |
