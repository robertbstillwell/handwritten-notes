# Simply Noted API — Key Details

## Overview

Simply Noted is a service that sends real handwritten notes using pen-plotting robots. Notes are physically written with real ink on real cards and mailed via USPS.

## API Details

- **Base URL**: `https://api.simplynoted.com/api`
- **Auth**: Bearer token in Authorization header
  ```
  Authorization: Bearer <SIMPLY_NOTED_API_KEY>
  ```
- **Content-Type**: `application/json`

## Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/orders` | POST | Send a handwritten note |
| `/cards` | GET | List available card designs |
| `/credits` | GET | Check remaining credit balance |
| `/orders/customer/` | GET | List past orders |

## Sending a Note (POST /orders)

Required fields in the request body:

```json
{
  "productId": "<card_id>",
  "handwritingStyle": "Tarzan",
  "customMessage": "Your message here (max 400 chars)",
  "signoff": "Best, Robert",
  "recipientData": [
    {
      "First Name": "Jane",
      "Last Name": "Doe",
      "Address": "123 Main St",
      "City": "Nashville",
      "State": "TN",
      "Zip": "37201"
    }
  ],
  "returnAddress": {
    "name": "Robert Stillwell",
    "address": "1598 Red Oak Lane",
    "city": "Brentwood",
    "state": "TN",
    "zip": "37027"
  }
}
```

## Cost & Credits

- **$3.58 per note**
- Robert has **~100 credits**
- Every send costs real money — **ALWAYS confirm with Robert before sending**
- There is no test/sandbox mode — all sends are live

## Environment Variables

The `.env` file holds:
- `SIMPLY_NOTED_API_KEY` — Bearer token for API auth
- `SIMPLY_NOTED_USER_ID` — Account user ID

## Gotchas

1. **No undo** — once a note is sent via API, it will be physically written and mailed
2. **400 character limit** — messages beyond this get truncated
3. **Valid US addresses only** — notes are mailed via USPS
4. **3-5 business day shipping** — plan accordingly for time-sensitive outreach
5. **Card design matters** — always let Robert pick or confirm the card design
6. **Handwriting styles vary** — "Tarzan" is the default but there are others available
