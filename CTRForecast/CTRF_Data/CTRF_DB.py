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

# word_package = 'titlt/desc1/desc2'
def create_new_word_value_table(word_package):
    table_name = 'ctrf_{}_words'.format(word_package)
    expired_table_name = table_name + '_' + str(datetime.date.today())

    rename_table_str = 'RENAME TABLE `{}` to `{}`'.format(table_name, expired_table_name)
    cur.execute(rename_table_str)

    create_table_like_old_str = 'create table `{}` like `{}`'.format(table_name, expired_table_name)
    cur.execute(create_table_like_old_str)

    return table_name

def write_word_value_to_table(file_name,table_name):
    file_write_in_table_str = 'LOAD DATA LOCAL INFILE `"{}"` INTO TABLE `{}` FIELDS TERMINATED BY " "'.\
                                format(file_name, table_name)
    cur.execute(file_write_in_table_str)
    conn.commit()

def write_to_search_history(search_type, search_words):
    table_name = 'ctrf_search_words_history'
    write_in_str = 'insert into `{}`(`search_type`, `search_words`) values ("{}", "{}")'.\
                        format(table_name, search_type, search_words)
    cur.execute(write_in_str)
    conn.commit()


# use for word:tfidf update to DB
def update_word_value_table(word_package, file_name):
    table_name = create_new_word_value_table(word_package)
    write_word_value_to_table(file_name, table_name)

# base in auto mode to match
# read out from : probability_prediction_table
def read_match_range_items(CTR_front_range,CTR_post_range):
    pass

# base in specific mode to match
def read_to_specific_mode():
    pass


# data = cur.fetchall()
# print(data)
cur.close()
cur.close()
