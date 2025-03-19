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
padding_len = 5
flag = "CRYPTO24{????????????????????????????????????}"

server = remote("130.192.5.212", 6542)

guessed = b""

for i in range(flag_len):
    data0 = b"A" * (block_len-padding_len)
    if(i < block_len):
        data1 = b"A" * (block_len-1-i)
    else:
        data1 = guessed[-(block_len-1):]
    data2 = b"A" * (data_len-1-i)

    for char in string.printable:
        if(i < block_len):
            data = data0 + data1 + guessed + char.encode() + data2
        else:
            data = data0 + data1 + char.encode() + data2
        print(f"{i=}")
        print(data)
        all_data=data+flag.encode()
        print(f"{all_data[16-5:32-5]} - {all_data[data_len+16-5:data_len+32-5]}")
        
        ciphertext = get_ciphertext(server, data)
        print(f"{guessed=}")
        if ciphertext[16:32] == ciphertext[data_len+16:data_len+32]:
            guessed += char.encode()
            print()
            break
        
print(guessed)
server.close()