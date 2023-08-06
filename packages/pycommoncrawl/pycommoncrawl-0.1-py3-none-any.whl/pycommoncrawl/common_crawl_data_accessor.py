import gzip
import os
import re
import urllib.request

import progressbar

from pycommoncrawl.utils import get_raw_html_page, BASE
from pycommoncrawl.version_getter import VersionGetter
from pycommoncrawl.warc_string_record import WARCStringRecord


class UnknownResourceName(Exception):

    def __init__(self, resources_available):
        super().__init__("Available resources: " + ", ".join(resources_available))


def get_destination(url):
    destination = url.split('/')[-1]
    return destination


class CommonCrawlDataAccessor(object):

    def __init__(self, url="latest", clean_after=True):
        if url == "latest":
            version_getter = VersionGetter()
            _, url = version_getter.get_latest_version()
        self.url = url
        self.clean_after = clean_after
        self.base = "/".join(url.split("/")[:-1])
        self.raw_info_page = get_raw_html_page(url)
        self.resources = dict(zip(self.get_part_names(), self.get_urls()))

    def get_part_names(self):
        regex = re.compile(r"<td>(?P<name>(\w|\s|\.|-)*)</td>")
        return [x.group("name") for x in regex.finditer(self.raw_info_page)]

    def get_urls(self):
        regex = re.compile(r'<td><a href="(?P<url>[^"]*)">[^<]*</a></td>')
        return [self.base + x.group("url")[1:] for x in regex.finditer(self.raw_info_page)]

    def get_number_files(self, resource_name):
        self.check_if_legal_resource(resource_name)
        return sum(self.apply_on_each_line(resource_name, lambda x: 1))

    def apply_on_each_line(self, resource_name, function):
        url = self.resources[resource_name]
        yield from self.apply_on_each_line_url(url, function)

    def apply_on_each_line_url(self, url, function):
        destination = get_destination(url)
        self.download(url, destination)
        with gzip.open(destination, 'rb') as f:
            for line in f:
                yield function(line.decode("utf-8"))
        if self.clean_after:
            os.remove(destination)

    def download(self, url, destination):
        if not os.path.exists(destination):
            urllib.request.urlretrieve(url, destination)

    def check_if_legal_resource(self, resource_name):
        if resource_name not in self.resources:
            raise UnknownResourceName(self.resources.keys())

    def get_raw_resource_data(self, resource_name, min_file_number=0, max_file_number=-1):
        self.check_if_legal_resource(resource_name)
        urls = list(self.apply_on_each_line(resource_name, lambda x: BASE + x.strip()))
        if max_file_number == -1:
            urls = urls[min_file_number:]
        else:
            urls = urls[min_file_number:max_file_number]
        bar = progressbar.ProgressBar(
            max_value=len(urls),
            widgets=[
                ' [', progressbar.Timer(), '] ',
                progressbar.Bar(),
                ' ',
                ' (', progressbar.ETA(), ') ',
                progressbar.Counter(format='%(value)02d/%(max_value)d'),
            ]
        )
        for i, url in enumerate(urls):
            bar.update(i)
            yield from self.apply_on_each_line_url(url, lambda x: x)
        bar.finish()

    def get_raw_resource_data_per_block(self, resource_name, min_file_number=0, max_file_number=-1):
        buffer = []
        for line in self.get_raw_resource_data(resource_name, min_file_number, max_file_number):
            line = line.strip()
            if line.startswith("WARC/") and buffer:
                yield "\n".join(buffer)
                buffer = []
            buffer.append(line)
        if buffer:
            yield "\n".join(buffer)

    def get_raw_resource_data_per_warc(self, resource_name, min_file_number=0, max_file_number=-1):
        for bloc in self.get_raw_resource_data_per_block(resource_name, min_file_number, max_file_number):
            yield WARCStringRecord(bloc)