from bs4 import BeautifulSoup as bs
import requests
import os

"""todo:
    # get dir
    # pick out pdf (assuming all pdf arxiv usable)
    # rename arxiv pdf to new name
    all encoding in utf8

    # filtering: ignoring non-arxiv pdf
    filtering: ignoring directories ending with a .pdf name
    custom: trim name to length
    custom: trim name to word count
    custom: keep arxiv code or not
    antiboom: illegal chars in title
    # readme
"""

# 当代弱智问题要用当代弱智方案解决：<arxiv为什么要用它发布得爽我们用着便秘的pdf标题>

pdf_dir = './demo/'

def mian():
    stuff_to_fix = get_file_names()
    for stuff in stuff_to_fix:
        actual_title = get_snake_title(stuff[:-4])
        new_name = actual_title + "_" + stuff
        print(new_name)
        os.rename(pdf_dir + stuff, pdf_dir +new_name)


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

    ans = ans.replace(' ', '_')
    ans = ans.lower()
    return ans


if __name__ == "__main__":
    mian()
