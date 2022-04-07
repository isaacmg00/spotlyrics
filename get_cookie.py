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
                 sp_adid,
                 sp_m,
                 sp_t,
                 spot,
                 optanon_consent,
                 _ga_S35RN5WNT2,
                 _ga,
                 _scid,
                 _cs_c,
                 _cs_id,
                 _sctr,
                 _fbp,
                 _pin_unauth,
                 optanon_alert_box_closed,
                 _ga_ZWG1NSHWD8,
                 ki_t,
                 ki_r,
                 sp_dc,
                 sp_key,
                 sp_last_utm,
                 sp_phash,
                 sp_gaid,
                 _rdt_uuid,
                 _gcl_au,
                 sp_landing):
        pass

    def create_cookie_header(self):
        cookie = "'sp_adid=" + self.sp_adid + ";sp_m=" + \
            self.sp_m + ";sp_t=" + self.sp_t + ";spot=" + \
            self.spot + ";OptanonConsent=" + self.optanon_consent + \
            ";_ga_S35RN5WNT2=" + self._ga_S35RN5WNT2 + \
            ";_ga=" + self._ga + ";_scid=" + self._scid + \
            ";_cs_c=" + self._cs_c + ";_cs_id=" + self._cs_id + ";_sctr=" + \
            self._sctr + ";_fbp=" + self._fbp + ";_pin_unauth=" + self._pin_unauth + ";OptanonAlertBoxClosed=" + \
            self.optanon_alert_box_closed + ";_ga_ZWG1NSHWD8=" + \
            self._ga_ZWG1NSHWD8 + ";ki_t=" + self.ki_t + ";ki_r=" + self.ki_r + ";sp_dc=" + self.sp_dc + \
            ";sp_key=" + self.sp_key + ";sp_last_utm=" + \
            self.sp_last_utm + ";sp_phash=" + self.sp_phash + \
            ";sp_gaid=" + self.sp_gaid + ";_rdt_uuid=" + \
            self._rdt_uuid + ";_gcl_au=" + self._gcl_au + \
            ";sp_landing=" + self.sp_landing + "'"
        return cookie


cookies = list(browser_cookie3.firefox(domain_name=".spotify.com"))

auth_cookie = Cookie(sp_adid=None,
                     sp_m=None,
                     sp_t=None,
                     spot=None,
                     optanon_consent=None,
                     _ga_S35RN5WNT2=None,
                     _ga=None,
                     _scid=None,
                     _cs_c=None,
                     _cs_id=None,
                     _sctr=None,
                     _fbp=None,
                     _pin_unauth=None,
                     optanon_alert_box_closed=None,
                     _ga_ZWG1NSHWD8=None,
                     ki_t=None,
                     ki_r=None,
                     sp_dc=None,
                     sp_key=None,
                     sp_last_utm=None,
                     sp_phash=None,
                     sp_gaid=None,
                     _rdt_uuid=None,
                     _gcl_au=None,
                     sp_landing=None)

cookie_list = []
for cookie in cookies:
    cookie_list.append(cookie.name)
    cookie_list.append(cookie.value)

cookie_dict = Convert(cookie_list)

auth_cookie.sp_adid = cookie_dict["sp_adid"]
auth_cookie.sp_m = cookie_dict["sp_m"]
auth_cookie.sp_t = cookie_dict["sp_t"]
auth_cookie.spot = cookie_dict["spot"]
auth_cookie.optanon_consent = cookie_dict["OptanonConsent"]
auth_cookie._ga_S35RN5WNT2 = cookie_dict["_ga_S35RN5WNT2"]
auth_cookie._ga = cookie_dict["_ga"]
auth_cookie._scid = cookie_dict["_scid"]
auth_cookie._cs_c = cookie_dict["_cs_c"]
auth_cookie._cs_id = cookie_dict["_cs_id"]
auth_cookie._sctr = cookie_dict["_sctr"]
auth_cookie._fbp = cookie_dict["_fbp"]
auth_cookie._pin_unauth = cookie_dict["_pin_unauth"]
auth_cookie.optanon_alert_box_closed = cookie_dict["OptanonAlertBoxClosed"]
auth_cookie._ga_ZWG1NSHWD8 = cookie_dict["_ga_ZWG1NSHWD8"]
auth_cookie.ki_t = cookie_dict["ki_t"]
auth_cookie.ki_r = cookie_dict["ki_r"]
auth_cookie.sp_dc = cookie_dict["sp_dc"]
auth_cookie.sp_key = cookie_dict["sp_key"]
auth_cookie.sp_last_utm = cookie_dict["sp_last_utm"]
auth_cookie.sp_phash = cookie_dict["sp_phash"]
auth_cookie.sp_gaid = cookie_dict["sp_gaid"]
auth_cookie._rdt_uuid = cookie_dict["_rdt_uuid"]
auth_cookie._gcl_au = cookie_dict["_gcl_au"]
auth_cookie.sp_landing = cookie_dict["sp_landing"]

spotify_cookie = auth_cookie.create_cookie_header()

headers = {'Cookie': spotify_cookie}
response = requests.request("GET", url, headers=headers, data=payload)

print(response.json()["accessToken"])
