from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json, base64

server = remote("130.192.5.212", 6551)

username = b'A"'
username += b'               '
username += b': true,         '
username += b'AAAAAA'

#START SIMULATION
token = json.dumps({
        "username": username.decode(),
        "admin": False
    })
print(token.encode())
padded_token = pad(token.strip().encode(),AES.block_size)
for i in range(0, len(padded_token) // 16):
    print(f'{i*16}:{i*16+16} - {padded_token[i*16:i*16+16]}')
print()

final_cookie = padded_token[:2*AES.block_size]                  # first 2 blocks
final_cookie += padded_token[3*AES.block_size:4*AES.block_size] # 4th block
final_cookie += padded_token[2*AES.block_size:3*AES.block_size] # 3th block
final_cookie += padded_token[1*AES.block_size:2*AES.block_size] # 2nd block
final_cookie += padded_token[1*AES.block_size:2*AES.block_size] # 2nd block
final_cookie += padded_token[4*AES.block_size:5*AES.block_size] # 5th block

for i in range(0, len(final_cookie) // 16):
    print(f'{i*16}:{i*16+16} - {final_cookie[i*16:i*16+16]}')
user = json.loads(unpad(final_cookie, AES.block_size))
print(user)
print(user.get("admin", False))
#END

server.sendline(username)
server.recvuntil(b'This is your token: ')
cookie = base64.b64decode(server.recvline().strip().decode())

forged_cookie = cookie[:2*AES.block_size]                  # first 2 blocks
forged_cookie += cookie[3*AES.block_size:4*AES.block_size] # 4th block
forged_cookie += cookie[2*AES.block_size:3*AES.block_size] # 3rd block
forged_cookie += cookie[1*AES.block_size:2*AES.block_size] # 2nd block
forged_cookie += cookie[1*AES.block_size:2*AES.block_size] # 2nd block
forged_cookie += cookie[4*AES.block_size:5*AES.block_size] # 5th block
# {'username': 'A"               AAAAAA', 'admin': True, '               ': False}
forged_cookie = base64.b64encode(forged_cookie)

server.sendlineafter(b'> ', b'flag')
server.sendlineafter(b'> ', forged_cookie)
server.recvuntil(b'This is your flag!\n')
print(server.recvline().strip().decode())
server.close()