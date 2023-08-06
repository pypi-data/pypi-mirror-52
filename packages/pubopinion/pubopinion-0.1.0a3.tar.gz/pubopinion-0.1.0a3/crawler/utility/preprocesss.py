import re

from crawler.utility import constants


def strip_tags(text):
    if text is None:
        return ""
    return re.sub(constants.RE_TAG_ALL, "", text)
