import hashlib
import os
import time
import urllib.request


def get_raw_html_page(url):
    cached_version = get_cached_version_if_possible(url)
    if cached_version is not None:
        return cached_version
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")
        save_cached_version(url, content)
        return content


def get_cached_version_if_possible(url):
    encoded_url = get_encoded_filename(url)
    if os.path.exists(encoded_url):
        creation_time = os.stat(encoded_url).st_ctime
        file_is_too_old = time.time() - creation_time > N_SECONDS_PER_DAY
        if not file_is_too_old:
            with open(encoded_url) as f:
                return f.read()
    return None


N_SECONDS_PER_DAY = 60 * 60 * 24


def save_cached_version(url, content):
    encoded_url = get_encoded_filename(url)
    with open(encoded_url, "w") as f:
        return f.write(content)


def get_encoded_filename(filename):
    return hashlib.sha512(filename.encode("utf-8")).hexdigest() + ".tmp"


BASE = "https://commoncrawl.s3.amazonaws.com/"