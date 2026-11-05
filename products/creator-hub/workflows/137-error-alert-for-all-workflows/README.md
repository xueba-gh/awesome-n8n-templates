# Error alert email for all your workflows

Set it once as the error workflow: whenever a production workflow fails, you get an email with the workflow, the failed node, the error and a link to the run.

## What you need

- Gmail

## Setup

1. Open **Settings** and set the email for alerts. Connect Gmail.
2. Save this workflow. You do not need to activate it.
3. In each workflow you want watched: **Settings > Error workflow** and choose this one.
4. Test: make a workflow fail on purpose (for example a Code node with `throw new Error('test')`) and run it from a schedule or webhook. Manual runs do not trigger error workflows.

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
