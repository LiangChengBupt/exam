# Medical Dataset Construction
## Project Structure
本项目使用了scrapy高性能并行爬虫框架，数据存放在baidu/data/
```txt
.
├── baidu # 爬虫相关pipeline middlewares settings spiders
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       ├── baiduspider.py
│       ├── content.py
│       ├── __init__.py
├── data
│   └── result
│       └── 第一词爬虫的搜索结果
    ├── content
        └── 对第一次搜索结果的具体页面爬取
├── dataset.py # 构建数据集
├── gpt4.py # gpt4 api
├── keywords.py # 搜索关键词
├── run_spider.py # 运行爬虫
├── score.py  #Util 打分函数
└── scrapy.cfg
```

## Usage
1. add the openai api_key in gpt4.py
2. 
```
pip install -r requirements.txt
cd baidu
python dataset.py
```