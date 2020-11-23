
"""
# coding:utf-8
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from pandas import Series
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# "D:\pychar\FilmTest\templates\movie.csv"
# new4 = pd.read_csv('new4.csv', encoding='UTF-8', index_col="title")

Film_reader = pd.read_csv('movie.csv', encoding='UTF-8')
Film_reader.head(5)

"""

"""

import csv
with open('D:\\pychar\\FilmTest\\templates\\movie.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    film = list(reader)

index_0 = 1000
print("First record of film, 电影名称[0]:{0}, 豆瓣评论数[1]:{1}, 豆瓣评分[2]:{2} \n"
      "                      上映日期[3]:{3}, 主演[4]:{4}, 制片国家/地区[5]:{5}  \n"
      "                       又名[6]:{6},     导演[7]:{7},   片长[8]:{8}           \n"
      "                       类型[9]:{9},     编剧[10]:{10},   语言[11]:{11}           \n"
      "                        r5[12]:{12}, r4[13]:{13}, r3[14]:{14}  , r2[15]:{15}, r1[16]:{16}    \n"
      .format(film[index_0][0], film[index_0][1], film[index_0][2], film[index_0][3], film[index_0][4],
              film[index_0][5], film[index_0][6], film[index_0][7], film[index_0][8], film[index_0][9],
              film[index_0][10], film[index_0][11], film[index_0][12], film[index_0][13],
              film[index_0][14], film[index_0][15], film[index_0][16]))

"""
