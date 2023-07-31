**Impl Merkle Tree following RFC6962**
-
Merkle Tree，又称哈希树（Hash Tree）或加密树（Cryptographic Tree），是一种基于哈希的树状数据结构，用于验证和管理大量数据的完整性和有效性。它由Ralph Merkle在1979年首次提出，现在被广泛应用于分布式系统、加密货币和区块链等领域。

**一、Merkle Tree**
-
为了方便自己与看到这个md文件的大家能够理解，这里首先根据参考【1】讲述一下Merkle Tree的发展

1、Hash

Hash函数大家非常熟悉，就是一个把任意长度的数据映射成固定长度数据的函数。例如，对于数据完整性校验，最简单的方法是对整个数据做Hash运算得到固定长度的Hash值，然后把得到的Hash值公布在网上，这样用户下载到数据之后，对数据再次进行Hash运算，比较运算结果和网上公布的Hash值进行比较，如果两个Hash值相等，说明下载的数据没有损坏。可以这样做是因为输入数据的稍微改变就会引起Hash运算结果的面目全非，而且根据Hash值反推原始输入数据的特征是困难的。

如果从一个稳定的服务器进行下载，采用单一Hash是可取的。但如果数据源不稳定，一旦数据损坏，就需要重新下载，这种下载的效率是很低的。于是有了以下的Hash List

2、Hash List

在点对点网络中作数据传输的时候，会同时从多个机器上下载数据，而且很多机器可以认为是不稳定或者不可信的。为了校验数据的完整性，更好的办法是把大的文件分割成小的数据块（例如，把分割成2K为单位的数据块）。这样的好处是，如果小块数据在传输过程中损坏了，那么只要重新下载这一快数据就行了，不用重新下载整个文件。

为了确定小的数据块没有损坏，只需要为每个数据块做Hash。BT（Bit Torrent）下载的时候，在下载到真正数据之前，我们会先下载一个Hash列表。而为了确定这个Hash列表本身是正确的，需要把每个小块数据的Hash值拼到一起，然后对这个长字符串再作一次Hash运算，这样就得到Hash列表的根Hash(Top Hash or Root Hash)。下载数据的时候，首先从可信的数据源得到正确的根Hash，就可以用它来校验Hash列表了，然后通过校验后的Hash列表校验数据块。

![NL~L@ LTR@MKCXS{JD}~R)O](https://github.com/QiusuoJC/homework_group28/assets/123710102/f9046317-fca4-4809-8803-98872a1decef)


3、Merkle Tree

Merkle Tree的基本思想是，将一组数据分成不同的块，并对每个块计算Hash。然后，将这些Hash按照一定的规则组合成一个新的Hash，作为它们的父节点的Hash值。不断重复这个过程，直到所有的Hash值都被组合成一个唯一的根Hash值，即Merkle Tree的根节点。

具体来说，Merkle Tree在最底层，和Hash List一样，我们把数据分成小的数据块，有相应的hash和它对应。但是往上走，并不是直接去运算根hash，而是把相邻的两个hash合并成一个字符串，然后运算这个字符串的hash。如果最底层的hash总数是单数，那到最后必然出现一个单着的hash，这种情况就直接对它进行hash运算，所以也能得到它的hash。于是往上推，依然是一样的方式，可以得到数目更少的新一级hash，最终必然形成一棵倒挂的二叉树，到了根节点的这个位置，就剩下一个根hash了，我们把它叫做 Merkle Root。

![B}D3 `E)67`@H9_@Z}6HWK6](https://github.com/QiusuoJC/homework_group28/assets/123710102/5c1e4d79-b595-4965-a165-f00281b5a707)

在p2p网络下载网络之前，先从可信的源获得文件的Merkle Tree树根。一旦获得了树根，就可以从其他从不可信的源获取Merkle tree。通过可信的树根来检查接受到的Merkle Tree。如果Merkle Tree是损坏的或者虚假的，就从其他源获得另一个Merkle Tree，直到获得一个与可信树根匹配的Merkle Tree。

Merkle Tree和Hash List的主要区别是，可以直接下载并立即验证Merkle Tree的一个分支。因为可以将文件切分成小的数据块，这样如果有一块数据损坏，仅仅重新下载这个数据块就行了。如果文件非常大，那么Merkle tree和Hash list都很到，但是Merkle tree可以一次下载一个分支，然后立即验证这个分支，如果分支验证通过，就可以下载数据了。而Hash list只有下载整个hash list才能验证。


**二、Merkle Tree特点**
-
1、Merkle Tree是一种树，大多数是二叉树，也可以多叉树，无论是几叉树，它都具有树结构的所有特点；

2、Merkle Tree的叶子节点的value是数据集合的单元数据或者单元数据HASH。

3、非叶子节点的value是根据它下面所有的叶子节点值，然后按照Hash算法计算而得出的。

**三、Merkle Tree操作**
-
1、创建Merkle Tree

2、检索数据块

3、更新、插入和删除

本次实验只用到了创建Merkle Tree，其余详细的操作可以见参考【1】【2】

**四、具体实现**
-
这里实现时，使用Hash函数SHA256进行hash运算

1、创建一个Merkle Tree包含10w个节点

   step1：对所有原始数据计算Hash值；注意当数据长度为奇数时，需要将最后一个Hash值再计算一次hash
   
   <img width="405" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/af90a451-54e6-415e-b4cd-ff056a0c5520">

   step2：相邻两个hash块串联，然后再做hash，不断重复这个过程，最后只剩一个hash值即为最后的Merkle Tree的根节点

   <img width="412" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/96e0e4d4-e4c9-488a-832c-76d44bda9f7d">

   step3：用gen_leafNode()函数随机生成10w个节点，每个元素包含3个字符的节点
   
   <img width="521" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/e1e9c064-95d9-4628-b364-cd6ed9466a7a">

2、进行inclusion proof（包含性证明）

inclusion proof是一种证明某个元素包含在Merkle树中的方法，其由一组哈希值构成的列表组成，这些哈希值是从包含该元素的叶子节点到根节点的路径上的所有节点的哈希值，以及在该路径上的每个节点的兄弟节点的哈希值。通过将这些哈希值按照顺序放入一个列表中，我们可以使用包含证明来证明某个元素包含在Merkle树中。使用包含证明，我们可以在不传输整个Merkle树的情况下证明某个元素包含在其中。

3、进行exclusion proof（排除性证明）

exclusion proof是一种证明某个元素不包含在Merkle树中的方法。其也由一组哈希值构成的列表组成，这些哈希值是从包含该元素的叶子节点到根节点的路径上的所有节点的兄弟节点的哈希值。排除证明不包含包含该元素的叶子节点的哈希值以及在该路径上的每个节点的哈希值。通过将这些哈希值按照顺序放入一个列表中，我们可以使用排除证明来证明某个元素不包含在Merkle Tree中。使用排除证明，我们可以在不传输整个Merkle树的情况下证明某个元素不包含在其中。

使用时，我们使用以下两个元素来验证：

<img width="345" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/0310e938-a35f-403d-aabb-12a54e190c78">

最终的输出结果如下：

<img width="927" alt="image" src="https://github.com/QiusuoJC/homework_group28/assets/123710102/3020cc10-3845-4580-a009-076b7d17536a">

**五、参考**
-
【1】https://blog.csdn.net/wo541075754/article/details/54632929

【2】https://crypto.stackexchange.com/questions/22669/merkle-hash-tree-updates

【3】上课PPT：SM3
