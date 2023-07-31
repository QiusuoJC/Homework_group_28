**Implement length extension attack for SM3, SHA256, etc.**
-
**一、长度扩展攻击**
-
长度扩展攻击：是指针对特定hash函数（尤其是MD结构的hash函数）的一种攻击手段，攻击者可以利用H(M1)和M1的长度，在不知道M1内容的情形下，将攻击者控制的M2计算出H（M1 ‖ M2）。

<img width="389" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/44669828-b064-4215-86c3-e95c67c16782">

其核心是将H(M1)作为对M2做hash的IV值输入，然后根据已知的M1的长度和M2的长度确定新的填充长度，在进行hash，就能得到伪造的H(M1||M2)的值

下图表示具体的对于长度扩展攻击如何实现

<img width="444" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/771e83dd-97eb-4b4e-89f2-5ce9f7b56e4a">

具体的关于长度扩展攻击的其他详细信息放到参考【1】中供大家学习。

**二、具体实现**
-
以下可以自己选择填写对应的消息

<img width="605" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/a197e0c0-3e16-4c7a-a6b5-fb2201c1c23c">

如图，EXMESS1_MESS2就是我们根据H(MESS1)和MESS1长度伪造hash的对应的信息，我们可以验证，上面的输出是我们进行伪造时得到的hash值，下面的输出是我们伪造的目标信息进行hash得到的结果

<img width="467" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/be6bd4f3-977b-423f-ad0c-922013701f1c">

经验证，根据H(MESS1)和MESS1长度伪造hash与对应信息的哈希值一致，说明我们的攻击成功

**三、参考**
-
【1】https://justcryptography.com/length-extension-attack/

【2】上课PPT：SM3
