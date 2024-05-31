# Medical Dataset Construction
编程题代码实现：
我们假设这道编程题的目标是：构建一个某方向的高质量数据集，方式是通过搜索引擎爬虫实现。
我们假设目的是构建一个中文医学数据集。主要流程包括：
1. 使用GPT-4生成用于搜索的查询。
2. 使用爬虫工具基于生成的查询获取详细内容。
3. 过滤广告内容。
4. 根据指定的策略判断内容是否与查询相关。
    我们设计了以下的策略：
    
5. 过滤并保存与查询相关的内容。
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

