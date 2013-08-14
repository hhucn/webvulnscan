from .client import Client, StrangeContentType
from .utils import get_url_host


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

        if client is None:
            self.client = Client()
        else:
            self.client = client

    def __iter__(self):
        try:
            page = self.client.download_page(self.entry_point)
        except StrangeContentType:
            return

        yield page

        for link in page.get_links():
            if get_url_host(link) in self.whitelist:
                if link not in self.client.visited_pages:
                    if link not in self.blacklist:
                        for new_page in Crawler(link, self.whitelist,
                                                self.client,
                                                self.blacklist):
                            yield new_page
