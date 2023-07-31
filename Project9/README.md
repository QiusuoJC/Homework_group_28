**AES and SM4 software implementation**
-
AES和SM4的软件实现

**AES实现**
-
**一、AES算法简介**
-
<img width="636" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/fc2f5750-9725-4995-9edf-b958ffef1eaa">

**SubBytes（S盒）**

<img width="444" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/ae0b7459-4bc5-45e3-b945-50e69fdb82a9">

选取原则：

<img width="523" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/3c27b815-c2fe-4cc6-bd9e-d3285fb18d64">

**ShiftRows（行移位）**

<img width="529" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/f5eebd70-6ff2-45c6-9e6d-fe6f112c2bb1">

**MixColumns（列混淆）**

<img width="462" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/39b8dad4-a9aa-44e0-b323-639813d2d982">

**AddRoundKeys（轮密钥加）**

<img width="408" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/4c2341b8-1482-4c91-974f-87d07b1fc46a">

**密钥置换函数**

![image](https://github.com/QiusuoJC/homework_group28/assets/123710102/c50453cc-2a15-47d7-b83c-f98d9f0cfc3e)

**二、具体实现**
-
实现时，当明文分组长度不够时，进行填充。

加密如下：

<img width="288" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/3f6c973d-7020-414a-9495-f5a8ed8d8e00">

---

**SM4实现**
-
**一、SM4算法简介**
-
<img width="373" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/e637e5da-75f9-434c-8566-7b95090ba6a6">

**轮函数**

![image](https://github.com/QiusuoJC/homework_group28/assets/123710102/c699f60e-930c-4e62-90a0-4e96095a5cd5)

**合成置换与反序变换**

<img width="494" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/4461d947-9cae-4921-82c3-0b8e9cd8dab8">

**密钥扩展算法**

<img width="502" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/984adee3-5ef0-40c6-b1aa-1d2d5c9dcbbe">

**二、具体实现**
-
1、不借助库用C++

见project_sm4_original.cpp

2、借助OpenSSL库

明文与密钥如下：

<img width="507" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/19652c9a-00c8-4942-8a0e-9670f35a1e51">

加密结果如下：

<img width="310" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/b7244214-16d1-456a-a92d-52e39f2d85fc">
