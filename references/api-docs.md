# Simply Noted API Reference

Official docs: https://documenter.getpostman.com/view/3418100/2sAYHxoQAD

## Base URL

```
https://api.simplynoted.com/api
```

## Authentication

All requests require a Bearer token in the Authorization header:

```
Authorization: Bearer <API_KEY>
```

Get your API key from your Simply Noted account under Account Details.

---

## Endpoints

### POST /orders — Send a Handwritten Note

Creates a new order to send a handwritten note.

**Request Body:**

```json
{
  "productId": "string (card design ID)",
  "handwritingStyle": "string (e.g. 'Tarzan', 'Claire', 'Stacy')",
  "customMessage": "string (max 400 characters)",
  "signoff": "string (e.g. 'Best, Robert')",
  "shippingDate": "string (optional, ISO date for delayed send)",
  "templateId": "string (optional, use a saved template)",
  "recipientData": [
    {
      "First Name": "string",
      "Last Name": "string",
      "Address": "string",
      "City": "string",
      "State": "string (2-letter code)",
      "Zip": "string",
      "Phone": "string (optional)",
      "Email": "string (optional)",
      "Company": "string (optional)"
    }
  ],
  "returnAddress": {
    "name": "string",
    "address": "string",
    "city": "string",
    "state": "string",
    "zip": "string"
  }
}
```

**Response:** Order confirmation with order ID.

---

### GET /cards — List Available Card Designs

Returns all available standard card designs.

**Query Parameters:**
- `offset` (optional) — Pagination offset

**Response:**

```json
[
  {
    "id": "string",
    "title": "string",
    "image": "string (URL)"
  }
]
```

---

### GET /credits — Check Credit Balance

Returns the current credit balance for the account.

**Response:**

```json
{
  "credits": number
}
```

---

### GET /orders/customer/ — List Past Orders

Returns past orders for the authenticated user.

**Query Parameters:**
- `offset` — Pagination offset (default: 0)
- `status` — Filter by status (e.g. "any", "pending", "shipped")
- `fulfillment_status` — Filter by fulfillment (e.g. "shipped", "unfulfilled")

---

### POST /createcard — Create Custom Card

Creates a new custom card design.

### POST /modifycard — Modify Custom Card

Modifies an existing flat custom card design.

---

## Handwriting Styles

Available styles include (check via API for current list):
- Tarzan (default)
- Claire
- Stacy
- And others

## Notes

- Each note costs approximately **$3.58**
- Notes are physically written with real ink and mailed via USPS
- Delivery takes **3-5 business days**
- Messages are truncated at **400 characters**
- All addresses must be valid US mailing addresses
