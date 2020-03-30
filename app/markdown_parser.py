#
# markdown_parser.py
#

import re

from flask import escape

def parse_markdown(markdown):
    # Replace newlines
    parsed_text = markdown.replace("\n\n", "<br><br>")
    parsed_text = parsed_text.replace("\n", "<br>")

    # Embolden
    parsed_text = re.sub(r"\*\*(.+)\*\*", lambda x: "<b>" + x.group(1) + "</b>", parsed_text)

    # Replace headers
    parsed_text = re.sub(r"# (.+)", lambda x: "<p class='md_header'>" + x.group(1) + "</p>", parsed_text)

    # Replace urls
    parsed_text = re.sub(r"\[(.+?)\]\((.+?)\)", lambda x: "<a target='_blank' rel='noopener' href=\"" + x.group(2) + "\">" + x.group(1) + "</a>", parsed_text)

    return parsed_text
