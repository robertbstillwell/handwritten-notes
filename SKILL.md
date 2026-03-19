# handwritten-notes

Send personalized handwritten notes via Simply Noted API. Use when: handwritten note, simply noted, thank you card, personal outreach, follow up card, physical note, handwritten card.

## Required Reading

Before drafting or sending any note, read these context files:

1. `context/businesses.md` — Robert's three businesses and their positioning
2. `context/sender-profile.md` — Robert's sender info, titles, and return address
3. `context/simply-noted.md` — API details, gotchas, and cost info
4. `references/api-docs.md` — Full API reference

## Workflow

1. **Robert provides**: recipient name, address, and context (why the note is being sent, which business it relates to)
2. **Agent drafts note**: Write a warm, personal handwritten-style message (keep it under 400 characters — that's the Simply Noted limit). Use the appropriate business context and Robert's matching title.
3. **Robert approves**: Show the full note preview including recipient, sender info, and message. Wait for explicit approval.
4. **Agent sends via API**: Run `scripts/send-note.py` with the approved details. The script has a built-in confirmation prompt — Robert must type `y` to send.

## Note Style Guide

- Keep it personal and genuine — this is handwritten, not a form letter
- First-person voice as Robert
- Short paragraphs, conversational tone
- Sign off naturally: "Best, Robert" or "Thanks, Robert" or similar
- Never use corporate jargon in a handwritten note
- Match the tone to the context (thank you, follow up, congratulations, etc.)

## Choosing a Card Design

Run `scripts/list-cards.py` to see available card designs. Let Robert pick one, or suggest one based on the occasion.

## Checking Credits

Run `scripts/check-balance.py` before sending to verify available credits.

## Gotchas

- **Each note costs $3.58 and real money** — ALWAYS confirm with Robert before sending
- **Robert has ~100 credits** — don't burn them on tests
- **400 character limit** on messages — Simply Noted truncates beyond this
- **Address must be valid US mailing address** — the note is physically mailed by a robot
- **No undo** — once sent, it's sent. A real pen-and-ink note will be written and mailed
- **API key is in .env** — never commit or expose it
- **Use the right title** — Robert's title varies by business (see sender-profile.md)
- **Shipping takes 3-5 business days** — factor this into time-sensitive outreach
