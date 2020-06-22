from bs4 import BeautifulSoup as bs
import progressbar, sys
import requests, time, random, urllib, re, os

# info = {'url' : 'http://www.dpi-proceedings.com/index.php/dtssehs/article/viewFile/33751/32338',
# 'folder' : './pdf_try/',
# 'filename' : "trying.pdf"}

# def unique_dir(file_dir: str ) -> str: 
#     pattern = r'^(?P<f_dir>\.?.*?)(?: \((?P<num>\d+)\))?\.(?P<ext>.+)$'
#     while os.path.exists(file_dir):
#         f_dir, num, ext = re.findall(pattern, file_dir)[0]
#         num = 1 if not num else int(num) + 1
#         file_dir = f'{f_dir} ({num}).{ext}'
#     return file_dir

# def download_pdf(url:str , folder:str = os.getcwd(), filename:str = 'untitled.pdf'):
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#     file_dir = unique_dir(os.path.join(folder, filename))
#     try:
#         print('downloading')
#         urllib.request.urlretrieve(url, file_dir)
#         print(f'pdf downloaded at {file_dir}')
#     except:
#         print(f'pdf download failed')
#         file_dir = '#'
#     return file_dir

# download_pdf(**info)

# f_dir = os.path.join(info['folder'], info['filename'])
# print(unique_dir(f_dir))

# s = 'L Li, Q Sun - … Transactions on Social Science, Education and …, 2019 - dpi-proceedings.com'
# pattern = r'(?P<authors>.*) - (?P<journal>.*), (?P<year>\d{4}) - (?P<site>.*)'
# authors, journal, year, site = re.findall(pattern, s)[0]

# def test():
#     if True:
#         return print('hehe')
#     print('sheshe')
# test()

# def total(i):
#     n = 765+i
#     return  n

# i = 0
# n = 25
# while (i + 10 <= n):
#     print(f'fetch {i}')
#     i += 10
# print(f'i = {i}')
# s1 = 'About 782 results (0.07 sec)'
# s2 = 'Page 2 of about 782 results (0.04 sec)'
# s3 = 'Page 78 of 765 results (0.18 sec)'

# p = r'(?:Page (?P<page>\d+))?.*?(?P<result>\d+).*?\((?P<sec>\d+\.\d+) sec\)'
# # p = r'.*?(\d+).*?(\d+).*?\((\d\.\d+) sec\)'
# print(re.findall(p, s1))
# print(re.findall(p, s2))
# print(re.findall(p, s3))

# headers = ['title', 'authors', 'journal', 'year', 'pdf']
# p = '| ' + " | ".join(headers) + " | "
# div_line = '| ' + ':---: |' * len(headers) + '\n'
# print(p)
# print(div_line)
# f_dir = "./pub_list.md"
# with open(f_dir, 'r') as md:
#     print(md.read())
    # if md.read().replace(' ','').startswith(p + div_line):
    #     print('yes')
    # else:
    #     print('no')

# s = 'IH Hsu, YY Zhou - paper.ieti.net'
# s = s = 'G Tian - 2019 3rd International Conference on Education …, 2019 - atlantis-press.com'
# pattern = r'(?P<authors>.*?)(?: - (?P<journal>.*), (?P<year>\d{4}))?(?: - (?P<site>.*))'
# pubinfo = re.match(pattern, s)
# cols = ['authors', 'journal', 'year', 'site']
# for col in cols:
#     print(pubinfo.group(col))


# arg = []
# for i in range(1, 7):
#     try:
#         arg.append(argv[i])
#     except:
#         arg.append(None)
# print(arg)

import argparse, datetime

# def dir_path(path):
#     if os.path.isdir(path):
#         return path
#     else:
#         raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def get_args():
    parser = argparse.ArgumentParser(
    prog = 'lit_search', 
    description = '''web crawler for google scholar, at least input one option to search'''
    )
    parser.add_argument("-k", "--keywords", help = 'keywords for searching the literature, e.g "GBA HK edu"', type=str)
    parser.add_argument("-d", "--pdf_folder", help = "pdf folder name", type = str, default = "pdf_gsch")
    parser.add_argument("-f", "--from_yr", help = f"from year of publication, default: {datetime.datetime.now().year - 10}", type=int, default = datetime.datetime.today().year - 10)
    parser.add_argument("-t", "--to_yr", help = f"to year of publication, default: {datetime.datetime.now().year}", type=int, default = datetime.datetime.today().year)
    parser.add_argument("-a", "--author", help = "for the particular authors", type=str)
    parser.add_argument("-p", "--publisher", help = "search with in a particular publisher or journal", type=str)
    parser.add_argument('-n', '--n_result', help = "limit search to n literatures", type=int, default=10)
    return parser.parse_args()
args = get_args()

print(args.keywords)
print(args.pdf_folder)
print(args.from_yr)
print(args.to_yr)
print(args.author)
print(args.publisher)
print(args.N)

print(sys.argv)