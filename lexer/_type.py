"""定义具体的单词符号类型"""

# 关键字
keyword = ['int', 'void', 'return', 'const']

# 运算符
operator = {
    'arithmetic': ['+', '-', '*', '/', '%'],
    'half': ['=', '>', '<', '!'],
    'relational': ['==', '<=', '>=', '!='],
    'bitwise': ['&', '|'],
    'logical': ['&&', '||']
}

# 界符
boundary = ['(', ')', '{', '}', ';', ',']


# """定义单词符号类型的正则表达式"""

# # 标识符
# identifier = "[a-zA-Z_][a-zA-Z_0-9]*"

# # 整数
# integer = "0|([1-9][0-9]*)"