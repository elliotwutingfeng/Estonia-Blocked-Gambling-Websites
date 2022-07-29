"""Extracts URLs found in the pdf file located at
https://www.emta.ee/ariklient/registreerimine-ettevotlus/hasartmangukorraldajale/blokeeritud-hasartmangu
and writes them to a .txt blocklist
"""
import logging
import re
from datetime import datetime

import camelot
import requests
import tldextract

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(message)s")


def current_datetime_str() -> str:
    """Current time's datetime string in UTC.

    Returns:
        str: Timestamp in strftime format "%d_%b_%Y_%H_%M_%S-UTC"
    """
    return datetime.utcnow().strftime("%d_%b_%Y_%H_%M_%S-UTC")


def clean_url(url: str) -> str:
    """Remove zero width spaces, leading/trailing whitespaces, trailing slashes,
    and URL prefixes from a URL

    Args:
        url (str): URL

    Returns:
        str: URL without zero width spaces, leading/trailing whitespaces, trailing slashes,
    and URL prefixes
    """
    removed_zero_width_spaces = re.sub(r"[\u200B-\u200D\uFEFF]", "", url)
    removed_leading_and_trailing_whitespaces = removed_zero_width_spaces.strip()
    removed_trailing_slashes = removed_leading_and_trailing_whitespaces.rstrip("/")
    removed_https = re.sub(r"^[Hh][Tt][Tt][Pp][Ss]:\/\/", "", removed_trailing_slashes)
    removed_http = re.sub(r"^[Hh][Tt][Tt][Pp]:\/\/", "", removed_https)

    return removed_http


def extract_urls() -> set[str]:
    """Extract URLs found in
    https://ncfailid.emta.ee/s/6BEtzQAgFH4y349/download/Blokeeritud_domeeninimed.pdf

    Returns:
        set[str]: Unique URLs
    """
    try:
        endpoint: str = "https://ncfailid.emta.ee/s/6BEtzQAgFH4y349/download/Blokeeritud_domeeninimed.pdf"
        res = requests.get(endpoint, verify=False)
        # TODO verify=False is unsafe, remove this when emta.ee sorts out their SSL issues
        with open('source.pdf', 'wb') as f:
            f.write(res.content)
        tables = camelot.read_pdf('source.pdf', pages='all')
        urls = set()
        for table in tables:
            urls.update([maybe_url for maybe_url in table.df[1].values
                        if (maybe_url_cleaned := clean_url(maybe_url)) and
                        len(tldextract.extract(maybe_url_cleaned).registered_domain)])
        return urls
    except Exception as error:
        logger.error(error)
        return set()


if __name__ == "__main__":
    urls: set[str] = extract_urls()
    if urls:
        timestamp: str = current_datetime_str()
        filename = "blocklist.txt"
        with open(filename, "w") as f:
            # Get rid of zero width spaces
            f.writelines("\n".join(sorted(urls)))
            logger.info("%d URLs written to %s at %s", len(urls), filename, timestamp)
    else:
        raise ValueError("URL extraction failed")
