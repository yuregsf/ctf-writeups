#!/usr/bin/env python
import time
import random

#### Crypto stuff not important
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[: AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size :])).decode("utf-8")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]


def slow_print(msg):
    print(msg, end="", flush=True)
    print()

class PathGroup:
    tiles = []
    current_cordinates = None
    path_history = []

    def __repr__(self):
        return "[X] {} -- {} \n".format(self.tiles, self.path_history)


grid = [
    [
        "SPHINX",
        "urn",
        "vulture",
        "arch",
        "snake",
        "urn",
        "bug",
        "plant",
        "arch",
        "staff",
        "SPHINX",
    ],
    [
        "plant",
        "foot",
        "bug",
        "plant",
        "vulture",
        "foot",
        "staff",
        "vulture",
        "plant",
        "foot",
        "bug",
    ],
    [
        "arch",
        "staff",
        "urn",
        "Shrine",
        "Shrine",
        "Shrine",
        "plant",
        "bug",
        "staff",
        "urn",
        "arch",
    ],
    [
        "snake",
        "vulture",
        "foot",
        "Shrine",
        "Shrine",
        "Shrine",
        "urn",
        "snake",
        "vulture",
        "foot",
        "vulture",
    ],
    [
        "staff",
        "urn",
        "bug",
        "Shrine",
        "Shrine",
        "Shrine",
        "foot",
        "staff",
        "bug",
        "snake",
        "staff",
    ],
    [
        "snake",
        "plant",
        "bug",
        "urn",
        "foot",
        "vulture",
        "bug",
        "urn",
        "arch",
        "foot",
        "urn",
    ],
    [
        "SPHINX",
        "arch",
        "staff",
        "plant",
        "snake",
        "staff",
        "bug",
        "plant",
        "vulture",
        "snake",
        "SPHINX",
    ],
]


def try_get_tile(tile_tuple):
    try:
        return grid[tile_tuple[0]][tile_tuple[1]], (tile_tuple[0], tile_tuple[1])
    except Exception as e:
        return None


# This is you at (3,10)!
starting_tile = (3, 10)
starting_path = PathGroup()
starting_path.tiles = ["vulture"]
starting_path.current_cordinates = starting_tile
starting_path.path_history = [starting_tile]

def can_move(tile):



def move(path, tile):
    sub_path = PathGroup()
    sub_path.tiles.append(tile)
    sub_path.current_cordinates = tile
    sub_path.path_history = path.path_history.copy()
    sub_path.path_history.append(tile)
    return sub_path


cur_tile = starting_tile


def check_path(path):
    if try_get_tile(path.current_cordinates)[0] == "Shrine":
        print("SHRINE")
        print([try_get_tile(x)[0] for x in path.path_history])
        key = "".join([try_get_tile(x)[0] for x in path.path_history])
        enc_flag = b"FFxxg1OK5sykNlpDI+YF2cqF/tDem3LuWEZRR1bKmfVwzHsOkm+0O4wDxaM8MGFxUsiR7QOv/p904UiSBgyVkhD126VNlNqc8zNjSxgoOgs="
        obj = AESCipher(key)
        dec_flag = obj.decrypt(enc_flag)
        if "pctf" in dec_flag:
            slow_print(
                bcolors.OKBLUE
                + "You've done it! All the traps depress and a rigid 'click' can be heard as the center chest opens! As you push open the top your prize sits inside!"
                + bcolors.ENDC
            )
            print(bcolors.OKCYAN + dec_flag + bcolors.ENDC)
            exit(0)
        else:
            slow_print(
                "You step onto the center area expecting your prize, but a loud whirling sound is heard instead. The floor plates make a large mechanical click sounds and engage the fire trap once again!"
            )
            how_did_you_succumb_to_a_trap()
            exit(-1)


cur_path = starting_path
while True:
    n_path = menu(cur_path)
    print(n_path)
    check_path(n_path)
    cur_path = n_path
