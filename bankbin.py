#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author by wangcw @ 2025
# @generate at 2025/2/7 10:17
# comment: 2025最新银联卡BIN表

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import os

# 初始化一个空的列表，用于存储所有行的数据
data = []
headers = []

# 从第一页开始循环
i = 1
while True:
    url = f'https://www.chakahao.com/bin/bin_{i}.html'
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        print("No more data available. Exiting loop.")
        break  # 如果请求失败，直接退出循环

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_="table card-table table-vcenter")

    if table:
        if not headers:
            headers = [header.text.strip() for header in table.find_all('th')]

        rows = table.find_all('tr')[1:]  # 获取表格中的所有行（跳过表头）
        if not rows:
            print(f"No data found on page {i}. Exiting loop.")
            break  # 如果没有数据，退出循环
        else:
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    row_data = [col.text.strip() for col in cols]
                    data.append(row_data)
    else:
        print(f"No table found on {url}. Exiting loop.")
        break  # 如果没有找到表格，退出循环

    i += 1  # 增加页码
    time.sleep(0.1)  # 控制请求频率

# 确保 files 文件夹存在
files_dir = "files"
os.makedirs(files_dir, exist_ok=True)

# 生成文件名，包含日期
current_date = datetime.now().strftime("%Y%m%d")
file_name = f"2025最新银联卡BIN表_{current_date}.xlsx"
file_path = os.path.join(files_dir, file_name)

# 将数据转换为 DataFrame
if headers and data:
    df = pd.DataFrame(data, columns=headers)
    # 将 DataFrame 写入 Excel 文件
    df.to_excel(file_path, index=False, engine='openpyxl')
    print(f"Data has been written to {file_path}.")
else:
    print("No data to write to Excel file.")
