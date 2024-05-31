# Chinese Medical Dataset Construction

编程题代码实现：
我们假设这道编程题的目标是：**构建一个某方向的高质量数据集**，方式是通过**搜索引擎爬虫**实现。
我们假设目的是构建一个**中文医学数据集**。主要流程包括：

1. 构建一个医学领域的关键词集合（如：口腔），对于每个关键词，使用GPT-4生成用于搜索的查询语句（如：智齿的术后维护）。
2. 使用爬虫工具基于生成的查询爬取搜索结果`data/result/`。
3. 对搜索结果进行二次爬取，得到详细内容``data/content/`
4. 过滤广告内容。
5. 根据指定的策略判断内容是否与查询相关。我们设计了以下的策略：
   1. **Api-based**：调用openai gpt-4接口判断该内容是否与搜索关键词相关
   2. 使用BLEU , GLUE进行打分
   3. **Embedding-based**：使用bert-base-chinese进行embedding后计算相似度
   4. **Rule-based**：我们定义了一个中文医学关键词集合，如果该网页中的内容包含该关键词集合中的一部分，频率和数量达到阈值。那么我们认为这篇内容是相关的。
6. 过滤并保存与查询相关的内容`data/filtered`。

## Project Structure

本项目使用了scrapy高性能并行爬虫框架，数据存放在`baidu/data/`

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

```bash
cd baidu
pip install -r requirements.txt
python dataset.py
````

## Discussion
由于时间的原因，我仅仅是跑通了pipeline，在数据的数量存在着不足。但关键的环节和技术，以及代码的框架已经构建完成。