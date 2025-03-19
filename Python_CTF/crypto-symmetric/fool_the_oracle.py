# Fool the Oracle - Adaptive Chosen Plaintext Attack

from Crypto.Cipher import AES
from pwn import *
from Crypto.Util.Padding import pad
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
flag = "CRYPTO24{????????????????????????????????????}"

server = remote("130.192.5.212", 6541)

guessed = b""

for i in range(flag_len):
    if(i < block_len):
        data1 = b"A" * (block_len-1-i)
    else:
        data1 = guessed[-(block_len-1):]
    data2 = b"A" * (data_len-1-i)

    for char in string.printable:
        print(f"{i=}")
        if(i < block_len):
            data = data1 + guessed + char.encode() + data2
            print(f"{data1=} - {guessed=} - {char.encode()=} - {data2=}")
        else:
            data = data1 + char.encode() + data2
            print(f"{data1=} - {char.encode()=} - {data2=}")
        print(f"data len: {len(data)}")
        all_data=pad(data+flag.encode(), block_len)
        
        print(f"0:16 {all_data[0:16]} - {data_len}:{data_len+16} {all_data[data_len:data_len+16]}")
        print(f"{guessed=}")
        
        ciphertext = get_ciphertext(server, data)
        if ciphertext[0:16] == ciphertext[data_len:data_len+16]:
            guessed += char.encode()
            print()
            break
    
    for i in range(0, int(len(all_data)/block_len)):
        print(f"{i*block_len}:{(i+1)*block_len} - {all_data[i*block_len:(i+1)*block_len]}")
print(guessed)
server.close()