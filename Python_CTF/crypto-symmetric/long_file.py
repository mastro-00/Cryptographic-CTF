# long file - Keystream Reuse

from numpy import zeros
from string import printable
from pwn import xor

KEYSTREAM_SIZE = 1000
CHARACTER_FREQ = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
} # from CryptoPals S3C19/S3C20

with open("./file.enc", "rb") as f:
    cipherTexts = []
    while block := f.read(KEYSTREAM_SIZE):
        cipherTexts.append(block)
        
print(f"N. ciphertexts: {len(cipherTexts)}")

max_len = len(max(cipherTexts, key=len))
print(f"Longest: {max_len}")

candidates_list = []

for byte_to_guess in range(max_len):
    char_frequency = zeros(256, dtype=float)
    for guessed_byte in range(256):
        for ciphertext in cipherTexts:
            if byte_to_guess >= len(ciphertext):
                continue
            decoded_char = chr(ciphertext[byte_to_guess] ^ guessed_byte)
            if decoded_char in printable:
                char_frequency[guessed_byte] += CHARACTER_FREQ.get(decoded_char.lower(),0)
    max_matches = max(char_frequency)
    match_list = [(char_frequency[i], i) for i in range(256)]
    ordered_match_list = sorted(match_list, reverse=True)
    candidates_list.append(ordered_match_list)
    
keystream = bytearray()
for candidates in candidates_list:
    keystream.append(candidates[0][1])

with open("long_file_output.txt", "w") as file:
    for ciphertext in cipherTexts:
        length = min(len(keystream),len(ciphertext))
        print(xor(ciphertext[:length],keystream[:length]).strip())
        file.write(str(xor(ciphertext[:length],keystream[:length]).strip()))

# CRYPTO24{6e7e9806-0162-4051-91b3-ef1b2e0e3dcd}