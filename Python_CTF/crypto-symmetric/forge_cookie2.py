# forge another cookie 
# ECB: copy&paste

from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

server = remote("130.192.5.212", 6552)

pad1 = b"a" * (AES.block_size - len(b"username="))
pad2 = pad(b"true", AES.block_size)
pad3 = b"a" * (AES.block_size - len(b"&admin="))
username = pad1 + pad2 + pad3

print(f'Bait: {username}')
server.sendline(username)
cookie = f"username={username.decode()}&admin=false"
padded_cookie = pad(cookie.encode(), AES.block_size)
for i in range(0, len(padded_cookie) // 16):
    print(f'{i*16}:{i*16+16} - {padded_cookie[i*16:i*16+16]}')
# 00:16 - username=aaaaaaa
# 16:32 - true\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c
# 32:48 - aaaaaaaaa&admin=
# 48:64 - false\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b

long_cookie = server.recvline().strip().decode().split(" ")[1]
server.recv(1024).decode()
server.sendline(b"flag")
server.recvuntil(b"Cookie: ")

bytes_cookie = long_to_bytes(int(long_cookie))
bytes_new_cookie = bytes_cookie[:48] + bytes_cookie[16:32]
# 00:16 - username=aaaaaaa
# 16:32 - true\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c
# 32:48 - aaaaaaaaa&admin=
# 16:32 - true\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c

#print(f"Long Cookie (len: {len(long_cookie)}): {long_cookie}")
#print(f"Bytes Cookie (len: {len(bytes_cookie)}): {bytes_cookie}")
#print(f"Bytes New Cookie (len: {len(bytes_new_cookie)}): {bytes_new_cookie}")

server.sendline(str(bytes_to_long(bytes_new_cookie)).encode())
print(server.recvline().decode())
server.close()