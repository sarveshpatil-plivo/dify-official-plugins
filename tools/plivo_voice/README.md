# Plivo Voice

## Overview

This plugin makes outbound voice calls through Plivo's Voice API from Dify workflows and agents.

## Configuration

1. Create or sign in to your [Plivo account](https://cx.plivo.com/?utm_source=github&utm_medium=oss&utm_campaign=dify-plivo-voice).
2. Copy the `auth_id` and `auth_token` from the Plivo console.
3. Install the plugin in Dify and fill in the credentials.

## Usage

Use the `make_call` tool with:

- `from_number`: a Plivo voice-enabled number that places the call, in E.164 format
- `to_number`: the destination phone number, in E.164 format
- `answer_url`: the URL Plivo fetches [Plivo XML](https://www.plivo.com/docs/voice/xml/?utm_source=github&utm_medium=oss&utm_campaign=dify-plivo-voice) from when the call is answered. This XML tells Plivo what to do on the call (speak text, play audio, connect, etc.)
- `answer_method` (optional): the HTTP method Plivo uses to fetch the Answer URL. Must be `GET` or `POST`. Defaults to `POST` when omitted.

On success the tool returns the Plivo `request_uuid` for the call. Errors (authentication, validation, or API failures) are returned as a structured JSON payload with `status: "failed"` and an `error` message.
