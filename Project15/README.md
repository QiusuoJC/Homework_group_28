**Implement sm2 2P sign with real network communication**
-
**一、project简介**
-
真实网络通信下SM2双方签名的实现。签名实现整体示意图：

<img src="https://github.com/QiusuoJC/homework_group28/assets/104217417/eb8f6d62-f385-49f1-9d1d-fcbcd4787de6">

**二、具体实现**
-
基于pycharm编译器导入gmssl库后运行。

**SM2_2P_sign实现**
-
导入自编写文件、库，初始化有限域的阶、椭圆曲线的阶和基本点、圆锥曲线相关参数，由MyFunc.py密钥生成函数生成公私钥对。

<img width="448" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/390b9abb-865f-4cb2-a9da-959b3947fd15">

定义函数calculate_ZA，实现对传递参数identifier、椭圆曲线参数a b、G点x y、公钥sk pk的拼接，继而由SM3算法对其进行哈希。

<img width="447" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/1ba68ec6-e4e8-4288-982e-ac684b9e5a9e">

**生成私钥private_key1、private_key2，计算public_key1**

<img src="https://github.com/QiusuoJC/homework_group28/assets/104217417/6c285a2c-34ad-4a5a-9fa9-067624ec2365" width=75% height=75%>

1. 由随机数生成器生成私钥private_key1、private_key2
2. 在发送方计算$public\_key1= private\_key1^{-1}*BASE\_POINT$
3. 将public_key1发送至接收方

<img width="426" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/ca6e0825-3172-45d7-ba7b-7183e42200ef">

**生成共享公钥shared_public_key**

<img src="https://github.com/QiusuoJC/homework_group28/assets/104217417/e3d62555-5ab9-4e71-ac55-70e2973ac039" width=40% height=40%>

接受方生成随机数private_key2后，计算$shared\_public\_key = private\_key2^{-1}*private\_key1-BASE\_POINT$。shared_public_key为共享公钥，需要公布。

<img width="467" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/714c3e4d-8962-4dff-a167-0e5ceba71607">

**设置计算Z_A为双方标识符,计算e和partial_public_key1并发送至接收方**

<img src="https://github.com/QiusuoJC/homework_group28/assets/104217417/3cde51a2-037f-4bfb-8727-df2f14285dfe" width=50% height=50%>

1. 在发送方，利用在准备阶段定义的calculate_ZA函数计算Z_A，并将其级联message哈希得到e。
2. 生成随机数random_number1，计算$partial\_public\_key1=random\_number1*BASE\_POINT$
3. 将e和partial_public_key1发送至接收方

<img width="527" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/0ee2dfb1-8021-46bc-b0ba-e254926b5491">


**计算部分签名r**

<img src="https://github.com/QiusuoJC/homework_group28/assets/104217417/f28aa04c-db76-4c9b-bd9a-c9a264d95f38" width=40% height=40%>

1. 接收方在此过程中会先生成两个随机数，分别称为random_number2和random_number3。
2. 接下来，他们将利用random_number2与基点BASE_POINT进行计算，得到partial_public_key2。
3. 在接收方的计算过程中，他们会利用partial_public_key2、combined_public_key[0]以及y1等值进行复杂的运算，最终得到变量r的值。这一过程包含了多个步骤，确保了r的安全性。
4. 同时，接收方还会通过使用private_key2和random_number2来计算变量s2，以及使用private_key2、r和random_number1来计算变量s3。
5. 最后，接收方将得到的变量r、s2和s3发送回发送方，完成整个流程。

###### 代码呈现

```python
random_number2 = secrets.randbelow(CURVE_ORDER-1)
    partial_public_key2 = MF.ECC_multiply(random_number2, BASE_POINT)
    partial_public_key3 = MF.ECC_multiply(random_number2, partial_public_key1)      #计算部分公钥3:将随机数2与部分公钥1相乘。
    combined_public_key = MF.ECC_add(partial_public_key3, partial_public_key2)
    r = (combined_public_key[0] + e) % CURVE_ORDER
    print("r =", r)
    s2 = (private_key2 * random_number2) % CURVE_ORDER
    s3 = (private_key2 * (r + random_number1)) % CURVE_ORDER
    print("s2 =", s2)
    print("s3 =", s3)
```

**生成签名s=(r,s)**

<img src="https://github.com/QiusuoJC/homework_group28/assets/104217417/48e3a25d-aba5-4b38-adce-2d76d624929b" width=50% height=50%>

1. 发送方接收到r，s2，s3后，计算$s=private\_key1 * random\_number1 * s2 + private\_key1 * s3 - r$
2. 判断其是否不等于零、是否不等于$CURVE\_ORDER - r$
3. 输出（r，s）

###### 代码呈现

```python
s = (private_key1 * random_number1 * s2 + private_key1 * s3 - r) % CURVE_ORDER
    if s != 0 and s != CURVE_ORDER - r:
        print("s =", s)
```

**输出结果展示**

设定发送方为Alice，所发送的消息为Hello_Bob，则真实网络通信下SM2双方签名实现的输出结果如下所示：

<img width="887" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/f37aa40a-08b2-4a09-b1f7-c2c73e821ae9">

**MyFunc实现**
-
**初始化椭圆曲线参数和有限域阶**

设置椭圆曲线和有限域的阶、椭圆曲线参数

```python
#设置椭圆曲线和有限域的阶
FIELD_ORDER = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
CURVE_ORDER = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
POINT_X = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
POINT_Y = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
BASE_POINT = (POINT_X, POINT_Y)

#设置椭圆曲线参数
CURVE_PARAM_A = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
CURVE_PARAM_B = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
```

**基于扩展欧几里得算法求逆**

```python
'''基于扩展欧几里得算法求逆'''
def calculate_inverse(a, b):
    if a == b:
        return (a, 1, 0)        #若相等,则直接返回
    else:
        flag = False
        c = [a]
        d = [b]
        e = []
        res = []
        #循环判断,直到res==0
        i = 0
        while not flag:
            e.append(d[i] // c[i])
            res.append(d[i] % c[i])
            d.append(c[i])
            c.append(res[i])
            i += 1
            if res[i-1] == 0:
                flag = True
        i -= 1
        res1 = [1]      #系数
        res2 = [0]      #系数
        res3 = c[i]     #公因子
        i -= 1
        num = i
        while i >= 0:
            res2.append(res1[num - i])
            res1.append(res2[num - i] - e[i] * res1[num - i])
            i -= 1
        if res3 == 1:
            return res1[-1] % b
        else:
            return -1
```

**Tonelli-Shanks求解二次剩余**

```python
'''Tonelli-Shanks求解二次剩余'''
def Tonelli_Shanks(y, p):
    #利用勒让德符号判断是否为二次剩余
    assert pow(y, (p - 1) // 2, p) == 1
    if p % 4 == 3:
        return pow(y, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for t in range(2, p):
        if pow(t, (p - 1) // 2, p) == p - 1:
            c = pow(t, q, p)
            break
    r = pow(y, (q + 1) // 2, p)
    t = pow(y, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:       #外层循环的判断条件
            temp = pow(t, 2**(i + 1), p)
            i += 1
            if temp % p == 1:
                b = pow(c, 2**(m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0       #每次内层循环结束后i值要更新为0
        return r
```

**椭圆曲线加法与乘法运算**

基于上述函数，定义椭圆曲线上的加法、乘法运算。

在加法运算中，包含斜率存在、斜率不存在，两种情况。利用微分求解。

```python
#椭圆曲线加法运算
def ECC_add(a, b):
    #考虑是否存在0的情况
    if a == 0 and b == 0:
        return 0
    if a == 0:
        return b
    if b == 0:
        return a
    if a == b:
        #此时无法直接求斜率，需要借助微分
        k = (3 * a[0] ** 2 + CURVE_PARAM_A) * calculate_inverse(2 * a[1], FIELD_ORDER) % FIELD_ORDER
        res = (k ** 2 - 2 * a[0]) % FIELD_ORDER
        list1 = [res, (k * (a[0] - res) - a[1]) % FIELD_ORDER]
        return list1
    else:
        #保证大数在前
        if a[0] > b[0]:
            temp = a
            a = b
            b = temp
        #计算斜率
        k = (b[1] - a[1]) * calculate_inverse(b[0] - a[0], FIELD_ORDER) % FIELD_ORDER
        #依据椭圆曲线的计算规则进行计算
        res = (k ** 2 - a[0] - b[0]) % FIELD_ORDER
        list2 = [res, (k * (a[0] - res) - a[1]) % FIELD_ORDER]
        return list2
```

```python
#椭圆曲线乘法运算
def ECC_multiply(a, b):
    res = 0     #初始化res为无穷远点O
    a_bin = bin(a)[2:]      #将a转为二进制
    b_temp = b
    for i in reversed(range(len(a_bin))):
        if a_bin[i] == '1':
            res = ECC_add(res, b_temp)
        b_temp = ECC_add(b_temp, b_temp)
    return res
```

**基于secret库实现密钥生成函数**

```python
'''基于secret库的密钥生成函数'''
def generate_key():
    private_key = int(secrets.token_hex(32), 16)
    public_key = ECC_multiply(private_key, BASE_POINT)
    return private_key, public_key
```

**变量类型转换函数**

将变量转换为bytes类型

```python
'''变量类型转换函数'''
#转换为bytes，第二参数为字节数，可以为空白
def to_byte(x, size=None):
    if isinstance(x, int):
        if size is None:        #计算合适的字节数
            size = 0
            tmp = x >> 64
            while tmp:
                size += 8
                tmp >>= 64
            tmp = x >> (size << 3)
            while tmp:
                size += 1
                tmp >>= 8
        elif x >> (size << 3):      #指定的字节数不够则截取低位
            x &= (1 << (size << 3)) - 1
        return x.to_bytes(size, byteorder='big')
    elif isinstance(x, str):
        x = x.encode()
        if size is not None and len(x) > size:      #超过指定长度
            x = x[:size]         #截取左侧字节
        return x
    elif isinstance(x, bytes):
        if size is not None and len(x) > size:      #超过指定长度
            x = x[:size]         #截取左侧字节
        return x
    elif isinstance(x, tuple) and len(x) == 2 and type(x[0]) == type(x[1]) == int:
        #针对坐标形式(x, y)
        return to_byte(x[0], size) + to_byte(x[1], size)
    return bytes(x)

```

**三、参考资料**
-
【1】<https://blog.csdn.net/qq_51999772/article/details/122642868>

【2】<https://blog.csdn.net/qq_43339242/article/details/123221091>

【3】上课PPT：SM2
