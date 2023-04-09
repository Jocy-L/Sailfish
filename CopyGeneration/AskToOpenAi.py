#coding=utf-8

import os, re
import openai

# openai.organization = "YOUR_ORG_ID"
# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.Model.list()

class AskToOpenAi():
    def __init__(self):
        self.OPENAI_API_KEY = None
        self.request_str = None
        self.request_items_num = None
        self.request_str_complete = None
        self.sensitive_word_file = 'SensitiveWord.txt'
        self.save_result_file = 'result.txt'
        
        super(AskToOpenAi, self).__init__()

    def request_str_combo(self):
        self.request_str_complete = "生成{}条关于'{}'的结果".format(self.request_items_num, self.request_str)

    def LinkToGptApi(self):
        openai.api_key = self.OPENAI_API_KEY
        response = openai.Completion.create(engine="davinci",
        # response = openai.Completion.create(model="text-davinci-003",
                                            prompt=self.request_str_complete,
                                            max_tokens=1000,
                                            temperature=0)
        res = response["choices"][0]["text"]
        # res = response
        return res

    def text_processing(self, res):
        # res = res["choices"][0]["text"]
        text_split = res.split('\n')
        text_need_check = []
        for p in text_split:
            if p != '':
                try:
                    ret = re.match("\d*.", p)
                    text_need_check.append(p.strip(str(ret)))
                except:
                    text_need_check.append(p)
        return text_need_check

    def sensitive_word_check(self, text_need_check):
        sensitive_word_list = []
        text_after_check = []
        with open(self.sensitive_word_file, 'r', encoding='utf-8') as f:
            for i in f.readlines():
                sensitive_word_list.append(i.strip('\n'))
        # print(sensitive_word_list)
        for text in text_need_check:
            for word in sensitive_word_list:
                if word not in text:
                    text_after_check.append(text)
        return text_after_check

    def write_to_csv(self, text_after_check):
        with open(self.save_result_file, 'a', encoding='utf-8') as f:
            for text in text_after_check:
                f.write(text)

    def run(self):
        self.request_str_combo()
        print(self.request_str_complete)
        res = self.LinkToGptApi()
        text_need_check = self.text_processing(res=res)
        text_after_check = self.sensitive_word_check(text_need_check=text_need_check)
        self.write_to_csv(text_after_check=text_after_check)


run_ask = AskToOpenAi()
run_ask.OPENAI_API_KEY = "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"
run_ask.request_str = "瑞幸"
run_ask.request_items_num = 1
run_ask.run()
# print(run_ask.LinkToGptApi())