import json

import requests


class Email:
    def init_app(self, app):
        self.mailgun_key = app.config.get("MAILGUN_API_KEY")
        self.from_address = "Scan & Sew <no-reply@scansew.com>"
        self.mail_domain = app.config.get("MAILGUN_DOMAIN_NAME", "")
        self.domain = app.config.get("DOMAIN", "")
        self.debug = app.config.get("DEBUG")

    def send_confirmation_email(self, username, token, to):
        if self.debug:
            print(token)
            return
        return requests.post(
            f"https://api.mailgun.net/v3/{self.mail_domain}/messages",
            auth=("api", self.mailgun_key),
            data={
                "from": self.from_address,
                "to": f"{username} <{to}>",
                "subject": "Please confirm your email",
                "template": "confirmation",
                "t:variables": json.dumps(
                    {"token": f"{token}", "username": f"{username}"}
                ),
            },
        )

    def send_reset_email(self, username, token, to):
        if self.debug:
            print(token)
            return
        return requests.post(
            f"https://api.mailgun.net/v3/{self.mail_domain}/messages",
            auth=("api", self.mailgun_key),
            data={
                "from": self.from_address,
                "to": f"{username} <{to}>",
                "subject": "Password reset request",
                "template": "reset",
                "t:variables": json.dumps(
                    {"token": f"{token}", "username": f"{username}"}
                ),
            },
        )

    def send_join_company(self, name, token, to, company_name):
        if self.debug:
            print(token)
            return
        return requests.post(
            f"https://api.mailgun.net/v3/{self.mail_domain}/messages",
            auth=("api", self.mailgun_key),
            data={
                "from": self.from_address,
                "to": f"{name} <{to}>",
                "subject": f"Invitation to {company_name}",
                "template": "join_company",
                "t:variables": json.dumps(
                    {
                        "token": f"{token}",
                        "name": f"{name}",
                        "company_name": f"{company_name}",
                        "domain": f"{self.domain}",
                    }
                ),
            },
        )

    def send_contact_email(self, email, username, message):
        if self.debug:
            print(email, username, message)
            return
        return requests.post(
            f"https://api.mailgun.net/v3/{self.mail_domain}/messages",
            auth=("api", self.mailgun_key),
            data={
                "from": f"Mailgun Sandbox <postmaster@{self.mail_domain}>",
                "to": self.admins,
                "subject": "Portal Issue",
                "template": "contact email",
                "t:variables": json.dumps(
                    {
                        "email": f"{email}",
                        "username": f"{username}",
                        "message": f"{message}",
                    }
                ),
            },
        )

    def add_list_member(self, email):
        if self.debug:
            print("added", email, "to mail list")
            return
        return requests.post(
            f"https://api.mailgun.net/v3/lists/mail@{self.mail_domain}/members",
            auth=("api", self.mailgun_key),
            data={"subscribed": True, "address": f"{email}"},
        )

    def send_sign_up_email(self, name, token, to):
        if self.debug:
            print(token)
            return
        return requests.post(
            f"https://api.mailgun.net/v3/{self.mail_domain}/messages",
            auth=("api", self.mailgun_key),
            data={
                "from": self.from_address,
                "to": f"{name} <{to}>",
                "subject": "Invitation to Scan & Sew",
                "template": "invitation",
                "t:variables": json.dumps({"token": f"{token}", "name": f"{name}"}),
            },
        )
