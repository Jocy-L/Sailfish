import datetime
import pymysql

# default ip :127.0.0.1 / localhost
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='root',
                       port=3306,
                       db='CTRF',
                       charset='utf8')

cur = conn.cursor()

# UI DB def
# -------------------------------------------------------------------------------
# word_package = 'title/desc'
def create_new_word_value_tables():
    word_package = ['title', 'desc']
    for package_name in word_package:
        table_name = 'ctrf_{}_words'.format(package_name)
        expired_table_name = table_name + '_' + str(datetime.date.today())

        rename_table_str = 'RENAME TABLE `{}` to `{}`'.format(table_name, expired_table_name)
        cur.execute(rename_table_str)

        create_table_like_old_str = 'create table `{}` like `{}`'.format(table_name, expired_table_name)
        cur.execute(create_table_like_old_str)

    return table_name

# def write_word_value_to_table(file_name,table_name):
#     file_write_in_table_str = 'LOAD DATA LOCAL INFILE `"{}"` INTO TABLE `{}` FIELDS TERMINATED BY " "'.\
#                                 format(file_name, table_name)
#     cur.execute(file_write_in_table_str)
#     conn.commit()

def write_to_search_history(search_type, search_words):
    table_name = 'ctrf_search_words_history'
    write_in_str = 'insert into `{}`(`search_type`, `search_words`) values ("{}", "{}")'.\
                        format(table_name, search_type, search_words)
    cur.execute(write_in_str)
    conn.commit()


# base in auto mode to match
# read out from : probability_prediction_table
def read_match_range_items(CTR_front_range,CTR_post_range):
    pass

# base in specific mode to match
def read_to_specific_mode():
    pass

# DATA DB def
# ----------------------------------------------------------------------------------
def write_data_word_table(table_name, word, value):
    insert_str = 'insert into `{}`(key_word, tfidf_value) values ("{}", {})'.format(table_name, word, value)
    cur.execute(insert_str)
    conn.commit()

# use for word:tfidf update to DB -----------same as def write_data_word_table(word_package, table_name, word, value)
# def update_word_value_table(word_package, file_name):
#     table_name = create_new_word_value_tables(word_package)
#     write_word_value_to_table(file_name, table_name)

def read_word_value_from_DB(table_name):
    read_str = 'select * from `{}`'.format(table_name)
    cur.execute(read_str)
    word_value_dict = {}
    DB_return_res = cur.fetchall()
    for res in DB_return_res:
        word_value_dict[res[1]] = res[2]

    return word_value_dict


# data = cur.fetchall()
# print(data)
def close_DB_sever():
    cur.close()
    conn.close()

# table_name = 'ctrf_title_words'
# word_value_dict = read_word_value_from_DB(table_name)
# print(word_value_dict)
