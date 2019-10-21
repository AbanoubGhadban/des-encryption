from des_utils import *
from data_utils import joinNumbers

def encrypt(msg:str, key:str):
    keys = generateKeys(key)

    text_bits = get_bits(msg)
    text_bits = add_pads_if_necessary(text_bits)

    final_cipher = []
    for i in range(0, len(text_bits), 64):
        final_cipher.extend(encryptBlock(text_bits[i:i+64], keys))

	# conversion of binary cipher into hex-decimal form
    hex_cipher = ''
    for i in range(0, len(final_cipher), 4):
        hex_cipher += bin_to_hex(joinNumbers(final_cipher[i:i+4]))
    return hex_cipher

def decrypt(cipher:str, key:str) -> str:
    keys = generateKeys(key)
    keys.reverse()
    text_bits = get_bits(cipher)

    msg = []
    for i in range(0, len(text_bits), 64):
        msg.extend(encryptBlock(text_bits[i:i+64], keys))

	# conversion of binary text into hex-decimal form
    hex_msg = ''
    for i in range(0, len(msg), 4):
        hex_msg += bin_to_hex(joinNumbers(msg[i:i+4]))
    return hex_msg.rstrip('\x00')
