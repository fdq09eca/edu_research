import time
import urllib.parse
 
import requests
from bs4 import BeautifulSoup
import re
 
from global_config import ConfigFile
from program_logger import logger
 
 
class ScholarScrape():
    def __init__(self):
        self.page = None
        self.last_url = None
        self.last_time = time.time()
        self.min_time_between_scrape = int(ConfigFile.instance().config.get('scholar','bot_avoidance_time'))
        self.header = {'User-Agent':ConfigFile.instance().config.get('scholar','user_agent')}
        self.session = requests.Session()
        pass
 
    def search(self, query=None, year_lo=None, year_hi=None, title_only=False, publication_string=None, author_string=None, include_citations=True, include_patents=True):
        url = self.get_url(query, year_lo, year_hi, title_only, publication_string, author_string, include_citations, include_patents)
        while True:
            wait_time = self.min_time_between_scrape - (time.time() - self.last_time)
            if wait_time > 0:
                logger.info("Delaying search by {} seconds to avoid bot detection.".format(wait_time))
                time.sleep(wait_time)
            self.last_time = time.time()
            logger.info("SCHOLARSCRAPE: " + url)
            self.page = BeautifulSoup(self.session.get(url, headers=self.header).text, 'html.parser')
            self.last_url = url
 
            if "Our systems have detected unusual traffic from your computer network" in str(self.page):
                raise BotDetectionException("Google has blocked this computer for a short time because it has detected this scraping script.")
 
            return
 
    def get_url(self, query=None, year_lo=None, year_hi=None, title_only=False, publication_string=None, author_string=None, include_citations=True, include_patents=True):
        base_url = "https://scholar.google.com.au/scholar?"
        url = base_url + "as_q=" + urllib.parse.quote(query)
 
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
 
    def get_results_count(self):
        e = self.page.findAll("div", {"class": "gs_ab_mdw"})
        try:
            item = e[1].text.strip()
        except IndexError as ex:
            if "Our systems have detected unusual traffic from your computer network" in str(self.page):
                raise BotDetectionException("Google has blocked this computer for a short time because it has detected this scraping script.")
            else:
                raise ex
 
        if self.has_numbers(item):
            return self.get_results_count_from_soup_string(item)
        for item in e:
            item = item.text.strip()
            if self.has_numbers(item):
                return self.get_results_count_from_soup_string(item)
        return 0
 
    @staticmethod
    def get_results_count_from_soup_string(element):
        if "About" in element:
            num = element.split(" ")[1].strip().replace(",","")
        else:
            num = element.split(" ")[0].strip().replace(",","")
        return num
 
    @staticmethod
    def has_numbers(input_string):
        return any(char.isdigit() for char in input_string)
 
 
class BotDetectionException(Exception):
    pass
 
if __name__ == "__main__":
    s = ScholarScrape()
    s.search(**{
        "query":"\"policy shaping\"",
        # "publication_string":"JMLR",
        "author_string": "gilboa",
        "year_lo": "1995",
        "year_hi": "2005",
 
    })
    x = s.get_results_count()
    print(x)