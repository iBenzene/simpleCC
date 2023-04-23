from .grammar import _get_grammar, _derivate


# 终结符列表
# _terminal = [
#     '$',    # 空
#     '#',    # 文本结束符
#     'IDN',  # 标识符
#     'INT',  # 整数
#     '+', '-', '*', '/', '%',
#     '=', '>', '<', '!',
#     '==', '<=', '>=', '!=',             # 运算符
#     'int', 'void', 'return', 'const',   # 关键字
#     '(', ')', '{', '}', ';', ',',       # 界符
# ]
_terminal = [
    '$',        # 空
    '#',        # 文本结束符
    'a', 'b'    # 终结符, <T>
]

# 所有符号列表
_all_symbols = []

def _get_all_symbols():
    """访问存储所有符号的列表"""
    global _all_symbols
    if not _all_symbols:
        for left, right in _get_grammar().items():
            if left not in _all_symbols:
                _all_symbols.append(left)
            for symbols in right:
                for symbol in symbols:
                    if symbol not in _all_symbols:
                        _all_symbols.append(symbol)
    return _all_symbols


def _first(expr: list) -> list:
    """计算表达式的 FIRST 集合"""

    # p 为表达式第一个有意义符号的索引, 
    # 由于表达式可能由若干个空符号开头, 
    # 因此需要对其进行修正
    p = 0
    while expr[p] == '$':
        p += 1
        if p == len(expr):
            # 意味着表达式为空串
            return ['$']

    # 表达式的第一个符号为终结符
    if expr[p] in _terminal:
        return [expr[p]]
    
    first = []
    
    # 表达式为一个非终结符
    if len(expr[p:]) == 1:
        next = _derivate(expr[p])
        for next_symbols in next:
            first += _first(next_symbols)
        return first

    # 表达式由非终结符开头, 且有效长度大于 1
    for symbol in expr[p:]:
        temp = _first([symbol])
        if '$' in temp:
            temp.remove('$')
            first += temp
        else:
            first += temp
            return first
    first.append('$')
    return first


def _follow(expr: str) -> list:
    """计算表达式的 FOLLOW 集合"""
    raise NotImplementedError("暂未实现表达式 FOLLOW 集合的计算")
    