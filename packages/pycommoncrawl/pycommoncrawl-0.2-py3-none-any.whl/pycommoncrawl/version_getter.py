import datetime
import re

from pycommoncrawl.utils import get_raw_html_page, BASE


class VersionGetter(object):

    def __init__(self):
        self.index_versions = get_index_versions()

    def get_latest_version(self):
        most_recent_date = None
        for key in self.index_versions:
            if most_recent_date is None:
                most_recent_date = key
            elif most_recent_date < key:
                most_recent_date = key
        return most_recent_date, self.index_versions[most_recent_date]

    def get_versions(self):
        return list(self.index_versions.keys())

    def get_url(self, version):
        if version not in self.index_versions:
            raise InvalidVersion
        return self.index_versions[version]


def get_version_html_page():
    return get_raw_html_page(BASE + "crawl-data/index.html")


def get_index_versions():
    page = get_version_html_page()
    regex = re.compile(r'<td><a href="(?P<url>./CC-MAIN[^"]*)">CC-MAIN-2019-35</a></td>[^<]*'
                       '<td><a href="(?P<urluseless>https?://commoncrawl.org/[^"]*)">(?P<date>[^<]*)</a></td>')
    versions = dict()
    for match in regex.finditer(page):
        versions[read_version_date(match.group("date"))] = BASE + "crawl-data/" + match.group("url")[2:]
    return versions


def read_version_date(raw_date):
    return datetime.datetime.strptime(raw_date, "%B %Y")


class InvalidVersion(Exception):
    pass
