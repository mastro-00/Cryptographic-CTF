# guess-mode double-shot 

from pwn import *

server = remote("130.192.5.212", 6532)

for i in range(128):
    print(f"Challenge #{i}")
    server.recvuntil(b"Input: ")
    
    input = bytes(32)
    print(f"Input: {input.hex().encode()}")
    
    server.sendline(input.hex().encode())
    output1 = server.recvuntil(b"Input: ").decode().split(": ")[1].split("\n")[0]
    print(f"Output1: {output1}")
    
    server.sendline(input.hex().encode())
    output2 = server.recvline(b"CBC)").decode().split(": ")[1].strip()
    print(f"Output2: {output2}")
    
    print(server.recv(1024).decode())
    if(output1 == output2):
        server.sendline(b"ECB")
        print("ECB")
    else:
        server.sendline(b"CBC")
        print("CBC")

print(server.recv(1024).decode())