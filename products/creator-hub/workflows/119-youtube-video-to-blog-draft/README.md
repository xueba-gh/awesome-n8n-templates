# New YouTube video to blog post draft and social posts

When a YouTube channel publishes a video, AI writes a blog post draft, a LinkedIn post and a tweet from the title and description, saved to a sheet.

## What you need

- Google Sheets
- OpenAI API key

## Setup

1. Open **Settings** and list your RSS feed URLs (most blogs have `/feed` or `/rss`; a YouTube channel is `https://www.youtube.com/feeds/videos.xml?channel_id=...`).
2. Use a Google Sheet with a tab named **Video content** and the headers in `sheet-headers.csv`, then connect Google Sheets and OpenAI.
3. Run it once by hand and look at **Keep new items**, then switch to **Active**.

## Google Sheet columns (row 1)

`title`, `link`, `published`, `blog_title`, `blog_draft`, `linkedin_post`, `tweet`, `saved_at`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
