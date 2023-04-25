from .table import _get_table
from .grammar import _reduce
from typing import Union
from os import PathLike


FilePath = Union[str, "PathLike[str]"]

def _log(no, csymbol, nsymbol, action):
    """记录语法分析器的一次行为"""
    _fout.write("%d\t%s#%s\t%s\n" % (no, csymbol, nsymbol, action))


def parse(input: FilePath, output: FilePath):
    """
    LR 语法分析器:
        根据词法分析结果进行语法分析, 
        通过查找 LR 分析表, 生成「移进-规约」序列
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
    parsing_table = _get_table()

    no = 0          # 序号
    states = [0]    # 状态栈
    symbols = []    # 符号栈

    while True:
        if istr[0][1] == '<IDN>':
            csymbol = 'IDN'
        elif istr[0][1] == '<INT>':
            csymbol = 'INT'
        else:
            csymbol = istr[0][0]
        no += 1
        
        # 表项为状态, 移进
        if isinstance(parsing_table[csymbol][states[-1]], int):
            _log(no, 'EOF' if not symbols else symbols[-1], istr[0][0], 'move')
            states.append(parsing_table[csymbol][states[-1]])
            symbols.append(csymbol)
            istr.pop(0)

        # 表项为产生式, 规约
        elif isinstance(parsing_table[csymbol][states[-1]], tuple):
            _log(no, symbols[-1], 'EOF' if istr[0][1] == '<EOF>' else istr[0][0], 'reduction')
            production = parsing_table[csymbol][states[-1]]

            rlen = len(production[1])
            csymbols = [symbols.pop() for _ in range(rlen)]
            csymbols.reverse()
            nsymbol = _reduce(csymbols, production)
            symbols.append(nsymbol)

            for _ in range(rlen):
                states.pop()
            nstate = parsing_table[nsymbol][states[-1]]
            states.append(nstate)

        # 表项为「accept」, 接受输入符号串, 语法分析完成
        elif parsing_table[csymbol][states[-1]] == 'accept':
            _log(no, symbols[-1], 'EOF', 'accept')
            break

        # 表项为「error」, 发现语法错误
        elif parsing_table[csymbol][states[-1]] == 'error':
            _log(no, 'EOF' if not symbols else symbols[-1], 
                 'EOF' if istr[0][1] == '<EOF>' else istr[0][0], 'error')
            _fout.close()
            raise NotImplementedError("存在语法错误, 暂不支持自动恢复, 分析中止")

    # 关闭输出的目标文件
    _fout.close()
