# Plivo Voice

## Overview

This plugin makes outbound voice calls through Plivo's Voice API from Dify workflows and agents.

## Configuration

1. Create or sign in to your [Plivo account](https://cx.plivo.com/?utm_source=github&utm_medium=oss&utm_campaign=dify-plivo-voice).
2. Copy the `auth_id` and `auth_token` from the Plivo console.
3. Install the plugin in Dify and fill in the credentials.

## Usage

Use the `make_call` tool with:

- `to_number`: the destination phone number, in E.164 format
- `from_number`: a Plivo voice-enabled number that places the call, in E.164 format

Two further settings are configured on the tool rather than supplied per call, because
what a call plays is a property of the deployment rather than something a model chooses.

- `answer_url` (optional): the URL Plivo fetches [Plivo XML](https://www.plivo.com/docs/voice/xml/?utm_source=github&utm_medium=oss&utm_campaign=dify-plivo-voice) from when the call is answered. This XML tells Plivo what to do on the call, such as speak text, play audio, or connect to another number. Leaving it empty uses Plivo's hosted sample XML, which answers the call and speaks a short message, so a call works with no extra setup.
- `answer_method` (optional): the HTTP method Plivo uses to fetch the Answer URL. Must be `GET` or `POST`. Defaults to `POST` when omitted.

On success the tool returns the Plivo `request_uuid` for the call. Errors (authentication, validation, or API failures) are returned as a structured JSON payload with `status: "failed"` and an `error` message.
