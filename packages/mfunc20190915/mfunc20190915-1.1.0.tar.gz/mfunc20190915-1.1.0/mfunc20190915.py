# -*- coding:utf-8 -*-
"""
__title__ = ''
__author__ = 'Miles'
__mtime__ = '2019/9/11'
# Bitter cold adds keen fragrance to plum blossom.
This is the standard way to include a multiple-line comment in your code.
"""

def print_lol(the_list):
    for each in the_list:
        if(isinstance(each,list)):
            print_lol(each)
        else:
            print(each)
