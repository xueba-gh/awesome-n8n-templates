# Price drop tracker with email alert

Reads a price from a product page every few hours and emails you when it drops to your target. Works on pages that show the price in plain HTML.

## What you need

- Gmail

## Setup

1. Open **Settings** and list the addresses to check (and your email). Set **target_price** and, if the page uses a different format, the **price_regex** (first capture group = the number).
2. Connect Gmail on **Email me the alert**.
3. Run it once by hand, look at **Judge the result** to see what it found, then switch to **Active**.
4. It only emails you when something is wrong, so a quiet inbox means all is well.

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
