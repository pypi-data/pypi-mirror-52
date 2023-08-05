"""Scraper for Army Court of Criminal Appeals
CourtID: acca
Reviewer: None
History:
  2015-01-08: Created by mlr
  2016-03-17: Website appears to be dead. Scraper disabled in __init__.py.
"""


import re
from lxml import html

from juriscraper.OpinionSite import OpinionSite
from juriscraper.lib.string_utils import convert_date_string


class Site(OpinionSite):
    def __init__(self, *args, **kwargs):
        super(Site, self).__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.url = 'https://www.jagcnet.army.mil/85257546006DF36B/ODD?OpenView&Count=-1'
        self.docket_case_name_splitter = re.compile('(.*[\dX]{5,8})(.*)')

    def _get_download_urls(self):
        path = "//a[@class='td_frmOpinion']/@href"
        return list(self.html.xpath(path))

    def _get_case_names(self):
        path = "//a[@class='td_frmOpinion']"
        case_names = []
        for e in self.html.xpath(path):
            s = html.tostring(e, method='text', encoding='unicode')
            m = self.docket_case_name_splitter.search(s)
            case_names.append(m.group(2))
        return case_names

    def _get_case_dates(self):
        path = "//a[@class='DtOpn2']/text()"
        return [convert_date_string(date_string) for date_string in  self.html.xpath(path)]

    def _get_precedential_statuses(self):
        return ['Published'] * len(self.case_names)

    def _get_docket_numbers(self):
        path = "//a[@class='td_frmOpinion']"
        docket_numbers = []
        for e in self.html.xpath(path):
            s = html.tostring(e, method='text', encoding='unicode')
            m = self.docket_case_name_splitter.search(s)
            docket_numbers.append(m.group(1))
        return docket_numbers
