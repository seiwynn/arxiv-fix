from bs4 import BeautifulSoup as bs
import requests
import os
import argparse
import re

"""todo:
    all encoding in utf8

    # filtering: ignoring non-arxiv pdf
    filtering: ignoring directories ending with a .pdf name
    custom: trim name to length
    custom: trim name to word count
    custom: keep arxiv code or not
    antiboom: illegal chars in title

    how argparse work
    implement actual params
"""

# 当代弱智问题要用当代弱智方案解决：<arxiv为什么要用它发布得爽我们用着便秘的pdf标题>

pdf_dir = './demo/'

def mian():
    args = get_args()
    files_to_fix = get_file_names()
    for stuff in files_to_fix:
        actual_title = get_snake_title(stuff[:-4])
        new_name = actual_title + "_" + stuff
        print(new_name)
        os.rename(pdf_dir + stuff, pdf_dir +new_name)

def get_args():
    # none actually implemented
    parser = argparse.ArgumentParser(description='fix arxiv titles')
    parser.add_argument('-dir', help='your directory of papers', default= './')
    parser.add_argument('-tc', help='truncate by char length', default=-1)
    parser.add_argument('-tw', help='truncate by word count', default=-1)
    parser.add_argument('-v', help='verbose', default=False)
    parser.add_argument('-b', help='backup your papers in said directory, ignore this arg to not backup', default='')

def get_file_names():
    everything = os.listdir(pdf_dir)
    to_fix = []
    for name in everything:
        if name[-4:] == '.pdf':
            to_fix.append(name)
    return to_fix


def get_snake_title(paper_id):
    arxiv_head = 'https://arxiv.org/abs/'
    result = requests.get(arxiv_head + paper_id)
    if result.status_code != 200:
        return ''

    c = result.content
    soup = bs(c, features="lxml")
    abstract = soup.find('div', 'leftcolumn')
    title = abstract.find('h1', 'title mathjax')
    ans = title.contents[1]

    full_snake_title = ans.lower()
    return safe_filename(full_snake_title)
	
def safe_filename(filename):
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', ' ']
    for char in illegal_chars:
        filename = filename.replace(char, '_')
	# 有时候会连着两个非法字符也太弱智了
    filename = re.sub(r'_+', '_', filename)
    return filename


if __name__ == "__main__":
    mian()
