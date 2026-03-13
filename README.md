# temp-gmail-api (upgraded)

Temporary email toolkit with:

- Python API (`temp_gmail.GMail`)
- Telegram bot powered by **Pyrogram**
- HTML inbox page powered by **Flask**
- Docker runtime for easy deployment

## Install

```bash
pip install -r requirements.txt
```

## Python API usage

```python
from temp_gmail import GMail

gmail = GMail()
email = gmail.create_email()
print(email)
print(gmail.load_list())
```

## Run inbox web page

```bash
python webapp.py
```

Open: `http://localhost:8080`

## Run Telegram bot

```bash
python telegram_bot.py
```

Default credentials are prefilled from your request, and can also be overridden with env vars:

- `BOT_TOKEN`
- `API_ID`
- `API_HASH`
- `INBOX_URL`

## Docker

```bash
docker build -t tempmail .
docker run --rm -p 8080:8080 tempmail
```

## Button features in Telegram

- Create new temp email
- Refresh inbox preview
- Open inbox HTML page link
