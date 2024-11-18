import uuid
import re
def keygen():
    mac_lst = re.findall('..', '%012x' % uuid.getnode())
    key_lst = []
    A = 'abcdEF123456gHIJklMNop556372834q6rs6TU7vWxyzAbcDEfgHiJklMNoPQrsTUVwxYZabcdEFgHIJklMNopqrsTUvWxyzAbcDEfgHiJklMNoPQrsTUVwxYZ'
    B = 'Abc123DEf5g6H7i8J8k9l0MNoPQrsTUVwxYZAbc7D6E5f4g3H2i2J2klMNoPQrsTUVwxYZabcdEFgHIJklMNopqrsTUvWxyzabcdEFgHIJklMNopqrsTUvWxyz'
    for l in mac_lst:
        # print(l.isnumeric())
        if  l.isnumeric() is not True:
            k = ''.join(format(ord(i), '08b') for i in l)
        else:
            a=int(l[0])
            b=int(l[1])
            c= str(a*b)
            k = ''.join(format(ord(i), '08b') for i in c)
        for i, a in enumerate(k):
            if int(a) == 0:
                key_lst.append(A[i])
            if int(a) == 1:
                key_lst.append(B[i])
    key = ''.join(key_lst)
    return key
