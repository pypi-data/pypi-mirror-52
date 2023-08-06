from warc import WARCReader


class WARCStringRecord(object):

    def __init__(self, warc_string):
        self.warc_reader = WARCReader(WARCFakeFile(warc_string))
        self.record = self._get_record()
        self.content = self.record.payload.read().decode("utf-8")

    def _get_record(self):
        for record in self.warc_reader:
            return record

    def __getitem__(self, item):
        return self.record[item]

    def get_content(self):
        return self.content

    def __contains__(self, item):
        return item in self.record


class WARCFakeFile(object):

    def __init__(self, string_to_fake):
        self.faked_string = string_to_fake.strip().split("\n")
        self.line_number = 0

    def readline(self):
        self.line_number += 1
        result = (self.faked_string[self.line_number - 1] + "\r\n").encode()
        return result

    def read(self, size):
        read_from = self.line_number
        self.line_number = len(self.faked_string)
        return ("\r\n".join(self.faked_string[read_from:]) + "\r\n").encode()