from data_utils import *
from des_constants import *

def generateKeys(key:str) -> list:
    key_bin = []
    for c in key:
        key_bin.extend(hex_to_bin(c))
    key_l = []
    key_r = []
    for i in range(28):
        key_l.append(key_bin[PC1_L[i]])
        key_r.append(key_bin[PC1_R[i]])

    keys = []
    for i in range(16):
        if i in [0, 1, 8, 15]:
            key_l = left_shift(key_l, 1)
            key_r = left_shift(key_r, 1)
        else:
            key_l = left_shift(key_l, 2)
            key_r = left_shift(key_r, 2)

        finalKey = []
        for j in range(24):
            finalKey.append(key_l[PC2_L[j]])
        for j in range(24):
            finalKey.append(key_r[PC2_R[j]])
        keys.append(finalKey)
    return keys

def initialPermutation(block:list) -> list:
    assert len(block) == 64, "Block size must be 64 bit"
    permutedBlock = []
    for i in range(64):
        permutedBlock.append(block[IP[i]])
    return permutedBlock

def expandRight(block_r:list) -> list:
    expandedBlock = []
    for i in range(48):
        expandedBlock.append(block_r[R_EXPANSION[i]])
    return expandedBlock

def applySBox(block_r:list) -> list:
    k = 0
    newBlock = []
    for i in range(0, 48, 6):
        sBlock = block_r[i:i+6]
        a = 16*get_row(str(sBlock[0]) + str(sBlock[-1]))
        a += get_column(str(sBlock[1]) + str(sBlock[2]) + str(sBlock[3]) + str(sBlock[4]))
        newBlock.extend(to_binary(s_boxes[k][a])[4:8])
        k += 1
    return newBlock

def permuteRight(block_r:list) -> list:
    return [block_r[R_P[i]] for i in range(32)]    

def encryptBlock(block:list, keys:list) -> list:
    assert len(keys) == 16, "16 keys needed"
    block = initialPermutation(block)

    for r in range(16):
        block_l = block[0:32]
        orig_block_r = block[32:64]
        block_r = expandRight(orig_block_r)
        block_r = xor_lists(block_r, keys[r])
        block_r = applySBox(block_r)
        block_r = permuteRight(block_r)

        for i in range(32):
            block[i] = orig_block_r[i]
        for i in range(32):
            block[i+32] = block_l[i]^block_r[i]

    f_block = []
    f_block.extend(block[32:64])
    f_block.extend(block[0:32])
    fb_block = []
    for i in range(64):
        fb_block.append(f_block[FINAL_P[i]])
    return fb_block
