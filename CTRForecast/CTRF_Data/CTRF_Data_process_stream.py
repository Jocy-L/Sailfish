# File content:
# Usage:

#coding=utf-8
import datetime
import json
import os

import jieba

from CTRF_Data.CTRF_Csv import csv_read_current_column, create_update_datafile_save_file


def batch_get_text_column_csv(initial_csv_dir, columns):
    for file_name in os.listdir(initial_csv_dir):
        full_file_path = os.path.join(initial_csv_dir, file_name)
        columns_mes = csv_read_current_column(full_file_path, columns)
        create_update_datafile_save_file(columns_mes)

# # get three text columns csv
# columns = ['创意标题', '创意描述1', '创意描述2']
# initial_csv_dir = 'E:\Project\CTRF\Data\Initial\\2023-05-07'
# batch_get_text_column_csv(initial_csv_dir, columns)

def word_segmentation(filepath):
    file_dir, file_name = os.path.split(filepath)
    file_name_base, extension = os.path.splitext(file_name)
    work_package = file_name_base
    save_dir = 'E:\Project\CTRF\Data\WordSegmentation'
    save_file_full = os.path.join(save_dir, '{}\{}.txt'.format(datetime.date.today(), work_package))
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

    print(words_dict)
    with open(save_file_full, 'w', encoding='utf-8') as fw:
    # with open('depart_word_all.txt', 'a+', encoding='utf-8') as fw:
    #     fw.write('{} {}\n'.format(word, counts))
        fw.write(str(words_dict))


# E:\Project\CTRF\Data\WordSegmentation
filepath = 'E:/Project/CTRF/Data/Columns/2023-05-08/desc1.txt'
word_segmentation(filepath)
