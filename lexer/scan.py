import pandas as pd
import string

from . import FSM
from ._type import keyword, operator, boundary


def _print_token(token, tp):
    """打印识别出的 token 及其所属的符号类型"""
    _f.write("%s\t<%s>\n" %(token, tp))


def _analyse_token(token):
    """分析 token, 将识别出的 token 输入有限状态自动机"""
    # 空 token, 直接返回
    if token == "":
        return
    
    # 判断 token 是否为关键字
    if token in keyword:
        _print_token(token, 'KW')
        return

    # 判断 token 是否为由两个字符组成的运算符
    if token in (operator['relational'] + operator['logical']):
        _print_token(token, 'OP')
        return
    
    # 判断 token 是否为半个关系运算符
    if token in operator['half']:
        _print_token(token, 'OP')
        return
    
    # 判断 token 是否为位运算符
    if token in operator['bitwise']:
        _print_token(token, 'OP')
        return

    # 将 token 输入有限状态自动机
    fstate = _fsm.mathch(token)
    if fstate == 2:
        _print_token(token, 'IDN')
    elif fstate == 3 or fstate == 4:
        _print_token(token, 'INT')
    else:
        print("词法分析错误: token 分析失败")


def scan(filepath, outpath):
    """"""
    # 打开源文件
    try:
        f = open(filepath, 'r')
    except:
        print("错误: 打开文件 %s 失败" % filepath)
        return
    
    # 读取源文件
    lines = f.readlines()
    f.close()

    # 创建用于词法分析的有限状态自动机
    delta = pd.DataFrame([
        {
            **{'': 0},  # 空串
            **{chr: 1 for chr in (string.ascii_uppercase + string.ascii_lowercase)},    # 大写或小写字母
            **{'_': 1}, # 下划线
            **{str(digit): 4 for digit in range(1, 10)}, # 数字 1-9
            **{str(0): 6}    # 数字
        },  # 初态

        {'': [1, 2]},   # 状态 1

        {
            **{'': [2, 3]},     # 空串
            **{chr: 2 for chr in (string.ascii_uppercase + string.ascii_lowercase)},    # 大写或小写字母
            **{'_': 1},         # 下划线
            **{str(digit): 2 for digit in range(0, 10)}, # 数字 0-9
        },              # 状态 2

        {'': 3},        # 状态 3

        {'': [4, 5]},   # 状态 4

        {
            **{'': [5, 6]},   # 空串
            **{str(digit): 5 for digit in range(0, 10)}, # 数字 0-9
        },              # 状态 5

        {'': 6}         # 状态 6
    ])

    global _fsm
    _fsm = FSM(delta, [0], [3, 6])
    _fsm.nfa2dfa()
    _fsm.minimize_dfa()

    # 打开输出的目标文件
    global _f
    _f = open(outpath, 'w')

    # 开始逐行逐字扫描源代码, 将识别出的 token 输入有限状态自动机
    token = ""
    for line in lines:
        for chr in line:
            # 当扫描到换行符和文本分隔符, 包括空格和制表符
            if chr in ('\n', ' ', '\t'):
                _analyse_token(token)
                token = ""
                continue             

            # 当扫描到界符
            if chr in boundary:
                _analyse_token(token)
                _print_token(chr, 'SE')
                token = ""
                continue
            
            # 当扫描到敏感运算符
            if chr in operator['half']:
                # 检查 token 是否也是半个关系运算符, 如果是且当前读入的是等号, 则说明扫描到了由2个字符组成的关系运算符
                if token in operator['half']:
                    if chr == '=':
                        token += chr
                        _analyse_token(token)
                        token = ""
                    else:
                        _print_token(token, 'OP')
                        _print_token(chr, 'OP')
                        token = ""
                else:
                    _analyse_token(token)
                    token = chr      
                continue

            if chr in operator['bitwise']:
                # 检查 token 是否也是位运算符, 如果是且当前读入了与 token 相同的位运算符, 则说明扫描到了由2个字符组成的逻辑运算符
                if token in operator['bitwise']:
                    if token == chr:
                        token += chr
                        _analyse_token(token)
                        token = ""
                    else:
                        _print_token(token, 'OP')
                        _print_token(chr, 'OP')
                        token = ""
                else:
                    _analyse_token(token)
                    token = chr
                continue

            # 当扫描到算术运算符
            if chr in operator['arithmetic']:
                _analyse_token(token)
                _print_token(chr, 'OP')
                token = ""
                continue

            # 当扫描到的并非特殊字符
            token += chr
    
    # 关闭输出的目标文件
    _f.close()