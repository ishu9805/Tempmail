from __future__ import annotations

import os
from collections import defaultdict

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from temp_gmail import GMail

BOT_TOKEN = os.getenv("BOT_TOKEN", "8261086638:AAFcwTP6ZixU1apn0VSwJHISy9OtHnr66VE")
API_ID = int(os.getenv("API_ID", "22792918"))
API_HASH = os.getenv("API_HASH", "ff10095d2bb96d43d6eb7a7d9fc85f81")
INBOX_URL = os.getenv("INBOX_URL", "http://localhost:8080")

app = Client("tempmail-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
mailboxes: dict[int, GMail] = defaultdict(GMail)


def action_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Create new temp email", callback_data="create")],
            [InlineKeyboardButton("Refresh inbox", callback_data="refresh")],
            [InlineKeyboardButton("Open inbox page", url=INBOX_URL)],
        ]
    )


@app.on_message(filters.command("start"))
async def start_handler(_: Client, message: Message) -> None:
    await message.reply_text(
        "TempMail bot is ready. Use the buttons below to create and check temporary email inboxes.",
        reply_markup=action_keyboard(),
    )


@app.on_callback_query(filters.regex("^create$"))
async def create_handler(_: Client, callback_query):
    user_id = callback_query.from_user.id
    mailbox = mailboxes[user_id]
    email = mailbox.create_email()
    await callback_query.message.reply_text(
        f"✅ New email created:\n`{email}`\n\nUse *Refresh inbox* to check incoming messages.",
        reply_markup=action_keyboard(),
    )
    await callback_query.answer("Email created")


@app.on_callback_query(filters.regex("^refresh$"))
async def refresh_handler(_: Client, callback_query):
    user_id = callback_query.from_user.id
    mailbox = mailboxes[user_id]

    if mailbox.email is None:
        await callback_query.answer("Create an email first", show_alert=True)
        return

    inbox = mailbox.load_list().get("messageData", [])
    if not inbox:
        text = f"📭 Inbox is empty for `{mailbox.email}`"
    else:
        top = inbox[:5]
        lines = [f"📨 Latest messages for `{mailbox.email}`"]
        for i, item in enumerate(top, 1):
            sender = item.get("from", "Unknown sender")
            subject = item.get("subject", "No subject")
            lines.append(f"{i}. From: {sender}\n   Subject: {subject}")
        text = "\n".join(lines)

    await callback_query.message.reply_text(text, reply_markup=action_keyboard())
    await callback_query.answer("Inbox updated")


if __name__ == "__main__":
    app.run()
