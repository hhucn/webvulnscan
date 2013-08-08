from .Client import Client, StrangeContentType
from .utils import get_url_host

class Crawler(object):
    def __init__(self, entry_point, whitelist, client=None):
        self.whitelist = whitelist
        self.entry_point = entry_point

        if client is None:
            self.client = Client()
        else:
            self.client = client

    def __iter__(self):
        try:
            page = self.client.download_page(self.entry_point)
        except StrangeContentType as error:
            return
        
        yield page

        for link in page.get_links():
            if get_url_host(link) in self.whitelist:
                if link not in self.client.visited_pages:
                    for new_page in Crawler(link, self.whitelist, self.client):
                        yield new_page
