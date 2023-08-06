from html.parser import HTMLParser


class HTMLParserSite(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.tagDict = {}

    def handle_starttag(self, tag, attrs):
        self.__add_tag__(tag)

    def handle_endtag(self, tag):
        self.__add_tag__(tag)

    def handle_startendtag(self, tag, attrs):
        self.__add_tag__(tag)

    def get_tags(self):
        return self.tagDict

    def __add_tag__(self, tag):
        value = self.tagDict.get(tag)
        if value is None:
            self.tagDict[tag] = 1
        else:
            self.tagDict[tag] = value + 1




