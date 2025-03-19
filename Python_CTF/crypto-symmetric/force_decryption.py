# force decryption - Bit-Flipping Attack

from pwn import *

leak = b"mynamesuperadmin"

server = remote("130.192.5.212", 6523)
server.recv(1024).decode()

# enc
server.send(b"enc\n")
server.recv(1024).decode()

plaintext = bytes(16)
server.sendline(plaintext.hex().encode())

iv = bytes.fromhex(server.recvline().decode().strip().split(": ")[1])
ciphertext = bytes.fromhex(server.recvline().decode().strip().split(": ")[1])
print(f"Plaintext: {plaintext.hex()} - IV: {iv.hex()} - Ciphertext: {ciphertext.hex()}")

server.recvuntil(b"> ").decode()

#dec
server.send(b"dec\n")
server.recv(1024).decode()

mask = xor(iv, leak)
print(f"Mask: {mask.hex()}")

server.sendline(ciphertext.hex().encode())
server.recvuntil(b"> ").decode()
server.sendline(mask.hex().encode())
print(server.recvuntil(b"}").decode())