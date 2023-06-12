# File content: About the whole process of CTR forecasting
# Usage: run this file

#coding=utf-8
import csv
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

from CTRF_Data.CTRF_Csv import csv_read_current_column, create_update_datafile_save_file
from CTRF_Data.CTRF_DB import write_data_word_table, create_new_word_value_tables, read_word_value_from_DB, \
    close_DB_sever
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
    # Customization
    # -----------------------------------------------------------------------------------------------------------
    # columns = ['创意标题', '创意描述1', '创意描述2', '点击率', '平均点击价格', '展现']
    columns = ['点击率', '平均点击价格']
    initial_csv_dir = 'E:\Project\CTRF\Data\Initial\\2023-05-08'
    # path_dir = 'E:\\Project\\CTRF\\Data\\Columns\\2023-05-22'
    Columns_txt_dir_name = 'text_column'
    # need_transform_item = ['title', 'desc1', 'desc2']
    need_transform_item = []
    items_float_file_name = 'items_float.txt'
    TrainingSet_file_name = 'TrainingSet.csv'
    # TrainingSet_file_name = 'Training.csv'
    predict_result_file = 'predict_CTR_base_ACP.xlsx'
    # -----------------------------------------------------------------------------------------------------------
    # Don`t change next part except developer

    # Processing stream
    # -----------------------------------------------------------------------------------------------------------
    # 一、将Initial的原始文件找到有用列，提取到相应的Columns列文件txt
    # get three text columns csv
    columns_mes, path_dir = batch_get_text_column_csv(initial_csv_dir, columns)

    # todo 手动剔除无效词

    # 二、列文件txt计算词值，str-->float，并写入DB对应word_value table
    if need_transform_item:
        create_new_word_value_tables()
        # Columns_txt_dir = 'E:/Project/CTRF/Data/Columns/2023-05-11/text_column'
        Columns_txt_dir = os.path.join(path_dir, Columns_txt_dir_name)
        table_name = ''
        if os.path.exists(Columns_txt_dir):
            for file_name in os.listdir(Columns_txt_dir):
                file_name_base, extension = os.path.splitext(file_name)
                table_name = select_word_value_table_name(file_name_base)
                if table_name == 'No match table':
                    continue
                else:
                    file_full_path = os.path.join(Columns_txt_dir, file_name)
                    words_float_to_DB(filepath=file_full_path, table_name=table_name)

            # 三、计算字段值
            # 1、计算items_float.txt 一表有多个相同词就按相加计算：word_value = word_value1 + word_value2 + ...
            title_list = []
            desc1_list = []
            desc2_list = []
            items_float_list = []
            for item in need_transform_item:
                # item_txt_path = 'E:\\Project\\CTRF\\Data\\Columns\\2023-05-11\\{}.txt'.format(item)
                item_txt_path = os.path.join(Columns_txt_dir, '{}.txt'.format(item))
                table_name = select_word_value_table_name(item)
                word_value_dict = read_word_value_from_DB(table_name)
                mes_items_value_list = compute_item_value(item_txt_path, word_value_dict)
                if item == 'title':
                    title_list = mes_items_value_list
                elif item == 'desc1':
                    desc1_list = mes_items_value_list
                elif item == 'desc2':
                    desc2_list = mes_items_value_list

            for title, desc1, desc2 in zip(title_list, desc1_list, desc2_list):
                # items_float = title*0.25 + desc1*0.15 + desc2*0.10
                items_float = title + desc1 + desc2
                items_float_list.append(items_float)

            # print(len(items_float_list))
            save_path = os.path.join(path_dir, items_float_file_name)
            # save_path = os.path.join('E:\\Project\\CTRF\\Data\\Columns\\2023-05-11', 'items_float.txt')
            with open(save_path, 'w') as f:
                for i in items_float_list:
                    f.write(str(i) + '\n')
            # print(len(items_float_list))


    # 2、字段拼接、获取训练集csv
    float_value_dict = {}
    # path_dir = 'E:\\Project\\CTRF\\Data\\Columns\\2023-05-12'
    for float_file in os.listdir(path_dir):
        float_file_path = os.path.join(path_dir, float_file)
        file_name_base, extension = os.path.splitext(float_file)
        if os.path.isfile(float_file_path):
            float_value_list = []
            with open(float_file_path, 'r') as f:
                float_value = f.readlines()
                for i in float_value:
                    float_value_list.append(i)
            float_value_dict[file_name_base] = float_value_list

        dataframe = pd.DataFrame(float_value_dict)
        dataframe.to_csv(os.path.join(path_dir, TrainingSet_file_name), sep=',', index=False)

    # 四、预测
    trainning_file = os.path.join(path_dir, TrainingSet_file_name)
    list_r = []
    if os.path.exists(trainning_file):
        # read data without '\n'
        with open(trainning_file, encoding='gbk') as f:
            r = csv.reader(f)
            for row in r:
                row = [col.replace('\n', '').replace('\r', '') for col in row]
                list_r.append(row)
        # astype()或to_numeric() 改变df数据类型
        df = pd.DataFrame(list_r[1:], columns=list_r[0])
        # print(df.head(2)) # print out two data row, if no num in (), default print out 5 rows
        df = df.astype(float)
        # # df.plot(kind='line')
        # # plt.show()
        train, test = train_test_split(df, test_size=0.2, random_state=1234)
        train = train.reset_index(drop=True)
        test = test.reset_index(drop=True)
        X_train, X_test = train.iloc[:, :-1], test.iloc[:, :-1]
        Y_train, Y_test = train.iloc[:, -1], test.iloc[:, -1]

        # 数据标准化（主要是为了构建支持向量机做准备）
        print('数据标准化----------------------------------')
        scaler = StandardScaler()
        x_scaler = scaler.fit(X_train)
        x_train = x_scaler.fit_transform(X_train)
        x_test = x_scaler.fit_transform(X_test)

        y_scaler = scaler.fit(Y_train.values.reshape(-1, 1))
        y_train = y_scaler.fit_transform(Y_train.values.reshape(-1, 1)).ravel()
        y_test = y_scaler.fit_transform(Y_test.values.reshape(-1, 1))
        # 支持向量机
        print('SVR----------------------------------')
        rbf_svr =SVR(kernel='rbf', C=10000, gamma=0.1)
        # rbf_svr =SVR(kernel='poly', C=1000, gamma=0.1)
        rbf_svr.fit(x_train, y_train)

        # 预测
        print('预测----------------------------------')
        rbf_svr_pred = rbf_svr.predict(x_test)
        y_scaler = scaler.fit(Y_train.values.reshape(-1, 1))
        y_scaler.fit_transform(Y_train.values.reshape(-1, 1))
        rbf_svr_pred = y_scaler.inverse_transform(rbf_svr_pred.reshape(-1, 1))

        # 模型评价
        print('模型评价1----------------------------------')
        rbf_svr_rmse = np.sqrt(mean_squared_error(Y_test, rbf_svr_pred))  # RMSE
        rbf_svr_mae = mean_absolute_error(Y_test, rbf_svr_pred)  # MAE
        rbf_svr_r2 = r2_score(Y_test, rbf_svr_pred)  # R2

        print("R^2 of RBF_SVR: ", rbf_svr_r2)
        print("The RMSE of RBF_SVR: ", rbf_svr_rmse)
        print("The MAE of RBF_SVR: ", rbf_svr_mae)

        # 输出预测值和真实值矩阵
        print('输出预测值和真实值矩阵----------------------------------')
        predict_result_file_full = os.path.join(path_dir, predict_result_file)
        rbf_svr_pred_true = pd.concat([pd.DataFrame(rbf_svr_pred), pd.DataFrame(Y_test)], axis=1)
        rbf_svr_pred_true.columns = ['pre_CTR', 'real_CTR']
        rbf_svr_pred_true.to_excel(predict_result_file_full, index=False)


    # 五、相关系数
    if os.path.exists(predict_result_file_full):
        data = pd.read_excel(predict_result_file_full)

        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None)
        # 禁止Dateframe自动换行(设置为Flase不自动换行，True反之)
        # pd.set_option('expand_frame_repr', False)
        print(data.corr())
        # print(data['avg_click_price'].corr(data['items_float']))
    # compare_excel_dir = 'E:\\PythonProjects\\CTRForecast\\compare_excel'
    # for i in os.listdir(compare_excel_dir):
    #     print(i)
    #     file_path_full = os.path.join(compare_excel_dir, i)
    #     data = pd.read_excel(file_path_full)
    #     print(data.corr())



    # 五、拟合

    # final step
    close_DB_sever()
    pass

SteamRun()

    
