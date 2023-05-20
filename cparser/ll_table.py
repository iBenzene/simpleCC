"""
预测分析表生成模块

功能:
    根据文法产生式字典来构造预测分析表, 支持 LL(1) 分析法.
    
"""
import pandas as pd
from .util import get_grammar, get_all_symbols, first, follow, _terminal


# 预测分析表
_parsing_table = pd.DataFrame()


def _generate_table():
    """生成预测分析表"""
    grammar_dict = get_grammar()

    all_symbols = get_all_symbols().copy()
    if '$' in all_symbols:
        all_symbols.remove('$')

    global _parsing_table
    _parsing_table = pd.DataFrame([{symbol: 'error' for symbol in _terminal}], index=list(set(all_symbols) - set(_terminal)))
    for left, right in grammar_dict.items():
        for symbols in right:
            # 对于文法的每一个产生式「A -> α」
            production = (left, [] if symbols == ['$'] else symbols)
            for asymbol in first(symbols):
                # 对于每个 FIRST(α) 中的终结符 a
                if asymbol == '$':
                    # 当该终结符 a 为空时, 对于每个 FOLLOW(A) 中的终结符 b, 把「A -> α」加入表中 b 对应的表项
                    for bsymbol in follow(left):
                        _parsing_table[bsymbol][left] = production
                else:
                    # 否则把「A -> α」加入表中 a 对应的表项
                    _parsing_table[asymbol][left] = production


def get_table():
    """访问预测分析表"""
    if _parsing_table.empty:
        _generate_table()
    return _parsing_table