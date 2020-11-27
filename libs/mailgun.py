from typing import List
from requests import Response, post


class Mailgun:
    MAILGUN_DOMAIN = "sandbox436e3a5721bf44659a923182ce11cd54.mailgun.org"
    MAILGUN_API_KEY = "0a35aa065f5de2be84ea8ac70c3f6ea2-360a0b2c-6a0f55b0"
    FROM_TITLE = "Stores REST API"
    FROM_EMAIL = "calvincolton@hotmail.com"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        # http://127.0.0.1:5000/user_confirm/1
        # link = request.url_root[0:-1] + url_for("userconfirm", user_id=self.id)
        return post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )
