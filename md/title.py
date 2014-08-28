from html.parser import HTMLParser


class StopParse(Exception):
    '''Custom exception to return early from the parsing.'''
    pass


class TitleFinder(HTMLParser):
    '''Custom parser to extract the first header.'''

    def feed(self, *args, **kwargs):
        self.title = False
        self.data = None
        self.tag = None

        try:
            super().feed(*args, **kwargs)
        except StopParse:
            pass

        return self.data

    def handle_starttag(self, tag, attrs):
        if len(tag) == 2 and tag[0] == 'h':
            self.title = True
            self.data = ''
            self.tag = tag

    def handle_data(self, data):
        if self.title:
            self.data += data

    def handle_endtag(self, tag):
        if tag == self.tag:
            raise StopParse()


def find(content):
    return TitleFinder().feed(content)
