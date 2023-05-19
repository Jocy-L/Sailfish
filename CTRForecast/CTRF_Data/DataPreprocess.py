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

# -----------------------------------------------------------------------------------------------------------
# 四、SVR
    # trainning_file = os.path.join(path_dir, TrainingSet_file_name)
    # list_r = []
    # if os.path.exists(trainning_file):
    #     # read data without '\n'
    #     with open(trainning_file, encoding='gbk') as f:
    #         r = csv.reader(f)
    #         for row in r:
    #             row = [col.replace('\n', '').replace('\r', '') for col in row]
    #             list_r.append(row)
    #     # astype()或to_numeric() 改变df数据类型
    #     df = pd.DataFrame(list_r[1:], columns=list_r[0])
    #     # print(df.head(2)) # print out two data row, if no num in (), default print out 5 rows
    #     # df = df.astype(float)
    #     # df.plot(kind='line')
    #     # plt.show()
    #     train, test = train_test_split(df, test_size=0.2, random_state=1234)
    #     train = train.reset_index(drop=True)
    #     test = test.reset_index(drop=True)
    #     X_train, X_test = train.iloc[:, :-1], test.iloc[:, :-1]
    #     Y_train, Y_test = train.iloc[:, -1], test.iloc[:, -1]
    #
    #     # 数据标准化（主要是为了构建支持向量机做准备）
    #     print('数据标准化----------------------------------')
    #     scaler = StandardScaler()
    #     x_scaler = scaler.fit(X_train)
    #     x_train = x_scaler.fit_transform(X_train)
    #     x_test = x_scaler.fit_transform(X_test)
    #
    #     y_scaler = scaler.fit(Y_train.values.reshape(-1, 1))
    #     y_train = y_scaler.fit_transform(Y_train.values.reshape(-1, 1)).ravel()
    #     y_test = y_scaler.fit_transform(Y_test.values.reshape(-1, 1))
    #     # 支持向量机
    #     rbf_svr =SVR(kernel='rbf', C=100, epsilon=0.1)
    #     rbf_svr.fit(x_train, y_train)
    #
    #     # 预测
    #     print('预测----------------------------------')
    #     rbf_svr_pred = rbf_svr.predict(x_test)
    #     y_scaler = scaler.fit(Y_train.values.reshape(-1, 1))
    #     y_scaler.fit_transform(Y_train.values.reshape(-1, 1))
    #     rbf_svr_pred = y_scaler.inverse_transform(rbf_svr_pred.reshape(-1, 1))
    #
    #     # 模型评价
    #     print('模型评价1----------------------------------')
    #     rbf_svr_rmse = np.sqrt(mean_squared_error(Y_test, rbf_svr_pred))  # RMSE
    #     rbf_svr_mae = mean_absolute_error(Y_test, rbf_svr_pred)  # MAE
    #     rbf_svr_r2 = r2_score(Y_test, rbf_svr_pred)  # R2
    #
    #     print("R^2 of RBF_SVR: ", rbf_svr_r2)
    #     print("The RMSE of RBF_SVR: ", rbf_svr_rmse)
    #     print("The MAE of RBF_SVR: ", rbf_svr_mae)
    #
    #     # 输出预测值和真实值矩阵
    #     print('输出预测值和真实值矩阵----------------------------------')
    #     rbf_svr_pred_true = pd.concat([pd.DataFrame(rbf_svr_pred), pd.DataFrame(Y_test)], axis=1)
    #     rbf_svr_pred_true.columns = ['预测值', '真实值']
    #     rbf_svr_pred_true.to_excel(r'predict_y.xlsx', index=False)
    #
    #     # 比较图
    #     print('比较图----------------------------------')
    #     plt.subplots(figsize=(10, 5), dpi=200)
    #     plt.plot(rbf_svr_pred, color='b', label='预测值')
    #     plt.plot(Y_test, color='r', label='真实值')
    #     plt.legend(loc=0)
    #
    #     # #### POLY_SVR
    #     poly_svr = SVR(kernel="poly", degree=2, C=100, epsilon=0.1, gamma="scale")
    #     poly_svr.fit(x_train, y_train)
    #
    #     # 预测y
    #     poly_svr_pred = poly_svr.predict(x_test)
    #     y_scaler = scaler.fit(Y_train.values.reshape(-1, 1))
    #     y_scaler.fit_transform(Y_train.values.reshape(-1, 1))
    #     poly_svr_pred = y_scaler.inverse_transform(poly_svr_pred.reshape(-1, 1))
    #
    #     # 模型评价
    #     print('模型评价2----------------------------------')
    #     poly_svr_rmse = np.sqrt(mean_squared_error(Y_test, poly_svr_pred))  # RMSE
    #     poly_svr_mae = mean_absolute_error(Y_test, poly_svr_pred)  # MAE
    #     poly_svr_r2 = r2_score(Y_test, poly_svr_pred)  # R2
    #
    #     print("R^2 of POLY_SVR: ", poly_svr_r2)
    #     print("The RMSE of POLY_SVR: ", poly_svr_rmse)
    #     print("The MAE of PLOY_SVR: ", poly_svr_mae)
    #
    #     plt.subplots(figsize=(10, 5), dpi=200)
    #     plt.plot(poly_svr_pred, color='b', label='预测值')
    #     plt.plot(Y_test, color='r', label='真实值')
    #     plt.legend(loc=0)
    #     plt.show()
    #
    # -----------------------------------------------------------------------------------------------------------------
    # 超参数调试选择
    # C_arr = [1, 10, 100, 200, 400, 600, 800, 1000]
    # gamma_arr = [0.001, 0.01, 0.1]
    # Pre_MAPE = 100
    # #     # Pre_MAPE: 100 \ C_out: 1000 \ gamma_out: 0.1
    # # Pre_MAPE = 100
    # Opt_C = 0
    # Opt_gamma = 0
    # for C_out in C_arr:
    #     for gamma_out in gamma_arr:
    #         print('C_out:{} \ gamma_out:{}'.format(C_out, gamma_out))
    #         svr_rbf = SVR(kernel='rbf', C=C_out, gamma=gamma_out)
    #         svr_rbf.fit(X_train, Y_train)
    #         Y_pred = svr_rbf.predict(X_test)
    #         Y_diff = Y_pred - Y_test
    #         relat_errors = Y_diff / Y_test
    #         abs_relat_errors = np.fabs(relat_errors)
    #         error_sum = np.sum(abs_relat_errors)
    #         valid_num = len(abs_relat_errors)
    #         MAPE = error_sum / valid_num
    #         if MAPE < Pre_MAPE:
    #             Pre_MAPE = MAPE
    #             Opt_C = C_out
    #             Opt_gamma = gamma_out
    #             print('Pre_MAPE:', Pre_MAPE)
    #             print('Opt_C:', Opt_C)
    #             print('Opt_gamma:', Opt_gamma)
    #
    # print('Pre_MAPE:{} \ C_out:{} \ gamma_out:{}'.format(Pre_MAPE, C_out, gamma_out))
    # svr_rbf = SVR(kernel='rbf', C=Opt_C, gamma=Opt_gamma)
    # # svr_rbf = SVR(kernel='rbf', C=C_out, gamma=gamma_out)
    # svr_rbf.fit(X_train, Y_train)
    # Y_pred = svr_rbf.predict(X_test)
    #
    # # 输出预测值和真实值矩阵
    # print('输出预测值和真实值矩阵----------------------------------')
    # rbf_svr_pred_true = pd.concat([pd.DataFrame(Y_pred), pd.DataFrame(Y_test)], axis=1)
    # rbf_svr_pred_true.columns = ['Y_pred', 'Y_test']
    # rbf_svr_pred_true.to_excel(r'predict.xlsx', index=False)