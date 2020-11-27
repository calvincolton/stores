from flask import request, url_for
from requests import Response, post
from db import db
from libs.mailgun import Mailgun


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_email(self) -> Response:
        # http://127.0.0.1:5000/user_confirm/1
        link = request.url_root[0:-1] + url_for("userconfirm", user_id=self.id)
        subject = "Registration Confirmation"
        text = f"Please click the link to confirm your registration: {link}"
        html = f'<html>Please click the link to confirm your registration: <a href="{link}">{link}</a></html>'

        return Mailgun.send_email([self.email], subject, text, html)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


# API key: 0a35aa065f5de2be84ea8ac70c3f6ea2-360a0b2c-6a0f55b0
# API base URL: https://api.mailgun.net/v3/sandbox436e3a5721bf44659a923182ce11cd54.mailgun.org
# def send_simple_message():
# 	return requests.post(
# 		"https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
# 		auth=("api", "YOUR_API_KEY"),
# 		data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
# 			"to": ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"],
# 			"subject": "Hello",
# 			"text": "Testing some Mailgun awesomness!"})