**Do your best to optimize SM3 implementation (software)**
-
基于个人实现的SM3进行软件优化，主要运用了循环展开和减少函数的调用来进行优化

**SM3概述**

MD结构，长度小于2<sup>64</sup>bit的消息

消息分组为512-bit，中间链接变量为256-bit，杂凑值为256-bit

压缩函数共64步操作

布尔函数：

![image](https://github.com/QiusuoJC/homework_group28/assets/123710102/1213abcf-acd5-4833-a64f-c0da984484b3)

置换函数：

![image](https://github.com/QiusuoJC/homework_group28/assets/123710102/79a689c5-bcd1-4b5e-b4f7-c1672a4fdbd1)

**一、消息填充算法**
-
SM3数据填充规则和SHA256一样，具体步骤如下：

1、先填充一个“1”，后面加上k个“0”。其中k是满足(n+1+k) mod 512 = 448的最小正整数。

2、追加64位的数据长度（bit为单位，大端序存放。观察算法标准原文附录A运算示例可以推知。）

<img width="405" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/1c6fc3fc-6d34-4963-a663-1ec7b3b086ca">

**二、消息扩展算法**
-
记第i个512比特的消息分组为𝑀<sub>0</sub><sup>𝑖</sup>,...,𝑀<sub>15</sub><sup>𝑖</sup>

按如下步骤生成132个32比特的消息字：

- For t=0 to 15
  
  𝑊<sub>t</sub> = 𝑀<sub>t</sub><sup>𝑖</sup>
    
- For t=16 to 67
  
  𝑊<sub>t</sub> = 𝑃<sub>1</sub>(𝑊<sub>t-16</sub>⨁𝑊<sub>t-9</sub>⨁(𝑊<sub>t-3</sub>⋘15))⨁(𝑊<sub>t-1</sub>⋘7)⨁𝑊<sub>t-6</sub>
    
- For t=0 to 63
  
  𝑊<sub>t</sub><sup>'</sup>=𝑊<sub>t</sub> ⨁𝑊<sub>t+4</sub>

<img width="344" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/c27a19b4-f963-4d1b-8e7d-834ca88f7706">

**三、压缩函数**
-
初始IV是固定的常数

<img width="414" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/f212a09b-850e-4362-8930-47c94e61d4e6">

<img width="637" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/1a08cfc1-7702-4782-892f-dedeb04b8818">

**迭代压缩**

<img width="546" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/56817cf5-2ea0-42ce-9fe1-fe1990b83a2b">

**四、具体实现**
-
1、使用了Loop Unrolling循环展开优化

<img width="215" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/8787ac15-eaa9-44ea-b811-6c13e7f00c5b">

2、使用了移位等操作代替乘除模

<img width="574" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/5d1c3af8-0fcf-445f-931d-6db0eee877b6">

运行方式:全局变量MESS为需要hash的信息，一个元素一个字节，int变量

**优化前**

<img width="434" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/44ea5964-a56e-4126-a793-cdd2b8ee783a">

**优化后**

<img width="437" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/8ee8bd4a-9169-49a2-a9c7-a57e7ad06380">

**使用OpenSSL库**

<img width="185" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/40f69c6e-3c07-45ce-b44c-dbd149bbaaea">

最后用图像来表示更为直观一些：

![image](https://github.com/QiusuoJC/homework_group28/assets/123710102/4f6e8a5e-0629-4c3a-af6b-abfce96838a4)

**五、参考**
-
【1】https://blog.csdn.net/qq_40662424/article/details/121637732

【2】https://zhuanlan.zhihu.com/p/129692191

【3】上课PPT：SM3
