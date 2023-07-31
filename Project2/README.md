**Implement the ρ method of reduced SM3**
-
Hash函数的ρ方法是用来寻找散列碰撞而不需要大量的内存。它的想法是不断地对前一个哈希运算的结果进行哈希运算。

当我们对一个起始值进行散列，然后对该散列进行散列，并重复这个过程，不会永远得到不同的数字。

最终我们会得到一个重复的值，之后所有进一步的值都是之前值的重复，在一个循环中进行，如下图所示。

<img width="290" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/b79e71e2-a4d0-4b54-b5a9-bacc76bd8400">

**一、低存储复杂度的寻找碰撞：ρ方法**
-
不同于生日攻击，ρ方法寻找碰撞只需要很少的存储空间，工作方式如下：

1、给定一个n-bit长的hash函数，随机选择hash值H1，并定义H<sub>1</sub>=H<sub>1</sub><sup> '</sup> 

2、计算H<sub>2</sub>=Hash(H<sub>1</sub>)，并计算H<sub>2</sub><sup>' </sup>=Hash(Hash(H<sub>1</sub><sup>' </sup>))。即在第一个情形中，我们应用一次Hash函数，而第二个情形中，我们应用两次

3、迭代这个过程并计算H<sub>i+1</sub>=Hash(H<sub>i</sub>)，H<sub>i+1</sub><sup>'</sup> =Hash(Hash(H<sub>i</sub><sup>'</sup> ))，直到计算到第i个数，满足H<sub>i+1</sub>=H<sub>i+1</sub><sup>'</sup> 

更进一步的寻找碰撞的技术的工作原理是：

首先检测循环的开始，然后查找碰撞。既不需要在内存中存储大量的值，也不需要对长的列表进行排序。

ρ方法大约需要2<sup>n/2</sup> 次操作才能成功。

平均来说，循环和尾部（图中从H<sub>1</sub>延伸到H<sub>5</sub>的部分）各包括约2<sup>n/2</sup> 个哈希值，其中n是哈希值的长度 

因此，我们需要至少2<sup>n/2</sup> + 2<sup>n/2</sup> 次计算来发现一个碰撞。

**二、具体实现**
-
本次实验我们对前4个字节，即前32bit进行碰撞测试

测试结果如下

<img width="359" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/d2a796be-aa59-43a7-ae39-2c294eec03df">

**三、参考**
-
【1】https://samsclass.info/141/proj/C106.htm#:~:text=The%20Rho%20method%20is%20used%20to%20find%20hash,do%20when%20calculating%20password%20hashes%20with%20many%20rounds.

【2】Serious Cryptography：A Practical Introduction to Modern Encryption by Jean-Philippe Aumasson

【3】上课PPT：SM3
