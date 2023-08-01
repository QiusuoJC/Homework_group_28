**Forge a signature to pretend that you are Satoshi**
-
根据上课PPT所讲，基于以下签名伪造的原理来伪造签名。

<img width="691" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/1cda16c6-133c-4ded-a249-825c2d69e835">

**一、具体实现**
-
**椭圆曲线公私钥对生成**

**sk,pk = MyFunc.generate_key()**

**签名函数**

**Sig(private_key, mes, k)**

生成ECDSA签名的过程：

首先，通过使用私钥对消息进行签名，得到一对数字 (r, s)。其中，r 表示椭圆曲线上某个点的 x 坐标，而 s 则是根据随机数 k 和私钥生成的一个数字。为了实现这一过程，可以按照以下方式进行：

- 步骤一：计算消息的哈希值 `hash`。首先，对消息 `mes` 进行哈希运算，使用 SHA-256 哈希算法，并将结果转换为整数
- 步骤二：使用随机数 `k` 与基本点 `BASE_POINT` 进行椭圆曲线上的点乘法运算，得到一个新的点 `G1`
- 步骤三：将 `G1` 的 x 坐标 `G1[0]` 取模 `FIELD_ORDER`，将结果添加到一个列表 `result` 中。这个值是签名的一部分
- 步骤四：利用计算随机数的逆元函数 `MyFunc.calculate_inverse(k, CURVE_ORDER)`，将 `k` 的逆元与 `(hash + result[0] * private_key)` 的乘积取模 `CURVE_ORDER`，并将结果添加到 `result` 列表中。这个结果同样是签名的一部分。
- 步骤五：`result` 列表中的值即为最终的签名结果。

```python
'''利用私钥进行签名'''
def Sig(private_key, mes,k):
    res = []
    hash = int(sha256(mes.encode('utf-8')).hexdigest(),16)
    G1 = MyFunc.ECC_multiply(k, BASE_POINT)
    res.append(G1[0] % FIELD_ORDER)
    res.append(MyFunc.calculate_inverse(k, CURVE_ORDER) * (hash + res[0] * private_key) % CURVE_ORDER)
    return res
```

**Leaking_k(mes, r, s)**

生成ECDSA签名的过程如下：

首先，使用私钥对消息进行签名，得到一对数字 (r, s)。其中，r 是椭圆曲线上的一个点的 x 坐标，而 s 则是根据随机数 k 和私钥生成的一个数字。为确保私钥安全，我们需要防止随机数 k 的泄露，以免导致私钥 d 的泄露。下面是一个新的实现方案：

- 将消息 `mes` 使用 SHA-256 哈希算法进行哈希运算，得到消息的哈希值 `e`，并将其转换为整数。
- 计算 `r` 的逆元 `r_`，这个值在后续计算中将会用到。
- 利用泄露的私钥 `k`，结合 `r_` 和签名中的 `s`、`e`，计算得到私钥 `d` 的新值。
- 将计算得到的 `d` 输出打印。

注意：为保障安全性，应当定期更新私钥，并妥善保管私钥和随机数，避免泄露可能导致的风险。

```python
def Leaking_k(mes,r,s):
    e = int(sha256(mes.encode('utf-8')).hexdigest(), 16)
    r_ = MyFunc.calculate_inverse(r, CURVE_ORDER) % CURVE_ORDER
    d = r_*(k*s-e) % CURVE_ORDER
    print("(1)pitfalls1:Leaking k leads to leaking of d ")
    print("d:",d)
```

**Reuseing_k(sk1, mes1, mes2)**

当同一个随机数k被多次用于不同场景，私钥d的安全性将受到威胁。下面我们介绍一种方法，通过使用函数`Sign`对两个不同消息`message1`和`message2`进行签名，从而推导出对方的私钥d：

- 对消息`message1`和`message2`分别调用`Sign`函数，得到对应的签名值`r1, s1`和`r2, s2`。
- 分别计算`message1`和`message2`的哈希值：`hash1`和`hash2`。
- 接下来计算`se`= `s1 * hash2 - s2 * hash1` ，`sr1`= `s2 * r1 - s1 * r2`。取它们对`CURVE_ORDER`的模，并计算`sr1`的逆元：`sr1_`。
- 使用公式 `d = (se * sr1_) % CURVE_ORDER` 来计算出泄露的私钥 `d`。
- 最后打印输出泄露的私钥 `d`，并检查泄露的私钥 `d` 是否与签名时使用的私钥 `secret_key1` 相等。

```python
''' Reusing k leads to leaking of d'''
def Reuseing_k(sk1, mes1, mes2):
    print("(2)Reusing k leads to leaking of d")
    [r1,s1] = Sig(sk1, mes1,k)
    [r2,s2] = Sig(sk1,mes2,k)
    print('签名时使用的私钥d:',sk1)

    e1 = int(sha256(mes1.encode('utf-8')).hexdigest(),16)
    e2 = int(sha256(mes2.encode('utf-8')).hexdigest(),16)
    se = s1*e2 - s2*e1
    sr1 = s2*r1-s1*r2 % CURVE_ORDER
    sr1_ = MyFunc.calculate_inverse(sr1,CURVE_ORDER)
    d = (se *sr1_) % CURVE_ORDER
    print('在重复使用k后计算出泄露的私钥d‘=',d)
    print('泄露出的私钥d‘与签名所使用的的d是否相等：',d == sk1)
```

**reusing_k_by_2(sk11, sk22, mes11, mes22)**

多次重复使用同一个随机数k会导致私钥d的泄漏。为避免这种情况，我们需要对于每个消息使用不同的随机数进行签名，这样即使多个用户使用相同的k值，也不会导致私钥泄漏的风险。

下面是对应的新文段：

如果我们在使用 `Sig` 函数时，对于相同的消息分别采用两个不同的随机数 `k1` 和 `k2` 进行签名，即分别生成两个签名对 `(r, s1)` 和 `(r, s2)`，那么就能避免私钥d的泄漏风险。具体过程如下：

   1. 两个用户分别使用 `Sig` 函数对各自的消息 `mes1` 和 `mes2` 进行签名，使用随机数 `k1` 和 `k2`，得到对应的签名值 `(r, s1)` 和 `(r, s2)`。
   2. 计算两个用户推导对方私钥的过程：
      1. 对于 user1 推导 user2 的私钥 `d2`：
         1. 计算 `se2 = s2 * e1 - s1 * e2 + (s2 * r * sk1)`
         2. 计算 `sr1 = (s1 * r) % CURVE_ORDER`
         3. 计算 `sr1` 的逆元 `sr1_`
         4. 计算 `d2 = (se2 * sr1_) % CURVE_ORDER`，得到 user2 使用的私钥 `d2`
      2. 对于 user2 推导 user1 的私钥 `d1_`：
         - 计算 `se1_ = s1 * e2 - s2 * e1 + (s1 * r * sk2)`
         - 计算 `sr2 = (s2 * r) % CURVE_ORDER`
         - 计算 `sr2` 的逆元：`sr2_`
         - 计算 `d1_ = (se1_ * sr2_) % CURVE_ORDER`，得到 user1 使用的私钥 `d1_`
   3. 打印计算得到的 user2 使用的私钥 `d2` 和 user1 使用的私钥 `d1_`，并检查推导出的私钥是否与原来的私钥相等。

   通过以上方式，我们可以有效地避免同一个随机数k被多次使用而导致私钥泄漏的问题。

```python
'''Two users, using k leads to leaking of d, that is they can deduce each other’s d'''
def reusing_k_by_2(sk11,sk22,mes11, mes22):
    [r,s11] = Sig(sk11,mes11,k)
    [r,s22] = Sig(sk22,mes22,k)
    print("(3)Two users, using k leads to leaking of d, that is they can deduce each other’s d")
    print("user1使用的私钥d1：",sk11)
    print("user2使用的私钥d2：",sk22)
    e11 = int(sha256(mes11.encode('utf-8')).hexdigest(),16)
    e22 = int(sha256(mes22.encode('utf-8')).hexdigest(),16)
    se = s22*e11 - s11*e22 +(s22 * r * sk11)
    sr1 = (s11*r) % CURVE_ORDER
    sr1_ = MyFunc.calculate_inverse(sr1,CURVE_ORDER)
    d = (se *sr1_) % CURVE_ORDER
    print('user1通过计算得出的user2使用的私钥d2’：',d)

    se_ = s11*e22 - s22*e11 +(s11 * r * sk22)
    sr2 = (s22*r) % CURVE_ORDER
    sr2_ = MyFunc.calculate_inverse(sr2,CURVE_ORDER)
    d_ = (se_ * sr2_) % CURVE_ORDER
    print('user1通过计算得出的user2使用的私钥d1',d_)
    print('user1与user2计算是否正确：',(d == sk22 and d_ == sk11))
```

**验证函数**

**verify_without_m(e, r, s, pk)**

验证不包含消息的签名：使用公钥pk对签名(r, s)进行验证，但并没有验证消息的内容。输入为一个哈希值e，签名结果r、s，以及公钥pk。此过程需要利用e、r、s生成两个坐标g1、g2并相加得到一个新点g，随后检查其横坐标x是否与r相同。

```python
'''verification does not check m'''
def verify_without_m(e,r,s,pk):
    s_ = MyFunc.calculate_inverse(s, CURVE_ORDER) % CURVE_ORDER
    es_ = e*s_ % CURVE_ORDER
    rs_ = r*s_ % CURVE_ORDER
    g1 = MyFunc.ECC_multiply(es_,BASE_POINT)
    g2 = MyFunc.ECC_multiply(rs_,pk)
    g = MyFunc.ECC_add(g1, g2)
    [x, y] = g
    if(x == r):
        print("pass verify")
        return True
    else:
        print("unpass verify")
        return False
```
**same_d_k(sk, mes)**

使用相同的随机数k和私钥d进行签名会导致私钥d的泄漏风险：
   1. 通过使用随机数 `rand_k` 和基本点 `BASE_POINT`，通过 `ECC_compute` 函数计算得到新的点 `g2`
   2. 计算消息 `message` 的哈希值 `hash_e`。此时哈希的数据不仅包括消息本身，还包括之前计算得到的点 `g2[0]`，且该哈希方法并不符合 ECDSA 的标准哈希要求
   3. 计算临时值 `temp_s` = `(rand_k + hash_e * secret_key) % CURVE_ORDER`
   4. 接着，计算消息 `message` 的标准哈希值 `standard_hash_e`
   5. 使用 `Sign` 函数对消息 `message` 进行签名，得到对应的签名值 `r2, s2`，这里仍然使用了相同的 `rand_k` 值
   6. 计算 `s2_` = `standard_hash_e + r2 * secret_key`
   7. 计算逆元 `s2__`，使得 `((temp_s - hash_e * secret_key) % CURVE_ORDER)` 成为 `s2__` 的乘法逆元
   8. 计算 `s2` = `(s2_ * s2__) % CURVE_ORDER`
   9. 利用 `s2`、`temp_s`、标准哈希值 `standard_hash_e`、签名值 `r2`，计算得到私钥 `private_key`
   10. 打印输出签名时使用的私钥 `secret_key`，与使用相同的 `private_key` 和 `rand_k` 计算得到的私钥 `private_key`，并检查它们是否相等

```python
def same_d_k(sk, mes):
    print("(7)Same d and k with ECDSA, leads to leaking of d")
    g1 = MyFunc.ECC_multiply(k,BASE_POINT)
    e = int(sha256((str(g1[0]) + str(mes)).encode('utf-8')).hexdigest(), 16)
    s= (k + e * sk) % CURVE_ORDER
    e1 = int(sha256(mes.encode('utf-8')).hexdigest(), 16)
    [r1,s1] = Sig(sk,mes,k)

    s1_ = e1 + r1*sk
    s1__ = MyFunc.calculate_inverse((s - e * sk) % CURVE_ORDER, CURVE_ORDER)
    s1 = (s1_*s1__) % CURVE_ORDER

    d_ = s1*s - e1
    d__ = MyFunc.calculate_inverse(s1*e+r1,CURVE_ORDER)
    d = (d_*d__) % CURVE_ORDER
    print('签名时使用的私钥d:', sk)
    print('与ECDSA使用相同的d、k从而计算出的私钥d:',d)
    print('使用相同d、k计算出的结果是否相等',sk==d)
```

**forge()**

- 假若消息的签名验证不对消息进行检查，那么任何人都可以伪造一个签名。为了阐明这一点，我们使用预先准备的 `verify_without_m` 函数进行验证
- 在开始时，我们生成两个介于 `[1, CURVE_ORDER)` 范围内的随机数 `k1` 和 `k2`。
- 接下来，利用这两个随机数，我们分别使用 `ECC_multiply` 函数将 `k1` 与基本点 `BASE_POINT` 相乘，得到新的点 `g1`；
- 同时，将 `k2` 与公钥 `pk` 相乘，得到新的点 `g2`。
- 然后，我们使用 `ECC_add` 函数将 `g1` 和 `g2` 进行点加法运算，得到点 `[r1, s1]`。
- 接下来，我们进行一系列计算。首先，计算临时值 `r_k1`，它等于 `r1` 乘以 `k1`。然后，计算 `k2` 在模 `CURVE_ORDER` 下的逆元 `k2_`。
- 之后，计算 `e1`，其值为 `(r_k1 * k2_) % CURVE_ORDER`。最后，计算 `s1`，其值为 `(r1 * k2_) % CURVE_ORDER`。
- 最后，我们调用 `verify_without_m` 函数来验证签名，但是请注意，该验证过程并没有验证消息的内容。如果验证成功，则会打印输出 "forge伪造成功"。

```python
def forge():
    print("(6)One can forge signature if the verification does not check m")
    k1 = secrets.randbelow(CURVE_ORDER)
    k2 = secrets.randbelow(CURVE_ORDER)
    g1 = MyFunc.ECC_multiply(k1,BASE_POINT)
    g2 = MyFunc.ECC_multiply(k2,pk)
    [r1,s1] = MyFunc.ECC_add(g1,g2)
    r_k1 = r1*k1
    k2_ = MyFunc.calculate_inverse(k2,CURVE_ORDER)
    e1 = (r_k1*k2_) % CURVE_ORDER
    s1 = (r1*k2_) % CURVE_ORDER
    if (verify_without_m(e1, r1, s1, pk)):
        print('forge伪造成功')
```

输出结果如下：

<img width="773" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/e72d9236-1c32-4d1d-a074-0a70763ec0e9">

<img width="726" alt="image" src="https://github.com/QiusuoJC/homework_group_28/assets/123710102/08e17a9a-4798-4e8b-b925-422f66660e91">

由输出结果可知，签名伪造成功

**二、参考**
-
【1】上课PPT：20230401-btc-public
