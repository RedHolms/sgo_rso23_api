from requests import Session as _requests_Session
from hashlib import md5 as _hash_md5

from .exceptions import *

API_ORIGIN = "https://sgo.rso23.ru/webapi/"

def _md5(data, _hard_encode = True):
  return _hash_md5(data.encode() if type(data) == str and _hard_encode else data)

def _hide_password(password, salt) -> tuple[str, str]:
  pw, pw2 = '', ''

  pwd_hash = _md5(password)
  pwd_hash_salted = salt + pwd_hash.hexdigest()
  pw2 = _md5(pwd_hash_salted).hexdigest()

  pw = pw2[:len(password)]

  return (pw, pw2)

class Session:
  __requests_session: _requests_Session
  __at: str

  def __init__(self) -> None:
    self.__requests_session = _requests_Session()

  def call_method(self, name: str, method: str = "GET", **kwargs):
    response = self.__requests_session.request(method, API_ORIGIN + name, **kwargs)

    if response.status_code not in range(200, 299):
      raise ApiError(response)

    return response.json()

  def auth(self, username: str, password: str):
    # headers only for logining to make website feel
    #  like we are normal user
    loginHeaders = {
      "Referer": "https://sgo.rso23.ru/?AL=Y",
      "Origin": "https://sgo.rso23.ru/"
    }

    # get data for auth
    authData = self.call_method("auth/getdata", method="POST", headers=loginHeaders)
    
    # generate hashed version of password
    pw, pw2 = _hide_password(password, str(authData["salt"]))

    # some numbers that defined city, school and etc.
    loginData = {
      "LoginType": '1',
      "cid": '2',
      "sid": '23',
      "pid": '9',
      "cn": '616',
      "sft": '2',
      "scid": '1716',
      "lt": authData["lt"],
      "pw2": pw2,
      "UN": username,
      "PW": pw,
      "ver": authData["ver"]
    }

    response = self.call_method("login", "POST", data=loginData, headers=loginHeaders)
    # todo: gare tokents or something similar 