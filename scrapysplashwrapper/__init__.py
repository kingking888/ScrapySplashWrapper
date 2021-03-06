__version__ = '0.1'

from .middleware import ScrapySplashWrapperDepthMiddleware  # noqa
from .crawler import ScrapySplashWrapperCrawler
import multiprocessing
from typing import List


def crawl(splash_url: str, url: str, depth: int=1,
          user_agent: str='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
          log_enabled: bool=False, log_level: str='WARNING') -> List[dict]:
    '''Send the URL to crawl to splash, returns a list of responses from splash. Each entry from the list corresponds to a single URL loaded by Splash.'''
    def _crawl(queue, splash_url, ua, url, depth, log_enabled, log_level):
        crawler = ScrapySplashWrapperCrawler(splash_url, ua, depth, log_enabled, log_level)
        res = crawler.crawl(url)
        queue.put(res)

    q = multiprocessing.Queue()
    if not user_agent:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    p = multiprocessing.Process(target=_crawl, args=(q, splash_url, user_agent, url,
                                                     depth, log_enabled, log_level))
    p.start()
    res = q.get()
    p.join()
    return res
