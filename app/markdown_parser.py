#
# markdown_parser.py
#

import re

from flask import escape

def parse_markdown(markdown):
    # Replace headers
    parsed_text = re.sub(r"^# (.+)\n", lambda x: "<p class='md_header'>" + x.group(1) + "</p>", markdown)

    # Replace newlines
    parsed_text = parsed_text.replace("\n", "<br>")

    # Embolden
    parsed_text = re.sub(r"\*\*(.+)\*\*", lambda x: "<b>" + x.group(1) + "</b>", parsed_text)

    # Replace urls
    parsed_text = re.sub(r"\[(.+?)\]\((.+?)\)", lambda x: "<a target='_blank' rel='noopener' href=\"" + x.group(2) + "\">" + x.group(1) + "</a>", parsed_text)

    return parsed_text
