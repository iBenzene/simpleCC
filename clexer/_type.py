"""定义具体的单词符号类型"""

# 关键字
_keyword = ['int', 'void', 'return', 'const']

# 运算符
_operator = {
    'arithmetic': ['+', '-', '*', '/', '%'],
    'half': ['=', '>', '<', '!'],
    'relational': ['==', '<=', '>=', '!='],
    'bitwise': ['&', '|'],
    'logical': ['&&', '||']
}

# 界符
_boundary = ['(', ')', '{', '}', ';', ',']


# """定义单词符号类型的正则表达式"""

# # 标识符
# _identifier = "[a-zA-Z_][a-zA-Z_0-9]*"

# # 整数
# _integer = "0|([1-9][0-9]*)"
