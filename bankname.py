#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author by wangcw @ 2025
# @generate at 2025/2/7 10:37
# comment: 银行信息爬取

import re
import time
from urllib import request
from urllib.request import urlopen
import pandas as pd
from datetime import datetime
import os


def timeCounter(fun):
    def wrapper(*arg, **kwargs):
        startTime = time.time()
        fun(*arg, **kwargs)
        endTime = time.time()
        print(f"{fun.__name__}运行时间为{endTime - startTime:.2f}秒")

    return wrapper


# 获取页面信息
def getPageInfo(url):
    try:
        pageInfo = urlopen(url)
        content = pageInfo.read().decode('utf-8')
        return content
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        print("由于网络原因，上述网页的解析并没有成功。请检查网页链接的合法性，并适当重试。")
        return None


# 利用正则匹配获取信息
def getInfo(data):
    pattern = r'<a rel="nofollow" href="(http.*?)".*?>\s+(.+?)\s+?</a>'
    info = re.findall(pattern, data)
    return info


@timeCounter
def main():
    url = 'http://www.cbrc.gov.cn/chinese/jrjg/index.html'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.63.6788.400 QQBrowser/10.3.2864.400"
    reqObj = request.Request(url, headers={'User-Agent': user_agent})
    pageInfo = getPageInfo(reqObj)

    if pageInfo is None:
        return

    # 获取数据
    data = getInfo(pageInfo)

    # 确保 files 文件夹存在
    files_dir = "files"
    os.makedirs(files_dir, exist_ok=True)

    # 生成文件名，包含日期
    current_date = datetime.now().strftime("%Y%m%d")
    file_name = f"银行信息_{current_date}.xlsx"
    file_path = os.path.join(files_dir, file_name)

    # 将数据转换为 DataFrame
    if data:
        df = pd.DataFrame(data, columns=["银行名称", "网址"])
        # 将 DataFrame 写入 Excel 文件
        df.to_excel(file_path, index=False, engine='openpyxl')
        print(f"Data has been written to {file_path}.")
    else:
        print("No data to write to Excel file.")


if __name__ == '__main__':
    main()
