**Implement the naïve birthday attack of reduced SM3**
-

实现精简版SM3的生日攻击

**一、生日攻击**
-
生日攻击是基于生日悖论建立的一种攻击方式，这种攻击可以在较小的时间内以至少1/2找到一组碰撞

**生日问题**

假设有m (m<365)个人，他们的生日在一年（365天）中均匀分布，为保证这m个人中，至少有两人生日相同的概率大于1/2，m应取多大？

答案：m=23, 考虑m个人生日都不同的概率

<img width="577" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/393ff35a-2899-4b54-8da5-c7f915a234ca">

**Hash函数的生日攻击**

定理：设杂凑函数h的输出值长n比特，则经过约2<sup>n/2 </sup>次杂凑运算，找到一对碰撞(x, x')的概率大于1/2

- 输出值长n比特 -> N = 2<sup>n </sup>
- N<sup>1/2 </sup> = 2<sup>n/2 </sup>

通过不断随机选择随机字符串进行hash，并将hash值记录下来，每次做完hash都将本次的hash值与之前进行对比，当找到相同的hash值时，说明我们找到了一组碰撞


**二、具体实现**
-

在本次实验中，我们选择对前32bit进行碰撞测试

运行方式：

attack函数的参数，num为攻击次数，n为碰撞长度，length为进行碰撞测试的字符串长度

<img width="249" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/8c6d2f49-d6c5-41f2-aeeb-7b117ad0b9fd">

如图所示就是找到的一对长度为8字节，hash值前28bit碰撞的字符串

<img width="208" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/86ea2276-b393-4f17-9876-909553f05bc7">


