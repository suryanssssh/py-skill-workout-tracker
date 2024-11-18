import json
import requests

class Database:
    def __init__(self, url, auth):
        self.url = url
        self.auth = auth

    def signup(self, email, password, username):
        signup_info = str(
            {f'\"{email}\":{{"Password":\"{password}\","Username":\"{username}\"}}'}
        )
        signup_info = signup_info.replace(".", "-")
        signup_info = signup_info.replace("\'", "")
        to_database = json.loads(signup_info)
        requests.patch(url=self.url, json=to_database)

    def login(self, email, password):
        response = requests.get(f"{self.url}?auth={self.auth}")
        data = response.json()
        if email.replace(".", "-") in data and data[email.replace(".", "-")]["Password"] == password:
            return data[email.replace(".", "-")]["Username"]
        return None
