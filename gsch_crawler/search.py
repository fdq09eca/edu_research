#! /usr/bin/python3
from bs4 import BeautifulSoup as bs
import requests, time, random, urllib, re, os, sys, argparse, datetime
from typing import Union, TextIO 

def get_url(
    query=None, year_lo=None, year_hi=None,
    title_only=False, publication_string=None,
    author_string=None, include_citations=True,
    include_patents=True, start = 0
    ) -> str:
    base_url = f"https://scholar.google.com/scholar?hl=en&start={start}"
    url = base_url + "&q=" + urllib.parse.quote(query)

    if year_lo is not None and bool(re.match(r'.*([1-3][0-9]{3})', str(year_lo))):
        url += "&as_ylo=" + str(year_lo)

    if year_hi is not None and bool(re.match(r'.*([1-3][0-9]{3})', str(year_hi))):
        url += "&as_yhi=" + str(year_hi)

    if title_only:
        url += "&as_yhi=title"
    else:
        url += "&as_yhi=any"

    if publication_string is not None:
        url += "&as_publication=" + urllib.parse.quote('"' + str(publication_string) + '"')

    if author_string is not None:
        url += "&as_sauthors=" + urllib.parse.quote('"' + str(author_string) + '"')

    if include_citations:
        url += "&as_vis=0"
    else:
        url += "&as_vis=1"

    if include_patents:
        url += "&as_sdt=0"
    else:
        url += "&as_sdt=1"
    return url

def get_page(url: str) -> object:
    
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,zh-HK;q=0.7,zh;q=0.6,vi-VN;q=0.5,vi;q=0.4,zh-TW;q=0.3,ja;q=0.2,zh-CN;q=0.1',
    'accept-encoding': 'gzip, deflate, br',
    'cookie': 'SID=yAfJ7-m8dwSzj-6FJqqRhsLjyqbP1LOeCT-nKYTQjvB_-9Jk2SsE7BqG68M0MttEG10bfw.; __Secure-3PSID=yAfJ7-m8dwSzj-6FJqqRhsLjyqbP1LOeCT-nKYTQjvB_-9JkfqRm5RHWRxw834UCA0CXAA.; HSID=ACgcZ9TnPtr27fLuF; SSID=AZKHRNo2_a-7SXZB4; APISID=AcjzGd5CR5b2e8AT/AVgcii9L9YUGkg8tx; SAPISID=U8YD3TWQNOKdSCXS/A26I1qoNTqoJYsUrJ; __Secure-HSID=ACgcZ9TnPtr27fLuF; __Secure-SSID=AZKHRNo2_a-7SXZB4; __Secure-APISID=AcjzGd5CR5b2e8AT/AVgcii9L9YUGkg8tx; __Secure-3PAPISID=U8YD3TWQNOKdSCXS/A26I1qoNTqoJYsUrJ; GSP=IN=ee35ef0725b57926+7e6cc990821af63:LD=en:CR=0:LM=1592365372:S=bYfO55MDRO_eyrnH; NID=204=vfBlG_j_4wFie7Ina1zfUvqTRm80U_yNPbJbW4iui5NRHCjms6KmzAkpXaibddoJUlnmtHxjKIDQ9aBMv9yKfh7RNcxeAB_AKsrOURjc3q23ldSAv83uWulcUTL1RTfRqIEVVBMf8R5W6IqJ0ZjtDRt91PrVJo9ymCI0jJx69KXdkeoQKv9HuJHr-Jw27TdaG7JHFjpUbzhQKOtAvSQIZol_81uzQ64vgAWBkSQiZZq_WwT_SAWQ40i8; 1P_JAR=2020-6-17-8; SIDCC=AJi4QfF705AjsX5gaNsskUIkW6pz86DsDoGqW3TM_3uc7ZDgiwZYNvS5kezY6q3CucKiLcYU5wM'
    }
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        print('== page requested successfully ==')
        page = bs(response.content, 'html.parser')
        return page
    else: 
        return exit('== page requested failed ==', 1)

def p_and_r(page: object) -> tuple:
    '''
    get the total number of result and current page of search
    '''
    n_result_str = page.find("div", id = 'gs_ab_md').text
    print(n_result_str)
    pattern = r'(?:Page (?P<page>\d+))?.*?(?P<result>\d+).*?\((?P<sec>\d+\.\d+) sec\)'
    p, r, sec = re.findall(pattern, n_result_str)[0]
    p = p if p else 1
    return p, r


def fetch_results(page: object) -> list:
    '''
    obtain all the publication-divs to return a list of soup object.
    '''
    results = page.find_all("div", class_ = 'gs_r gs_or gs_scl')
    p, r = p_and_r(page)
    # print(f'fetched {len(results)} results on page {p}')
    return results


def fetch_pdf_url(result: object) -> str:
    '''
    return pdf url in the result if available.
    '''
    pdf_div = result.find('div', class_= 'gs_ggsd')
    try:
        if pdf_div.a.span.text == "[PDF]":
            return pdf_div.a['href']
    except AttributeError:
        return None


def download_pdf(url:str , folder:str = os.getcwd(), filename:str = 'untitled.pdf') -> Union[str, None]:
    '''
    download pdf the assigned folder, return the local directory
    '''
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_dir = unique_dir(os.path.join(folder, filename))
    try:
        rps = requests.get(url, stream=True)
        with open(file_dir, 'wb') as fd:
            for chunk in rps.iter_content(2000):
                fd.write(chunk)
        print(f'pdf downloaded at {file_dir}')
    except:
        print(f'Download failed')
        file_dir = '#'
    return file_dir
    

def unique_dir(file_dir: str ) -> str:
    '''
    rename the filename to unqiue if duplicated
    '''
    pattern = r'^(?P<f_dir>.*?)(?: \((?P<num>\d+)\))?\.(?P<ext>.+)$'
    while os.path.exists(file_dir):
        f_dir, num, ext = re.findall(pattern, file_dir)[0]
        num = 1 if not num else int(num) + 1
        file_dir = f'{f_dir} ({num}).{ext}'
    return file_dir


def pub_filename(authors_ls: list, year: str) -> str:
    '''
    formating pdf filename
    '''
    authors = [author.replace(' ', '_') for author in authors_ls.split(', ')]
    if len(authors) > 3:
        return f'{authors[0]}_etal_{year}.pdf'
    elif len(authors) == 1:
        return f'{authors[0]}_{year}.pdf'
    return f'{"_".join(authors)}_{year}.pdf'


def gen_pub_dict(results: list, pdf_folder: str = 'pdf_gsch') -> dict:
    '''
    obtain publications detail from the input result (a list of soup object)
    download, if any, pdf to ./pdf_gsch/ as default 
    '''
    print("fetching publication info", end ='')
    pubs = {}
    for r in results:
        ref_div = r.find("h3", class_ = 'gs_rt')
        if ref_div.a:
            ref_div = ref_div.a
        title = ref_div.text
        pubs[title] = {}
        pubs[title]['link'] = ref_div.get('href')
        
        pubinfo_str = r.find("div", class_ = 'gs_a').text.replace('\xa0', ' ')
        pattern = r'(?P<authors>.*?)(?: - (?P<journal>.*), (?P<year>\d{4}))?(?: - (?P<site>.*))'
        pubinfo = re.match(pattern, pubinfo_str)
        cols = ['authors', 'journal', 'year']
        for col in cols:
            pubs[title][col] = pubinfo.group(col)
        pdf_url = fetch_pdf_url(r)

        if pdf_url:
            print('\nfound potential pdf url, downloading...')
            pubs[title]['pdf'] = download_pdf(
                url = pdf_url,
                folder = os.path.join(os.getcwd(),pdf_folder), 
                filename = pub_filename(pubs[title]['authors'], pubs[title]['year'])
                )
        # else:
        #     pubs[title]['pdf'] = '--'
        print('.', end = '')
    return pubs


def write_md_th(headers: list, f_dir: str) -> TextIO :
    '''
    create and write table header to markdown file at f_dir
    '''
    with open(f_dir, 'w') as md:
        hd = '| ' + " | ".join(headers) + " | \n"
        c_line = '|' + ' :---: |' * len(headers) + '\n'
        md.write(hd + c_line)
        


def write_md_tr(pubs:dict, f_dir:str) -> TextIO :
    '''
    write table rows to markdown file at f_dir
    '''
    with open(f_dir, 'a') as md:
        for title, infos in pubs.items():
            infos_itr = iter(infos)
            link = next(infos_itr)
            md.write(f'| [{title}]({pubs[title][link]}) |')
            for detail in infos_itr:
                if detail == 'pdf':
                    md.write(f' [.pdf]({infos.get(detail)}) |')
                else:
                    md.write(f'{infos.get(detail)} |')
            md.write("\n")


def write_to_md(pubs: object, f_dir:str = "./pub_list.md") -> TextIO :
    '''
    write table to markdown file at f_dir. 
    '''
    headers = ['title', 'authors', 'journal', 'year', 'pdf']
    if not os.path.exists(f_dir):
        write_md_th(headers, f_dir)
    write_md_tr(pubs, f_dir)
    print(f"result wrote to {f_dir}")


def search(
    keywords: str,
    from_yr: int = None,
    to_yr:int = None,
    publisher:str = None,
    author:str = None,
    start: int = 0,
    pdf_folder:str = 'pdf_gsch') -> int:
    '''
     get url of page
     get page 
     get all results on the page
        if no result on the page:
            1. you are detected by google as bot
            2. you finish scraping
    scrap every pubs info, put them into a dictionary
        - title [key]
        - publication link
        - authors
        - year
        - .pdf (if download link avaiable)
    wrtie result to markdown file, pub_list.md by default
    return number of result obtained
    '''
    url = get_url(
        query = keywords, 
        year_lo = from_yr, 
        year_hi = to_yr,
        title_only = False,
        publication_string = publisher,
        author_string = author,
        include_citations = True,
        include_patents = True,
        start = start
    )
    page = get_page(url)

    if page:
        results = fetch_results(page)
        if not results:
            respond_pth = os.path.join(os.getcwd(), 'respond.html')
            with open(respond_pth, 'w') as f:
                f.write(page.prettify())
            sys.exit(f"No result returned, see ./respond.html for detail.")
        pubs = gen_pub_dict(results, pdf_folder)
        write_to_md(pubs)
    return len(pubs)


def main(**kwargs):
    '''
    n means fetch n result
    '''
    print('== program begins ==')
    i, pub_record = 0, 0
    while i + 10 <= kwargs['n']:
        pub_record += search(
            keywords = kwargs['keywords'],
            from_yr = kwargs['from_yr'],
            to_yr = kwargs['to_yr'],
            publisher = kwargs['publisher'],
            author = kwargs['author'],
            start = i,
            pdf_folder = kwargs['pdf_folder']
            )
        i += 10
        if i > kwargs['n']:
            break
        n_sec = random.randint(30, 40)
        print(f"sleep for {n_sec} sec")
        time.sleep(n_sec)
    print(f'{pub_record} publication is recorded in total.')
    print('== program ends ==')
    sys.exit(0)

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
    parser.add_argument('-n', '--n_result', help = "limit search to n literatures, at least 10 (10 results/page), default: 10", type=int, default=10)
    if len(sys.argv) == 1:
        parser.print_help()
        print('At least input one query e.g. python3 search.py "GBA HK edu"')
        return sys.exit(1)
    return parser.parse_args()


def run(get_args):
    if __name__ == '__main__':
        args = get_args()
        main(
            n = args.n_result, 
            keywords = args.keywords,
            from_yr = args.from_yr,
            to_yr = args.to_yr,
            publisher = args.publisher,
            author = args.author,
            pdf_folder = args.pdf_folder
        )
run(get_args)