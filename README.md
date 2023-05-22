# 简易的编译器前端

本项目为一个简易的编译器前端，包括词法分析器、语法分析器、语义分析和中间代码生成（暂未实现）。

C-- 语言是该编译器的源语言，这是一个 C 语言的子集。相比于 C 语言，C-- 语言是单文件的，去除了 C 语言中的文件包含、宏定义、指针、结构体等比较复杂的特性。

项目内的词法分析器和语法分析器可以组成一个完整的编译流程，针对输入的 C-- 语言源码，可以输出词法分析器的单词符号序列和语法分析器的分析状态序列。

其中，语法分析器支持 LL(1)、LR(0)、LR(1) 三种文法，由于目前实现的 C-- 文法不属于 LR 文法，因此语法分析器暂时只能使用  LL(1) 分析器。

## 运行方法

我们提供了一个自动化测试脚本，在 `samples/` 目录下的所有测试样例上测试词法分析器和 LL(1) 语法分析器。

``` shell
python3 test.py
```

如果需要自行测试词法分析器或语法分析器，我们也提供了相关的接口方法以供调用。

词法分析器封装在包 `clexer` 下，用于对 C-- 源码进行词法扫描和分析的接口方法为 `scan` 方法。

语法分析器封装在包 `cparser` 下，用于对 C-- 源码的单词符号序列进行语法分析的接口方法为 `ll_parser` 方法。

这两个方法在调用时，都分别接收两个必要参数，用于指定输入文件路径和输出文件路径。

下面给出一个调用词法分析器和语法分析器的示例，假设输入的源码文件是 `demo.c` 。

```python
import clexer
import cparser

# 对「demo.c」进行词法分析, 结果保存在「demo_lexical」
clexer.scan("demo.c", "demo_lexical")

# 对「demo_lexical」进行语法分析, 结果保存在「demo_grammar」
cparser.ll_parse("demo_lexical", "demo_grammar")
```
