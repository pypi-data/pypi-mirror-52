from tagcounter.htmlParser import HTMLParserSite
from tagcounter.htmlReader import read_data
from tagcounter.DB.models.domain import Domain
from tagcounter.DB.models.page import Page
from datetime import datetime
from tagcounter.DB.domainRepo import DomainRepo
from tagcounter.DB.pageRepo import PageRepo
from tagcounter import urlParser
from tagcounter import yamlService
from tld import get_tld

import pickle


class TagService:

    def __init__(self):
        self.parser = HTMLParserSite()
        self.page_repo = PageRepo()
        self.domain_repo = DomainRepo()

    def count_tags(self, url):
        value = yamlService.get_value_by_key(url)
        if value is not None:
            url = value

        url = urlParser.add_http_to_url(url)
        urlParser.validate_url(url)
        info = get_tld(url, as_object=True)
        domain_with_suffix = info.parsed_url[1]

        domain = self.domain_repo.get_domain_by_name(urlParser.url_without_protocol(domain_with_suffix))
        if domain is not None:
            page = self.page_repo.get_page_by_domain_id_and_url(domain.id, url)
            if page is not None:
                loaded_tags = pickle.loads(page.tag_data)
            else:
                tags = read_data(url)
                self.parser.feed(tags)
                serialized_tag_data = pickle.dumps(self.parser.get_tags())
                page = Page(url, datetime.now(), serialized_tag_data, domain.id)
                self.page_repo.add_page(page)
                loaded_tags = self.parser.get_tags()
        else:
            tags = read_data(url)
            self.parser.feed(tags)
            serialized_tag_data = pickle.dumps(self.parser.tagDict)
            domain = Domain(name=urlParser.url_without_protocol(domain_with_suffix))
            self.domain_repo.add_domain(domain)
            page = Page(url, datetime.now(), serialized_tag_data, domain.id)
            self.page_repo.add_page(page)
            loaded_tags = self.parser.get_tags()

            # d = info.domain
            # key = d[0]+d[int(len(d)/2)]+d[len(d)-1]
            # yaml1.add_value(key, domain_with_suffix)

        return loaded_tags
