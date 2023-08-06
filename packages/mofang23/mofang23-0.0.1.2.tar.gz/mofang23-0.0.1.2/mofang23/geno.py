# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     geno
   Description :
   Author :        Asdil
   date：          2019/5/8
-------------------------------------------------
   Change Activity:
                   2019/5/8:
-------------------------------------------------
"""
__author__ = 'Asdil'
import pandas as pd
import gzip

# 识别过滤的行数
def skipRow(path, key):
    skip = 0
    with open(path, 'r') as f:
        for line in f:
            if key == line[:len(key)]:
                return skip
            skip += 1
    return skip


# 读取call文件
def readCall(path, key='probeset_id'):
    df = pd.read_table(path, skiprows=skipRow(path, key), low_memory=False)
    return df


# 读取vcf
def readVcf(path, key='#CHROM'):
    df = pd.read_table(path, skiprows=skipRow(path, key), low_memory=False)
    return df

def skipRowGZ(path):
    skiprows = 0
    with gzip.open(path, 'rb') as f:
        for line in f:
            line = line.decode('utf-8')
            if line[0] != '#':
                break
            skiprows += 1
    skiprows -= 1
    print(skiprows)
    return skiprows

# 读取vcf
def readVcfGZ(path):
    df = pd.read_table(path, skiprows=skipRowGZ(path), low_memory=False)
    return df