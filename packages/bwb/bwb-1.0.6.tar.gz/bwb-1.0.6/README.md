# bwb

bot with bot.

## Usage

Install with `pip install --upgrade bwb`.

```text
# Import one of:
from bwb.tanner import bwb
from bwb.jason import bwb
from bwb.tdev import bwb
from bwb.molly import bwb
```

### Handshaking

On boot up, send `000000handshake` to BWB chat.

When you see a `000000handshake`:

```text
secret = bwb.init()
await client.send_message(BWB, '000000handshake ' + secret)
```

When you see a `000000handshake [secret data]`:

```text
bwb.init(secret_data)
await client.send_message(BWB, bwb.wrap('🤝'))
```

When you see and authed '🤝', reply with *unauthed* '🤝'.

### Interaction

Run every incoming message through `bwb.parse()` since it's inexpensive. This will decrypt and remove base58 encoding. If the command is invalid, `text` will be `None`.

Example:

```text
if text.startswith('!'):
    ...
else:
    authed, text = bwb.parse(text)
    if not text: return
```

Use `bwb.wrap()` to auth and encode outgoing commands.

Params:

```text
wrap(text, target=None, b58=False, enc=False)
```

Examples:
```text
out = bwb.wrap('ping')  # broadcast all bots
out = bwb.wrap('ping', target=TANNER)  # auth for Tannerbot
out = bwb.wrap('ping', target=JASON, enc=True)  # base58 encrypt
out = bwb.wrap('ping', target=MOLLY, b58=True)  # base58
```

## Development

### Setup

Clone the repo.

To test your changes:

```text
pip install --upgrade ~/path/to/bwb
```

### Deployment

Install setuptools:

```text
python3 -m pip install --user --upgrade setuptools wheel
```

* Increment version number in `setup.py`

Build and upload:

```text
bash build-upload.sh
```
