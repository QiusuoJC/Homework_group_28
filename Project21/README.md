**Schnorr Batch**
-
首先我们根据参考【1】简单介绍一下Batch verification（批量验证）。

**一、Batch verification（批量验证）原理**
-
<img width="700" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/e6dc2965-e85f-449e-a98e-8ebcf7bbd6bf" >

<img width="700" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/a1893f2e-eb33-4ee6-b0fd-da50829344b3">

<img width="700" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/a7b406bb-dc6c-45f2-94bd-9f49fa94cd76">

**流程**

<img width="547" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/1022bf6b-decc-419e-876c-4d0839b3f97f">

**二、具体实现**
-
**定义椭圆曲线加法、乘法运算函数**

1. `add_points(P, Q, q_int)`：实现椭圆曲线上的点加法运算
2. `double_point(P, a_int, q_int)`：实现椭圆曲线上的点加倍运算
3. `scalar_multiply(P, k, a_int, q_int)`：实现椭圆曲线上的点的标量乘法运算，即将点P与整数k相乘得到点Q

```python
'''定义椭圆曲线加法和乘法运算函数'''
def add_points(P, Q, q_int):
    # 椭圆曲线点加法运算
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    x1, y1, x2, y2 = P[0], P[1], Q[0], Q[1]
    tmp1, tmp2 = y2 - y1, pow(x2 - x1, -1, q_int)
    l = (tmp1 * tmp2) % q_int
    x = (l * l - x1 - x2) % q_int
    y = (l * (x1 - x) - y1) % q_int
    return x, y

def double_point(P, a_int, q_int):
    # 椭圆曲线点加倍运算
    if P == (0, 0):
        return P
    x1, y1 = P[0], P[1]
    tmp1 = (3 * x1 * x1 + a_int) % q_int
    tmp2 = pow(2 * y1, -1, q_int)
    l = (tmp1 * tmp2) % q_int
    x = (l * l - 2 * x1) % q_int
    y = (l * (x1 - x) - y1) % q_int
    return x, y

def scalar_multiply(P, k, a_int, q_int):
    # 椭圆曲线点的标量乘法运算
    Q = (0, 0)
    while k > 0:
        if k & 1:
            Q = add_points(Q, P, q_int)
        k >>= 1
        P = double_point(P, a_int, q_int)
    return Q
```

**验证点是否在椭圆曲线上**

- `check_point(P, a_int, b_int, q_int)`：验证给定的点P是否在指定的椭圆曲线上。

```python
'''检查点是否在椭圆曲线上'''
def check_point(P, a_int, b_int, q_int):
    # 验证给定点是否在椭圆曲线上
    x, y = P[0], P[1]
    if (y * y) % q_int == (x * x * x + a_int * x + b_int) % q_int:
        return True
    return False
```

**实现Schnorr签名方案**

- `Schnorr_sign(M, G, n, q_int, a_int, d_int)`: 生成Schnorr签名。

   1. 生成随机数k

   2. 计算点R = k*G

   3. 计算e = H(x_R || y_R || M)（其中H为SM3哈希函数）

   4. 计算签名s = (k + e * d) % n

   5. 返回签名R、s和哈希值e

<img src="https://github.com/QiusuoJC/homework_group28/assets/104217417/9026abf9-2889-4b12-b38a-7b9615361b4c" width=30% height=30%>

- `Schnorr_verify(R, s, e, G, P, q_int, a_int, n)`: 验证Schnorr签名

   1. 根据签名中的e值计算点eP = e*P、sG = s*G

   2. 计算R_sum = R + eP

   3. 比较sG与R_sum是否相等


<img src="https://github.com/QiusuoJC/homework_group28/assets/104217417/1a25824f-a007-48f1-8201-c82eec82afb6" width=40% height=40%>

```python
'''实现Schnorr签名方案'''
def Schnorr_sign(M, G, n, q_int, a_int, d_int):
    # Schnorr签名生成
    k = random.randint(1, n - 1)
    R = scalar_multiply(G, k, a_int, q_int)
    x_R, y_R = R[0], R[1]
    e = sm3_hash(str(x_R) + str(y_R) + M)
    s = hex((k + int(e, 16) * d_int) % n)[2:]
    return R, s, e

def Schnorr_verify(R, s, e, G, P, q_int, a_int, n):
    # Schnorr签名验证
    sG = scalar_multiply(G, int(s, 16), a_int, q_int)
    eP = scalar_multiply(P, int(e, 16), a_int, q_int)
    R_sum = add_points(R, eP, q_int)
    if sG == R_sum:
        return True
    return False
```

**批量验证**

1. 使用随机选择的私钥d生成三个不同消息的Schnorr签名
2. 分别验证签名的正确性
3. 使用批量验证函数`Schnorr_verify_Batch`验证三个签名是否有效

<img src="https://github.com/QiusuoJC/homework_group28/assets/104217417/8ac3bcb7-50d2-4172-b5a8-9dc2665a8eb4" width=75% height=75%>

```python
'''批量验证'''
# 生成Schnorr签名并输出结果
R1, s1, e1 = Schnorr_sign(M1, G, int(n, 16), int(q, 16), int(a, 16), d)
print(f'R1, s1, e1: {R1, s1, e1}')

R2, s2, e2 = Schnorr_sign(M2, G, int(n, 16), int(q, 16), int(a, 16), d)
print(f'R2, s2, e2: {R2, s2, e2}')

R3, s3, e3 = Schnorr_sign(M3, G, int(n, 16), int(q, 16), int(a, 16), d)
print(f'R3, s3, e3: {R3, s3, e3}')

R_list = [R1, R2, R3]
s_list = [s1, s2, s3]
e_list = [e1, e2, e3]

# 批量验证Schnorr签名并输出结果
res_Batch = Schnorr_verify(R_list[0], s_list[0], e_list[0], G, P, int(q, 16), int(a, 16), int(n, 16))
print(f'Res(Batch): {res_Batch}')
```

**输出结果展示**

<img width="886" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/77b6e465-0478-4972-9965-78acaa4f1b8d">

**三、参考**
-
【1】https://www.btcstudy.org/2021/12/06/schnorr-applications-batch-verification/

【2】https://link.springer.com/content/pdf/10.1007/978-3-540-30539-2_20.pdf

【3】上课PPT：20230401-btc-public
