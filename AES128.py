
def umn2vgalua(num):
    num = int(num, 16)

    a = bin(num * 2)[2:]

    if len(a) < 9:
        return hex(int(a, 2))
    else:
        a = a[1:]
        polinom = '00011011'
        res = ''

        for i in range(8):
            if a[i] == polinom[i]:
                res += '0'
            else:
                res += '1'

        return hex(int(res, 2))


def umn3vgalua(num):
    num = int(num, 16)
    a = bin(num)[2:]

    res1 = ''

    x2 = a + '0'
    x1 = '0' + a

    for i in range(len(x2)):
        if x2[i] == x1[i]:
            res1 += '0'
        else:
            res1 += '1'

    if len(res1) < 9:
        return int(res1, 2)
    elif len(res1) == 9:

        res_1 = res1[1:]
        polinom = '00011011'
        res2 = ''

        for i in range(8):
            if res_1[i] == polinom[i]:
                res2 += '0'
            else:
                res2 += '1'

        return int(res2, 2)


def umn9vgalua(num):
    a = umn2vgalua(umn2vgalua(umn2vgalua(num)))
    return int(a, 16) ^ int(num, 16)


def umn0Bvgalua(num):
    return int(umn2vgalua(umn2vgalua(umn2vgalua(num))), 16) ^ int(umn2vgalua(num), 16) ^ int(num, 16)


def umn0Dvgalua(num):
    return int(umn2vgalua(umn2vgalua(umn2vgalua(num))), 16) ^ int(umn2vgalua(umn2vgalua(num)), 16) ^ int(num, 16)


def umn0Evgalua(num):
    a = umn2vgalua(umn2vgalua(umn2vgalua(num)))
    b = umn2vgalua(umn2vgalua(num))
    c = umn2vgalua(num)

    return int(a, 16) ^ int(b, 16) ^ int(c, 16)


def stringToBytes(in_string):
    res = [[], [], [], []]
    padded_string = in_string.ljust(16, '\0')
    i = 1
    while i < 17:

        new_string = hex(ord(padded_string[i - 1]))

        if len(new_string) < 4:
            new_string = new_string[0:2] + '0' + new_string[-1]

        if i % 4 == 1:
            res[0].append(new_string)

        elif i % 4 == 2:
            res[1].append(new_string)

        elif i % 4 == 3:
            res[2].append(new_string)

        elif i % 4 == 0:
            res[3].append(new_string)

        i += 1

    return res


def key(in_string):
    res = [[], [], [], []]

    i = 1
    while i < 17:
        num = hex(ord(in_string[i - 1]))

        if len(num) < 4:
            num = num[0:2] + '0' + num[-1]

        if i % 4 == 1:
            res[0].append(num)

        if i % 4 == 2:
            res[1].append(num)

        if i % 4 == 3:
            res[2].append(num)

        if i % 4 == 0:
            res[3].append(num)

        i += 1

    return res


def SubBytes(array):
    sbox = [
        [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
    ]
    for i in range(4):
        array[i][0] = hex(sbox[int(array[i][0][2], 16)][int(array[i][0][3], 16)])
        array[i][1] = hex(sbox[int(array[i][1][2], 16)][int(array[i][1][3], 16)])
        array[i][2] = hex(sbox[int(array[i][2][2], 16)][int(array[i][2][3], 16)])
        array[i][3] = hex(sbox[int(array[i][3][2], 16)][int(array[i][3][3], 16)])

    return array


def ShiftRows(array):
    str1 = array[1][1:] + array[1][:1]
    str2 = array[2][2:] + array[2][:2]
    str3 = array[3][3:] + array[3][:3]

    res = [array[0], str1, str2, str3]
    return res


def MixColums(array):
    res = [[], [], [], []]

    for i in range(4):

        column = [x[i] for x in array]

        str1 = int(umn2vgalua(column[0]), 16) ^ umn3vgalua(column[1]) ^ int(column[2], 16) ^ int(column[3], 16)

        str2 = int(column[0], 16) ^ int(umn2vgalua(column[1]), 16) ^ umn3vgalua(column[2]) ^ int(column[3], 16)

        str3 = int(column[0], 16) ^ int(column[1], 16) ^ int(umn2vgalua(column[2]), 16) ^ umn3vgalua(column[3])

        str4 = umn3vgalua(column[0]) ^ int(column[1], 16) ^ int(column[2], 16) ^ int(umn2vgalua(column[3]), 16)

        num = hex(str1)

        if len(num) < 4:
            num = num[0:2] + '0' + num[-1]

        res[0].append(num)

        num = hex(str2)

        if len(num) < 4:
            num = num[0:2] + '0' + num[-1]

        res[1].append(num)

        num = hex(str3)

        if len(num) < 4:
            num = num[0:2] + '0' + num[-1]

        res[2].append(num)

        num = hex(str4)

        if len(num) < 4:
            num = num[0:2] + '0' + num[-1]

        res[3].append(num)

    return res


def AddRoundKey(array):
    global key

    res = [[], [], [], []]

    for i in range(4):

        columntext = [x[i] for x in array]

        columnkey = [x[i] for x in key]

        str1 = int(columntext[0], 16) ^ int(columnkey[0], 16)

        str2 = int(columntext[1], 16) ^ int(columnkey[1], 16)

        str3 = int(columntext[2], 16) ^ int(columnkey[2], 16)

        str4 = int(columntext[3], 16) ^ int(columnkey[3], 16)

        columnkey = hex(str1)

        if len(columnkey) < 4:
            columnkey = columnkey[0:2] + '0' + columnkey[-1]

        res[0].append(columnkey)

        columnkey = hex(str2)

        if len(columnkey) < 4:
            columnkey = columnkey[0:2] + '0' + columnkey[-1]

        res[1].append(columnkey)

        columnkey = hex(str3)

        if len(columnkey) < 4:
            columnkey = columnkey[0:2] + '0' + columnkey[-1]

        res[2].append(columnkey)

        columnkey = hex(str4)

        if len(columnkey) < 4:
            columnkey = columnkey[0:2] + '0' + columnkey[-1]

        res[3].append(columnkey)

    return res


def crypt(a):
    b = stringToBytes(a)

    b = AddRoundKey(b)

    for x in range(9):
        b = SubBytes(b)
        b = ShiftRows(b)
        b = MixColums(b)
        b = AddRoundKey(b)

    b = SubBytes(b)
    b = ShiftRows(b)
    b = AddRoundKey(b)

    res = ''
    for i in range(4):
        for j in range(4):
            res += chr(int(b[j][i], 16))

    return res


def InvSubBytes(array):
    invsbox = [
        [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
        [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
        [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
        [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
        [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
        [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
        [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
        [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
        [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
        [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
        [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
        [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
        [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
        [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
        [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
        [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]]

    for i in range(4):
        array[i][0] = hex(invsbox[int(array[i][0][2], 16)][int(array[i][0][3], 16)])
        array[i][1] = hex(invsbox[int(array[i][1][2], 16)][int(array[i][1][3], 16)])
        array[i][2] = hex(invsbox[int(array[i][2][2], 16)][int(array[i][2][3], 16)])
        array[i][3] = hex(invsbox[int(array[i][3][2], 16)][int(array[i][3][3], 16)])

    return array


def InvShiftRows(array):
    list1 = array[1][3:] + array[1][:3]
    list2 = array[2][2:] + array[2][:2]
    list3 = array[3][1:] + array[3][:1]

    res = [array[0], list1, list2, list3]
    return res


def InvMixColums(array):
    res = [[], [], [], []]

    for i in range(4):

        a = [x[i] for x in array]

        str1 = umn0Evgalua(a[0]) ^ umn0Bvgalua(a[1]) ^ umn0Dvgalua(a[2]) ^ umn9vgalua(a[3])
        str2 = umn9vgalua(a[0]) ^ umn0Evgalua(a[1]) ^ umn0Bvgalua(a[2]) ^ umn0Dvgalua(a[3])
        str3 = umn0Dvgalua(a[0]) ^ umn9vgalua(a[1]) ^ umn0Evgalua(a[2]) ^ umn0Bvgalua(a[3])
        str4 = umn0Bvgalua(a[0]) ^ umn0Dvgalua(a[1]) ^ umn9vgalua(a[2]) ^ umn0Evgalua(a[3])

        b = hex(str1)
        if len(b) < 4:
            b = b[0:2] + '0' + b[-1]

        res[0].append(b)

        b = hex(str2)
        if len(b) < 4:
            b = b[0:2] + '0' + b[-1]
        res[1].append(b)

        b = hex(str3)
        if len(b) < 4:
            b = b[0:2] + '0' + b[-1]
        res[2].append(b)

        b = hex(str4)
        if len(b) < 4:
            b = b[0:2] + '0' + b[-1]
        res[3].append(b)

    return res


def decrypt(a):
    b = stringToBytes(a)

    b = AddRoundKey(b)

    for x in range(9):
        b = InvShiftRows(b)
        b = InvSubBytes(b)
        b = AddRoundKey(b)
        b = InvMixColums(b)

    b = InvShiftRows(b)
    b = InvSubBytes(b)
    b = AddRoundKey(b)

    res = ''
    for i in range(4):
        for j in range(4):
            res += chr(int(b[j][i], 16))

    return res


if __name__ == "__main__":

    print('Enter 16b key')
    k = input()
    key = key(k)
    if input("encrypt - 0, decrypt - 1: ") == "0":
        if input("Enter from user - 0, read from file - 1: ") == "0":
            print('Enter open text')
            text = input()
            res = crypt(text)
            print("encrypt result: ")
            print(res)
        else:
            f = open('en', 'r', encoding='utf-8')
            text = f.read()
            print(text)
            res = crypt(text)
            f1 = open('file1', 'w', encoding='utf-8')
            f1.write(res)
            f1.close()
            print("encrypt result: ")
            print(res)
    else:
        if input("Enter from user - 0, read from file - 1: ") == "0":
            print("Enter cipher text ")
            text = input()
            print("decrypt result: ")
            print(decrypt(text))
        else:
            f = open('file1', 'r', encoding='utf-8')
            text = f.read()
            print(text)
            print("decrypt result: ")
            print(decrypt(text))
            f.close()


#,)[ÉÇ©ÉËóËz¯3±
# æ¶íp3£¦Þ{þ