# File content:
# Usage:

#coding=utf-8

window_size = {
    'height': 500,
    'weight': 800
}

selected_mode = ['Auto_mode', 'Specific_mode']

# maybe need to move to Global when DB have build
auto_res_table_titles = ['预测点击率', 'title关键词组合', 'desc1组合', 'desc2组合']
specific_res_table_idea_titles = ['关键字组合', 'title受欢迎度', 'desc1受欢迎度', 'desc2受欢迎度']
specific_res_table_keyword_titles = ['关键字组合', '预测点击率', '预测上方平均排名', '预测上方展示胜出率']

auto_input_tips = 'CTR_front_range%, CTR_post_range%, requests_num'
specific_input_tips = 'keyword1,keyword2,keyword...'

output_result_csv_dir = ''