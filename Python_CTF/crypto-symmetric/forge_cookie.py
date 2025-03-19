# forge a cookie
# Key Stream Reuse Attack
# https://www.youtube.com/watch?v=Gtfr1dBGzHg

from pwn import *
import base64

server = remote("130.192.5.212", 6521)

server.recvline()
text = b"flavio00flavio00"

server.sendline(text)

read = server.recvuntil(b"the flag").decode()

token_plaintext = read.split("\n")[0].split("> ")[1]
print(f"Plaintext: {token_plaintext}")

# nonce = base64.b64decode(read.split(".")[0])
nonce = read.split("\n")[1].split(": ")[1].split(".")[0]
print(f"Nonce: {nonce}")
token_ciphertext = base64.b64decode(read.split("\n")[1].split(": ")[1].split(".")[1])
print(f"Hex Token: {token_ciphertext.hex()}")

# token_plaintext =   b'{"username": "flavio00flavio00"}'
new_token_plaintext = b'{"username": "f", "admin": true}'

new_token_ciphertext = xor(new_token_plaintext, xor(bytes(token_plaintext, "utf-8"), token_ciphertext))
print(f"New Hex Token: {new_token_ciphertext.hex()}")

flag = b"flag"
server.sendline(flag)

server.recvuntil(b"?").decode()

response = f"{nonce}.{base64.b64encode(new_token_ciphertext).decode()}"
print(f"New Nonce+Token: {response}")
server.sendline(response.encode())
print(server.recvuntil(b"}").decode().split("> ")[1])
