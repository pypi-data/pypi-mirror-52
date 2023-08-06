#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : hash_util.py
@Desc    : 签名计算，加密计算，哈希值计算等
"""
import hashlib
import base64


def process_appkey(app_key):
    """
    完美api签名计算规则之一，固定的appkey剪裁
    :param app_key:
    :return:
    """
    enc_key = app_key[2:5] + app_key[10:16] + app_key[18:20] + app_key[14:19]
    return enc_key


def wanmei_api_sign(param, app_key, verbose=True):
    """
    计算完美api签名
    :param param: 所有url参数字典，当中可能含有sign参数，需要排除
    :param app_key: app秘钥
    :param verbose:
    :return:
    """
    # if len(app_key) > 30:
    # app_key = process_appkey(app_key)
    # 按参数的键值做排序
    keys = list(param.keys())
    keys.sort()
    text_array = []
    for key in keys:
        if key == "sign":
            continue
        value = str(param[key])
        text_array.append(key)
        text_array.append("=")
        # 限制最长参数值为500
        if len(value) > 500:
            value = value[:500]
        text_array.append(value)
        text_array.append("&")
    # 去除最后一个&
    text_array = text_array[:-1]
    text_to_sign = "".join(text_array)
    sign = salt_SHA256(app_key, text_to_sign)
    if verbose:
        print("text_to_sign:", text_to_sign)
        print("sign=", sign)
    return sign


def salt_SHA256(salt, word):
    """
    带盐的sha256加密算法
    :param salt:
    :param word:
    :return:
    """
    hsobj = hashlib.sha256(salt.encode("utf-8"))
    hsobj.update(word.encode("utf-8"))
    result = hsobj.digest()
    result = base64.b64encode(result).decode("utf-8")
    return result


# @timer
def md5sum(filename):
    """
    计算文件md5值,在计算小文件时没有问题
    :param filename:
    :return:
    """
    fd = open(filename, "rb")
    fcont = fd.read()
    fd.close()
    fmd5 = hashlib.md5(fcont)
    return fmd5.hexdigest()


# @timer
def md5sum2(filename):
    """
      计算文件md5值,通过流式读取文件进行计算，比较适合用于大文件
      :param filename:
      :return:
      """
    m = hashlib.md5()
    n = 1024 * 4
    inp = open(filename, 'rb')
    while True:
        buf = inp.read(n)
        if buf:
            m.update(buf)
        else:
            break
    return m.hexdigest()
