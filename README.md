# youtube-subscriptions

A simple subscription downloader to help download videos without going to Youtube. Videos are only downloaded in audio format.

This makes use of the excellent youtube-dl project. So please support that.

## Requirements

The requirements needed are:

1. youtube-dl https://github.com/rg3/youtube-dl
2. Python 2.7

## Usage

### `add <channel> <key>`

Adds a subscriber, e.g.
`python subscription.py add https://www.youtube.com/user/ReviewTechUSA rtu`

### `list_subscriptions`

Lists your current subscriptions

### `list`

Lists the most recent videos in your feed from oldest to newest. Follow the on-screen prompts to download.

### `help`

Prints basic help message

## Troubleshooting

This makes use of youtube-dl. It may be likely that that service needs updating. Please check their page: https://github.com/rg3/youtube-dl.
