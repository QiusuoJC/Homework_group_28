**Implement a PGP scheme with SM2**
-
PGP(Pretty Good Privacy)是一种加密通信协议和软件。PGP协议可以用于保护电子邮件、文件和磁盘等数据的机密性和完整性，以及验证数字签名。

**一、实现原理**
-
根据上课PPT所讲：

<img width="606" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/45dc826f-32df-43d3-ab77-9ae75cf096d5">

1. 会话密钥生成：随机生成会话密钥并用SM2的密钥交换协议进行密钥分发；

2. 加密会话密钥：利用SM2公钥加密算法加密会话密钥

3. 加密数据：利用对称加密算法进行加密数据

**二、具体实现**
-

1、首先随机生成公私钥对：

<img width="321" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/fa68ac58-9cee-44c2-acfd-64f19b701351">

SM2加解密算法以及数字签名的正确性验证：

<img width="722" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/d13ec0e6-d97a-4426-8dca-eaf10f377310">

2、之后为了实现密钥交换，我们建立了Client-Server的TCP通信框架：

<img width="446" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/fa9ed361-1f39-4860-8b06-0acc6a2810b5">

3、在密钥交换之后，我们需要用对称加密方案对数据进行加密，这里我们调用国密SM4来加密数据：

原始数据：

<img width="308" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/a9a022b7-0321-4ead-952d-3f8cda977726">

加密结果：

<img width="311" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/055493f2-e1a2-4ac7-9276-0324e8af4cd6">
