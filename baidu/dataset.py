from run_spider import *
from gpt4 import query_gpt
import json
import os
from keywords import zh_medical_biology_words
from tqdm import tqdm
import ast
from score import calculate_bleu,calculate_glue,calculate_gpt4,calculate_bertscore
class dataset_construction():
    def __init__(self,query_num=5,policy='gpt-4',threshold=0.5):
        self.keywords = zh_medical_biology_words
        self.query_num = 5
        self.policy = policy
        self.threshold = 0.5
    def search_info(self):
        """
        Fisrtly use gpt-4 to generate search querys for the keywords in zh_medical_biology_words.
        Then use the search querys to run spiders to get the detailed content.
        """
        for keyword in tqdm(zh_medical_biology_words):
            prompt = f"""
                    I want to construct a chinese medical dataset by searching the web.
                    {keyword} is the keyword for searching medical biology information.
                    Please generate {self.query_num} search querys for this keyword.
                    Respond with the format of[query1 , query2, ...] directly, DO NOT EXPLAIN.
                    """
            res = query_gpt(prompt)
            print(f'Generated search querys for {keyword}: {res}')
            try:
                res_list = ast.literal_eval(res)
            except:
                print(res)
                print("Error in ast.literal_eval")
            run_spiders(res_list, pages=20)
            get_content(res_list)

    def filter_ads(self,content):
        prompt = f"""
        I want to filter the advertisement content from the web content.
        Origin web content: 
        <<<
        {content}
        >>>
        Please respond with the filtered content directly , DO NOT EXPLAIN.
        """
        return query_gpt(prompt)
    def related_judge(self,query,content):
        if self.policy == 'gpt-4':
            return calculate_gpt4(query,content)
        elif self.policy == 'bert':
            P, R, F1 = calculate_bertscore(query,content) > self.threshold
            if F1 > self.threshold:
                return True
            if P > self.threshold:
                return True
            if R > self.threshold:
                return True
            return False
        elif self.policy == 'bleu':
            return calculate_bleu(query,content) > self.threshold
        elif self.policy == 'glue':
            return calculate_glue(query,content) > self.threshold
    
    def filter_info(self):
        """
        Filter the content from the spiders.
        """
        content_dir = 'data/content/'
        ouput_dir = 'data/filtered'
        # 遍历文件夹，读取json文件内容，进行过滤
        for file in os.listdir(content_dir):
            with open(content_dir+file,'r') as f:
                content = json.load(f)
                # 判断是否与关键词相关
                if not self.related_judge(file,content):
                    continue
                # 过滤内容
                content = self.filter_ads(content)
                # 保存到新的文件夹
                with open(ouput_dir+file,'w') as f:
                    json.dump(content,f)
medical_dataset = dataset_construction()
medical_dataset.search_info()
medical_dataset.filter_info()