# File content:
# Usage:

#coding=utf-8
import os

import pandas as pd

from CTRF_Data.CTRF_Csv import csv_read_current_column, create_update_datafile_save_file
from CTRF_Data.CTRF_DB import write_data_word_table, create_new_word_value_tables, read_word_value_from_DB
from CTRF_Data.DataPreprocess import word_segmentation, words_to_float, compute_item_value


def batch_get_text_column_csv(initial_csv_dir, columns):
    for file_name in os.listdir(initial_csv_dir):
        file_full_path = os.path.join(initial_csv_dir, file_name)
        columns_mes = csv_read_current_column(file_full_path, columns)
        # print(columns_mes['desc1'])
        # print(type(columns_mes['desc1']))
        path_dir = create_update_datafile_save_file(columns_mes)

    return columns_mes, path_dir

def words_float_to_DB(filepath, table_name):
    words_dict = word_segmentation(filepath)
    words_float_dict = words_to_float(words_dict)
    for key, value in words_float_dict.items():
        write_data_word_table(table_name=table_name, word=key, value=value)

def select_word_value_table_name(file_name_base):
    if 'desc' in file_name_base:
        table_name = 'ctrf_desc_words'
    elif 'title' in file_name_base:
        table_name = 'ctrf_title_words'
    else:
        table_name = 'No match table'
    return table_name


def SteamRun():
    # # 一、将Initial的原始文件找到有用列，提取到相应的Columns列文件txt
    # # get three text columns csv
    # columns = ['创意标题', '创意描述1', '创意描述2', '点击率', '平均点击价格', '展现']
    # initial_csv_dir = 'E:\Project\CTRF\Data\Initial\\2023-05-07'
    # columns_mes, path_dir = batch_get_text_column_csv(initial_csv_dir, columns)

    # todo 手动剔除无效词

    # # 二、列文件txt计算词值，str-->float，并写入DB对应word_value table
    # create_new_word_value_tables()
    # # Columns_txt_dir = 'E:/Project/CTRF/Data/Columns/2023-05-11/text_column'
    # Columns_txt_dir = os.path.join(path_dir, 'text_column')
    # table_name = ''
    # if os.path.exists(Columns_txt_dir):
    #     for file_name in os.listdir(Columns_txt_dir):
    #         file_name_base, extension = os.path.splitext(file_name)
    #         table_name = select_word_value_table_name(file_name_base)
    #         if table_name == 'No match table':
    #             continue
    #         else:
    #             file_full_path = os.path.join(Columns_txt_dir, file_name)
    #             words_float_to_DB(filepath=file_full_path, table_name=table_name)

        # # 三、计算字段值
        # # 1、计算items_float.txt 一表有多个相同词就按相加计算：word_value = word_value1 + word_value2 + ...
        # need_transform_item = ['title', 'desc1', 'desc2']
        # title_list = []
        # desc1_list = []
        # desc2_list = []
        # items_float_list = []
        # for item in need_transform_item:
        #     # item_txt_path = 'E:\\Project\\CTRF\\Data\\Columns\\2023-05-11\\{}.txt'.format(item)
        #     item_txt_path = os.path.join(Columns_txt_dir, '{}.txt'.format(item))
        #     table_name = select_word_value_table_name(item)
        #     word_value_dict = read_word_value_from_DB(table_name)
        #     mes_items_value_list = compute_item_value(item_txt_path, word_value_dict)
        #     if item == 'title':
        #         title_list = mes_items_value_list
        #     elif item == 'desc1':
        #         desc1_list = mes_items_value_list
        #     elif item == 'desc2':
        #         desc2_list = mes_items_value_list
        #
        # for title, desc1, desc2 in zip(title_list, desc1_list, desc2_list):
        #     items_float = title*0.25 + desc1*0.15 + desc2*0.10
        #     items_float_list.append(items_float)
        #
        # # print(len(items_float_list))
        # save_path = os.path.join(path_dir, 'items_float.txt')
        # # save_path = os.path.join('E:\\Project\\CTRF\\Data\\Columns\\2023-05-11', 'items_float.txt')
        # with open(save_path, 'w') as f:
        #     for i in items_float_list:
        #         f.write(str(i) + '\n')
        # # print(len(items_float_list))


        # # 2、字段拼接、获取训练集csv
        # float_value_dict = {}
        # for float_file in os.listdir(path_dir):
        #     float_file_path = os.path.join(path_dir, float_file)
        #     file_name_base, extension = os.path.splitext(float_file)
        #     if os.path.isfile(float_file_path):
        #         float_value_list = []
        #         with open(float_file_path, 'r') as f:
        #             float_value = f.readlines()
        #             for i in float_value:
        #                 float_value_list.append(i)
        #         float_value_dict[file_name_base] = float_value_list
        #
        #     dataframe = pd.DataFrame(float_value_dict)
        #     dataframe.to_csv(os.path.join(path_dir, 'TrainingSet.csv'), sep=',', index=False)

    # 四、SVR
    # 五、拟合

    # # final step
    # final_step = close_DB_sever()
    pass

SteamRun()
