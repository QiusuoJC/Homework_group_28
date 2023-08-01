**Impl sm2 with RFC6979**
-

![01](https://github.com/QiusuoJC/homework_group28/assets/104217417/51f76b6d-600d-470f-8e2f-f4c8f5d35a09)

**一、具体实现**
-

首先需要安装bitcoin库

导入自编写文件、库，初始化有限域的阶、椭圆曲线的阶和基本点、圆锥曲线相关参数，由MyFunc.py密钥生成函数生成公私钥对。

**计算消息的标识符ZA**

定义函数cal_ZA，实现对传递参数ID、椭圆曲线参数A1 B1、G点X1 Y1、公钥pk1 pk2的拼接，继而由sha256算法对其进行哈希。

```python
'''计算消息的标识符ZA'''
def cal_ZA(ID, A1, B1, X1, Y1, pk1, pk2):
    #获取bit位数
    ENTLA=str(len(ID.encode()) << 3)
    #将所有输入混合进行拼接后利用sha256进行哈希
    mix_mes = ENTLA + ID + str(A1) + str(B1) + str(X1) + str(Y1) + str(pk1) + str(pk2)
    hash = int(sha256(mix_mes.encode('utf-8')).hexdigest(),16)
    return hash
```

**签名**

<img src="https://github.com/QiusuoJC/homework_group28/assets/104217417/c4264b90-e71c-4ad2-81e3-29ffa680a095" width=35% height=35%>

1. 将消息标识符 `ZA` 和消息 `mes` 拼接起来，利用 SHA-256 哈希算法计算哈希值 `hash1`
2. 由 `int(hash1, 16)` 将其转换为整数 `hash2`
3. 通过 `bitcoin.main.deterministic_generate_k(hash1, private_key)` 函数，由哈希值 `hash1` 、私钥 `private_key` 确定随机数 `k`
4. 将随机数 `k` 、基本点 `basic_point` 进行椭圆曲线上的点乘法运算，得到点 `G`
5. 将签名结果存储在 `sign` 列表中。列表中应有两个元素：
   - `(hash2 + G[0]) % P2`，即消息哈希值 `hash2` 与点 `G` 的 x 坐标相加，然后再取模 `P2`
   - `(MyFunc.calculate_inverse(1 + pk, P2) * (k - sign[0] * pk)) % P2`用于计算椭圆曲线上的第二个坐标
6. `sign` 列表作为签名结果返回
7. 进行实际签名操作
   1. 调用 `cal_ZA` 函数计算消息标识符 `ZA`
   2. 调用 `Sig` 函数对消息进行签名
   3. 将签名结果存储在变量 `sign` 中

```python
'''签名'''
def Sig(pk, mes, ZA):
    hash1 = sha256(str(ZA+mes).encode('utf-8')).hexdigest()
    hash2 = int(hash1,16)
    # 生成随机数k，利用k与基本点相乘得到一个随机的点G
    k = bitcoin.main.deterministic_generate_k(hash1,private_key)
    #k = 1
    G = MyFunc.ECC_multiply(k, basic_point)

    sign = []
    sign.append(( hash2+G[0] ) % P2)
    sign.append((MyFunc.calculate_inverse(1 + pk, P2) * (k - sign[0] * pk)) % P2)  #用私钥进行签名
    return sign

mes = "HelloBob"
ID='Alice'
ZA=str(cal_ZA(ID, A, B, X, Y, public_key[0], public_key[1]))
sign = Sig(private_key, mes, ZA)
```

**验证**

<img src="https://github.com/QiusuoJC/homework_group28/assets/104217417/9c3822db-afb0-4496-86cc-f02acbfc58a6" width=40% height=40%>

该步骤的核心思路是：通过对消息标识符 `ZA` 和消息 `mes` 进行哈希运算，然后利用椭圆曲线上的点运算进行签名验证。如果验证通过，说明签名是由拥有对应私钥的实体生成的，并且消息在传递过程中没有被篡改。实现细节如下：

1. 调用 `cal_ZA` 函数计算消息的标识符 `ZA`
2. 将消息的标识符 `ZA` 和消息 `mes` 进行拼接，然后利用 SHA-256 哈希算法计算哈希值 `hash`，并将其转换为整数
3. 使用签名中的第二个元素 `sign[1]` 与基本点 `basic_point` 进行椭圆曲线上的点乘法运算，得到一个新的点 `mul1`
4. 使用签名中的第一个元素 `(sign[0] + sign[1]) % P2` 与公钥 `public_key` 进行椭圆曲线上的点乘法运算，得到一个新的点 `mul2`
5. 对点 `mul1` 和点 `mul2` 进行椭圆曲线上的点加法运算，得到一个新的点 `add1`
6. 将消息哈希值 `hash` 与点 `add1` 的 x 坐标相加后再取模 `P2` ，得到私钥 `sk1`
7. 将签名中的第一个元素 `sign[0]` 和计算得出的新私钥 `sk1` 进行比较。如果相等，说明签名验证通过

```python
'''验证'''
def check(public_key, ID, mes, sign):
    ZA=str(cal_ZA(ID, A, B, X, Y, public_key[0], public_key[1]))
    hash = int(sha256(str(ZA+mes).encode('utf-8')).hexdigest(),16)

    mul1=MyFunc.ECC_multiply(sign[1], basic_point)
    mul2=MyFunc.ECC_multiply((sign[0]+sign[1]) % P2, public_key)
    add1=MyFunc.ECC_add(mul1, mul2)

    sk1= (hash+add1[0]) % P2
    print('私钥:',sign[0])
    print('计算得出的私钥',sk1)

    return sk1==sign[0]

if(check(public_key, ID, mes, sign)):
    print('验证通过')
```

**输出结果展示**

设定发送方为Alice，所发送的消息为HelloBob，则基于RFC6979的SM2实现的输出结果如下所示：

<img width="886" alt="image" src="https://github.com/QiusuoJC/Homework_group_28/assets/123710102/9fed3d44-d559-46fb-809a-187f3410b928">


**二、参考资料**
-

【1】<https://blog.csdn.net/qq_51999772/article/details/122642868>

【2】<https://blog.csdn.net/qq_43339242/article/details/123221091>

【3】上课PPT：SM2
