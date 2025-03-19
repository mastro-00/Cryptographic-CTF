# decrypt the flag! - Keystream Reuse Known Plaintext Attack

from Crypto.Cipher import AES
from pwn import *

server = remote("130.192.5.212", 6561)

def get_ciphertext(server, payload):
    server.recv(1024)
    server.sendline(b"y")
    server.recv(1024)
    server.sendline(payload)
    return bytes.fromhex(server.recvline().decode().strip())

server.recvuntil(b"> ")
seed = b'1'
server.sendline(seed)
server.recvline()
encrypted_flag = bytes.fromhex(server.recvline().strip().decode())
print(f"{encrypted_flag.hex()=}")

plaintext = b"a"*len(encrypted_flag)
print(f"{plaintext.hex()=}")
ciphertext = get_ciphertext(server, plaintext)
print(f"{ciphertext.hex()=}")

keystream = xor(plaintext, ciphertext)
decrypted_flag = xor(keystream, encrypted_flag)
print(decrypted_flag)