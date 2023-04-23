"""
文法生成模块

功能:
    根据提供的文法文件 grammar.txt 来生成拓广文法.
    
"""
import os


# 存储拓广文法的字典
_grammar_dict = {}

# 拓广文法的开始符号
_grammar_begin = ''

def _load_grammar():
    """从文法文件 grammar.txt 中加载文法产生式, 生成文法产生式字典"""
    grammar_path = os.path.join(os.path.dirname(__file__), 'grammar.txt')

    # 读取文法文件 grammer.txt
    with open(grammar_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            symbols = line.split()
            symbols.remove('->')
            if lines.index(line) == 0:
                global _grammar_begin
                _grammar_begin = symbols[0]
            global _grammar_dict
            if symbols[0] in _grammar_dict:
                _grammar_dict[symbols[0]].append([symbol for symbol in symbols[1:]])
            else:
                _grammar_dict[symbols[0]] = [[symbol for symbol in symbols[1:]]]


def _get_grammar():
    """访问文法产生式字典"""
    if not _grammar_dict:
        _load_grammar()
    return _grammar_dict


def _get_grammar_begin():
    """获取文法的开始符号"""
    if not _grammar_begin:
        _load_grammar()
    return _grammar_begin


def _derivate(symbol: str) -> list:
    """推导"""
    if symbol in _get_grammar():
        return _get_grammar()[symbol]
    else:
        print("错误: 未知符号 %s" % symbol)


def _reduce(symbols: list, production: tuple) -> str:
    """
    规约
    production 参数要求是一个二元组, 对应一个产生式, 
    第一个元素为产生式左端, 第二个元素为产生式右端符号的列表
    """
    try:
        if production[1] == symbols:
            return production[0]
    except:
        pass
    print("错误: %s 规约失败" % symbols)
