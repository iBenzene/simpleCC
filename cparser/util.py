from .grammar import get_grammar, get_grammar_begin


# 终结符列表
_terminal = [
    '#',    # 文本结束符
    'IDN',  # 标识符
    'INT',  # 整数
    '+', '-', '*', '/', '%',
    '=', '>', '<', '!',
    '==', '<=', '>=', '!=',             # 运算符
    'int', 'void', 'return', 'const',   # 关键字
    '(', ')', '{', '}', ';', ',',       # 界符
]

# 所有符号列表
_all_symbols = []

def get_all_symbols():
    """访问存储所有符号的列表"""
    global _all_symbols
    if not _all_symbols:
        for left, right in get_grammar().items():
            if left not in _all_symbols:
                _all_symbols.append(left)
            for symbols in right:
                for symbol in symbols:
                    if symbol not in _all_symbols:
                        _all_symbols.append(symbol)
    return _all_symbols


def _derivate(symbol: str) -> list:
    """根据文法字典中的产生式规则进行推导"""
    if symbol in get_grammar():
        return get_grammar()[symbol]
    else:
        print("错误: 未知符号 %s" % symbol)


def first(expr: list) -> list:
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
    
    _first = []
    
    # 表达式为一个非终结符
    if len(expr[p:]) == 1:
        next = _derivate(expr[p])
        for next_symbols in next:
            _first += first(next_symbols)
        return _first

    # 表达式由非终结符开头, 且有效长度大于 1
    for symbol in expr[p:]:
        temp = first([symbol])
        if '$' in temp:
            temp.remove('$')
            _first += temp
        else:
            _first += temp
            return _first
    _first.append('$')
    return _first


def follow(expr: str) -> list:
    """计算表达式的 FOLLOW 集合"""
    _follow = []

    # 表达式为拓广文法的开始符号
    if expr == get_grammar_begin():
        return ['#']
    
    # 表达式为其它非终结符
    grammar_dict = get_grammar()
    for left, right in grammar_dict.items():
        for symbols in right:
            if expr not in symbols:
                continue
            expr_idx = symbols.index(expr)

            if expr_idx < len(symbols) - 1:
                # 对于产生式「A -> αBβ」
                temp = first([symbols[expr_idx + 1]])
                if '$' in temp:
                    temp.remove('$')
                    if left != expr:
                        _follow += follow(left)
                _follow += temp
            else:
                # 对于产生式「A -> αB」
                if left != expr:
                    _follow += follow(left)
    return _follow  
    