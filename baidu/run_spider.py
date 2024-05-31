import subprocess
from keywords import zh_medical_biology_words
def run_spiders(keywords, pages=1):
    """
    Run scrapy spiders to crawl search results from Baidu.
    """
    for keyword in keywords:
        query = keyword.strip()
        output_file = f'{query}.json'
        print(f'Running spider for {query}...')
        cmd = [
            'scrapy', 'crawl', 'baidu',
            '-a', f'query={query}',
            '-a', f'pages={pages}',
            '-o', f'data/result/{output_file}'
        ]
        subprocess.run(cmd)

def get_content(keywords):
    """
    Run scrapy spiders to crawl content from search results.
    The input file is the output file from the previous step.
    """
    for keyword in keywords:
        query = keyword.strip()
        input_file = f'data/result/{query}.json'
        output_file = f'{query}.json'
        cmd = [
            'scrapy', 'crawl', 'baidu_content',
            '-a', f'input_file={input_file}',
            '-o', f'data/content/{output_file}'
        ]
        subprocess.run(cmd)

if __name__ == '__main__':
    keywords = zh_medical_biology_words
    run_spiders(keywords, pages=20)
    get_content(keywords)
