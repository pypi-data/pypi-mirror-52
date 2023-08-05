# bwb

bot with bot.

## Usage

Install with `pip install bwb`.

```
# Import one of:
from bwb.tanner import bwb
from bwb.jason import bwb
from bwb.tdev import bwb
from bwb.molly import bwb
```

### Handshaking

On boot up, send `000000handshake` to BWB chat.

When you see a `000000handshake`:

```
secret = bwb.init()
await client.send_message(BWB, '000000handshake ' + secret)
```

When you see a `000000handshake [secret data]`:

```
bwb.init(secret_data)
await client.send_message(BWB, bwb.wrap('🤝'))
```

When you see and authed '🤝', reply with '🤝'.

### Interaction

Run every incoming message through `bwb.parse()` since it's inexpensive. This will decrypt and remove base58 encoding. If the command is invalid, `text` will be `None`.

Example:

```
if text.startswith('!'):
    ...
else:
    authed, text = bwb.parse(text)
    if note text: return
```

Use `bwb.wrap()` to auth and encode outgoing commands.

Params:

```
wrap(text, target=None, b58=False, enc=False)
```

Examples:
```
out = bwb.wrap('ping')  # broadcast all bots
out = bwb.wrap('ping', target=TANNER)  # auth for Tannerbot
out = bwb.wrap('ping', target=JASON, enc=True)  # encrypt
out = bwb.wrap('ping', target=MOLLY, b58=True)  # base58
```

## Development

### Setup

Clone the repo.

To test your changes:

```
pip install --upgrade ~/path/to/bwb
```

### Deployment

Install setuptools:

```
python3 -m pip install --user --upgrade setuptools wheel
```

* Increment version number in `setup.py`

Build and upload:

```
bash build-upload.sh
```
