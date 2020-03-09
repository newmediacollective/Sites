#
# markdown_parser.py
#

import re

from flask import escape


def parse_markdown(markdown):
    # Replace newlines
    parsed_text = markdown.replace("\n\n", "\n<br><br>\n")

    # Replace urls
    parsed_text = re.sub(r"\[(.+?)\]\((.+?)\)", lambda x: "<a target='_blank' rel='noopener' href=\"" + x.group(2) + "\">" + x.group(1) + "</a>", parsed_text)

    return parsed_text
