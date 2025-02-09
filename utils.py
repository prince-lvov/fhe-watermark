import random
import string
import hashlib
import numpy as np


def generate_random_text(length):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def get_letter_bits(letter):
    ascii_code = ord(letter)
    return [
        int(_) for _ in bin(ascii_code)[2:].zfill(8)
    ]

def get_watermark_text_bits(watermark_text):
    watermark_text_hash = hashlib.sha256(watermark_text.encode("utf-8")).hexdigest()[:16]
    return [
        _
        for letter in watermark_text_hash
        for _ in get_letter_bits(letter)
    ]

def create_inputset_for_circuit(img_size):
    inputset_for_compiler = []

    for _ in range(10):
        random_img_array = np.random.randint(-2000, 2000, size=img_size, dtype=np.int16)
        random_message_array = np.random.randint(0, 2, size=img_size, dtype=np.int16)
        inputset_for_compiler.append((random_img_array, random_message_array))
    return inputset_for_compiler

def create_zero_diagonal_mask(img_size):
    mask = np.ones(img_size, dtype=np.int16)
    block_size = 8

    block_index = 0
    for row in range(img_size[0] // block_size):
        block_h_index = row * block_size
        for col in range(img_size[1] // block_size):
            block_w_index = col * block_size

            for index in range(block_size):
                mask[block_h_index + (block_size - 1 - index), block_w_index + index] = 0

            block_index += 1
    return mask


def create_watermark_mask(
    watermark_text, img_size, block_size=8, revert=False
):
    blocks_total = (img_size[0] * img_size[1]) // (
        block_size * block_size
    )
    
    if len(watermark_text) * 8 > blocks_total:
        raise ValueError("Watermark text is too long")

    mask = np.zeros(img_size, dtype=np.int16)

    watermark_bites = get_watermark_text_bits(watermark_text)
    watermark_bites_length = len(watermark_bites)

    block_index = 0
    for row in range(img_size[0] // block_size):
        block_h_index = row * block_size
        for col in range(img_size[1] // block_size):
            bit = watermark_bites[block_index % watermark_bites_length]
            if revert:
                bit = bit ^ 1
            block_w_index = col * block_size

            for index in range(block_size):
                mask[block_h_index + (block_size - 1 - index), block_w_index + index] = bit

            block_index += 1
    return mask


def create_verification_mask(watermark_text, img_size, block_size=8):
    return create_watermark_mask(watermark_text, img_size, block_size, revert=True)


def print_block(array, bh_index, bw_index, block_size, channel=1):
    for i in range(block_size):
        row_index = bh_index * block_size + i
        col_index = bw_index * block_size
        print(array[row_index, col_index: col_index + block_size, channel])