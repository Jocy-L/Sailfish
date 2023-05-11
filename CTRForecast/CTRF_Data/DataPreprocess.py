# File content:
# Usage:

#coding=utf-8
import datetime
import os

import jieba
import numpy as np
import pandas as pd
from sklearn import preprocessing

from CTRF_Data.CTRF_Csv import csv_read_current_column

# path = 'C:/Users/11/Documents/WXWork/1688855519447112/Cache/File/2023-04/关键词427.csv'
# # if encoding=’utf-8’ wrong try encoding=GB2312/gbk/ISO-8859-1
# df = pd.read_csv(path, low_memory=False, encoding='gbk')
# # Cut the columns of data that need to be processed
# t = df.iloc[:, 8:]
#
# columns = {
#     '展现': 'MM_Manual_show',
#     '点击': 'MM_Manual_click',
#     '消费': 'MM_Manual_spend',
#     '点击率': 'MM_Manual_CTR',
#     '平均点击价格': 'MM_Manual_avg_click_price',
#     '上方位平均排名': 'MM_Manual_avg_top_No.',
#     '上方位展现': 'MM_Manual_show_top',
#     '上方位点击': 'MM_Manual_top_click',
#     '上方位消费': 'MM_Manual_top_spend',
#     '上方展现胜出率': 'MM_Manual_top_win_rate',
#     '上方展现胜出率(精确)': 'MM_Manual_top_win_rate_exact',
#
#     0: 'MM_Manual_show',
#     1: 'MM_Manual_click',
#     2: 'MM_Manual_spend',
#     3: 'MM_Manual_CTR',
#     4: 'MM_Manual_avg_click_price',
#     5: 'MM_Manual_avg_top_No.',
#     6: 'MM_Manual_show_top',
#     7: 'MM_Manual_top_click',
#     8: 'MM_Manual_top_spend',
#     9: 'MM_Manual_top_win_rate',
#     10: 'MM_Manual_top_win_rate_exact'
# }
#
# # Three standardized ways
# # ----- min-max -----
# MM_Manual = (t - t.min()) / (t.max() - t.min())
# MM_Manual.rename(columns=columns, inplace=True)
#
# MM_Auto = preprocessing.minmax_scale(t)
# MM_Auto_arry_to_data = pd.DataFrame(MM_Auto)
# MM_Auto_arry_to_data.rename(columns=columns, inplace=True)
#
#
# # ----- Z-score -----
# ZS_Manual = (t - t.mean()) / (t.std())
# ZS_Auto = preprocessing.scale(t)
#
#
# # ----- Decimal calibration normalization [-1,1] -----
# TT = t / 10 ** np.ceil(np.log10(t.abs().max()))
# TT.rename(columns=columns, inplace=True)
#
#
# # Stitch table data
# # mix_data = pd.concat([df, MM_Manual], axis=1)
# # mix_data = pd.concat([df, MM_Auto_arry_to_data], axis=1)
# # mix_data = pd.concat([df, ZS_Manual], axis=1)
# # mix_data = pd.concat([df, ZS_Auto], axis=1)
# # mix_data = pd.concat([df, TT], axis=1)
# # pd.set_option('display.max_columns', 50)
# # pd.set_option('display.width', 1000)
# # print(mix_data)


# ------------------------------------------------------------------------------------------------------------
from CTRF_Data.CTRF_DB import read_word_value_from_DB


def word_segmentation(filepath):
    with open(filepath, 'r') as f:
        str = f.read()
    # Search mode
    words = jieba.lcut_for_search(str)
    # All mode
    # words = jieba.lcut(str, cut_all=True)
    # Precision mode
    # words = jieba.lcut(str, cut_all=True)
    counts = {}
    words_dict = {}
    for word in words:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1

    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    for i in range(len(items)):
        word, counts = items[i]
        words_dict[word] = counts

    # print(words_dict)
    return words_dict

def words_to_float(words_dict):
    words_times = 0
    words_value_dict = {}
    for value in words_dict.values():
        words_times += value
    for key, value in words_dict.items():
        word_value = value / words_times
        words_value_dict[key] = word_value
    return words_value_dict

# # E:\Project\CTRF\Data\WordSegmentation
# filepath = 'E:/Project/CTRF/Data/Columns/2023-05-08/desc1.txt'
# words_dict = word_segmentation(filepath)
# words_to_float(words_dict)


def compute_item_value(item_txt_path, word_value_dict):
    with open(item_txt_path, 'r') as f:
        columns_mes = f.readlines()
        mes_items_value_list = []
        for mes in columns_mes:
            mes_words = jieba.lcut_for_search(mes)
            # print(mes_words)
            item_sum = 0
            alive_word = 0
            for word in mes_words:
                if word in word_value_dict.keys():
                    item_sum += word_value_dict[word]
                    alive_word += 1
            try:
                mes_item_value = item_sum / alive_word
            except:
                mes_item_value = 0
            mes_items_value_list.append(mes_item_value)
            # print('{}:{}/{}'.format(mes_item_value, item_sum, alive_word))
    return mes_items_value_list



# item_txt_path = 'E:\\Project\\CTRF\\Data\\Columns\\2023-05-11\\title.txt'
# # item_value(item_txt_path)
# word_value_dict = ''
# compute_item_value(item_txt_path, word_value_dict)