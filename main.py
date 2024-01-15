import re

from bs4 import BeautifulSoup
import js2py
import requests
requests.packages.urllib3.disable_warnings()

_, cryptojs = js2py.run_file("crypto.js")

class MitraStarRouterAPI:
    base_url = "http://192.168.1.1"

    def __init__(self):
        self.session = requests.Session()
        self.session.proxies = {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080"
        }
        self.sid = self._get_sid()

    def _get_sid(self):
        html = self.session.get(self.base_url).text
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find_all('script')[-1].text
        m = re.search("\svar sid = '(\w*)';", script)
        return m.group(1)

    def hash_password(self, password):
        return cryptojs.hex_md5(f"{password}:{self.sid}")

    def login(self, password):
        payload = {
            "sessionKey": "",
            "submitValue": 1,
            "fake_syspasswd": "",
            "syspasswd_1": "",
            "syspasswd": self.hash_password(password),
            "leaveBlur": 0,
            "Submit": "Entrar"
        }
        response = self.session.post(self.base_url, data=payload)
        print(response.cookies)

    def logout(self):
        response = self.session.get(f"{self.base_url}/cgi-bin/Logout.cgi")
        print(response.cookies)

api = MitraStarRouterAPI()
print(api.hash_password("test"))
#api.login("test")
#api.logout()
