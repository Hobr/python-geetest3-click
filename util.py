import json
import math
import random
from binascii import hexlify

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from loguru import logger


class Enc:
    def _JGH(self, e) -> str:
        t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()"
        return "." if e < 0 or e >= len(t) else t[e]

    def _JIY(self, e, t) -> int:
        return (e >> t) & 1

    def _JJM(self, e) -> dict:
        def t(e, t):
            n = 0
            for r in range(24 - 1, -1, -1):
                if self._JIY(t, r) == 1:
                    n = (n << 1) + self._JIY(e, r)
            return n

        n = ""
        r = ""
        a = len(e)
        s = 0
        while s < a:
            if s + 2 < a:
                c = (e[s] << 16) + (e[s + 1] << 8) + e[s + 2]
                n += (
                    self._JGH(t(c, 7274496))
                    + self._JGH(t(c, 9483264))
                    + self._JGH(t(c, 19220))
                    + self._JGH(t(c, 235))
                )
            else:
                u = a % 3
                if u == 2:
                    c = (e[s] << 16) + (e[s + 1] << 8)
                    n += self._JGH(t(c, 7274496)) + self._JGH(t(c, 9483264)) + self._JGH(t(c, 19220))
                    r = "."
                elif u == 1:
                    c = e[s] << 16
                    n += self._JGH(t(c, 7274496)) + self._JGH(t(c, 9483264))
                    r = ".."
            s += 3
        return {"res": n, "end": r}

    def encode(self, e) -> str:
        t = self._JJM(e)
        return t["res"] + t["end"]


class W:
    @logger.catch
    def __init__(self, key: str, gt: str, challenge: str, c: str, s: str) -> None:
        self.key = key
        self.gt = gt
        self.challenge = challenge
        self.c = c
        self.s = s
        self.aeskey = self.Key()

    def Key(self) -> bytes:
        var = []
        for _ in range(4):
            random_value = int(65536 * (1 + random.random()))
            hex = format(random_value, "04x")[1:]
            var.append(hex)
        dist = ("".join(var)).encode()
        return dist

    @logger.catch
    def RSA(self, data: str) -> str:
        k = int(
            "00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81",
            16,
        )
        e = int("010001", 16)
        pubKey = RSA.construct((k, e))
        cipher = PKCS1_v1_5.new(pubKey)
        encryptedData = cipher.encrypt(data.encode())
        encryptedHex = hexlify(encryptedData)
        return encryptedHex.decode()

    @logger.catch
    def AES(self, data: str) -> list:
        iv = b"0000000000000000"
        cipher = AES.new(self.aeskey, AES.MODE_CBC, iv)
        pad_pkcs7 = pad(data.encode(), AES.block_size, style="pkcs7")
        encrypted = cipher.encrypt(pad_pkcs7)
        return [encrypted[i] for i in range(len(encrypted))]

    @logger.catch
    def Calculate(self) -> str:
        dic = {
            "lang": "zh-cn",
            "passtime": math.floor((random.random() * 500) + 4000),
            "a": "5363_8046,3130_3310,6599_4788",  # 点选位置, e
            "pic": "/captcha_v3/batch/v3/74760/2024-06-29T01/word/xxx.jpg",
            "tt": "xxxM4W8Pxxxx",  # s
            "ep": {
                "ca": [  # 规矩
                    {"x": 1014, "y": 306, "t": 1, "dt": 2745},
                    {"x": 940, "y": 149, "t": 1, "dt": 393},
                    {"x": 1055, "y": 198, "t": 1, "dt": 691},
                    {"x": 1122, "y": 395, "t": 3, "dt": 646},
                ],
                "v": "3.1.0",
                "$_FB": False,
                "me": True,
                "tm": {  # 性能
                    "a": 1714499620351,
                    "b": 1714499620593,
                    "c": 1714499620593,
                    "d": 0,
                    "e": 0,
                    "f": 1714499620357,
                    "g": 1714499620357,
                    "h": 1714499620357,
                    "i": 1714499620357,
                    "j": 1714499620357,
                    "k": 1714499620357,
                    "l": 1714499620357,
                    "m": 1714499620574,
                    "n": 1714499620593,
                    "o": 1714499620593,
                    "p": 1714499620702,
                    "q": 1714499620709,
                    "r": 1714499620757,
                    "s": 1714499620759,
                    "t": 1714499620759,
                    "u": 1714499620776,
                },
            },
            "h9s9": "1816378497",
            "rp": "059b65ecc532496663c442cbd2196e9d",  # ?
        }

        params = json.dumps(dic)

        # u = xxxxx
        u = self.RSA(self.aeskey.decode())
        # h = [116,13,253,xxxxxxxxxxxxxxxx,70,100]
        h = self.AES(data=params)
        # aewrhtjyksudlyi;ulkutyjrhtegwfqed eergty
        p = Enc().encode(h)
        w = p + u
        return w
