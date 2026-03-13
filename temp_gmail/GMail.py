from __future__ import annotations

from typing import Any

from curl_cffi import requests

class GMail:
    """Client for interacting with Emailnator temporary inboxes."""

    BASE_URL = "https://www.emailnator.com"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": self.BASE_URL,
            "Referer": f"{self.BASE_URL}/",
            "Sec-Ch-Ua": '"Google Chrome";v="125", "Not;A Brand";v="99", "Chromium";v="125"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Linux"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.email: str | None = None
        self.session.get(f"{self.BASE_URL}/")
        self.update_tokens()

    def update_tokens(self) -> None:
        xsrf = self.session.cookies.get("XSRF-TOKEN")
        sesh = self.session.cookies.get("gmailnator_session")

        if xsrf:
            self.headers["X-Xsrf-Token"] = xsrf.replace("%3D", "=")
        if xsrf and sesh:
            self.headers["Cookie"] = f"XSRF-TOKEN={xsrf}; gmailnator_session={sesh};"

    def create_email(self) -> str:
        response = self.session.post(
            f"{self.BASE_URL}/generate-email",
            headers=self.headers,
            json={"email": ["plusGmail", "dotGmail"]},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        self.email = data["email"][0]
        self.update_tokens()
        return self.email

    def load_item(self, message_id: str) -> str:
        if not self.email:
            raise ValueError("No inbox is active. Call create_email() first.")

        response = self.session.post(
            f"{self.BASE_URL}/message-list",
            headers=self.headers,
            json={"email": self.email, "messageID": message_id},
            timeout=30,
        )
        response.raise_for_status()
        self.update_tokens()
        return response.text

    def load_list(self) -> dict[str, Any]:
        if not self.email:
            raise ValueError("No inbox is active. Call create_email() first.")

        self.update_tokens()
        response = self.session.post(
            f"{self.BASE_URL}/message-list",
            headers=self.headers,
            json={"email": self.email},
            timeout=30,
        )
        response.raise_for_status()
        self.update_tokens()
        return response.json()

    def check_new_item(self, keyword: str) -> dict[str, str | None]:
        response_data = self.load_list()
        for message in response_data.get("messageData", []):
            if keyword.lower() in str(message.get("from", "")).lower():
                return {"messageId": message.get("messageID")}
        return {"messageId": None}
