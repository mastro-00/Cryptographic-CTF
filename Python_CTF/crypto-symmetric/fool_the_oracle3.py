# Fool the Oracle v2 - Adaptive Chosen Plaintext Attack

from Crypto.Cipher import AES
from pwn import *
from math import ceil

def get_ciphertext(server, payload):
    server.recvuntil(b"> ")
    server.sendline("enc".encode())
    server.recv(1024)
    server.sendline(payload.hex().encode())
    ciph = server.recvline().decode().strip()
    return bytes.fromhex(ciph)

block_len = AES.block_size
flag_len = len("CRYPTO24{}") + 36
data_len = math.ceil(flag_len/block_len)*block_len

server = remote("130.192.5.212", 6543)

for pad in range(1, 16):
    padding_len = pad
    guessed = b""
    
    for i in range(flag_len):
        data0 = b"A" * (block_len-padding_len)
        if(i < block_len):
            data1 = b"A" * (block_len-1-i)
        else:
            data1 = guessed[-(block_len-1):]
        data2 = b"A" * (data_len-1-i)
        found = False
        
        for char in string.printable:
            if(i < block_len):
                data = data0 + data1 + guessed + char.encode() + data2
            else:
                data = data0 + data1 + char.encode() + data2
            print(f"{i=} - {pad=}")
            print(data)
            ciphertext = get_ciphertext(server, data)
            print(f"{guessed=}")
            if ciphertext[16:32] == ciphertext[data_len+16:data_len+32]:
                guessed += char.encode()
                print()
                found = True
                break
        if not found:
            break
        
    if len(guessed) == flag_len:
        break
        
print(guessed)
server.close()