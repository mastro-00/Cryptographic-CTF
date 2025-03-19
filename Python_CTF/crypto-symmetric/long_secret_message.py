#  long secret message - Keystream Reuse

from numpy import zeros
from string import printable
from pwn import xor

CHARACTER_FREQ = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
} # from CryptoPals S3C19/S3C20

with open("./hacker-manifesto.enc") as f:
    cipherTexts = []
    for line in f.readlines():
        cipherTexts.append(bytes.fromhex(line.strip()))

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

def char_correction(column, row, char):
    keystream[row] = cipherTexts[column][row] ^ ord(char)
    
char_correction(0, 0, 'T')
char_correction(0, 1, 'h')
char_correction(0, 2, 'i')
char_correction(0, 3, 's')
char_correction(0, 5, 'i')
char_correction(0, 28, 'o')
char_correction(0, 38, 'e')
char_correction(5, 40, 'a')
char_correction(5, 42, 's')
char_correction(5, 43, ' ')
char_correction(3, 17, ' ')
char_correction(3, 20, 'l')
char_correction(1, 43, 'e')
char_correction(3, 53, 'd')
char_correction(4, 45, 'u')
char_correction(4, 46, 't')
char_correction(4, 49, 'a')
char_correction(4, 58, 'y')
char_correction(4, 59, ',')
char_correction(4, 65, 'o')
char_correction(4, 67, 't')
char_correction(6, 69, 's')

# This is our world now... the world of the electron and the switch, the
# beauty of the baud.  We make use of a service already existing without paying
# for what could be dirt-cheap if it wasn't run by profiteering gluttons, and
# you call us criminals.  We explore... and you call us criminals.  We seek
# after knowledge... and you call us criminals.  We exist without skin color,
# without nationality, without religious bias... and you call us criminals.
# You build atomic bombs, you wage wars, you murder, cheat, and lie to us
# and try to make us believe it's for our own good, yet we're the criminals.

for ciphertext in cipherTexts:
    length = min(len(keystream),len(ciphertext))
    print(xor(ciphertext[:length],keystream[:length]).strip())
    
# CRYPTO24{71bef20b-6f03-47a1-92de-12ef382d5c16}