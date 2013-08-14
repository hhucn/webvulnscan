from .client import Client
from .utils import get_url_host

from collections import deque


class Crawler(object):
    """ Generator which systematically searches through a site. """
    def __init__(self, entry_point, whitelist, client=None, blacklist=set()):
        """
        Parameters:
          entry_point - where to start the search.
          whitelist - which host are allowed to be crawled.
          client - A client object which can be used.
        """
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.entry_point = entry_point

        self.visited_pages = set()
        self.to_visit = deque()

        if client is None:
            self.client = Client()
        else:
            self.client = client

    def __iter__(self):
        self.to_visit.append(self.entry_point)

        while self.to_visit:
            link = self.to_visit.pop()

            if get_url_host(link) not in self.whitelist:
                continue

            if link in self.blacklist:
                continue

            if link in self.visited_pages:
                continue

            page = self.client.download_page(link)
            yield page

            self.to_visit.extend(page.get_links())

            self.visited_pages.add(link)
