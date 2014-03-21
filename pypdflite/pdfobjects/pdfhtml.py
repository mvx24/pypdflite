from HTMLParser import HTMLParser
from pdfcolor import PDFColor
from pdffont import PDFFont
from pdftext import PDFText


class PDFHTMLParser(HTMLParser):
    def __init__(self):
        # HTMLParser is old-style class
        HTMLParser.__init__(self)
        self.commandlist = []
        self.datastring = ''

    def handle_starttag(self, tag, attrs):
        if self.datastring != '' and len(self.commandlist) >= 1:
            self.commandlist[-1]['data'] = " ".join(self.datastring.split())
            self.datastring = ''
        self.commandlist.append({'name': tag, 'attributes': attrs})


    def handle_data(self, data):
        print data
        self.datastring += data

    def handle_endtag(self, tag):
        print "endtag", tag
        if tag == 'span':
            last = self.commandlist[-2]
            self.commandlist.append({'name': last['name'], 'attributes': last['attributes']})
            self.datastring = ''
        if tag == 'p':
            if self.datastring != '':
                self.commandlist[-1]['data'] = " ".join(self.datastring.split())
                self.datastring = ''


    def get_commandlist(self):
        return self.commandlist


class PDFHtml(object):
    def __init__(self, parent, session, page, htmltext, cursor, formats=None, context=None):
        self.document = parent
        self.session = session
        self.page = page
        self.htmltext = str(htmltext)
        self.context = {}
        if isinstance(context, dict):
            self.context = context
        self.formats = {}
        if isinstance(formats, dict):
            self.formats = formats
        self._parseformats()
        self._parsehtml()
        self._runlist()

    def _parsehtml(self):
        parser = PDFHTMLParser()
        parser.feed(self.htmltext)
        self.commandlist = parser.get_commandlist()

    def _parseformats(self):
        print self.formats

    def _runlist(self):
        for tag in self.commandlist:
            if tag['name'] == 'h1':
                self.document.set_font(self.formats['h1'])
                self.document.add_text('%s' % tag['data'])
                self.document.add_newline()
            elif tag['name'] == 'p':
                self.document.set_font(self.formats['p'])
                self.document.add_text('%s' % tag['data'])
            elif tag['name'] == 'span':
                savefont = self.document.get_font()
                font, color, variable = self.parse_atts(tag['attributes'])
                if variable is not None:
                    PDFText(self.session, self.page, ' %s' % variable, font, color, self.page.cursor)
                    self.document.set_font(savefont)

    def parse_atts(self, atts):
        formats = []
        font = None
        color = None
        variable = None
        for item in atts:
            if item[0] == 'class':
                formats = item[1].split(' ')
            elif item[0] == 'data-bind':
                variable = self.context[item[1]]

        for key in formats:
            if key in self.formats:
                value = self.formats[key]
                if isinstance(value, PDFFont):
                    font = value
                if isinstance(value, PDFColor):
                    color = value
        return font, color, variable