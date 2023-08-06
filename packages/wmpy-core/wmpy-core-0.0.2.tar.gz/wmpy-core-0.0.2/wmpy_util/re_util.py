#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : re_util.py
@Desc    : 通过正则表达式处理字符串工具模块
"""
import re
import traceback


def hump2underline(hump_str):
    '''
    驼峰形式字符串转成下划线形式
    :param hump_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    '''
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', hump_str).lower()
    return sub


def underline2hump(underline_str):
    '''
    下划线形式字符串转成驼峰形式
    :param underline_str: 下划线形式字符串
    :return: 驼峰形式字符串
    '''
    # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
    sub = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), underline_str)
    # sub = re.sub(r'(_\w)', lambda x: trans(x), underline_str)
    return sub


array_word_pattern = re.compile(r'^(?P<key>\w*)(?P<bracket>\[(?P<index>\d*)\])?$')


def process_array_word(array_word):
    """
    处理数组格式的文字.eg num[0]，返回实际key和对应的index .eg ('num', 0)
    :return:
    """
    try:
        match = array_word_pattern.match(array_word)
        if match is not None:
            key = match.group("key")
            bracket = match.group("bracket")
            index = match.group("index")
            index_num = None
            if bracket is not None:
                if index == "":
                    index_num = 0
                else:
                    index_num = int(index)
            return key, index_num
    except Exception as error:
        print(traceback.print_exc())
    return None, None


def remove_num(text):
    """
    移除文字当中的数字
    :param text:
    :return:
    """
    p = re.compile(r'\d')
    return re.sub(p, '', text)


def trans(x):
    print(x)
    g = x.group(0)
    g1 = g[1]
    return x.group(1)[1].upper()


if __name__ == '__main__':
    # a = hump2underline("cBuildCondtion")
    # print(a)
    # print(underline2hump(a))
    # print(remove_num("港口城市1"))
    # result = process_array_word(None)
    result = process_array_word("num[0]")
    result = process_array_word("fail_num")
    print(result)
