"""Extracts URLs found in the pdf file located at
https://www.emta.ee/ariklient/registreerimine-ettevotlus/hasartmangukorraldajale/blokeeritud-hasartmangu
and writes them to a .txt blocklist
"""
import logging
import re
from datetime import datetime

import requests
import tldextract
from pdfminer.high_level import extract_text

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
        res = requests.get(endpoint, verify=True, timeout=120)
        with open("source.pdf", "wb") as f:
            f.write(res.content)
        text = extract_text("source.pdf")
        entries = [
            f
            for e in text.split("\n")
            if not (f := e.strip()).isnumeric()  # type: ignore
        ]
        urls = set(
            maybe_url_cleaned
            for maybe_url in entries
            if (maybe_url_cleaned := clean_url(maybe_url))  # type: ignore
            and len(tldextract.extract(maybe_url_cleaned).registered_domain)
        )
        return urls
    except Exception as error:
        logger.error(error)
        return set()


if __name__ == "__main__":
    urls: set[str] = extract_urls()
    registered_domains: set[str] = set(
        tldextract.extract(url).registered_domain for url in urls
    )
    if not urls:
        raise ValueError("URL extraction failed")
    timestamp: str = current_datetime_str()

    filename = "blocklist.txt"
    with open(filename, "w") as f:
        f.writelines("\n".join(sorted(urls)))
        logger.info("%d URLs written to %s at %s", len(urls), filename, timestamp)

    filename = "blocklist_UBL.txt"
    with open(filename, "w") as f:
        f.writelines("\n".join(f"*://*.{r}/*" for r in sorted(registered_domains)))
        logger.info(
            "%d Registered Domains written to %s at %s",
            len(registered_domains),
            filename,
            timestamp,
        )
