from __future__ import annotations

import os
from datetime import datetime, timezone

from flask import Flask, render_template

from temp_gmail import GMail

app = Flask(__name__)
mailbox = GMail()


@app.get("/")
def inbox_dashboard():
    if mailbox.email is None:
        mailbox.create_email()

    data = mailbox.load_list()
    messages = data.get("messageData", [])
    return render_template(
        "inbox.html",
        email=mailbox.email,
        messages=messages,
        refreshed_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=False)
