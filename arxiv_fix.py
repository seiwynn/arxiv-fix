from bs4 import BeautifulSoup as bs
import requests
import os
import argparse
import re

# Modern problems require modern solutions：
# we still don't know why arxiv use urls as file names


def main():
    args = get_args()

    files_to_fix = get_file_names(args.directory)
    for file_name in files_to_fix:
        actual_title = get_snake_title(file_name[:-4])

        # only rename if we get a title
        if len(actual_title) > 0:
            new_name = safe_filename(actual_title + "_" + file_name)

            if args.verbose:
                print(f"renaming {file_name} \n\tto {new_name}...")
            os.rename(args.directory + file_name, args.directory + new_name)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='fix arxiv titles')
    parser.add_argument(
        '-dir', '--directory', help='your directory of papers', type=str, default='./demo/')
    parser.add_argument(
        '-v', '--verbose', help='toggle verbose output', action='store_true')

    # TODO: haven't implemented these
    parser.add_argument(
        '-cp', '--copy', help='copy to new file instead of renaming', action='store_true')
    # parser.add_argument(
    #     '-r', '--recursive', help='toggle recursive (similar to rm -rf)', action='store_true')
    parser.add_argument(
        '-t', '--truncate', help='truncate file name by char length, rounds down to the last word', type=int, default=40)

    args = parser.parse_args()
    return args


def get_file_names(directory: str) -> list[str]:
    all_files = os.listdir(directory)
    files_to_fix = []
    for file_name in all_files:
        if file_name[-4:] == '.pdf' and os.path.isfile(directory + file_name):
            files_to_fix.append(file_name)
    return files_to_fix


def get_snake_title(paper_id: str) -> str:
    arxiv_head = 'https://arxiv.org/abs/'
    response = requests.get(arxiv_head + paper_id)
    if response.status_code != 200:
        return ''

    # because I'm too lazy to install lxml
    # soup = bs(response.content, features="lxml")
    soup = bs(response.content, features="html.parser")

    abstract = soup.find('div', 'leftcolumn')
    title = abstract.find('h1', 'title mathjax')
    ans = title.contents[1]

    full_snake_title = ans.lower()
    return full_snake_title


# use this before renaming
def safe_filename(filename: str) -> str:
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', ' ']
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    # merge consecutive underscores
    filename = re.sub(r'_+', '_', filename)
    return filename


if __name__ == "__main__":
    main()
