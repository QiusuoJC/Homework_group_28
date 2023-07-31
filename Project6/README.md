**Impl this protocol with actual network communication**
-
利用hash函数实现range proof（范围证明）

**一、Range proof**
-
首先我们根据参考【1】来介绍一下什么是Range proof（范围证明）

Range proof（范围证明）是一种特殊的零知识证明，用于证明一个给定的数值在一个区间内，同时不泄露任何关于这个整数的信息。

一个对承诺值的典型的零知识范围证明（ZKRP）涉及密码学承诺和证明。承诺必须满足隐藏和绑定的条件，而证明必须满足完备性、合理性和零知识性。ZKRPs已经被用于在区块链上构建私人交易和以太坊上具有隐私保护的智能合约。它们还被提议用于处理偿付能力证明、电子投票和拍卖系统的隐私以及匿名凭证。

ZKRPs的一些应用存在于这样的环境中：可信实体充当生成或验证整数数值的承诺的权威。作为一个说明性的例子，考虑这样一个设定：公民希望向服务提供商证明他们的年龄超过一定的阈值，同时不透露他们自己的出生日期。受信任的实体（例如政府身份提供者）可以发布声明，承诺证明者的年龄，并且证明者有能力使用ZKRP协议生成证明，使验证者相信他们的年龄确实高于所要求的阈值。

尽管上述场景可以用现有的ZKRP结构（如Bulletproofs或Pedersen commitment）来解决，但在资源受限的环境中，这些解决方案通常不太实用，因为非对称密钥加密操作被认为是昂贵的。在需要频繁地生成和验证这些证明的应用程序中，专注于实现更简单、轻量级的原语可能是一个更有吸引力的选择。

**二、Range proof with hash function**
-
Hash函数可以帮助构建Range proof

假设我们要证明一个数值x在一个区间[a, b]内，其中a和b是已知的上限和下限。我们可以使用一个哈希函数H，将x和一个随机数r作为输入，产生一个哈希值h = H(x, r)。然后，我们可以将h与一个特定的比较值c进行比较，以证明x在指定区间内。比较值c的选择取决于所需的证明强度和精度。

阈值c的选取：

c = H(a, r) + (x - a) * H(b - a, r)

其中，H(a, r)和H(b - a, r)是使用相同的随机数r和哈希函数H计算的哈希值。如果h小于等于c，则我们可以证明x在区间[a, b]内。

参考【1】的论文中介绍了他们的工作：使用Hash函数来完成range proof，并构建了一个新的协议：HashWires。

虽然本次project并没有完全用到以下的参考文献，但是在学习零知识证明以及range proof时还找到了其他介绍这些知识的好的文章便一并放到了参考中。

**三、具体实现**
-
根据上述过程可以完成本次project：

<img width="469" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/c7ee9534-195a-4a37-bc5f-5157d68f3ef1">


1、Alice构造证明

<img width="580" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/ea2c09dd-1a97-4f1c-a8ac-65aab9a65d4d">

2、Bob验证证明

<img width="577" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/f1254170-82ec-4601-b071-efdb87d7e78c">

当Alice用实际年龄时（43岁），可以得到验证通过：

<img width="149" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/ae9cc64e-ed0a-41d9-abbd-b005143240b4">

当欺骗者以不到21岁的年龄进行欺骗时（如20岁），则可以发现无法通过验证：

<img width="925" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/5d094f30-e2e9-43a5-9b8b-fdbf27fe6ad3">

**四、参考**
-
【1】https://eprint.iacr.org/2021/297.pdf

【2】https://zkproof.org/2021/05/05/hashwires-range-proofs-from-hash-functions/

【3】https://arxiv.org/abs/1907.06381

【4】https://blog.csdn.net/weixin_41746734/article/details/115030537

【5】https://cloud.tencent.com/developer/article/1682725

【6】上课PPT--SM3
