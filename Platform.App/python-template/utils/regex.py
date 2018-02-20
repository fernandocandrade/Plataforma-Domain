import re


def replace(pattern, target, parser):
    regex = re.compile(pattern)
    return regex.sub(parser, target)
