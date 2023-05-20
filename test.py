import cparser
import clexer
import os


# 测试样例目录
samples_dir = 'samples'

# 遍历所有的测试样例
for sample_name in os.listdir(samples_dir):
    sample_dir = os.path.join(samples_dir, sample_name)
    if not os.path.isdir(sample_dir):
        continue

    # 首先测试词法分析器
    input_file = os.path.join(sample_dir, '{}.txt'.format(sample_name))
    temp_file = 'temp_lexical.txt'
    with open(temp_file, 'w') as temp:
        clexer.scan(input_file, temp_file)
    expected_file = os.path.join(sample_dir, '{}_lexical.txt'.format(sample_name))

    with open(temp_file) as temp, open(expected_file) as expected:
        if temp.read() == expected.read():
            print('[\033[32mOK\033[0m]Test lexer succeed for {}'.format(sample_name))
        else:
            print('[\033[31mFailed\033[0m]Test lexer failed for {}'.format(sample_name))

    # 接着测试 LL(1) 语法分析器
    input_file = temp_file
    temp_file = "temp_grammar.txt"
    try:
        with open(temp_file, 'w') as temp:
            cparser.ll_parse(input_file, temp_file)
    except:
        # 忽略语法分析器的报错
        pass
    expected_file = os.path.join(sample_dir, '{}_grammar.txt'.format(sample_name))

    with open(temp_file) as temp, open(expected_file) as expected:
        if temp.read() == expected.read():
            print('[\033[32mOK\033[0m]Test parser succeed for {}'.format(sample_name))
        else:
            print('[\033[31mFailed\033[0m]Test parser failed for {}'.format(sample_name))

    os.remove(temp_file)
    os.remove(input_file)