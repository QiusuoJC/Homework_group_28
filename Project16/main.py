# # -*- coding:utf-8 -*-
# import secrets
# from gmssl import sm3, func
# import MyFunc as MF
#
# '''导入必要的库和模块,初始化椭圆曲线参数和有限域阶'''
# #设置椭圆曲线和有限域的阶
# FIELD_ORDER = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
# CURVE_ORDER = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
# POINT_X = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
# POINT_Y = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
# BASE_POINT = (POINT_X, POINT_Y)
#
# #设置椭圆曲线参数
# CURVE_PARAM_A = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
# CURVE_PARAM_B = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
#
# secret_key, public_key = MF.generate_key()      # 调用MF.generate_key()生成密钥对
#
# '''计算消息标识符ZA'''
# def calculate_ZA(identifier, a, b, x, y, sk, pk):
#     entl = str(len(identifier.encode()) << 3)
#     joint = entl + identifier + str(a) + str(b) + str(x) + str(y) + str(sk) + str(pk)
#     joint_bytes = bytes(joint, encoding='utf-8')
#     hash_value = sm3.sm3_hash(func.bytes_to_list(joint_bytes))
#     return int(hash_value, 16)
#
# '''生成私钥private_key1、private_key2，计算public_key1'''
# if __name__ == '__main__':
#     #生成私钥1、私钥2
#     private_key1 = secrets.randbelow(CURVE_ORDER-1)
#     private_key2 = secrets.randbelow(CURVE_ORDER-1)
#     #生成私钥1、私钥2的乘法逆元
#     private_key1_inverse = MF.calculate_inverse(private_key1, CURVE_ORDER)
#     private_key2_inverse = MF.calculate_inverse(private_key2, CURVE_ORDER)
#     public_key1 = MF.ECC_multiply(private_key1_inverse, BASE_POINT)     #计算公钥1
#     print("private_key1 =", private_key1)
#     print("private_key2 =", private_key2)
#     print("public_key1 =", public_key1)
#
#     '''生成共享公钥shared_public_key'''
#     partial_public_key = MF.ECC_multiply(private_key2_inverse, public_key1)     #计算部分公钥
#     base_point_inverse = [POINT_X, -POINT_Y]
#     shared_public_key = MF.ECC_add(partial_public_key, base_point_inverse)      #计算共享公钥
#     print("shared_public_key =", shared_public_key)
#
#     '''设置计算Z_A为双方标识符,计算e和partial_public_key1并发送至接收方'''
#     identifier = "Alice"
#     Z_A = calculate_ZA(identifier, CURVE_PARAM_A, CURVE_PARAM_B, POINT_X, POINT_Y, secret_key, public_key)      #计算标识符Z_A
#     message = b'Hello_Bob'
#     _message = b''.join([MF.to_byte(i) for i in [Z_A, message]])        # 构造消息,将Z_A和消息合并为字节串
#     print("Message sent by Alice:", message)
#     e = int.from_bytes(MF.to_byte(sm3.sm3_hash(func.bytes_to_list(_message))), byteorder='big')     # 将合并后的消息进行哈希,转换得整数e
#     random_number1 = secrets.randbelow(CURVE_ORDER-1)
#     partial_public_key1 = MF.ECC_multiply(random_number1, BASE_POINT)
#     print("e =", e)
#     print("partial_public_key1 =", partial_public_key1)
#
#     '''计算部分签名r'''
#     random_number2 = secrets.randbelow(CURVE_ORDER-1)
#     partial_public_key2 = MF.ECC_multiply(random_number2, BASE_POINT)
#     partial_public_key3 = MF.ECC_multiply(random_number2, partial_public_key1)      #计算部分公钥3:将随机数2与部分公钥1相乘。
#     combined_public_key = MF.ECC_add(partial_public_key3, partial_public_key2)
#     r = (combined_public_key[0] + e) % CURVE_ORDER
#     print("r =", r)
#     s2 = (private_key2 * random_number2) % CURVE_ORDER
#     s3 = (private_key2 * (r + random_number1)) % CURVE_ORDER
#     print("s2 =", s2)
#     print("s3 =", s3)
#
#     '''生成签名s=(r,s)'''
#     s = (private_key1 * random_number1 * s2 + private_key1 * s3 - r) % CURVE_ORDER
#     if s != 0 and s != CURVE_ORDER - r:
#         print("s =", s)


import MyFunc
import secrets
import math
from SM3 import sm3_hash

'''设置有限域的阶以及椭圆曲线的阶'''
P1 = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
P2 = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
X = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Y = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G = (X, Y)

'''设置椭圆曲线参数'''
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93

#密钥生成函数
def KDF(z, klen):       #klen:密钥长度
    ct=1
    k=''
    for _ in range(math.ceil(klen/256)):
        k=k+sm3_hash(hex(int(z+'{:032b}'.format(ct),2))[2:])        #迭代z,然后进行SM3哈希
        ct=ct+1
    #连接密钥片段，根据klen截取长度
    k='0'*((256-(len(bin(int(k,16))[2:])%256))%256)+bin(int(k,16))[2:]
    return k[:klen]

'''Generate sub private key d1、d2'''
d1 = secrets.randbelow(P2-1)
d2 = secrets.randbelow(P2-1)
d1d2_ = MyFunc.calculate_inverse(d1 * d2, P1)
P = MyFunc.ECC_multiply(d1d2_ - 1, G)        #生成公钥
print('Public key P:',P)

'''get ciphertext C'''
#加密函数
def Encryt(M):
    M= '0' * ((4 - (len(bin(int(M.encode().hex(), 16))[2:]) % 4)) % 4) + bin(int(M.encode().hex(), 16))[2:]     #将明文转为二进制并填充
    klen = len(M)
    k = secrets.randbelow(P2-1)
    C1 =MyFunc.ECC_multiply(k,G)     #生成随机参数k对应的点C1
    [x2,y2] = MyFunc.ECC_multiply(k,P)       #生成中间点x2,y2
    x2, y2 = '{:0256b}'.format(x2), '{:0256b}'.format(y2)
    x2_y2 = x2+y2
    t = KDF(x2_y2,klen)     #基于密钥生成函数KDF生成密钥t
    C2 = ((klen//4)-len(hex(int(M,2)^int(t,2))[2:]))*'0'+hex(int(M,2)^int(t,2))[2:]
    C3_ = x2+M+y2
    C3 = sm3_hash(hex(int(C3_,2))[2:])      #SM3哈希计算密文C3
    return [C1,C2,C3]

M = 'Author is JasonCheng'        #明文
[C1,C2,C3] = Encryt(M)
C = str(C1[0])+str(C1[1])+C2+C3     #将密文各部分组合为完整密文
print('计算得到的ciphertext C:',C)
if(C1 != 0):        #若C1不为0则继续解密
    d1_ = MyFunc.calculate_inverse(d1,P1)
    T1 = MyFunc.ECC_multiply(d1_,C1)
    print("计算得到的T1：",T1)

'''计算T2'''
d2_ = MyFunc.calculate_inverse(d2,P1)
T2 = MyFunc.ECC_multiply(d2_,T1)
print("计算得到的T2：",T2)

'''恢复明文 M_'''
def decypt(C1,C2,C3):
    klen = len(C2)*4
    kP = MyFunc.ECC_multiply(d1d2_-1,C1)     #kP=(d1*d2-1)*C1
    [x2,y2] = kP
    x2, y2 = '{:0256b}'.format(x2), '{:0256b}'.format(y2)
    x2_y2 = x2+y2
    t = KDF(x2_y2,klen)     #生成解密密钥t
    M__ = '0' * (klen - len(bin(int(C2, 16) ^ int(t, 2))[2:])) + bin(int(C2, 16) ^ int(t, 2))[2:]
    u_ = x2+M__+y2
    u = sm3_hash(hex(int(u_,2))[2:])
    if(u == C3):
        M__ = hex(int(M__,2))[2:]
        M__ =str(bytes.fromhex(M__))
        M__ = '\n'.join(M__[2:-1].split('\\n'))
        print("最终解密得到的M‘’为：",M__)
        print("M与M''是否相等：", M == M__)
decypt(C1,C2,C3)