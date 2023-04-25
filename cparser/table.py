"""
分析表生成模块

功能:
    根据文法产生式字典来构造 LR(1) 分析表.
    
"""
import os
import pandas as pd
from .grammar import _get_grammar_begin
from .util import _get_grammar, _get_all_symbols, _first, _terminal


# LR(1) 分析表
_parsing_table = pd.DataFrame()


class Item:
    """
    LR(1) 项目, 由以下属性构成
        target: 产生式左部符号
        done: 产生式右部已分析完成的符号列表
        undone: 产生式右部未分析完成的符号列表
        lookahead: 展望串列表, 对于 LR(1) 文法, 每个展望串的长度为 1
    """
    def __init__(self, target, done, undone):
        self.target = target
        self.done = done.copy()
        self.undone = undone.copy()
        self.lookahead = ''

    # 重载「==」运算符
    def __eq__(self, obj):
        if isinstance(obj, Item) and \
            self.target == obj.target and \
            self.done == obj.done and \
            self.undone == obj.undone and \
            self.lookahead == obj.lookahead:
            return True
        else:
            return False
        
    # 对象拷贝
    def copy(self):
        new = Item(self.target, self.done, self.undone)
        new.lookahead = self.lookahead
        return new


def _items_closure(items, all):
    """构造 LR(1) 项目集的闭包"""
    closure = items.copy()
    items_ = closure.copy()
    while True:
        new = []
        for item in items_:
            # 如果项目为「A -> α·Bβ, a」
            if item.undone and item.undone[0] not in _terminal:
                if len(item.undone) == 1:
                    # β 为空时
                    followit = '$'
                else:
                    followit = item.undone[1]
                
                # 找到所有形如「B -> ·ξ, b」的项目
                next = []
                for oth_item in all:
                    if oth_item.target == item.undone[0] and not oth_item.done:
                        next.append(oth_item)

                # 对于每一个终结符 b, 如果「B -> ·ξ, b」不在闭包中, 则把它加进去
                for next_item in next:
                    for symbol in _first([followit, item.lookahead]):
                        temp = next_item.copy()
                        temp.lookahead = symbol
                        if temp not in closure:
                            closure.append(temp)
                            new.append(temp)
        if not new:
            break
        items_ = new.copy()
    return closure


def _items_go(items, symbol, all):
    """项目集转换函数"""
    next = []
    for item in items:
        if item.undone and item.undone[0] == symbol:
            item_ = item.copy()
            item_.done.append(item_.undone[0])
            item_.undone.pop(0)
            next.append(item_)
    return _items_closure(next, all)


def _generate_table():
    """生成 LR(1) 分析表"""
    grammar_dict = _get_grammar()
    grammar_begin = _get_grammar_begin()

    # 根据文法的产生式规则生成项目
    all_items = []
    for left, right in grammar_dict.items():
        for symbols in right:
            if symbols == ['$']:
                all_items += [Item(left, [], [])]
            else:
                symbols_len = len(symbols)
                items_ = [Item(left, symbols[:i], symbols[i:]) for i in range(symbols_len + 1)]
                all_items += items_

    # 构造 LR(1) 项目集规范族
    collection = []
    all_items[0].lookahead = '#'
    collection.append(_items_closure([all_items[0]], all=all_items))

    all_symbols = _get_all_symbols().copy()
    all_symbols.remove(grammar_begin)
    if '$' in all_symbols:
        all_symbols.remove('$')

    collection_ = collection.copy()
    while True:
        new = []
        for items in collection_:
            for symbol in all_symbols:
                next = _items_go(items, symbol, all=all_items)
                if next and next not in collection:
                    collection.append(next)
                    new.append(next)
        if not new:
            break
        collection_ = new

    # 根据项目集规范族和项目集转换函数构造 LR(1) 语法分析表
    global _parsing_table
    _parsing_table = pd.DataFrame([{symbol: 'error' for symbol in (all_symbols + ['#'])} for _ in collection])
    for items in collection:
        for item in items:
            if item.undone:
                # 面临终结符需要移进或面临非终结符需要跳转
                next = _items_go(items, item.undone[0], all=all_items)
                if next in collection:
                    _parsing_table[item.undone[0]][collection.index(items)] = collection.index(next)
            else:
                if item.target == grammar_begin:
                    # 面临终结符需要接受
                    _parsing_table['#'][collection.index(items)] = 'accept'
                else:
                    # 面临终结符需要规约
                    production = (item.target, item.done)
                    _parsing_table[item.lookahead][collection.index(items)] = production
    
    # 缓存 LR（1） 分析表, 供以后使用
    _parsing_table.to_csv(table_path, sep=',', index=False, header=True)


def _load_table():
    """
    从分析表文件 table.txt 中加载 LR(1) 分析表, 
    若分析表文件不存在, 则自动生成一张 LR(1) 分析表
    """
    global table_path
    table_path = os.path.join(os.path.dirname(__file__), 'table.txt')
    try:
        global _parsing_table
        _parsing_table = pd.read_csv(table_path)
        for index in _parsing_table.index:
            for column in _parsing_table.columns:
                try:
                    _parsing_table[column][index] = eval(_parsing_table[column][index])
                except NameError:
                    pass
    except:
        _generate_table()


def _get_table():
    """访问 LR(1) 分析表"""
    if _parsing_table.empty:
        _load_table()
    return _parsing_table
