import browser_cookie3
import requests

url = "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
payload = {}


def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct


class Cookie:
    def __init__(self,
                 sp_t,
                 sp_dc
                 ):
        pass

    def create_cookie_header(self):
        cookie = "sp_t=" + self.sp_t + ";sp_dc=" + self.sp_dc
        return cookie


cookies = list(browser_cookie3.firefox(domain_name=".spotify.com"))

auth_cookie = Cookie(
    sp_t=None,
    sp_dc=None
)

cookie_list = []
for cookie in cookies:
    cookie_list.append(cookie.name)
    cookie_list.append(cookie.value)


cookie_dict = Convert(cookie_list)
auth_cookie.sp_t = cookie_dict["sp_t"]
auth_cookie.sp_dc = cookie_dict["sp_dc"]

spotify_cookie = auth_cookie.create_cookie_header()

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0", 'Cookie': spotify_cookie}
response = requests.request("GET", url, headers=headers, data=payload)

print(response.json()["accessToken"])
