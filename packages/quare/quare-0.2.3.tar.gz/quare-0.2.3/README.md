# quare

[![pipeline status](https://gitlab.com/jstvz/quare/badges/master/pipeline.svg)](https://gitlab.com/jstvz/quare/commits/master)
[![coverage report](https://gitlab.com/jstvz/quare/badges/master/coverage.svg)](https://gitlab.com/jstvz/quare/commits/master)
[![PyPI - License](https://img.shields.io/pypi/l/quare.svg)](https://www.gnu.org/licenses/lgpl-3.0.en.html)
![PyPI](https://img.shields.io/pypi/v/quare.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/quare.svg)
![PyPI - Status](https://img.shields.io/pypi/status/quare.svg)

Interact with Quip from the command line.

![quare streaming messages](https://github.com/jstvz/quare/blob/master/docs/assets/quare.png?raw=true)

## Introduction ##
quare allows interaction with [Quip](https://quip.com) via the command line. While `quare` is in alpha, there are some features you may find useful:
- Pipe the output of a command to a chat or document and format it as monospace.
- Archive messages by piping them into a local file
- Securely store authentication tokens for multiple Quip instances.

This tool is in its early stages of development, and is subject to change (or abandonment) at any time. Use at your own risk.

## Installation ##

```console
$ pipx install quare
```

## Usage ##

### Authentication ###
Store a Quip API token (See: https://quip.com/dev/token):

```console
$ quare auth
Token: long_token_string
Token stored.
```
If you have multiple Quip instances (like multiple Slack Workspaces), you can specify an alias for them. You can also pass your token directly to `auth`:

```console
$ quare msg auth --alias test_server --token 't1DJBQWBXHCYgh1=|2983928392|nYtRFIhV7nl4...'
```

#### Whoami ####

To see information about the logged in user:
```console
$ quare msg whoami
┌Default───────┬───────────────┐
│ Name         │ Tests Testeri │
├──────────────┼───────────────┤
│ Email(s)     │ t@testz.dev   │
├──────────────┼───────────────┤
│ Quip User ID │ mRLA6Zdn3PO   │
└──────────────┴───────────────┘
```

### Sending messages ###
The destination may be a document or chat:

```console
$ quare msg send --room room_id --content 'Hello everyone!'
```

#### Pipe content from `stdin` ####

Message content can be piped from `stdin`:
```console
$ uname -a | quare msg send --room room_id --content '-'
```

While Quip allows formatting messages using some markdown markup, it doesn't recognize markdown code blocks ("\`\`\`"). To define a code block, use the `--monospace` option:

```console
$ dmesg | tail -n 5 | quare msg send --room room_id --content '-' --monospace
```

### Receiving messages ###

#### Stream to stdout ####
To stream every message appearing in the Updates tab:

```console
$ quare msg stream
Streaming updates... press Ctrl-C to exit.
[Sun Jun 30 17:23:09 2019 | (Test Log) | @Tests Testeri] ok ok
```

#### Dump the content of a chat room ####
To get the last 5 messages in a chat room or document:
```console
$ quare msg get --room room_id --last 5
[Sat Jun 29 03:19:09 2019 | @Tester Testeri] This is a monologue!
[Sat Jun 29 16:00:12 2019 | @Tester Testeri] ok
[Sat Jun 29 16:34:51 2019 | @Tester Testeri] I'm done!
[Sun Jun 30 17:30:14 2019 | @Tester Testeri] 🌮
[Sun Jun 30 17:30:27 2019 | @Tester Testeri] 🥃
```

To get the last 2 messages as JSON:
```console
$ quare msg get  -r "IcTAAAtVxXb" --last 2 --json
[{"author_id": "mRLA6Zdn3PO", "visible": true, "id": "IcderpEe8wG", "created_usec": 1561849212672040, "updated_usec": 1561849212696571, "text": "ok", "author_name": "Tester Testeri"}, {"author_id": "mRLA6Zdn3PO", "visible": true, "id": "IcNodg7n2Tx", "created_usec": 1561851291612434, "updated_usec": 1561851291620308, "text": "chat", "author_name": "Tester Testeri"}]
```

To dump the last 200 messages in a chat room into a text file:
```console
$ quare msg get --room room_id --last 200 > interesting_conversation.log
```

To get all messages since a datetime:
```console
$ quare msg get --room room_id --since 2019-01-01T00:32:00Z > greppable_archive.log
```

The `--since` option recognizes any date recognized by [dateparser](https://dateparser.readthedocs.io/en/latest/):
```console
$ quare msg get --room room_id --since 'Monday' > this_week.log
$ quare msg get --room room_id --since '2 months ago' > this_quarter.log
```

### Editing documents ###

To append a markdown file to an existing document
```console
$ quare doc append --id xxxDoc_IDxxx --file /tmp/foo.md
$ cat /tmp/foo.md | quare doc append --id xxxDoc_IDxxx --file -
```

To append a markdown-format string to an existing document
```console
$ quare doc append --id xxxDoc_IDxxx --content '## Headline\n\n'
```

## Development ##

This work is licensed under the terms of the [LGPL-3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html).
### Contributions ###
See CONTRIBUTING.rst
