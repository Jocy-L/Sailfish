#coding=utf-8
import datetime
import openai

class AskToOpenAi():
    def __init__(self):
        self.OPENAI_API_KEY = None
        self.request_items_num = None
        self.request_type = None
        self.request_key_words = None
        self.words_length = None
        self.request_str_complete = None
        self.sensitive_word_file = 'SensitiveWord.txt'
        self.save_result_file = 'result.txt'
        
        super(AskToOpenAi, self).__init__()

    def request_str_combo(self):
        self.request_str_complete = "write {} {} contain words {} and {} chinese words and {} appear once".format(
            self.request_items_num,
            self.request_type,
            self.request_key_words,
            self.words_length,
            self.request_key_words)

    def LinkToGptApi(self):
        openai.api_key = self.OPENAI_API_KEY
        # response = openai.Completion.create(engine="davinci",
        response = openai.Completion.create(model="text-davinci-003",
                                            prompt=self.request_str_complete,
                                            max_tokens=3000,
                                            temperature=0)
        res = response["choices"][0]["text"]
        return res

    def text_processing(self, res):
        text_split = res.split('\n')
        text_need_check = []
        for p in text_split:
            if p != '':
                # if self.request_items_num != 'one':
                #         ret = re.match("\d*.", p)
                #         text_need_check.append(p.strip(str(ret)))
                # else:
                #     text_need_check.append(p)
                text_need_check.append(p)
        return text_need_check

    def sensitive_word_check(self, text_need_check):
        sensitive_word_list = []
        text_after_check = []
        with open(self.sensitive_word_file, 'r', encoding='utf-8') as f:
            for i in f.readlines():
                sensitive_word_list.append(i.strip('\n'))
        for text in text_need_check:
            for word in sensitive_word_list:
                if word not in text and text not in text_after_check:
                    text_after_check.append(text)
        return text_after_check

    def write_to_csv(self, text_after_check):
        with open(self.save_result_file, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.now()) + '   items:' + str(len(text_after_check)) + '\n')
            for text in text_after_check:
                f.write(text + '\n')

    def run(self):
        self.request_str_combo()
        print(self.request_str_complete)
        res = self.LinkToGptApi()
        text_need_check = self.text_processing(res=res)
        text_after_check = self.sensitive_word_check(text_need_check=text_need_check)
        self.write_to_csv(text_after_check=text_after_check)

        return text_after_check


# run_ask = AskToOpenAi()
# # OPENAI_API_KEY常更新
# run_ask.OPENAI_API_KEY = ""
# run_ask.request_items_num = 'five'
# run_ask.request_type = 'description'
# run_ask.request_key_words = "'加盟， 咖啡'"
# run_ask.length = 'more than 15 words and less than 20 '
# run_ask.run()