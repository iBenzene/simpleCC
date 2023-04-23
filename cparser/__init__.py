"""
语法分析器
--------
功能:
    输入C--语言的单词符号序列, 输出用规范规约产生语法树的「移进-规约」序列.

输出格式:
    [序号][TAB][栈顶符号]#[面临的输入符号][TAB][执行动作]

    执行动作包括「reduction 规约」,「move 移进」,「accept 接受」和「error 出错」

"""

from .lr_parser import parse
