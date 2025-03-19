#  Back to the future - KeyStream BitFlipping

import requests
import json
from Crypto.Util.number import long_to_bytes, bytes_to_long
import time
from pwn import xor

session = requests.Session()
username = "f"
admin = 1

req_time = int(time.time())
expire_date = req_time + 30 * 24 * 60 * 60
plain_expires = str(expire_date).encode()

res_json = json.loads(session.get(f"http://130.192.5.212:6522/login?username={username}&admin={admin}").content.decode())
nonce = int(res_json["nonce"])
cookie = long_to_bytes(int(res_json["cookie"]))
# cookie = "username=f&expires=expire_date&admin=1"

cipher_expires = cookie[19:29] # expire_date -> 10 characters long

for rand_day in range((290 - 266), (300 - 10)): # int(time.time()) - randint(10, 266)
    wanted_expires = str(req_time + rand_day * 24 * 60 * 60).encode()
    print(f"i: {rand_day}")
    print(f"plain: {time.ctime(int(plain_expires))} - cipher: {cipher_expires} - wanted: {time.ctime(int(wanted_expires))}")
    print(f"xor: {xor(plain_expires, cipher_expires, wanted_expires)}")
    new_cookie = cookie[:19] + xor(plain_expires, cipher_expires, wanted_expires) + cookie[29:]
    new_cookie = bytes_to_long(new_cookie)

    res = session.get(
        f"http://130.192.5.212:6522/flag?nonce={nonce}&cookie={new_cookie}")
    if (res.content != b"You have expired!"):
        print(res.content)
        break