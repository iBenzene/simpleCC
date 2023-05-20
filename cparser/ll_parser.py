from .ll_table import get_table
from .grammar import get_grammar_begin, derivate
from typing import Union
from os import PathLike


FilePath = Union[str, "PathLike[str]"]

def _log(no, csymbol, nsymbol, action):
    """记录语法分析器的一次行为"""
    _fout.write("%s#%s\t%s\n" % (csymbol, nsymbol, action))


def parse(input: FilePath, output: FilePath):
    """
    LL 语法分析器:
        根据词法分析结果进行语法分析, 
        通过查找预测分析表, 生成最右推导序列
    """
    istr = []
    # 读取词法分析结果, 
    # 将单词符号及其类别以二元组的方式存储到输入串列表 istr 中
    try:
        with open(input, 'r') as f:
            lines = f.readlines()
            for line in lines:
                istr.append(tuple(line.replace('\n', '').split('\t')))
    except Exception as e:
        print("语法分析错误:", e)
        return
    
    # 打开输出的目标文件
    global _fout
    _fout = open(output, 'w')

    istr.append(('#', '<EOF>'))
    parsing_table = get_table()

    no = 0                               # 序号
    stack = ['#', get_grammar_begin()]  # 符号栈

    while True:
        if istr[0][1] == '<IDN>':
            csymbol = 'IDN'
        elif istr[0][1] == '<INT>':
            csymbol = 'INT'
        else:
            csymbol = istr[0][0]
        no += 1

        # 栈顶符号与面临的输入符号相同
        if stack[-1] == csymbol:
            # 栈顶符号和面临的输入符号都是文本终结符, 接受输入符号串, 语法分析完成
            if csymbol == '#':
                _log(no, 'EOF', 'EOF', 'accept')
                break

            # 栈顶符号和面临的输入符号都是某个终结符, 跳过
            else:
                _log(no, stack[-1], csymbol, 'move')
                stack.pop()
                istr.pop(0)

        # 栈顶符号为非终结符, 查看预测分析表
        else:
            # 表项为产生式, 推导
            if isinstance(parsing_table[csymbol][stack[-1]], tuple):
                _log(no, stack[-1], 'EOF' if csymbol == '#' else csymbol, 'reduction')
                production = parsing_table[csymbol][stack[-1]]
                nsymbols = derivate(stack.pop(), production)
                nsymbols.reverse()
                stack += nsymbols

            # 表项为「error」, 发现语法错误
            elif parsing_table[csymbol][stack[-1]] == 'error':
                _log(no, 'EOF' if stack[-1] == '#' else stack[-1],
                     'EOF' if csymbol == '#' else csymbol, 'error')
                _fout.close()
                raise NotImplementedError("存在语法错误, 暂不支持自动恢复, 分析中止")
            
    # 关闭输出的目标文件
    _fout.close()
