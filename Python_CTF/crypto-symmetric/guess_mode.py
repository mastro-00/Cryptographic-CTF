# guess mode one-shot

from pwn import *

server = remote("130.192.5.212", 6531)

for i in range(128):
    otp = server.recvuntil(b"Input: ").decode().split("\n")[-2].split(": ")[1]
    print("Otp: " + otp)
    
    server.sendline(bytes(otp, "utf-8"))

    output = server.recvuntil(b")\n").decode().split("\n")[0].split(": ")[1]
    print("Output: " + output)
    
    print(output[0:32])
    print(output[32:64])
    
    if(output[0:32] == output[32:64]):
        server.sendline(b"ECB")
        print("ECB")
    else:
        server.sendline(b"CBC")
        print("CBC")

print(server.recvline())
print(server.recvline())