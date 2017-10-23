import unicodedata
import re


def slugify(value):
    """Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    # taken from http://stackoverflow.com/a/295466
    # with some modification
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = str(re.sub(r'[^\w\s.]', '', value.decode('ascii')).strip())
    # value = re.sub(r'[-\s]+', '-', value.decode('ascii')) # not replacing space with hyphen
    return value
