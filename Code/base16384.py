s = "一二三四五六七八九十"
a = s.encode('gbk')  # input().encode('utf8')
print(s)


# bits = "".join(str(bin(char))[2:] for char in a)
# # print(bits)
# count = len(bits) // 14 + bool(len(bits) % 14)
# bits = bits.ljust(count * 14, '0')
# out = ""
# for i in range(0, len(bits), 14):
#     out += chr(int(bits[i:i + 14], 2) + 0x4e00)
# print(out)


class BaseN:
    def __init__(self, n):
        self.n = n
        self.L = len(str(bin(n))[2:]) - 1
        # self.digits = string.digits + string.ascii_letters

    @staticmethod
    def bytes2bis(s):
        return "".join(str(bin(char))[2:] for char in s)

    def encode(self, s):
        bits = self.bytes2bis(s.encode())  # ('gbk'))
        count = len(bits) // self.L + bool(len(bits) % self.L)
        # bits = bits.ljust(count * self.L, '0')
        print(bits)
        out = ""
        for i in range(0, len(bits), self.L):
            out += chr(int(bits[i:i + self.L], 2) + 0x4e00)
        return out

    def decode(self, s):
        # bits = self.bytes2bis(s.encode())
        bits = "".join(str(bin(ord(c) - 0x4e00))[2:].ljust(self.L, '0') for c in s)
        print(bits)
        return bytes(int(bits[i:i + 3], 2) for i in range(0, len(bits), 8)).decode()  # ('gbk')


q = BaseN(16384)
print(q.encode(s))
print(q.decode(q.encode(s)))
